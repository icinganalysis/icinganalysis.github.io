from math import pi
from scipy.interpolate import interp1d
from icinganalysis.air_properties import calc_altitude, CP_AIR
from icinganalysis.langmuir_cylinder_values import calc_re as calc_reynolds
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis.naca_tn_1472_data import interp_wet_dry_ratio
from icinganalysis.units_helpers import tc_to_k, tk_to_c
from icinganalysis.water_properties import (
    RATIO_MOLECULAR_WEIGHTS,
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
)

CAL_PER_JOULE = 0.23900573614
G_PER_KG = 1000
CM_PER_M = 100
MB_PER_PA = 0.01


def calc_vapor_p(tk):
    dt = tk - 273.15
    pv = 610.78 + (
        dt
        * (
            44.365
            + (
                dt
                * (
                    1.4289
                    + (
                        dt
                        * (
                            2.6506e-2
                            + (
                                dt
                                * (3.0312e-4 + (dt * (2.0341e-6 + (dt * (6.1368e-9)))))
                            )
                        )
                    )
                )
            )
        )
    )
    return pv


def calc_htc_lam(tk, p, u, d):
    k = (tk * 1.8 + 81) * 1e-7 / CAL_PER_JOULE * CM_PER_M
    reynolds = calc_reynolds(tk, p, u, d)
    nu = 0.24 * reynolds ** 0.6
    return nu * k / d


def calc_htc_turb(tk, p, u, d):
    k = (tk * 1.8 + 81) * 1e-7 / CAL_PER_JOULE * CM_PER_M
    reynolds = calc_reynolds(tk, p, u, d)
    nu = 0.024 * reynolds ** 0.805
    return nu * k / d


def get_htc(tk, p, u, d):
    reynolds = calc_reynolds(tk, p, u, d)
    if reynolds < 100000:
        return calc_htc_lam(tk, p, u, d)
    else:
        return calc_htc_turb(tk, p, u, d)


def find_p2(tk, p, tk2):
    p2_guess = p * (tk2 / tk) ** 3.5  # if a dry adiabat
    dp = (p - p2_guess) / 20
    p2 = float("nan")  # just to make the IDE happy
    for i in range(1000):  # it might take many more than 20 steps
        p2 = p - dp
        tk2_dry = tk * (p2 / p) ** (1 / 3.5)
        tk2_w = tk + (tk2_dry - tk) * interp_wet_dry_ratio(tk, calc_altitude(p))
        if tk2_w < tk2:
            p2 = interp1d((tk, tk2_w), (p, p2))(tk2)
            break
        tk = tk2_w
        p = p2
    return float(p2)


def calc_lwc_critical(tk, p, u, d, e=1.0):
    t_surface = 273.15
    hc = get_htc(tk, p, u, d)
    q_convection = hc * (t_surface - tk)
    n_s = RATIO_MOLECULAR_WEIGHTS * calc_vapor_p(t_surface) / p
    n_o = RATIO_MOLECULAR_WEIGHTS * calc_vapor_p(tk) / p
    m_evap = hc / CP_AIR * (n_s - n_o)
    q_evap = m_evap * L_EVAPORATION

    def calc_lwc_diff(lwc):
        m_water_impingement = e * lwc / G_PER_KG * u / pi
        q_sensible = m_water_impingement * WATER_SPECIFIC_HEAT * (t_surface - tk)
        q_freeze = m_water_impingement * L_FREEZING
        return abs(q_freeze - q_sensible - q_convection - q_evap)

    lwc = solve_minimize_f(calc_lwc_diff, [0, 20])
    return lwc


