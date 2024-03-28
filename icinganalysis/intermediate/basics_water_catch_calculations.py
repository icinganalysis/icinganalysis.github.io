"""DOT/FAA/CT-88/8-1 Examples 2-1 through 2-4"""
import matplotlib.pyplot as plt
from icinganalysis import air_properties
from icinganalysis import langmuir_cylinder_values
from icinganalysis import units_helpers
from icinganalysis import water_properties
from icinganalysis.intermediate import figure_2_11
from icinganalysis.intermediate import figure_2_12


def calc_k(tk, u, drop_diameter_micrometer, significant_length):
    k = (
        1
        / 18
        * water_properties.WATER_DENSITY
        * (drop_diameter_micrometer / units_helpers.MICROMETERS_PER_METER) ** 2
        * u
        / air_properties.calc_air_viscosity(tk)
        / significant_length
    )  # Equation 2-6
    return k


def calc_water_catch_span_rate(lwc, u, em, h_projected):
    """
    Calculate the water catch rate

    Reference equations:
    ADS-4 2.3.1
    DOT/FAA/CT-88/8-1 2.2.1.5 Equation 2-26

    Note that chord (c) has been algebraically removed,
    and h_projected is used
    (not the "h" from DOT/FAA/CT-88/8-1 2.2.1.5 2-26,
    which is h_projected/chord)

    Calculation uses SI units
    (except for LWC, which is an entrenched exception)

    :param lwc: liquid water content, g/m^3
    :param u: airspeed, m/s
    :param em: collection efficiency
    :param h_projected: projected height, m
    :return: water catch rate, kg/s/m-span
    """
    wcr = lwc / units_helpers.G_PER_KG * u * em * h_projected
    return wcr


def calc_local_water_catch_rate(lwc, u, beta):
    """
    Calculate the water catch rate

    Reference equations:
    DOT/FAA/CT-88/8-1 2.2.1.5 Equations 2-30, 2-31

    Note that chord (c) has been algebraically removed

    Calculation uses SI units
    (except for LWC, which is an entrenched exception)

    :param lwc: liquid water content, g/m^3
    :param u: airspeed, m/s
    :param beta: collection efficiency
    :return: water catch rate, kg/s/m^2
    """
    wcsr = lwc / units_helpers.G_PER_KG * u * beta
    return wcsr


def example_2_4_water_catch_span_rate(em):
    c, u, p, tk, drop_diameter, lwc, icing_time = get_example_flight_values()
    h_c_ratio = 0.12
    reference_value = 0.045  # lbm/min-ft-span
    h_projected = c * h_c_ratio
    water_catch_span_rate = calc_water_catch_span_rate(
        lwc, u, em, h_projected
    )  # kg/s/m-span
    wcsr_reference_units = (  # unit conversions to lbm/min-ft-span
        water_catch_span_rate
        * units_helpers.LBM_PER_KG
        * units_helpers.S_PER_MINUTE
        * units_helpers.ft_to_m(1)
    )
    print()
    print(f"DOT/FAA/CT-88/8-1 Example 2-4 Water Catch Span Rate Calculation")
    print(f"Reference value               : {reference_value:.4f} lbm/min-ft-span")
    print(f"calculated value              : {wcsr_reference_units:.4f} lbm/min-ft-span")
    fraction_difference = (wcsr_reference_units - reference_value) / reference_value
    print(
        f"fraction difference           :{fraction_difference    :+.4f} (calc-reference)/reference"
    )


def calc_ko(tk, p, u, drop_diameter_micrometer, significant_length):
    k = calc_k(tk, u, drop_diameter_micrometer, significant_length)
    re = langmuir_cylinder_values.calc_re(
        tk, p, u, drop_diameter_micrometer / units_helpers.MICROMETERS_PER_METER
    )
    lambda_lambda_s = langmuir_cylinder_values.calc_lambda_lambda_s(re)
    ko = k * lambda_lambda_s
    return k, re, lambda_lambda_s, ko


def get_example_flight_values():
    c = units_helpers.ft_to_m(3.1)
    ktas = 200
    u = units_helpers.ktas_to_ms(ktas)
    altitude = units_helpers.ft_to_m(10000)
    p = air_properties.calc_pressure(altitude)
    tf = -4
    tk = units_helpers.tf_to_k(tf)
    drop_diameter = 20
    lwc = 0.4
    icing_time = 5 * units_helpers.S_PER_MINUTE
    return c, u, p, tk, drop_diameter, lwc, icing_time


