from icinganalysis import units_helpers
from icinganalysis import air_properties
from icinganalysis.langmuir_cylinder_values import get_mids, langmuir_lwc_fractions
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis.intermediate import standard_computational_model
import matplotlib.pyplot as plt

p = air_properties.calc_pressure(units_helpers.ft_to_m(5000))
diameter = units_helpers.inch_to_m(2)
lwc = 0.2  # Figure 2-81
mvd = 15


def find_t_for_n(n, p, u, lwc, mvd, diameter, distribution="Langmuir A"):

    d_mids = get_mids(distribution)

    def f(t):
        beta = 0
        for r, w in zip(d_mids, langmuir_lwc_fractions):
            ko = standard_computational_model.calc_ko_d2(t, p, u, r * mvd, diameter)
            beta += w * max(
                0,
                standard_computational_model.cylinder_beta_max_from_figure_2_43.get_beta(
                    ko
                ),
            )
        hc = standard_computational_model.calc_hc_o_cylinder_from(u, t, diameter, p)
        n_ = standard_computational_model.calc_energy_and_mass_balance(
            t, p, u, lwc, hc, beta
        )[0]
        return abs(n - n_)

    t = solve_minimize_f(f, [233.15, 273.15])
    beta = 0
    for r, w in zip(d_mids, langmuir_lwc_fractions):
        ko = standard_computational_model.calc_ko_d2(t, p, u, r * mvd, diameter)
        beta += w * max(
            0,
            standard_computational_model.cylinder_beta_max_from_figure_2_43.get_beta(
                ko
            ),
        )
    if beta < 0.03:  # n is not well-defined if evaporation == impingement
        t = float("nan")
    return t


if __name__ == "__main__":

    vs = []

    for ktas in plt.np.arange(1, 550, 1):
        row = [ktas]
        n = 0
        t = find_t_for_n(n, p, units_helpers.ktas_to_ms(ktas), lwc, mvd, diameter)
        tf = units_helpers.tk_to_f(t)
        row.append(tf)
        n = 0.66
        t = find_t_for_n(n, p, units_helpers.ktas_to_ms(ktas), lwc, mvd, diameter)
        tf = units_helpers.tk_to_f(t)
        row.append(tf)
        n = 1
        t = find_t_for_n(n, p, units_helpers.ktas_to_ms(ktas), lwc, mvd, diameter)
        tf = units_helpers.tk_to_f(t)
        row.append(tf)
        vs.append(row)
    ktas, tf, tf_66, tf_1 = list(zip(*vs))
    plt.figure(figsize=(7, 7))
    plt.suptitle(
        "Calculation with Standard Computational Model"
        "\n2 inch diameter cylinder stagnation line analysis"
        "\n5000 ft. altitude, 0.2 g/m^3, MVD=15"
    )
    plt.plot(ktas, tf, "-", label="n=0")
    plt.plot(ktas, tf_66, "-.", label="n=0.66")
    plt.plot(ktas, tf_1, "--", label="n=1")
    plt.xlim(0, 550)
    plt.xlabel("Air Speed KTAS")
    plt.ylim(-30, 40)
    plt.ylabel("Ambient Temperature, F")
    plt.legend()
    plt.grid()
    plt.savefig("dot_faa_ct_88_8_1_fig_2-81.png")

    lwc = 0.5  # Figure 2-82

    vs = []

    for ktas in plt.np.arange(1, 550, 1):
        row = [ktas]
        n = 0
        t = find_t_for_n(n, p, units_helpers.ktas_to_ms(ktas), lwc, mvd, diameter)
        tf = units_helpers.tk_to_f(t)
        row.append(tf)
        n = 0.66
        t = find_t_for_n(n, p, units_helpers.ktas_to_ms(ktas), lwc, mvd, diameter)
        tf = units_helpers.tk_to_f(t)
        row.append(tf)
        n = 1
        t = find_t_for_n(n, p, units_helpers.ktas_to_ms(ktas), lwc, mvd, diameter)
        tf = units_helpers.tk_to_f(t)
        row.append(tf)
        vs.append(row)
    ktas, tf, tf_66, tf_1 = list(zip(*vs))
    plt.figure(figsize=(7, 7))
    plt.suptitle(
        "Calculation with Standard Computational Model"
        "\n2 inch diameter cylinder stagnation line analysis"
        "\n5000 ft. altitude, 0.5 g/m^3, MVD=15"
    )
    plt.plot(ktas, tf, "-", label="n=0")
    plt.plot(ktas, tf_66, "-.", label="n=0.66")
    plt.plot(ktas, tf_1, "--", label="n=1")
    plt.xlim(0, 550)
    plt.xlabel("Air Speed KTAS")
    plt.ylim(-30, 40)
    plt.ylabel("Ambient Temperature, F")
    plt.legend()
    plt.grid()
    plt.savefig("dot_faa_ct_88_8_1_fig_2-82.png")

    plt.show()
