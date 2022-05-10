from math import pi, log10
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from icinganalysis.water_properties import (
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
    RATIO_MOLECULAR_WEIGHTS,
    T_MP,
    calc_vapor_p,
)
from icinganalysis.air_properties import (
    CP_AIR,
    calc_air_density,
    calc_air_thermal_conductivity,
    calc_air_viscosity,
)
from icinganalysis.messinger import (
    find_lwc_critical_lam,
    find_lwc_critical_turb,
    find_lwc_critical_rough,
)
from icinganalysis.ludlam import calc_lwc_critical
from icinganalysis.ltr_lt_92 import interp_lwc_critical as interp_lwc_critical_ltr
from icinganalysis.langmuir_blodgett_multicylinder import (
    calc_em_with_distribution_to_use,
)
from icinganalysis.units_helpers import G_PER_KG, INCH_PER_M
from icinganalysis import fraser


def calc_hc_cyl(tk, p, u, d_cyl):
    re = calc_air_density(tk, p) * u * d_cyl / calc_air_viscosity(tk)
    nu = 0.082 * re ** 0.747  # NACA-TR-1215 (F12)
    hc = nu * calc_air_thermal_conductivity(tk) / d_cyl
    return hc


def calc_rotating_cylinder_heat_balance_terms(
    tk, p, u, lwc, em, h, ts=T_MP, r=0.75, u1=None
):  # r from Appendix F
    if u1 is None:
        u1 = u
    q_conv = pi * h * (ts - tk - u ** 2 / 2 / CP_AIR * (1 - u1 ** 2 / u ** 2 * (1 - r)))
    q_evap = (
        pi
        * h
        * RATIO_MOLECULAR_WEIGHTS
        / CP_AIR
        * L_EVAPORATION
        * (calc_vapor_p(ts) - calc_vapor_p(tk))
        / p
    )
    q_sensible = em * lwc / CP_AIR * u * WATER_SPECIFIC_HEAT * (ts - tk)
    q_kinetic = -em * lwc / CP_AIR * u * u ** 2 / 2
    q_freezing = q_conv + q_evap + q_sensible + q_kinetic

    return q_freezing, q_conv, q_evap, q_sensible, q_kinetic


def find_critical_lwc_em_freeze(tk, p, u, h, u1=None):
    if u1 is None:
        u1 = u
    em = 1

    def f(lwc):
        (
            qf,
            q_conv,
            q_evap,
            q_sensible,
            q_kinetic,
        ) = calc_rotating_cylinder_heat_balance_terms(tk, p, u, lwc, em, h, u1=u1)
        mf = qf / L_FREEZING
        me = q_evap / L_EVAPORATION
        return abs(lwc * em * u / G_PER_KG - mf - me)

    lwc_em = minimize_scalar(f, bounds=(0, 100), method="bounded").x
    (
        qf,
        q_conv,
        q_evap,
        q_sensible,
        q_kinetic,
    ) = calc_rotating_cylinder_heat_balance_terms(tk, p, u, lwc_em, em, h)
    me = q_evap / L_EVAPORATION
    lwc_em_evap = me * G_PER_KG / u
    lwc_em_freeze = lwc_em - lwc_em_evap
    return lwc_em_freeze


d_cyls = ([0.19, 0.535, 1.3, 3, 4.6],)
em_lwcs = ([0.235, 0.175, 0.13, 0.05, 0.025],)

c_d_cyl_inch = (0.185, 0.53, 1.25, 3, 4.5)
c_d_cyl = [_ * 0.0254 for _ in c_d_cyl_inch]
c_d_cyl_em_lwc = (0.235, 0.18, 0.134, 0.05, 0.025)
c_d_cyl_critical_inch = (0.1, 5.9)
c_d_cyl_critical = [_ * 0.0254 for _ in c_d_cyl_critical_inch]
c_critical_em_lwc = (0.332, 0.118)
c_d_cyl_runoff_inch = (0.15, 3.6)
c_d_cyl_runoff = [_ * 0.0254 for _ in c_d_cyl_runoff_inch]
c_runoff_em_lwc = (0.248, 0.109)

