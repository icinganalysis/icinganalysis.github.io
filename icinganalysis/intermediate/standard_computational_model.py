from icinganalysis import water_properties
from icinganalysis import air_properties
from icinganalysis import compressible_flow
from icinganalysis import units_helpers
from icinganalysis.intermediate import cylinder_beta_max_from_figure_2_43
from icinganalysis.langmuir_cylinder_values import calc_ko_d2


T_MP = 273.15  # melting temperature of ice, K
CP_AIR = air_properties.CP_AIR


def calc_m_imp(u, lwc, beta):
    """Equation 2-34
    We will eschew the part
    "However, if the local velocity at the edge of the boundary layer is
    available, that velocity should be used rather than the freestream velocity"
    as that is not how conventional Beta values work.
    """
    m_imp = u * lwc / units_helpers.G_PER_KG * beta
    return m_imp


def calc_t_film(t, t_surface=T_MP):
    """

    :param t:
    :param t_surface:
    :return:
    """
    t_film = (t + t_surface) / 2
    # return t_surface
    return t_film


def calc_k_a(t_film):
    """
    Calculate the thermal conductivity of air
    Equation A.3 in NASA/CR-2004-212875 implemented SI units
    Symbol k_a
    Note that the examples use t_film (average of static air temperature and t_surface)
    :param t_film: temperature, K
    :return: air thermal conductivity, W/m-K (J/s-m-K)
    """
    return -0.0147486 + 0.00235815 * t_film**0.5


def calc_mu_a(t):
    """
    Calculate the dynamic viscosity of air
    Equation A.24 in NASA/CR-2004-212875 implemented SI units
    Symbol: mu_a
    :param t: temperature, K
    :return: viscosity, kg/m-s
    """
    return 1e-5 / (0.12764 + 124.38 / t)


def calc_pr_a(mu_a, k_a):
    """
    Calculate the Prandtl number
    Equation A.42 in NASA/CR-2004-212875 implemented SI units
    Symbol: pr_a
    :param mu_a: viscosity of air, kg/m-s
    :param k_a: thermal conductivity of air, W/m-K
    :return: Prandtl Number (dimensionless)
    """
    return CP_AIR * mu_a / k_a


def calc_re_a(ms, d, rho_a, mu_a):
    """
    Calculate Reynolds number
    Equation A.44 in NASA/CR-2004-212875 implemented SI units
    Symbol: re_a
    :param ms: airspeed, m/s
    :param d: leading edge diameter of curvature, m
    :param rho_a: air density, kg/m^3.
    :param mu_a: air viscosity, kg/m-s
    :return: Reynolds number (dimensionless)
    """
    return ms * d * rho_a / mu_a


def calc_reynolds_from(ms, t, p, d):
    """
    Calculate the Reynold number for air
    :param ms: airspeed, m/s
    :param t: air static temperature, K
    :param p: air static pressure, Pa
    :param d: length, m
    :return: Reynolds number for air
    """
    return calc_re_a(ms, d, air_properties.calc_air_density(t, p), calc_mu_a(t))


def calc_d_v(t_film, p_st):
    """
    Calculate the thermal diffusivity of water vapor in air
    Equation A.4 in NASA/CR-2004-212875 implemented SI units
    Symbol d_v
    Note that the examples use t_film (average of static air temperature and t_surface)
    :param t_film: temperature, K
    :param p_st: air static pressure, Pa (N/m^2)
    :return: diffusivity, m^2/s
    """
    return 0.211 / 100**2 * (t_film / 273.15) ** 1.94 * (101320 / p_st)


def calc_schmidt(mu_a, rho_a, d_v):
    """
    Calculate the Schmidt number
    Equation A.46 in NASA/CR-2004-212875 implemented SI units
    Symbol: s_c_a
        :param mu_a: air viscosity, kg/m-s
    :param rho_air: air density, kg/m^3.
    :param d_v: diffusivity of water vapor in air, m^2/s
    :return: Schmidt number (dimensionless)
    """
    return mu_a / (rho_a * d_v)


def calc_hc_o_cylinder_from(u, t, diameter, p):
    """
    Calculate the heat transfer coefficient at the stagnation line of a cylinder
    :param u: airspeed, m/s
    :param t: air static temperature, K
    :param diameter: significant length, m (diameter of curvature)
    :param p: air static pressure, Pa
    :return: heat transfer coefficient at the stagnation line of a cylinder, W/m^2-K
    """
    t_film = calc_t_film(t)
    pr = calc_pr_a(calc_mu_a(t_film), calc_k_a(t_film))
    re_a = calc_reynolds_from(u, t_film, p, diameter)
    nu_a = (
        1.14 * pr**0.4 * re_a**0.5
    )  # From Kreith, "Principles of Heat Transfer" for a laminar cylinder leading edge
    hc = calc_k_a(t_film) * nu_a / diameter
    return hc


def calc_q_aero_heat(u, hc, rc=0.9):
    """Equation 2-38"""
    q_aero_heat = hc * rc * u**2 / (2 * CP_AIR)
    return q_aero_heat


def calc_q_conv(hc, t, t_surface=T_MP):
    """Equation 2-42"""
    q_conv = hc * (t_surface - t)
    return q_conv


