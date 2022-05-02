from math import pi
from icinganalysis.air_properties import (
    CP_AIR,
    calc_pressure,
    calc_air_thermal_conductivity,
)
from icinganalysis.langmuir_cylinder_values import calc_re as calc_reynolds
from icinganalysis.iteration_helpers import solve_minimize_f, take_by
from icinganalysis.units_helpers import tc_to_k, FT_PER_M, INCH_PER_M, G_PER_KG
from icinganalysis.water_properties import (
    RATIO_MOLECULAR_WEIGHTS,
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
)

CAL_PER_JOULE = 0.23900573614
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


def calc_htc(tk, p, u, d):
    k = calc_air_thermal_conductivity(tk)
    reynolds = calc_reynolds(tk, p, u, d)
    nu = 0.24 * reynolds ** 0.6
    return nu * k / d


def calc_hc_cyl_naca_tr_1215(tk, p, u, d_cyl):
    reynolds = calc_reynolds(tk, p, u, d_cyl)
    nu = 0.082 * reynolds ** 0.747  # NACA-TR-1215 (F12)
    hc = nu * calc_air_thermal_conductivity(tk) / d_cyl
    return hc


def calc_lwc_critical(tk, p, u, d, e=1.0, r=0.85, calc_hc=calc_htc, rh=1.0):
    t_surface = 273.15
    hc = calc_hc(tk, p, u, d)
    q_convection = hc * (t_surface - tk)
    m_evap = (
        hc
        * RATIO_MOLECULAR_WEIGHTS
        / CP_AIR
        * (calc_vapor_p(t_surface) - rh * calc_vapor_p(tk))
        / p
    )
    q_evap = m_evap * L_EVAPORATION
    qv = hc * r * u ** 2 / (2 * CP_AIR)

    def calc_lwc_diff(lwc):
        m_water_impingement = e * lwc / G_PER_KG * u / pi
        q_sensible = m_water_impingement * WATER_SPECIFIC_HEAT * (t_surface - tk)
        qk = m_water_impingement * u ** 2 / 2
        q_freeze = m_water_impingement * L_FREEZING
        return abs(q_freeze + qk + qv - q_sensible - q_convection - q_evap)

    lwc = solve_minimize_f(calc_lwc_diff, [0, 20])
    return lwc


def calc_freezing_rate(tk, p, u, d, lwc, e=1.0, r=0.85, rh=1.0):
    t_surface = 273.15
    ml = calc_lwc_critical(tk, p, u, d, e, r, rh=rh)
    if lwc < ml:
        mi = lwc
        ff = 1
    else:
        ff = WATER_SPECIFIC_HEAT * (t_surface - tk) / L_FREEZING
        mi = ml + ff * (lwc - ml)
    return mi, ff, ml


alt = 0
d_fig1_180fps = (  # tc, lwc_crititcal
    -2.5,
    0.25,
    -10,
    1.46,
    -20,
    3.28,
    -27.5,
    4.95,
)
tcs_fig1_180fps = d_fig1_180fps[::2]
lwcs_fig1_180fps = d_fig1_180fps[1::2]

# fmt: off
df_fig3 = (
    -1, 0.17,
    -1.4, 0.03,
    -1.5, 0.21,
    -1.6, 0.28,
    -1.9, 0.08,
    -2.2, 0.11,
    -2.3, 0.19,
    -2.7, 0.14,
    -3.5, 0.15,
    -3.8, 0.1,
    -3.8, 0.24,
    -4.3, 0.21,
    -4.3, 0.3,
    -4.7, 0.29,
    -4.8, 0.28,
    -5, 0.32,
    -5.1, 0.31,
    -5.3, 0.44,
    -5.6, 0.42,
    -6, 0.44,
    -6.7, 0.44,
    -7, 0.44,
    -7.8, 0.51,
    -7.8, 0.56,
    -9.7, 0.44,
    -9.7, 0.5,
    -10.7, 0.44,
    -11.7, 0.44,
    -11.8, 0.5,
    -13.5, 0.44,
    -13.7, 0.44,
    -14.6, 0.43,
    -14.9, 0.44,
    -16.3, 0.51,
    -16.4, 0.43,
    -17.6, 0.51,
    -17.7, 0.43,
    -18.7, 0.43,
    -19.1, 0.43,
)
# fmt: on
tc_fig3 = df_fig3[::2]
lwc_fig3 = df_fig3[1::2]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from icinganalysis import csv_helper

    p = calc_pressure(0)
    u = 180 / FT_PER_M
    d_cyl = 0.125 / INCH_PER_M
    tcs = plt.np.linspace(-40, 0)
    lwcs = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    u = 300 / FT_PER_M
    d_cyl = 2 / INCH_PER_M
    lwcs_2 = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    plt.figure()
    plt.suptitle(
        "Fraser Figure 1 Calculated Ludlam Lines for 1/8 inch diameter rotating cylinder"
    )
    (line,) = plt.plot(
        tcs_fig1_180fps, lwcs_fig1_180fps, label="Fraser Figure 1 Sea Level V=180 fps"
    )
    plt.plot(tcs, lwcs, "--", c=line.get_color(), label="Calculated")
    plt.plot(tcs, lwcs_2, ":", label="Calculated 2 inch 300 fps")
    plt.xlim(-40, 0)
    plt.xlabel("Ambient Air Temperature, C")
    plt.ylim(0, 5)
    plt.ylabel("Liquid Water Content, LWC, g/m^3")
    plt.legend()

    plt.figure()
    plt.suptitle(
        "Fraser Figure 3 Calculated Ludlam Lines for 1/8 inch diameter cylinder"
    )
    e = 1
    p = calc_pressure(0)
    u = 180 / FT_PER_M
    d_cyl = 0.125 / INCH_PER_M
    lwcs = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    u = 300 / FT_PER_M
    d_cyl = 0.125 / INCH_PER_M
    lwcs_2 = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    u = 450 / FT_PER_M
    d_cyl = 0.1 / INCH_PER_M
    lwcs_3 = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]

    plt.plot(tcs, lwcs, label="Sea level, 1/8 inch, 180 fps")
    plt.plot(tcs, lwcs_2, label="Sea level, 1/8 inch, 300 fps")
    plt.plot(tcs, lwcs_3, label="Sea level, 0.1 inch, 450 fps")
    plt.xlim(-40, 0)
    plt.xlabel("Ambient Air Temperature, C")
    plt.ylim(0, 5)
    plt.ylabel("Liquid Water Content, LWC, g/m^3")
    plt.legend()

    csv_helper.save_data(
        "fraser_fig3.csv",
        ("tcs", "lwcs_180fps", "lwcs_300fps", "lwcs_450fps"),
        (tcs, lwcs, lwcs_2, lwcs_3),
    )

    plt.show()
