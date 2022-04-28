from math import pi
from scipy.interpolate import interp1d
from icinganalysis.air_properties import calc_altitude, CP_AIR, calc_pressure, calc_air_thermal_conductivity
from icinganalysis.langmuir_cylinder_values import calc_re as calc_reynolds
from icinganalysis.iteration_helpers import solve_minimize_f, take_by
from icinganalysis.naca_tn_1472_data import interp_wet_dry_ratio
from icinganalysis.units_helpers import tc_to_k, tk_to_c, FT_PER_M, INCH_PER_M
from icinganalysis.water_properties import (
    RATIO_MOLECULAR_WEIGHTS,
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
)
from icinganalysis.langmuir_cylinder_values import calc_em

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


def calc_lwc_critical(tk, p, u, d, e=1.0, r=0.85, calc_hc=calc_htc, rh=1.):
    t_surface = 273.15
    hc = calc_hc(tk, p, u, d)
    q_convection = hc * (t_surface - tk)
    m_evap = hc * RATIO_MOLECULAR_WEIGHTS / CP_AIR * (calc_vapor_p(t_surface) - rh * calc_vapor_p(tk)) / p
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


def calc_freezing_rate(tk, p, u, d, lwc, e=1.0, r=0.85, rh=1.):
    t_surface = 273.15
    # hc = calc_htc(tk, p, u, d)
    # q_convection = hc * (t_surface - tk)
    # m_evap = hc * RATIO_MOLECULAR_WEIGHTS / CP_AIR * (calc_vapor_p(t_surface) - calc_vapor_p(tk)) / p
    # q_evap = m_evap * L_EVAPORATION
    # qv = hc * r * u ** 2 / (2 * CP_AIR)
    m_water_impingement = e * lwc / G_PER_KG * u / pi
    # q_sensible = m_water_impingement * WATER_SPECIFIC_HEAT * (t_surface - tk)
    # qk = m_water_impingement * u ** 2 / 2

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
    -2.5, .25,
    -10, 1.46,
    -20, 3.28,
    -27.5, 4.95,
)
tcs_fig1_180fps = d_fig1_180fps[::2]
lwcs_fig1_180fps = d_fig1_180fps[1::2]

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
    plt.suptitle('Fraser Figure 1 Calculated Ludlam Lines for 1/8 inch diameter rotating cylinder')
    line, = plt.plot(tcs_fig1_180fps, lwcs_fig1_180fps, label="Fraser Figure 1 Sea Level V=180 fps")
    plt.plot(tcs, lwcs, '--', c=line.get_color(), label="Calculated")
    plt.plot(tcs, lwcs_2, ':', label="Calculated 2 inch 300 fps")
    plt.xlim(-40, 0)
    plt.xlabel('Ambient Air Temperature, C')
    plt.ylim(0, 5)
    plt.ylabel('Liquid Water Content, LWC, g/m^3')
    plt.legend()

    plt.figure()
    plt.suptitle('Fraser Figure 3 Calculated Ludlam Lines for 1/8 inch diameter cylinder')
    e = 1
    p = calc_pressure(0)
    u = 180 / FT_PER_M
    d_cyl = 0.125 / INCH_PER_M
    lwcs = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    u = 300 / FT_PER_M
    d_cyl = 0.125 / INCH_PER_M
    lwcs_2 = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    lwcs_2x = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl, calc_hc=calc_hc_cyl_naca_tr_1215) for _ in tcs]
    u = 450 / FT_PER_M
    d_cyl = 0.1 / INCH_PER_M
    lwcs_3 = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl) for _ in tcs]
    lwcs_3x = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl, calc_hc=calc_hc_cyl_naca_tr_1215) for _ in tcs]
    lwcs_3y = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl, rh=0.35) for _ in tcs]

    lwc = 0.45
    mi, ff, ml = zip(*[calc_freezing_rate(tc_to_k(_), p, u, d_cyl, lwc) for _ in tcs])
    print(mi)
    print(ff)
    print(ml)
    plt.plot(tcs, mi, '--')
    plt.plot(tcs, ff, ':')

    plt.plot(tcs, lwcs, label="Sea level, 1/8 inch, 180 fps")
    plt.plot(tcs, lwcs_2, label="Sea level, 1/8 inch, 300 fps")
    plt.plot(tcs, lwcs_2x, ':', label="Sea level, 1/8 inch, 300 fps")
    plt.plot(tcs, lwcs_3, label="Sea level, 0.1 inch, 450 fps")
    plt.plot(tcs, lwcs_3y, ':', label="Sea level, 0.1 inch, 450 fps")
    plt.xlim(-40, 0)
    plt.xlabel('Ambient Air Temperature, C')
    plt.ylim(0, 5)
    plt.ylabel('Liquid Water Content, LWC, g/m^3')
    plt.legend()

    csv_helper.save_data(
        'fraser_fig3.csv',
        ('tcs', 'lwcs_180fps', 'lwcs_300fps', 'lwcs_450fps'),
        (tcs, lwcs, lwcs_2, lwcs_3)
    )

    from icinganalysis import ludlam

    plt.figure()
    # Figure 1 conditions
    u = 90
    p0 = 900 / MB_PER_PA

    tk0 = tc_to_k(5)
    ps_tb5 = [ludlam.find_p2(tk0, p0, tc_to_k(tc)) for tc in ludlam.tcs_fig1]

    d = 0.35 / CM_PER_M
    e = 1
    lwcs_ludlam_0035_tb5 = [
        ludlam.calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(ludlam.tks_fig1, ps_tb5)
    ]
    lwcs_fraser_0035_tb5 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(ludlam.tks_fig1, ps_tb5)
    ]
    print(lwcs_ludlam_0035_tb5)
    line, = plt.plot(ludlam.tcs_fig1, ludlam.lwc_0_35cm_tc5_fig1, label="Ludlam Figure 1")
    plt.plot(ludlam.tcs_fig1, lwcs_fraser_0035_tb5, '--', c=line.get_color(), label="Fraser")

    d = 15 / CM_PER_M
    e = 0.6
    lwcs_fraser_15_tb5 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(ludlam.tks_fig1, ps_tb5)
    ]
    line, = plt.plot(ludlam.tcs_fig1, ludlam.lwc_15cm_tc5_fig1, label="Ludlam Figure 1 15 cm")
    plt.plot(ludlam.tcs_fig1, lwcs_fraser_15_tb5, '--', c=line.get_color(), label="Fraser")

    tk0 = tc_to_k(20)
    ps_tb20 = [ludlam.find_p2(tk0, p0, tc_to_k(tc)) for tc in ludlam.tcs_fig1]

    d = 0.35 / CM_PER_M
    e = 1
    lwcs_fraser_0035_tb20 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(ludlam.tks_fig1, ps_tb20)
    ]

    line, = plt.plot(ludlam.tcs_fig1, ludlam.lwc_0_35cm_tc20_fig1, label="Ludlam Figure 1 0.35 cm tb20")
    plt.plot(ludlam.tcs_fig1, lwcs_fraser_0035_tb20, '--', c=line.get_color(), label="Fraser")

    d = 15 / CM_PER_M
    e = 0.4
    lwcs_fraser_15_tb20 = [
        calc_lwc_critical(tk, p, u, d, e) for tk, p in zip(ludlam.tks_fig1, ps_tb20)
    ]
    line, = plt.plot(ludlam.tcs_fig1, ludlam.lwc_15cm_tc20_fig1, label="Ludlam Figure 1 15 cm tb20")
    plt.plot(ludlam.tcs_fig1, lwcs_fraser_15_tb20, '--', c=line.get_color(), label="Fraser")
    plt.legend()

    plt.figure()
    e = 0.9
    p = calc_pressure(0)
    u = 175 / FT_PER_M
    d_cyl = 0.25 / INCH_PER_M
    tc = -10
    tk = tc_to_k(tc)
    mvd = 20
    e = calc_em(tk, p, u, mvd, d_cyl)
    print('e', e)

    lwc = calc_lwc_critical(tc_to_k(tc), p, u, d_cyl, e=e)
    print(lwc)
    lwcs = plt.np.linspace(0, 4)
    mi, ff, ml = zip(*[calc_freezing_rate(tc_to_k(tc), p, u, d_cyl, _, e=e) for _ in lwcs])
    plt.plot(lwcs, mi, 'o', fillstyle='none')
    plt.plot(lwcs, ml, '--x')
    plt.plot(lwcs, lwcs, '-.')
    plt.plot(lwcs, ff, ':')
    mi, ff, ml = zip(*[calc_freezing_rate(tc_to_k(tc), p, u, d_cyl, _, e=e, rh=0.5) for _ in lwcs])
    plt.plot(lwcs, mi, '^', fillstyle='none')
    plt.xlim(0)
    plt.ylim(0)

    plt.figure()
    e = 1
    p = calc_pressure(0)
    u = 175 / FT_PER_M
    d_cyl = 1/16 / INCH_PER_M
    lwcs = plt.np.linspace(0, 2.5)
    mi, ff, ml = zip(*[calc_freezing_rate(tc_to_k(-6), p, u, d_cyl, _, e=e) for _ in lwcs])
    plt.plot(lwcs, mi)
    mi, ff, ml = zip(*[calc_freezing_rate(tc_to_k(-12), p, u, d_cyl, _, e=e) for _ in lwcs])
    plt.plot(lwcs, mi)
    plt.xlim(0, 2.5)
    plt.ylim(0, 2.5)

    plt.figure()
    tcs = plt.np.linspace(-5, -15)
    p = 80000
    u = 77
    e = 0.9
    d_cyl = 0.25 / INCH_PER_M
    lwcs = [calc_lwc_critical(tc_to_k(_), p, u, d_cyl, e) for _ in tcs]
    plt.plot(tcs, lwcs)
    plt.xlim(-15, 0)
    plt.ylim(0)




    plt.show()