# fmt: off
c_d = (
    0.1, 0.4,
    0.15, 0.379,
    0.2, 0.35,
    0.25, 0.33,
    0.3, 0.315,
    0.35, 0.3,
    0.4, 0.28,
    0.5, 0.25,
    0.6, 0.23,
    0.7, 0.21,
    0.8, 0.191,
    0.9, 0.175,
    1, 0.162,
    1.25, 0.134,
    1.5, 0.115,
    2, 0.086,
    2.5, 0.066,
    3, 0.05,
    3.5, 0.04,
    4, 0.032,
    5, 0.021,
)
# fmt: on
c_d_cyl_impingement_inch = c_d[::2]
c_d_cyl_impingement = [_ * 0.0254 for _ in c_d_cyl_impingement_inch]
c_impingement_em_lwc = c_d[1::2]

b_d_cyl_inch = (0.223, 0.55, 1.25, 3)
b_d_cyl = [_ * 0.0254 for _ in b_d_cyl_inch]
b_d_cyl_em_lwc = (0.35, 0.28, 0.195, 0.09)
b_d_cyl_critical_inch = (0.1, 3.5)
b_d_cyl_critical = [_ * 0.0254 for _ in b_d_cyl_critical_inch]
b_critical_em_lwc = (0.45, 0.18)
b_d_cyl_runoff_inch = (0.1, 3.5)
b_d_cyl_runoff = [_ * 0.0254 for _ in b_d_cyl_runoff_inch]
b_runoff_em_lwc = (0.43, 0.17)

d_d_cyl_inch = (
    0.265,
    0.61,
    1.3,
    3,
)
d_d_cyl = [_ * 0.0254 for _ in d_d_cyl_inch]
d_d_cyl_em_lwc = (
    1.1,
    0.885,
    0.73,
    0.595,
)

d_d_cyl_critical_inch = 0.155, 5.4
d_d_cyl_critical = [_ * 0.0254 for _ in d_d_cyl_critical_inch]
d_critical_em_lwc = 1.33, 0.53
d_d_cyl_runoff_inch = (0.155, 5.4)
d_d_cyl_runoff = [_ * 0.0254 for _ in d_d_cyl_runoff_inch]
d_runoff_em_lwc = (1.27, 0.51)

a_d_cyl_critical_inch = 0.155, 5.1
a_d_cyl_critical = [_ * 0.0254 for _ in a_d_cyl_critical_inch]
a_critical_em_lwc = 0.68, 0.28
a_d_cyl_runoff_inch = float("nan"), float("nan")
a_d_cyl_runoff = float("nan"), float("nan")
a_runoff_em_lwc = float("nan"), float("nan")

vs = (
    (a_d_cyl_critical_inch, a_critical_em_lwc, a_d_cyl_runoff_inch, a_runoff_em_lwc),
    (b_d_cyl_critical_inch, b_critical_em_lwc, b_d_cyl_runoff_inch, b_runoff_em_lwc),
    (c_d_cyl_critical_inch, c_critical_em_lwc, c_d_cyl_runoff_inch, c_runoff_em_lwc),
    (d_d_cyl_critical_inch, d_critical_em_lwc, d_d_cyl_runoff_inch, d_runoff_em_lwc),
)


def make_log_yticks(ymin, ymax):
    vs = [ymin]
    for i in range(20):
        increment = 10 ** (int(log10(vs[-1])) - 1)
        v = vs[-1] + increment
        if v > ymax:
            break
        vs.append(v)
    return vs