def example_2_1_water_drop_parameters():
    c, u, p, tk, drop_diameter, lwc, icing_time = get_example_flight_values()
    k_calc, re_calc, lambda_lambda_s_calc, ko_calc = calc_ko(tk, p, u, drop_diameter, c)
    re = 5.537e-6 * 0.001862 * 200 * 20 / 0.3252e-6
    mu = 0.3252e-6  # slug/ft-s
    mu_calc = langmuir_cylinder_values.calc_air_viscosity(tk)
    mu_calc_reference_units = (
        mu_calc
        / units_helpers.LBM_PER_SLUG
        * units_helpers.LBM_PER_KG
        / units_helpers.FT_PER_M
    )

    k2 = 1.958e-12 * 1 * 20**2 * 200 / 3.1 / 0.3252e-6
    lambda_lambda_s = 0.32
    ko = k2 * lambda_lambda_s
    mu_fd = (mu_calc_reference_units - mu) / mu
    ko_fd = (ko_calc - ko) / ko
    re_fd = (re_calc - re) / re
    k_fd = (k_calc - k2) / k2
    ls_fd = (lambda_lambda_s - lambda_lambda_s_calc) / lambda_lambda_s

    print()
    print(f"DOT/FAA/CT-88/8-1 Example 2-1 Calculation")
    print(f"mu reference               : {mu:.3e}")
    print(f"mu calculated              : {mu_calc_reference_units:.3e}")
    print(f"mu fraction difference     :{mu_fd:+.3f}")
    print(f"K reference                : {k2:.3e}")
    print(f"K calculated               : {k_calc:.3e}")
    print(f"K fraction difference      :{k_fd:+.3f}")
    print(f"Re_drop reference          : {re:.3e}")
    print(f"Re_drop calculated         : {re_calc:.3e}")
    print(f"Re_drop fraction difference:{re_fd:+.3f}")
    print(f"Ratio reference            : {lambda_lambda_s:.3e}")
    print(f"Ratio calculated           : {lambda_lambda_s_calc:.3e}")
    print(f"Ratio fraction difference  :{ls_fd:+.3f}")
    print(f"Ko reference               : {ko:.3e}")
    print(f"Ko calculated              : {ko_calc:.3e}")
    print(f"Ko fraction difference     :{ko_fd:+.3f}")
    return k_calc, re_calc, lambda_lambda_s_calc, ko_calc


def example_2_4_rime_ice_thick(beta):
    c, u, p, tk, drop_diameter, lwc, icing_time = get_example_flight_values()

    ice_density = 800  # kg/m^3
    reference_ice_thick = 0.39  # inch
    wcr = calc_local_water_catch_rate(lwc, u, beta)
    water_catch_intensive = wcr * icing_time  # kg/m^2
    thick = water_catch_intensive / ice_density  # m
    thick_reference_units = units_helpers.m_to_inch(thick)
    print()
    print(f"DOT/FAA/CT-88/8-1 Example 2-4 Rime Ice Thickness Calculation")
    print(f"Reference value               : {reference_ice_thick:.3f} inch")
    print(f"calculated value              : {thick_reference_units:.3f} inch")
    fraction_difference = (
        thick_reference_units - reference_ice_thick
    ) / reference_ice_thick
    print(
        f"fraction difference           :{fraction_difference:+.3f} (calc-reference)/reference"
    )


