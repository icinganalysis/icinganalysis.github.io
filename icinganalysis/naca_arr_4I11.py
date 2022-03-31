from icinganalysis import air_properties
from icinganalysis import water_properties
from scipy.optimize import minimize_scalar

PA_PER_INCH_HG = 3386.389
R_WATER_VAPOR = water_properties.RATIO_MOLECULAR_WEIGHTS * air_properties.R_AIR
G_PER_KG = 1000
M_PER_INCH = 0.0254
MS_PER_MPH = 0.44704
INCHES_PER_FT = 12
SQ_FT_PER_SQ_M = (INCHES_PER_FT * M_PER_INCH) ** -2
M_PER_FT = M_PER_INCH * INCHES_PER_FT


def approximate_true_airspeed(v_indicated, t_f, p_mm_hg):
    rho_0 = air_properties.calc_air_density(
        (59 + 459.67) / 1.8, PA_PER_INCH_HG * 29.92
    )  # note after equation 2
    rho = air_properties.calc_air_density((t_f + 459.67) / 1.8, PA_PER_INCH_HG * p_mm_hg)
    v_approximate_true = v_indicated * (rho_0 / rho) ** 0.5  # https://en.wikipedia.org/wiki/True_airspeed#Low-speed_flight
    return v_approximate_true


def calc_n_equation_1(tk0, tk1, p):
    """
    The value of e1 is the vapor pressure, at saturation, at the temperature of the dew point of the air in the duct.
    The values given in the Smithsonian Physical Tables (1934 edition) have bean used for all the calculations.
    :param tk0:
    :param tk1:
    :param p:
    :return:
    """

    e0 = water_properties.vapor_p_smithsonian_tables_1934(tk0)
    e1 = water_properties.vapor_p_smithsonian_tables_1934(tk1)
    n = water_properties.RATIO_MOLECULAR_WEIGHTS * (e1 - e0) / p
    return n


def calc_m_equation_2(tk0, tk1, p):
    rho_0 = air_properties.calc_air_density(
        (59 + 459.67) / 1.8, PA_PER_INCH_HG * 29.92
    )  # note after equation 2
    rho = air_properties.calc_air_density(tk1, p)
    lwc = G_PER_KG * calc_n_equation_1(tk0, tk1, p)
    return lwc * rho / rho_0


def calc_delta_t_f_equation_3_naca_units(v_mph, t_f, p):
    u = v_mph * MS_PER_MPH
    tk = (t_f + 459.67) / 1.8
    cp_wet = calc_cp_wet(u, tk, p)
    ratio = air_properties.CP_AIR / cp_wet
    delta_t = 1.77 * air_properties.CP_AIR / cp_wet * (v_mph / 100) ** 2
    return delta_t


def calc_delta_tk_equation_3(u, tk0, tk1, p):
    cp_wet = calc_cp_wet(tk0, tk1, p)
    delta_tk = u ** 2 / 2 / cp_wet
    print("     ", cp_wet, delta_tk)
    return delta_tk


def calc_delta_tk_dry_equation_4(u):
    delta_tk = u ** 2 / 2 / air_properties.CP_AIR
    return delta_tk


def calc_delta_tk(u, tk_dew_point, p, r=0.8):
    q_viscous = u ** 2 / 2 * r
    e0 = water_properties.calc_vapor_pressure_gg(tk_dew_point)
    # e0 = water_properties.vapor_p_smithsonian_tables_1934(tk_static)
    e1 = water_properties.calc_vapor_pressure_gg(tk_dew_point)

    # e1 = water_properties.vapor_p_smithsonian_tables_1934(tk_dew_point)

    def f(tk):
        # e1 = water_properties.calc_vapor_pressure_gg(tk)
        e0 = water_properties.calc_vapor_pressure_gg(tk)
        # e0 = water_properties.vapor_p_smithsonian_tables_1934(tk)
        # e1 = water_properties.vapor_p_smithsonian_tables_1934(tk)
        n = water_properties.RATIO_MOLECULAR_WEIGHTS * (e1 - e0) / p
        cp_mix = (
            1 - n
        ) * air_properties.CP_AIR + n * water_properties.WATER_SPECIFIC_HEAT
        # q_sensible = cp_mix * (tk - tkx)
        q_sensible = cp_mix * (tk_dew_point - tk)
        q_evaporation = n * water_properties.L_EVAPORATION
        return abs(q_viscous - q_sensible - q_evaporation)

    solution = minimize_scalar(f, bounds=[273.15 - 50, 273.15 + 50], method="bounded")
    tk = float("nan")
    if solution.success:
        tk = solution.x
    return tk_dew_point - tk