# fmt: off
d_fig1 = (
    0, 1.7, 6.1, 0, 0, 0, 0,
    -5, 2.4, 6.5, 0.65, 1.8, 0.6, 0.8,
    -10, 2.9, 6.7, 1.3, 2.9, 1.2, 1.4,
    -15, 3.3, 6.7, 1.9, 3.6, 1.8, 2,
    -20, 3.6, 6.6, 2.52, 4.5, 2.4, 2.6,
    -25, 3.65, 6.4, 3.15, 5.5, 3, 3.15,
    -30, 3.6, 6.2, 4, 6.6, 3.7, 3.8,
)
"""
Note: it appears that the notations m''5 (lwc_15cm_tc5) and m''20 (lwc_15cm_tc20) are swapped on the figure, 
they are corrected below
"""
# fmt: on
tcs_fig1 = d_fig1[::7]
tks_fig1 = [tc_to_k(_) for _ in d_fig1[::7]]
lwc_tc5_fig1 = d_fig1[1::7]
lwc_tc20_fig1 = d_fig1[2::7]
lwc_0_35cm_tc5_fig1 = d_fig1[3::7]
lwc_15cm_tc20_fig1 = d_fig1[4::7]
lwc_0_35cm_tc20_fig1 = d_fig1[5::7]
lwc_15cm_tc5_fig1 = d_fig1[6::7]


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Figure 1 conditions
    u = 90
    p0 = 900 / MB_PER_PA

    tk0 = tc_to_k(5)
    ps_tb5 = [find_p2(tk0, p0, tc_to_k(tc)) for tc in tcs_fig1]

    d = 0.35 / CM_PER_M
    e = 1
    lwcs_0035_tb5 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(tks_fig1, ps_tb5)
    ]
    print(lwcs_0035_tb5)

    d = 15 / CM_PER_M
    e = 0.6
    lwcs_15_tb5 = [calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(tks_fig1, ps_tb5)]
    print(lwcs_15_tb5)

    tk0 = tc_to_k(20)
    ps_tb20 = [find_p2(tk0, p0, tc_to_k(tc)) for tc in tcs_fig1]

    d = 0.35 / CM_PER_M
    e = 1
    lwcs_0035_tb20 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(tks_fig1, ps_tb20)
    ]
    print(lwcs_0035_tb20)

    d = 15 / CM_PER_M
    e = 0.4
    lwcs_15_tb20 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(tks_fig1, ps_tb20)
    ]
    print(lwcs_15_tb20)

    plt.figure()
    tcs = range(5, -30 - 5, -5)
    p5s = [find_p2(tc_to_k(5), p0, tc_to_k(_)) for _ in tcs]
    plt.plot(tcs, p5s, "-o", label="T_base = 5C")
    tcs = range(20, -30 - 5, -5)
    p20s = [find_p2(tc_to_k(20), p0, tc_to_k(_)) for _ in tcs]
    plt.plot(tcs, p20s, "-s", label="T_base = 20C")
    plt.legend()
    plt.xlim(20, -30)
    plt.xlabel("T at altitude, C")
    plt.ylim(0)
    plt.ylabel("Air pressure, Pa")
    plt.savefig("ludlam_ps.png")

    plt.figure()
    (line,) = plt.plot(
        tcs_fig1,
        lwc_0_35cm_tc5_fig1,
        label="Ludlam Figure 1, T_base=5C, Diameter=0.35 cm",
    )
    plt.plot(
        tcs_fig1,
        lwcs_0035_tb5,
        "--",
        c=line.get_color(),
        label="Calculated T_base=5C, Diameter=0.35 cm",
    )
    (line,) = plt.plot(
        tcs_fig1,
        lwc_0_35cm_tc20_fig1,
        label="Ludlam Figure 1, T_base=20C, Diameter=0.35 cm",
    )
    plt.plot(
        tcs_fig1,
        lwcs_0035_tb20,
        "--",
        c=line.get_color(),
        label="Calculated T_base=20C, Diameter=0.35 cm",
    )

    plt.xlim(0, -30)
    plt.xlabel("T at altitude, C")
    plt.ylim(0,)
    plt.ylabel("LWC, g/m^3")
    plt.legend()
    plt.savefig("ludlam0_35cm.png")

    plt.figure()
    (line,) = plt.plot(
        tcs_fig1, lwc_15cm_tc5_fig1, label="Ludlam Figure 1, T_base=5C, Diameter=15 cm"
    )
    plt.plot(
        tcs_fig1,
        lwcs_15_tb5,
        "--",
        c=line.get_color(),
        label="Calculated T_base=5C, Diameter=15 cm",
    )
    (line,) = plt.plot(
        tcs_fig1,
        lwc_15cm_tc20_fig1,
        label="Ludlam Figure 1, T_base=20C, Diameter=15 cm",
    )
    plt.plot(
        tcs_fig1,
        lwcs_15_tb20,
        "--",
        c=line.get_color(),
        label="Calculated T_base=20C, Diameter=15 cm",
    )

    plt.xlim(0, -30)
    plt.xlabel("T at altitude, C")
    plt.ylim(0, 7)
    plt.ylabel("LWC, g/m^3")
    plt.legend()
    plt.savefig("ludlam15cm.png")

    plt.show()
