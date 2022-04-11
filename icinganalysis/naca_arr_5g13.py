from icinganalysis import water_properties
from icinganalysis import air_properties
from icinganalysis import iteration_helpers
from icinganalysis import markdown_table_helper
from icinganalysis import ethanol_properties
from icinganalysis.units_helpers import MM_HG_PER_PA, FT_PER_M, tf_to_k, tk_to_f

RATIO_MOLECULAR_WEIGHTS = water_properties.RATIO_MOLECULAR_WEIGHTS  # water to air


vapor_p_function = water_properties.calc_vapor_p


table_i_v_fps = 600
table_i = (  # tf_static, p_mm_hg, tf_surface, ratio dt_wet to dt_dry
    (0, 760, 19.4, 0.77),
    (0, 350, 15.8, 0.62),
    (25, 760, 40.1, 0.60),
    (25, 350, 35.5, 0.49),
)


def calc_tk_surface_wet(tk, p, u):
    dt_dry = calc_dt_dry(u)
    e_vapor = vapor_p_function(tk)

    def f(tk_surface):
        e_surface = vapor_p_function(tk_surface)
        dt_evap = (
            RATIO_MOLECULAR_WEIGHTS
            / p
            * (e_surface - e_vapor)
            * water_properties.L_EVAPORATION
            / air_properties.CP_AIR
        )
        return abs(tk_surface - tk - dt_dry + dt_evap)

    tk_surface = iteration_helpers.solve_minimize_f(
        f,
        bounds=[
            223.15,
            323.15,
        ],  # selected to work with water_properties.vapor_p_smithsonian_tables_1934
    )
    return tk_surface


def calc_delta_t_wet(tk, p, u):
    tk_surface = calc_tk_surface_wet(tk, p, u)
    e_surface = vapor_p_function(tk_surface)
    e_vapor = vapor_p_function(tk)
    dt_evap = (
        RATIO_MOLECULAR_WEIGHTS
        / p
        * (e_surface - e_vapor)
        * water_properties.L_EVAPORATION
        / air_properties.CP_AIR
    )
    return dt_evap


def calc_cp_wet(tk, p, tk_surface):
    e_vapor = vapor_p_function(tk)
    e_surface = vapor_p_function(tk_surface)
    cp_wet = air_properties.CP_AIR + RATIO_MOLECULAR_WEIGHTS / p * (
        e_surface - e_vapor
    ) * water_properties.L_EVAPORATION / (tk_surface - tk)
    return cp_wet


def calc_dt_dry(u, r=0.84):  # laminar recovery value, equation (13) with Pr=0.71
    return r * u ** 2 / 2 / air_properties.CP_AIR


def calc_tk_surface_wet_with_ethanol(tk, p, u):
    dt_dry = calc_dt_dry(u)
    e_vapor = vapor_p_function(tk)

    def f(tk_surface):
        e_surface = vapor_p_function(tk_surface)
        dt_evap = (
            RATIO_MOLECULAR_WEIGHTS
            / p
            * (e_surface - e_vapor)
            * water_properties.L_EVAPORATION
            / air_properties.CP_AIR
        )
        dt_evap_ethanol = (
            air_properties.MOLECULAR_MASS
            / ethanol_properties.MOLECULAR_MASS
            / p
            / (ethanol_properties.calc_p_vapor(tk_surface) - 0)
            * ethanol_properties.L_EVAPORATION
            / air_properties.CP_AIR
        )
        return abs(tk_surface - tk - dt_dry + dt_evap + dt_evap_ethanol)

    tk_surface = iteration_helpers.solve_minimize_f(
        f,
        bounds=[
            223.15,
            323.15,
        ],  # selected to work with water_properties.vapor_p_smithsonian_tables_1934
    )
    return tk_surface


