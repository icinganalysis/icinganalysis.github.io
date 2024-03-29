from icinganalysis import air_properties, simple_csv_reader
from icinganalysis import compressible_flow
from icinganalysis import units_helpers
from icinganalysis import water_properties
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


# DOT/FAA/CT-88/8-1
tables_2_5_to_8 = """Case, U, D, LWC, TC, N, PQV, PQF, PQK, PQC, PQE, PQW
2-5-a, 70, 20, 0.7, -26, 0.9, 5, 94, 1, 48, 16, 36
2-5-a, 70, 20, 0.7, -20, 0.7, 6, 93, 1, 47, 18, 35
2-5-a, 70, 20, 0.7, -14, 0.49, 8, 91, 1, 46, 21, 33
2-5-a, 70, 20, 0.7, -8, 0.27, 14, 84, 2, 44, 24, 32
2-5-a, 70, 20, 0.7, -2, 0.03, 53, 38, 9, 44, 25, 31
2-5-b, 70, 20, 0.1, -6, 0.93, 24, 75, 1, 60, 34, 6
2-5-b, 70, 20, 0.1, -4, 0.53, 36, 63, 1, 59, 35, 6
2-5-b, 70, 20, 0.1, -2, 0.10, 73, 25, 2, 60, 34, 6
2-6-a, 70, 20, 0.7, -26, .90, 5, 95, 1, 48, 15, 36
2-6-a, 70, 20, 0.8, -26, .83, 4, 95, 1, 46, 14, 40
2-6-a, 70, 20, 0.9, -26, .78, 4, 95, 1, 44, 14, 42
2-6-a, 70, 20, 1.0, -26, .73, 4, 95, 1, 42, 13, 45
2-6-a, 70, 20, 2.0, -26, .54, 3, 96, 1, 29,  9, 62
2-6-a, 70, 20, 3.0, -26, .47, 2, 96, 2, 22,  7, 71
2-6-a, 70, 20, 4.0, -26, .44, 2, 97, 2, 18,  6, 77
2-6-a, 70, 20, 5.0, -26, .42, 1, 97, 2, 15,  5, 80
2-6-b, 70, 20, 0.1, -6, .93, 24, 75,  1, 60, 34, 6
2-6-b, 70, 20, 0.4, -6, .28, 21, 77,  2, 51, 29, 21
2-6-b, 70, 20, 0.7, -6, .19, 18, 79,  3, 44, 25, 32
2-6-b, 70, 20, 1.0, -6, .15, 16, 80,  4, 39, 22, 40
2-6-b, 70, 20, 1.3, -6, .14, 14, 82,  4, 34, 19, 46
2-6-b, 70, 20, 1.6, -6, .12, 13, 82,  5, 31, 18, 51
2-6-b, 70, 20, 1.9, -6, .11, 12, 83,  5, 28, 16, 56
2-6-b, 70, 20, 2.2, -6, .11, 11, 84,  6, 26, 15, 59
2-6-b, 70, 20, 2.5, -6, .10, 10, 84,  6, 24, 14, 62
2-6-b, 70, 20, 2.8, -6, .10, 9 , 85,  6, 23, 13, 65
2-7-a, 70, 20, 0.7, -26, 0.90, 5, 95, 1, 48, 15, 36
2-7-a, 70, 40, 0.7, -26, 0.68, 4, 95, 1, 39, 12, 48
2-7-a, 70, 60, 0.7, -26, 0.64, 3, 95, 1, 37, 11, 52
2-7-a, 70, 80, 0.7, -26, 0.62, 3, 96, 1, 35, 11, 54
2-7-b, 70, 20, 0.1, -6, .93, 24, 75, 1, 60, 34, 6
2-7-b, 70, 40, 0.1, -6, .60, 24, 76, 1, 58, 33, 10
2-7-b, 70, 60, 0.1, -6, .52, 23, 76, 1, 57, 32, 11
2-7-b, 70, 80, 0.1, -6, .49, 23, 76, 1, 56, 32, 12
2-8-a, 70, 20, 0.7, -26, .90, 5 , 95, 1, 48, 15, 36
2-8-a, 80, 20, 0.7, -26, .82, 6 , 93, 1, 46, 14, 39
2-8-a, 90, 20, 0.7, -26, .76, 7 , 92, 1, 45, 14, 42
2-8-a, 100, 20, 0.7, -26, .71, 8 , 90, 2, 43, 13, 44
2-8-a, 110, 20, 0.7, -26, .67, 10, 88, 2, 42, 13, 46
2-8-a, 120, 20, 0.7, -26, .62, 11, 86, 3, 40, 12, 48
2-8-a, 130, 20, 0.7, -26, .59, 13, 84, 4, 39, 11, 49
2-8-b, 70 ,20, 0.1, -6, .93, 24, 75, 1, 60, 34, 6
2-8-b, 80 ,20, 0.1, -6, .74, 32, 67, 1, 60, 33, 7
2-8-b, 90 ,20, 0.1, -6, .58, 40, 58, 1, 60, 32, 8
2-8-b, 100,20, 0.1, -6, .44, 50, 48, 2, 60, 32, 8
2-8-b, 110,20, 0.1, -6, .31, 61, 37, 2, 60, 30, 9
2-8-b, 120,20, 0.1, -6, .19, 72, 25, 3, 60, 30, 10
2-8-b, 130,20, 0.1, -6, .08, 85, 11, 3, 61, 29, 10
"""


if __name__ == "__main__":
    from io import StringIO
    import matplotlib.pyplot as plt

    header, vs = simple_csv_reader.simple_csv_reader_file_descriptor(StringIO(tables_2_5_to_8))

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
