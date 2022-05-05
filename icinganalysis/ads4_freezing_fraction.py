import matplotlib.pyplot as plt
from icinganalysis.air_properties import calc_pressure
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis import messinger
from icinganalysis.langmuir_blodgett_table_ii import calc_beta_o
from icinganalysis.langmuir_cylinder_values import calc_k, calc_phi
from icinganalysis.units_helpers import (
    INCH_PER_M,
    FT_PER_M,
    KNOTS_PER_MS,
    tk_to_f,
)

# ADS-4 Figure 3-33
mvd = 15
d_cyl = 2 / INCH_PER_M
alt = 5000 / FT_PER_M
p = calc_pressure(alt)

for lwc, fig_name in (
    (0.2, "3-33"),
    (0.5, "3-34"),
    (1.0, "3-35"),
):
    vs = []
    for kts in range(1, 550 + 1, 1):
        u = kts / KNOTS_PER_MS

        def calc_diff(tk):
            beta = calc_beta_o(calc_k(tk, u, mvd, d_cyl), calc_phi(tk, p, u, d_cyl))
            hc = messinger.calc_htc_lam(tk, p, u, d_cyl)
            return abs(messinger.calc_n_unlimited(tk, p, u, hc, beta * lwc / 1000 * u) - 1)

        tk = solve_minimize_f(calc_diff, [173, 333])

        n_target = 0.67

        def calc_diff(tk):
            beta = calc_beta_o(calc_k(tk, u, mvd, d_cyl), calc_phi(tk, p, u, d_cyl))
            hc = messinger.calc_htc_lam(tk, p, u, d_cyl)
            return abs(messinger.calc_n_unlimited(tk, p, u, hc, beta * lwc / 1000 * u) - n_target)

        tk67 = solve_minimize_f(calc_diff, [173, 333])

        n_target = 0.0

        def calc_diff(tk):
            beta = calc_beta_o(calc_k(tk, u, mvd, d_cyl), calc_phi(tk, p, u, d_cyl))
            hc = messinger.calc_htc_lam(tk, p, u, d_cyl)
            return abs(messinger.calc_n_unlimited(tk, p, u, hc, beta * lwc / 1000 * u) - n_target)

        tk0 = solve_minimize_f(calc_diff, [173, 333])
        vs.append((u * KNOTS_PER_MS, tk_to_f(tk), tk_to_f(tk67), tk_to_f(tk0)))

    kts, tf1, tf67, tf0 = zip(*vs)

    plt.figure()
    plt.suptitle(f"ADS-4 Figure {fig_name}, LWC={lwc:.1f} g/m^3")
    plt.plot(kts, tf0, label="n=0")
    plt.plot(kts, tf67, label="n=0.67")
    plt.plot(kts, tf1, label="n=1")
    plt.xlim(0, 550)
    plt.ylim(-30, 40)
    plt.xlabel("Airspeed, KTAS")
    plt.ylabel("Ambient Temperature, F")
    plt.legend()
    plt.savefig(f"ADS-4_figure{fig_name}.png")

plt.show()
