from math import pi
from icinganalysis.air_properties import (
    CP_AIR,
    calc_air_thermal_conductivity,
    calc_air_density,
    calc_air_viscosity,
)
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis.units_helpers import G_PER_KG
from icinganalysis.water_properties import (
    calc_vapor_p,
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
    RATIO_MOLECULAR_WEIGHTS,
    T_MP,
)


def calc_hc_cyl(tk, p, u, d_cyl):
    re = calc_air_density(tk, p) * u * d_cyl / calc_air_viscosity(tk)
    nu = 0.082 * re ** 0.747  # NACA-TR-1215 (F12)
    hc = nu * calc_air_thermal_conductivity(tk) / d_cyl
    return hc


def calc_rotating_cylinder_heat_balance_terms(
    tk, p, u, lwc, em, h, ts=T_MP, r=0.75, u1=1.0
):  # r from Appendix F
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


def find_critical_lwc_em_freeze(tk, p, u, h, u1=1.0):
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

    lwc_em = solve_minimize_f(f, bounds=(0, 100))

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

if __name__ == "__main__":

    from icinganalysis import NACA_TR_1215_fig_24_conditions
    import matplotlib.pyplot as plt

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

    for d, ylim, fig_scale in zip(data.keys(), ylims, fig_sizes):
        plt.figure(figsize=fig_scale)
        u = data[d]["u"]
        tk = data[d]["tk"]
        p = data[d]["p"]
        hcs = [calc_hc_cyl(tk, p, u, d_) for d_ in data[d]["d_cyls_m"]]
        critical_values = [
            find_critical_lwc_em_freeze(
                tk,
                p,
                u,
                hc,
                local_airspeed_ratio  # not entirely clear that Fig. 24 used the ratio
                * u,
            )
            for hc in hcs
        ]
        critical_values_no_u_ratio = [
            find_critical_lwc_em_freeze(
                tk, p, u, hc, 1 * u,  # not entirely clear that Fig. 24 used the ratio
            )
            for hc in hcs
        ]
        plt.plot(
            data[d]["d_cyls"],
            critical_values,
            "o",
            fillstyle="none",
            label=f"Calculated with U_ratio={local_airspeed_ratio}",
        )
        plt.plot(
            data[d]["d_cyls"],
            critical_values_no_u_ratio,
            "s",
            fillstyle="none",
            label=f"Calculated with U_ratio=1",
        )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlim(xlims)
        plt.ylim(ylim)
        n = d[:23] + " critical.png"
        plt.legend()
        plt.savefig(n, transparent=True)
        print(critical_values)

        plt.figure()
        plt.suptitle(d)
        plt.plot(c_d_cyl_critical_inch, c_critical_em_lwc)
        plt.plot(
            data[d]["d_cyls"],
            critical_values,
            "o",
            fillstyle="none",
            label=f"Calculated with U_ratio={local_airspeed_ratio}",
        )
        plt.plot(
            data[d]["d_cyls"],
            critical_values_no_u_ratio,
            "s",
            fillstyle="none",
            label=f"Calculated with U_ratio=1",
        )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlim(xlims)
        plt.ylim(ylim)
        plt.legend()

    plt.show()