def make_fig(
    case,
    d_cyl_inch,
    d_cyl_em_lwc,
    d_cyl_critical_inch,
    critical_em_lwc,
    d_cyl_runoff_inch,
    runoff_em_lwc,
    calc_critical_values,
    calc_critical_values_no_u_ratio,
    xlims=(0.1, 10),
    ylims=(0.01, 10),
    figsize=(7, 8),
):
    plt.figure(figsize=figsize)
    fig_name = case[:23]
    plt.suptitle(case)
    plt.plot(
        d_cyl_inch,
        d_cyl_em_lwc,
        "o",
        fillstyle="none",
        c="k",
        ms=10,
        mew=3,
        label=f"{fig_name} Cylinder masses",
    )
    plt.plot(d_cyl_critical_inch, critical_em_lwc, label=f"{fig_name} Critical Line")
    plt.plot(d_cyl_runoff_inch, runoff_em_lwc, "--", label=f"{fig_name} Run-off Line")
    plt.plot(
        d_cyl_inch,
        calc_critical_values,
        "o",
        fillstyle="none",
        label=f"NACA-TR-1215 Calculated with U_ratio={local_airspeed_ratio}",
    )
    plt.plot(
        d_cyl_inch,
        calc_critical_values_no_u_ratio,
        "s",
        fillstyle="none",
        label=f"NACA-TR-1215 Calculated with U_ratio=1",
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim(xlims)
    plt.ylim(ylims)

    from matplotlib.ticker import FormatStrFormatter

    plt.tick_params(axis="y", which="minor")
    plt.gca().yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
    plt.grid(which="both", axis="both")

    plt.xlabel("Cylinder diameter, inch")
    plt.ylabel("Em*LWC, g/m^3")
    plt.legend()


if __name__ == "__main__":
    from icinganalysis import NACA_TR_1215_fig_24_conditions

    data = NACA_TR_1215_fig_24_conditions.conditions_data
    local_airspeed_ratio = 1.12  # Appendix F

    xlims = (0.1, 10)
    ylims = (0.02, 0.8), (0.04, 0.6), (0.02, 0.6), (0.4, 2.0)

    fig_sizes = (
        (3.6, 2.9),
        (3.6, 2.1),
        (3.6, 2.67),
        (3.6, 1.27),
    )  # make over-lays to compare with Figure 24

    for case, ylim, fig_scale, pvs in zip(data.keys(), ylims, fig_sizes, vs):
        d_cyl_critical_inch, critical_em_lwc, d_cyl_runoff_inch, runoff_em_lwc = pvs
        u = data[case]["u"]
        tk = data[case]["tk"]
        p = data[case]["p"]
        mvd = data[case]["mvd"]
        distribution = data[case]["distribution"]
        hcs = [calc_hc_cyl(tk, p, u, d_) for d_ in data[case]["d_cyls_m"]]
        critical_values = [
            find_critical_lwc_em_freeze(
                tk,
                p,
                u,
                hc,
                local_airspeed_ratio
                * u,  # not entirely clear that Fig. 24 used the ratio
            )
            for hc in hcs
        ]
        critical_values_no_u_ratio = [
            find_critical_lwc_em_freeze(
                tk, p, u, hc, 1 * u,  # not entirely clear that Fig. 24 used the ratio
            )
            for hc in hcs
        ]
        messinger_lams = [
            find_lwc_critical_lam(tk, p, u, 1 / pi, d_) for d_ in data[case]["d_cyls_m"]
        ]
        messinger_turbs = [
            find_lwc_critical_turb(tk, p, u, 1 / pi, d_)
            for d_ in data[case]["d_cyls_m"]
        ]
        messinger_rough = [
            find_lwc_critical_rough(tk, p, u, 1 / pi, d_)
            for d_ in data[case]["d_cyls_m"]
        ]
        ludlam = [calc_lwc_critical(tk, p, u, d_, 1) for d_ in data[case]["d_cyls_m"]]
        em_0_25 = calc_em_with_distribution_to_use(
            tk, p, u, mvd, 0.25 / INCH_PER_M, distribution
        )
        em_0_1 = calc_em_with_distribution_to_use(
            tk, p, u, mvd, 0.1 / INCH_PER_M, distribution
        )
        lwc_ltr = interp_lwc_critical_ltr(tk, u)

        make_fig(
            case,
            data[case]["d_cyls"],
            data[case]["em_lwcs"],
            d_cyl_critical_inch,
            critical_em_lwc,
            d_cyl_runoff_inch,
            runoff_em_lwc,
            critical_values,
            critical_values_no_u_ratio,
            xlims,
            ylims=ylim,
        )
        plt.savefig(f"{case[:23]}_critical.png")
        plt.plot(
            data[case]["d_cyls"],
            messinger_lams,
            ":^",
            label="Messinger nu = 0.24 * reynolds ** 0.6",
        )
        plt.plot(
            data[case]["d_cyls"],
            messinger_turbs,
            ":v",
            label="Messinger nu = 0.024 * reynolds ** 0.805",
        )
        plt.plot(
            data[case]["d_cyls"],
            messinger_rough,
            ":>",
            label="Messinger nu = 0.082 * re ** 0.747",
        )

        lwc_fraser = [
            fraser.calc_lwc_critical(tk, p, u, d_, 1) for d_ in data[case]["d_cyls_m"]
        ]
        plt.plot(
            data[case]["d_cyls"],
            lwc_fraser,
            "--x",
            ms=14,
            label="Fraser nu = 0.24 * reynolds ** 0.6",
        )

        plt.plot(data[case]["d_cyls"], ludlam, ":x", label="Ludlam")
        plt.plot(0.1, lwc_ltr * em_0_1, "<", ms=14, mew=3, c="r", label="LT-LTR-92")

        plt.legend()
        plt.savefig(f"{case[:23]}_critical_plus.png")

    plt.show()