def calc_q_conv2(hc, tr, t_surface=T_MP):
    """Equation 2-42b"""
    q_conv2 = hc * (t_surface - tr)
    return q_conv2


def calc_tr(t, hc, rc, u):
    """Equation 2-42c"""
    tr = t + hc * rc * u**2 / (2 * CP_AIR)
    return tr


def calc_q_drop_warm(m_imp, t, t_surf=T_MP):
    """Equation 2-43"""
    q_drop_warm = m_imp * water_properties.WATER_SPECIFIC_HEAT * (t_surf - t)
    return q_drop_warm


def calc_q_ice_cool(n, m_imp, t_surf=T_MP):
    """
    Equation 2-40

    I believe that there is a typo in the source (both the 1991 and 1193 update).
    The product n*M"ice does not make sense.
    Either n*M"imp or M"ice would make sense.
    n*M"imp is the form used in NASA-CR-2004-212875, Section 3.5, term (9).

    :param n:
    :param m_imp:
    :param t_surf:
    :return:
    """
    m_ice = m_imp * n
    q_ice_cool = m_ice * water_properties.ICE_SPECIFIC_HEAT * (T_MP - t_surf)
    return q_ice_cool


def calc_m_evap(t, p, hc, u, t_surf=T_MP, po=None, to=None):
    if po is None:
        po = p
    if to is None:
        to = t
    t_film = calc_t_film(t)
    schmidt = calc_schmidt(
        calc_mu_a(t_film),
        air_properties.calc_air_density(t_film, p),
        calc_d_v(t_film, p),
    )
    g = (
        hc
        / CP_AIR
        * (calc_pr_a(calc_mu_a(t_film), calc_k_a(t_film)) / schmidt) ** 0.667
    )
    b1 = (
        water_properties.calc_vapor_p(t_surf) / t
        - po / p * water_properties.calc_vapor_p(t) / to
    )
    b2 = 1 / 0.622 * po / to - water_properties.calc_vapor_p(t_surf) / t
    delta_b = b1 / b2
    m_evap = g * delta_b
    return m_evap


def calc_q_evap(m_evap):
    q_evap = m_evap * water_properties.L_EVAPORATION
    return q_evap


def calc_q_drop_ke(m_imp, u):
    q = m_imp * u**2 / 2
    return q


def calc_energy_and_mass_balance(
    t, p, u, lwc, hc, beta, m_run_in=0, t_surf=T_MP, po=None, to=None, rc=0.85
):
    if po is None:
        po = p
    if to is None:
        to = t
    m_imp = calc_m_imp(u, lwc, beta)
    m_incoming = m_imp + m_run_in
    q_aero_heat = calc_q_aero_heat(u, hc, rc)
    q_drop_ke = calc_q_drop_ke(m_imp, u)
    q_conv = calc_q_conv(hc, t, t_surf)
    q_drop_warm = calc_q_drop_warm(m_imp, t, t_surf)
    m_evap = calc_m_evap(t, p, hc, u, t_surf, po, to)
    m_evap = min(m_incoming, m_evap)
    q_evap = calc_q_evap(m_evap)
    q_sink = q_conv + q_drop_warm + q_evap
    q_freeze = -(q_aero_heat + q_drop_ke - q_sink)
    m_freeze = q_freeze / water_properties.L_FREEZING
    q_source = q_freeze + q_drop_ke + q_aero_heat
    if m_incoming == 0:
        n = 0
        if m_freeze > 0:
            n = 1
    else:
        n = m_freeze / m_incoming
    return (
        n,
        q_aero_heat,
        q_freeze,
        q_drop_ke,
        q_conv,
        q_evap,
        q_drop_warm,
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import simple_csv_reader

    f = r"tables_2_5_to_8.csv"

    header, vs = simple_csv_reader.simple_csv_reader(f)

    p = air_properties.calc_pressure(0)
    diameter = 0.2  # m, 20 cm

    ws = []

    for case, u, mvd, lwc, tc, n, pqv, pqf, pqk, pqc, pqe, pqw in vs:
        t = units_helpers.tc_to_k(tc)
        hc = calc_hc_o_cylinder_from(u, t, diameter, p)
        beta = cylinder_beta_max_from_figure_2_43.get_beta(calc_ko_d2(t, p, u, mvd, diameter))
        cp = 1
        mach = compressible_flow.calc_mach(u, t)
        po = p * (0.7 * cp * mach**2 + 1)
        to = t * (p / po) ** (1 / 3.5)

        (
            n_calc,
            q_aero_heat,
            q_freeze,
            q_drop_ke,
            q_conv,
            q_evap,
            q_drop_warm,
        ) = calc_energy_and_mass_balance(t, p, u, lwc, hc, beta, po=po, to=to)
        n_calc = min(float(n_calc), 1)

        ws.append((case, tc, n, n_calc, beta))

    ws = list(ws)
    case, tc, n, n_calc, beta = list(zip(*ws))

    plt.figure()
    plt.suptitle("Handbook Table 2-5 to 2-8 data")
    plt.plot((0, 1), (0, 1), "--", label="Perfect agreement")
    plt.plot(n, n_calc, "+", label="calculated points")
    plt.xlim(0, 1)
    plt.ylim(0, 1.1)
    plt.xlabel("Freezing fraction reference, n")
    plt.xlabel("Freezing fraction calculated")
    plt.legend()

    plt.show()