if __name__ == "__main__":
    u = table_i_v_fps / FT_PER_M

    # "classic" vapor pressure
    vapor_p_function = water_properties.vapor_p_smithsonian_tables_1934

    rows = []
    for tf, p_mm_hg, tf_surface, ratio in table_i:
        p = p_mm_hg / MM_HG_PER_PA
        tk = tf_to_k(tf)
        tk_surface = tf_to_k(tf_surface)
        tkw = calc_delta_t_wet(tk, p, u)
        dt_dry = calc_dt_dry(u)
        tk_surface_calc = calc_tk_surface_wet(tk, p, u)
        tf_surface_calc = tk_to_f(tk_surface_calc)
        cp_wet = calc_cp_wet(tk, p, tk_surface_calc)
        dtkw = calc_delta_t_wet(tk, p, u)
        ratio_calc = air_properties.CP_AIR / cp_wet
        rows.append(
            [
                f"{tf}",
                f"{p_mm_hg}",
                f"{tf_surface}",
                f"{tf_surface_calc:.1f}",
                f"{ratio}",
                f"{ratio_calc:.2f}",
            ]
        )
    print()
    header = (
        "T, F",
        "P, mm_hg",
        "NACA-ARR-5G13 T_surface, F",
        "Calculated T_surface, F",
        "NACA-ARR-5G13 Ratio, Cp/Cp_wet",
        "Calculated Ratio, Cp/Cp_wet",
    )
    text = markdown_table_helper.make_nice_width_markdown_table(header, rows)
    print(text)

    # "modern" function matches slightly better
    vapor_p_function = water_properties.calc_vapor_pressure_gg
    rows = []
    for tf, p_mm_hg, tf_surface, ratio in table_i:
        p = p_mm_hg / MM_HG_PER_PA
        tk = tf_to_k(tf)
        tk_surface = tf_to_k(tf_surface)
        tkw = calc_delta_t_wet(tk, p, u)
        dt_dry = calc_dt_dry(u)
        tk_surface_calc = calc_tk_surface_wet(tk, p, u)
        tf_surface_calc = tk_to_f(tk_surface_calc)
        cp_wet = calc_cp_wet(tk, p, tk_surface_calc)
        dtkw = calc_delta_t_wet(tk, p, u)
        ratio_calc = air_properties.CP_AIR / cp_wet
        rows.append(
            [
                f"{tf}",
                f"{p_mm_hg}",
                f"{tf_surface}",
                f"{tf_surface_calc:.1f}",
                f"{ratio}",
                f"{ratio_calc:.2f}",
            ]
        )
    print()
    header = (
        "T, F",
        "P, mm_hg",
        "NACA-ARR-5G13 T_surface, F",
        "Calculated T_surface, F",
        "NACA-ARR-5G13 Ratio, Cp/Cp_wet",
        "Calculated Ratio, Cp/Cp_wet",
    )
    text = markdown_table_helper.make_nice_width_markdown_table(header, rows)
    print("Table I")
    print(text)

    with open("naca_arr_5g13_table1.md", "w") as fd:
        fd.writelines(text)

    u = 450 / FT_PER_M
    p = 760 / MM_HG_PER_PA
    # fmt: off
    naca_arr_5g13_table_ii = (  # Tf, kg_ethanol/kg_water
        450, 15.2, 760, 23, .124, 'ethanol',
        450, 15.2, 760, 25.5, .092, 'nv',
        450, 19.2, 350, 23.0, .124, 'ethanol',
        450, 19.2, 350, 26.3, .07, 'nv',
        250, 24.2, 350, 23, .124, 'ethanol',
        250, 24.2, 350, 26.6, .075, 'nv',
        250, 19.2, 350, 18, .184, 'ethanol',
        250, 19.2, 350, 22.1, .135, 'nv',
        450, 1.6, 760, 10.6, .270, 'ethanol',
        450, 1.6, 760, 13.3, .239, 'nv',
        450, 5.5, 350, 10.6, .270, 'ethanol',
        450, 5.5, 350, 15.8, .270, 'nv',
    )
    # fmt: on

    rows = []
    for v_fps, tf, p_mm_hg, tf_surface, conc, fluid in zip(
        *(iter(naca_arr_5g13_table_ii),) * 6
    ):
        if "ethanol" not in fluid:
            continue
        p = p_mm_hg / MM_HG_PER_PA
        tk = tf_to_k(tf)
        u = v_fps / FT_PER_M
        tk_surface = calc_tk_surface_wet_with_ethanol(tk, p, u)
        tf_surface_calc = tk_to_f(tk_surface)
        tf_mp = tk_to_f(ethanol_properties.interp_mp(conc / (1 + conc)))
        rows.append([v_fps, tf, p_mm_hg, f"{tf_surface:.1f}", f"{tf_surface_calc:.1f}", f"{tf_mp:.1f}", conc])
    header = ["V, fps", "T, F", "Pressure, mm_hg", "Surface T, F", "Calculated Surface T, F", "Calculated freezing T, F", "Ethanol concentration, kg/kg_water"]
    text = markdown_table_helper.make_nice_width_markdown_table(header, rows)
    print("Table II")
    print(text)

    with open("naca_arr_5g13_tableii.md", "w") as fd:
        fd.writelines(text)

    # NACA-ARR-4I11 conditions
    alt_ft = 3900
    alt = alt_ft / FT_PER_M
    p = air_properties.calc_pressure(alt)
    MS_PER_MPH = 0.44704
    u = 175 * MS_PER_MPH
    print(0.24 / 0.361)  # page 6, cp/cp_wet, cp_wet from table in
    for tf in (24.3, 27.1, 30.2):  # candidate temperatures
        tk = tf_to_k(tf)
        tk_surface_calc = calc_tk_surface_wet(tk, p, u)
        cp_wet = calc_cp_wet(tk, p, tk_surface_calc)
        ratio_calc = air_properties.CP_AIR / cp_wet
        print(tf, ratio_calc)
    # All of the ratio values are below the reported value
    # I believe that Hardy had a change in methods from 1944 to 1945,
    # perhaps he learned to more accurately calculate Cp_wet himself
