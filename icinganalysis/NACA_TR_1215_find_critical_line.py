from math import pi
from scipy.optimize import minimize_scalar
from icinganalysis.water_properties import calc_vapor_p
from icinganalysis.water_properties import (
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
    RATIO_MOLECULAR_WEIGHTS,
T_MP
)
from icinganalysis import air_properties
from icinganalysis.air_properties import CP_AIR
G_PER_KG = 1000


def calc_hc_cyl(tk, p, u, d_cyl):
    re = (
        air_properties.calc_air_density(tk, p)
        * u
        * d_cyl
        / air_properties.calc_air_viscosity(tk)
    )
    nu = 0.082 * re ** 0.747  # NACA-TR-1215 (F12)
    hc = nu * air_properties.calc_air_thermal_conductivity(tk) / d_cyl
    return hc


def calc_rotating_cylinder_heat_balance_terms(tk, p, u, lwc, em, h, ts=T_MP, r=0.75, u1=None):  # r from Appendix F
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
        qf, q_conv, q_evap, q_sensible, q_kinetic = calc_rotating_cylinder_heat_balance_terms(tk, p, u, lwc, em, h, u1=u1)
        mf = qf / L_FREEZING
        me = q_evap / L_EVAPORATION
        return abs(lwc * em * u / G_PER_KG - mf - me)

    lwc_em = minimize_scalar(f, bounds=(0, 100), method="bounded").x
    qf, q_conv, q_evap, q_sensible, q_kinetic = calc_rotating_cylinder_heat_balance_terms(tk, p, u, lwc_em, em, h)
    me = q_evap / L_EVAPORATION
    lwc_em_evap = me * G_PER_KG / u
    lwc_em_freeze = lwc_em - lwc_em_evap
    return lwc_em_freeze


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
        hcs = [calc_hc_cyl(tk, p, u, d) for d in data[d]["d_cyls_m"]]
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

    plt.show()
