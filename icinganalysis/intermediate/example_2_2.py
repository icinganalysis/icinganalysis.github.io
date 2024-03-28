from icinganalysis import air_properties
from icinganalysis import units_helpers
from icinganalysis.intermediate import basics_water_catch_calculations, figure_2_11


if __name__ == "__main__":
    c = units_helpers.ft_to_m(3.1)
    ktas = 200
    u = units_helpers.ktas_to_ms(ktas)
    altitude = units_helpers.ft_to_m(10000)
    p = air_properties.calc_pressure(altitude)
    tf = 15
    tk = units_helpers.tf_to_k(tf)
    drop_diameter = 20
    (
        k_calc,
        re_calc,
        lambda_lambda_s_calc,
        ko_calc,
    ) = basics_water_catch_calculations.calc_ko(tk, p, u, drop_diameter, c)

    em = figure_2_11.interp_em(ko_calc)
    print(f"E interpolated from Figure 2-11: {em:.3f}")

    from icinganalysis import langmuir_cylinder_values

    drs = langmuir_cylinder_values.langmuir_d_mids
    weights = langmuir_cylinder_values.langmuir_lwc_fractions
    print(drs)

    em_bar = 0
    print()
    print("DOT/FAA/CT-88/8-1 Example 2-3 Table 2-2 Calculations")
    print(f"{'Ko':7s}  {'Δv':6s}{'E':6s} {'E*Δv':7s}")
    for ratio, weight in zip(drs, weights):
        d_ = drop_diameter * ratio
        ko = basics_water_catch_calculations.calc_ko(tk, p, u, d_, c)[-1]
        em_ = figure_2_11.interp_em_with_linear_extrapolation(ko)
        em_bar += em_ * weight
        # print(d_, ko, em_, em_ * weight)
        print(f"{ko:.5f}  {weight:.2f}  {em_:.3f}  {em_ * weight:.3f}")
    print(f"       E_bar = {em_bar:.3f}")

    """
    DOT/FAA/CT-88/8-1 Example 2-3 Table 2-2 Calculations
    Ko       Δv    E      E*Δv   
    0.00704  0.05  0.021  0.001
    0.01676  0.10  0.083  0.008
    0.02799  0.20  0.141  0.028
    0.04882  0.30  0.231  0.069
    0.08084  0.20  0.325  0.065
    0.11806  0.10  0.402  0.040
    0.17307  0.05  0.488  0.024
           E_bar = 0.237
    """