def calc_delta_tk_from(u, tk_static, p, r=0.8):
    q_viscous = u ** 2 / 2 * r
    e0 = water_properties.calc_vapor_pressure_gg(tk_static)

    def f(tk):
        e1 = water_properties.vapor_p_smithsonian_tables_1934(tk)
        n = water_properties.RATIO_MOLECULAR_WEIGHTS * (e1 - e0) / p
        cp_mix = (
            1 - n
        ) * air_properties.CP_AIR + n * water_properties.WATER_SPECIFIC_HEAT
        q_sensible = cp_mix * (tk - tk_static)
        q_evaporation = n * water_properties.L_EVAPORATION
        return abs(q_viscous - q_sensible - q_evaporation)

    solution = minimize_scalar(f, bounds=[273.15 - 50, 273.15 + 50], method="bounded")
    tk = float("nan")
    if solution.success:
        tk = solution.x
    return tk - tk_static


def calc_cp_wet(tk0, tk1, p):
    e0 = water_properties.calc_vapor_pressure_gg(tk0)
    e1 = water_properties.calc_vapor_pressure_gg(tk1)
    n = water_properties.RATIO_MOLECULAR_WEIGHTS * (e1 - e0) / p
    h = n * water_properties.L_EVAPORATION
    cp_wet = air_properties.CP_AIR + h / (tk1 - tk0)

    return cp_wet


def example():
    v_mph_indicated = 170
    v_mph_true = 177
    t_static_f = 27.1
    t_dew_f = 30.3
    alt_ft = 3900
    p = air_properties.calc_pressure(alt_ft * M_PER_FT)
    u = v_mph_true * MS_PER_MPH
    tk = (t_static_f + 459.67) / 1.8
    tk_dew_point = (t_dew_f + 459.67) / 1.8
    delta_t_dry = calc_delta_tk_dry_equation_4(u)
    print(delta_t_dry)
    print(delta_t_dry * 1.8)
    ratio = 0.24 / 0.361
    e1 = water_properties.vapor_p_smithsonian_tables_1934(tk_dew_point)
    print(e1, e1 / water_properties.PA_PER_MM_HG)
    t0_f = 24.2
    tk0 = (t0_f + 459.67) / 1.8
    delta_t_wet = calc_delta_tk_equation_3(u, tk0, tk_dew_point, p)
    effective_delta_t_wet = 0.8 * delta_t_wet
    print("delta_t_wet", delta_t_wet, 1.8 * delta_t_wet, 1.8 * effective_delta_t_wet)
    tx = calc_delta_tk(u, tk_dew_point, p)
    print("tx", tx, 1.8 * tx)
    effective_static_air_temperature_f = t_static_f - 1.8 * effective_delta_t_wet
    effective_static_air_temperature = tk - 0.8 * delta_t_wet

    cp_wet = calc_cp_wet(tk0, tk_dew_point, p)
    r2 = air_properties.CP_AIR / cp_wet
    print("ratio", ratio, r2, cp_wet, 0.24 / r2)
    e0 = water_properties.vapor_p_smithsonian_tables_1934(
        effective_static_air_temperature
    )
    print(e0, e0 / water_properties.PA_PER_MM_HG)
    print(e0 / water_properties.PA_PER_MM_HG - e1 / water_properties.PA_PER_MM_HG)

    print(p, p / water_properties.PA_PER_MM_HG)
    print(0.622 * (0.96 / 600))

    n = calc_n_equation_1(effective_static_air_temperature, tk_dew_point, p)
    print(n)
    print(calc_m_equation_2(effective_static_air_temperature, tk_dew_point, p))
    print()
    tx = calc_delta_tk(u, tk_dew_point, p)
    print("tx", tx, 1.8 * tx)
    tkd = calc_delta_tk_from(u, tk+tx, p)
    print(tkd)
    print()
    print()
    print()
    print()
    print()


if __name__ == "__main__":
    v_mph = 175
    p = 101325
    print(calc_delta_t_f_equation_3_naca_units(v_mph, 32 - 9, p))
    u = v_mph * MS_PER_MPH
    tk0 = 273.15 - 5

    # print()
    # for tk in [_+273.15 for _ in range(-40, 20, 10)]:
    #     print(tk, calc_delta_tk_equation_3(u, tk, p))
    #
    # u = 375
    # print()
    # for tk in [_+273.15 for _ in range(-40, 20, 10)]:
    #     print(tk, calc_delta_tk_equation_3(u, tk, p))

    print()
    vs = example()