if __name__ == "__main__":
    k_calc, re_calc, lambda_lambda_s_calc, ko_calc = example_2_1_water_drop_parameters()
    print()
    print(f"Ko = {ko_calc:.4f}")

    em = figure_2_11.interp_em(ko_calc)
    print(f"E interpolated from Figure 2-11: {em:.3f}")

    figure_2_11.calc_e_and_make_plot(ko_calc)
    plt.xlim(0.001, 10)
    plt.legend()
    plt.savefig("Example 2-2 Em.png")

    beta = figure_2_12.calc_beta_and_make_plot(ko_calc)
    plt.xlim(0.001, 10)
    plt.legend()
    plt.savefig("Example 2-2 beta.png")

    print(f"Beta interpolated from Figure 2-12: {beta:.3f}")

    ratios_of_drop_diameters = langmuir_cylinder_values.langmuir_d_mids
    weights = langmuir_cylinder_values.langmuir_lwc_fractions

    c, u, p, tk, drop_diameter, lwc, icing_time = get_example_flight_values()

    em_bar = 0
    beta_bar = 0
    print()
    print("DOT/FAA/CT-88/8-1 Example 2-3 Table 2-2 Calculations")
    print(f"{'Ko':7s}  {'Δv':6s}{'E':6s} {'E*Δv':5s} {'Beta':s}  {'Beta*Δv':s}")
    kos = []
    ems_ = []
    betas_ = []
    for ratio, weight in zip(ratios_of_drop_diameters, weights):
        d_ = drop_diameter * ratio
        ko = calc_ko(tk, p, u, d_, c)[-1]
        kos.append(ko)
        em_ = figure_2_11.interp_em_with_linear_extrapolation(ko)
        ems_.append(em_)
        em_bar += em_ * weight
        beta_ = figure_2_12.interp_beta_max_with_linear_extrapolation(ko)
        betas_.append(beta_)
        beta_bar += beta_ * weight
        print(
            f"{ko:.5f}  {weight:.2f}  {em_:.3f}  {em_ * weight:.3f} {beta_:.3f} {beta_*weight:.3f} "
        )
    print(f"       E_bar = {em_bar:.3f}   Beta_bar = {beta_bar:.3f}")

    figure_2_11.calc_e_and_make_plot(ko_calc)
    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-3")
    plt.plot(kos, ems_, "s", fillstyle="none", label="7 bin components")
    plt.plot(ko_calc, em_bar, "*", label="7 bin weighted average")
    plt.xlim(0.001, 10)
    plt.legend()
    plt.savefig("Example 2-3 Em.png")

    figure_2_11.calc_e_and_make_plot(ko_calc)
    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-3")
    plt.plot(kos, ems_, "s", fillstyle="none", label="7 bin components")
    plt.plot(ko_calc, em_bar, "*", label="7 bin weighted average")
    plt.xlim(0.02, 0.1)
    plt.ylim(0.1, 0.3)
    plt.legend()
    plt.savefig("Example 2-3 Em zoom.png")

    beta = figure_2_12.calc_beta_and_make_plot(ko_calc)
    plt.plot(kos, betas_, "s", fillstyle="none", label="7 bin components")
    plt.plot(ko_calc, beta_bar, "*", label="7 bin weighted average")
    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-3")
    plt.xlim(0.001, 10)
    plt.legend()
    plt.savefig("Example 2-3 beta.png")

    example_2_4_water_catch_span_rate(em_bar)
    example_2_4_rime_ice_thick(beta_bar)

    plt.show()
""" Sample output:  
DOT/FAA/CT-88/8-1 Example 2-1 Calculation
mu reference               : 3.252e-07
mu calculated              : 3.365e-07
mu fraction difference     :+0.035
K reference                : 1.554e-01
K calculated               : 1.502e-01
K fraction difference      :-0.033
Re_drop reference          : 1.268e+02
Re_drop calculated         : 1.225e+02
Re_drop fraction difference:-0.034
Ratio reference            : 3.200e-01
Ratio calculated           : 3.259e-01
Ratio fraction difference  :-0.018
Ko reference               : 4.972e-02
Ko calculated              : 4.895e-02
Ko fraction difference     :-0.015

Ko = 0.0490
E interpolated from Figure 2-11: 0.231
Beta interpolated from Figure 2-12: 0.676

DOT/FAA/CT-88/8-1 Example 2-3 Table 2-2 Calculations
Ko       Δv    E      E*Δv  Beta  Beta*Δv
0.00710  0.05  0.021  0.001 0.251 0.013 
0.01686  0.10  0.084  0.008 0.451 0.045 
0.02813  0.20  0.142  0.028 0.561 0.112 
0.04895  0.30  0.231  0.069 0.676 0.203 
0.08096  0.20  0.325  0.065 0.756 0.151 
0.11817  0.10  0.402  0.040 0.808 0.081 
0.17296  0.05  0.488  0.024 0.849 0.042 
       E_bar = 0.237   Beta_bar = 0.647

DOT/FAA/CT-88/8-1 Example 2-4 Water Catch Span Rate Calculation
Reference value               : 0.0450 lbm/min-ft-span
calculated value              : 0.0446 lbm/min-ft-span
fraction difference           :-0.0091 (calc-reference)/reference

DOT/FAA/CT-88/8-1 Example 2-4 Rime Ice Thickness Calculation
Reference value               : 0.390 inch
calculated value              : 0.393 inch
fraction difference           :+0.008 (calc-reference)/reference
"""
