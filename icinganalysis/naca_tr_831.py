from scipy.interpolate import interp1d

from icinganalysis.water_properties import (
    WATER_SPECIFIC_HEAT,
    L_EVAPORATION,
    vapor_p_smithsonian_tables_1934,
    PA_PER_MM_HG,
    calc_vapor_pressure_gg,
    RATIO_MOLECULAR_WEIGHTS,
)
from icinganalysis.air_properties import (
    CP_AIR,
    calc_air_density,
    calc_pressure,
)
from icinganalysis import langmuir_cylinder_values
from icinganalysis import iteration_helpers
from icinganalysis.units_helpers import (
    LBM_PER_KG,
    FT_PER_M,
    MPH_PER_M_S,
    S_PER_HOUR,
    BTU_H_FT2_F_PER_W_M2_K,
    G_PER_KG,
    tf_to_k,
    tk_to_f,
)

FT_S_PER_MPH = 1.466667


def calc_n(tk, p):
    e_o = vapor_p_smithsonian_tables_1934(tk)
    n = RATIO_MOLECULAR_WEIGHTS * e_o / p
    return n


def equation_4_dry(u, tk, hc, t_surface):
    t_o = tk + u ** 2 / CP_AIR
    q_convection = hc * (t_surface - t_o)
    return q_convection


def equation_4(
    u, tk, p, hc, t_surface, water_catch_rate=0, t_o=None, limit_evaporation=False
):
    rho_air = calc_air_density(tk, p)
    k_h = hc / (rho_air * u * CP_AIR)
    if t_o is None:
        t_o = tk + u ** 2 / CP_AIR
    q_sensible = WATER_SPECIFIC_HEAT * water_catch_rate * (t_surface - t_o)
    q_convection = hc * (t_surface - t_o)
    n_s = calc_n(t_surface, p)
    n_o = calc_n(t_o, p)
    m_evaporation = k_h * rho_air * u * (n_s - n_o)
    if limit_evaporation:
        m_evaporation = min(water_catch_rate, k_h * rho_air * u * (n_s - n_o))
    q_evaporation = L_EVAPORATION * m_evaporation
    return q_sensible + q_convection + q_evaporation


def calc_x(t_o_f, t_s_f, p, p_o=None):
    t_o = tf_to_k(t_o_f)
    t_s = tf_to_k(t_s_f)
    e_o = vapor_p_smithsonian_tables_1934(t_o) / PA_PER_MM_HG
    e_s = vapor_p_smithsonian_tables_1934(t_s) / PA_PER_MM_HG
    if p_o is None:
        p_o = p
    # "In the present calculation the ratio of kw to kh has been taken as unity so that the equation becomes"
    x = 1 + 3.75 * (e_s - e_o) / (t_s_f - t_o_f) * (p_o / p)
    return x


def calc_x2(t_o_f, t_s_f, p_ratio):
    p_o = 101325
    p = p_o / p_ratio
    t_o = tf_to_k(t_o_f)
    t_s = tf_to_k(t_s_f)
    e_o = calc_vapor_pressure_gg(t_o)
    e_s = calc_vapor_pressure_gg(t_s)
    # "In the present calculation the ratio of kw to kh has been taken as unity so that the equation becomes"
    x = 1 + 1.0 * (e_s - e_o) / (t_s - t_o) * (
        RATIO_MOLECULAR_WEIGHTS * L_EVAPORATION
    ) / (p * CP_AIR)
    return x


def calc_equation_13(em, lwc, u, s_c, d, c):
    if s_c == 0:
        m = em * lwc / G_PER_KG * u  # using em as beta max?
    elif abs(s_c) <= 0.0125:
        m = em * lwc / G_PER_KG * u * d / 2
    else:
        m = 0
    return m


def calc_equation_13_naca_units(y, m, v_mph, s_c, d_cyl_ft, chord_ft):
    if s_c == 0:
        M = y / 100 * m * v_mph * FT_S_PER_MPH
    elif abs(s_c) <= 0.0125:
        M = y / 100 * 1.25 / 100 * m * v_mph * FT_S_PER_MPH * d_cyl_ft / 2 * chord_ft
    else:
        M = 0
    return M * S_PER_HOUR


_d_transition = (  # Figure 1, s/c, hc (BTU/h-ft^2-F)
    0,
    23,
    0.025,
    12,
    0.05,
    8.5,
    0.075,
    7,
    0.1,
    15,
    0.125,
    24.5,
    0.15,
    32,
    0.175,
    31,
    0.2,
    30,
)
s_c_transition = _d_transition[::2]
hc_btu_transition = _d_transition[1::2]
hcs_transition = [_ / BTU_H_FT2_F_PER_W_M2_K for _ in hc_btu_transition]
hc_interpolator_transition = interp1d(s_c_transition, hcs_transition)

_d = (  # Figure 1, s/c, hc (BTU/h-ft^2-F)
    0,
    23,
    0.025,
    12,
    0.05,
    8.5,
    0.075,
    7,
    0.1,
    5.5,
    0.125,
    4.5,
)
s_c = _d[::2]
hc_btu = _d[1::2]
hcs = [_ / BTU_H_FT2_F_PER_W_M2_K for _ in hc_btu]
hc_interpolator = interp1d(s_c, hcs)

fig3_tb_s_c = 0, 0.12
fig3_tb = 195, 107

fig3_ts_s_c = 0, 0.025, 0.05, 0.08, 0.11
fig3_ts = 100, 100, 118, 117, 95

fig4_tb_s_c = 0, 0.12
fig4_tb = 236, 98

fig4_ts_s_c = 0, 0.025, 0.05, 0.08, 0.11
fig4_ts = 86, 87, 94, 82, 67


def calc_dry_air_fig_3(hc_interpolator=hc_interpolator):
    chord_ft = 13.2
    v_mph = 180
    t_f = 28.5
    tk = (t_f + 459.67) / 1.8
    chord = chord_ft / FT_PER_M
    u = v_mph / MPH_PER_M_S
    delta_t_f_heat = 197
    hc_btu = 23
    hc = hc_btu / BTU_H_FT2_F_PER_W_M2_K
    ds = 0.025 * chord

    heating_air_flow_lbm = 84  # lbm/hr-ft.LE, upper surface (only)
    heating_air_flow = (
        heating_air_flow_lbm / LBM_PER_KG / S_PER_HOUR * FT_PER_M
    )  # kg/s/m-LE
    t_o = tk + u ** 2 / 2 / CP_AIR
    t_heating_air = t_o + delta_t_f_heat / 1.8
    h_heating_air_btu = 21  # BTU/hr-ft^2-F
    h_heating_air = h_heating_air_btu / BTU_H_FT2_F_PER_W_M2_K  # W/m^2-K

    tbs = []
    tss = []
    s_c_surface = []

    for s in [ds * i for i in range(6)]:
        s_c_surface.append(s / chord)
        hc = hc_interpolator(s / chord)

        def calc_ts(ts):
            qh = h_heating_air * (t_heating_air - ts)
            qc = hc * (ts - t_o)
            return abs(qh - qc)

        ts = iteration_helpers.solve_minimize_f(calc_ts, [173, 473])
        tss.append(ts)
        qh = h_heating_air * (t_heating_air - ts) * ds
        dt_heating_air = qh / (heating_air_flow * CP_AIR)
        tbs.append(t_heating_air)
        t_heating_air -= dt_heating_air

    return t_o, tss, tbs, s_c_surface


def calc_figure_6(t_f, mvd, lwcs=tuple([0.1 * _ for _ in range(0, 40 + 1, 1)])):
    chord_ft = 13.2
    d_cyl_ft = 0.72
    v_mph = 180
    alt_ft = 4000
    tk = (t_f + 459.67) / 1.8
    chord = chord_ft / FT_PER_M
    d_cyl = d_cyl_ft / FT_PER_M
    u = v_mph / MPH_PER_M_S
    p = calc_pressure(alt_ft / FT_PER_M)
    em = langmuir_cylinder_values.calc_em(tk, p, u, mvd, d_cyl)
    t_heating_air = tf_to_k(236)
    h_heating_air_btu = 21  # BTU/hr-ft^2-F
    h_heating_air = h_heating_air_btu / BTU_H_FT2_F_PER_W_M2_K  # W/m^2-K
    hc = hc_interpolator(0)
    tss = []
    for lwc in lwcs:
        t_o, lwc2 = calc_t_total_water_drops_in_equilibrium(tk, p, u, lwc)
        m = calc_equation_13(em, lwc2, u, 0, d_cyl, chord)
        if m <= 0:
            ts = calc_dry_surface_temperture(t_o, hc, h_heating_air, t_heating_air)
        else:

            ts = calc_wet_surface_temperture(
                t_o, p, u, hc, m, h_heating_air, t_heating_air, limit_evaporation=False
            )
        tss.append(ts)
    return lwcs, tss


def calc_wet_air_fig_4(hc_interpolator=hc_interpolator, t_f=28.5):
    chord_ft = 13.2
    d_cyl_ft = 0.72
    v_mph = 180
    alt_ft = 4000
    # t_f = 28.5
    tk = (t_f + 459.67) / 1.8
    chord = chord_ft / FT_PER_M
    d_cyl = d_cyl_ft / FT_PER_M
    u = v_mph / MPH_PER_M_S
    p = calc_pressure(alt_ft / FT_PER_M)
    ds = 0.0125 * chord
    mvd = 10
    lwc = 1.2

    em = langmuir_cylinder_values.calc_em(tk, p, u, mvd, d_cyl)

    heating_air_flow_lbm = 84  # lbm/hr-ft.LE, upper surface (only)
    heating_air_flow = (
        heating_air_flow_lbm / LBM_PER_KG / S_PER_HOUR * FT_PER_M
    )  # kg/s/m-LE
    t_o, lwc2 = calc_t_total_water_drops_in_equilibrium(tk, p, u, lwc)
    m = calc_equation_13(em, lwc2, u, 0, d_cyl, chord)
    t_heating_air = tf_to_k(t_f + 207.5)
    h_heating_air_btu = 21  # BTU/hr-ft^2-F
    h_heating_air = h_heating_air_btu / BTU_H_FT2_F_PER_W_M2_K  # W/m^2-K

    tbs = []
    tss = []
    s_c_surface = []
    limit_evaporation = False
    m_evaps = []

    for s in [ds * i for i in range(11)]:
        s_c_surface.append(s / chord)
        hc = hc_interpolator(s / chord)
        ts = calc_wet_surface_temperture(
            tk, p, u, hc, m, h_heating_air, t_heating_air, limit_evaporation
        )
        tss.append(ts)
        qh = h_heating_air * (t_heating_air - ts) * ds
        dt_heating_air = qh / (heating_air_flow * CP_AIR)
        tbs.append(t_heating_air)
        t_heating_air -= dt_heating_air
        rho_air = calc_air_density(t_o, p)
        k_h = hc / (rho_air * u * CP_AIR)
        n_s = calc_n(ts, p)
        n_o = calc_n(t_o, p)
        m_evaporation = k_h * rho_air * u * (n_s - n_o)
        m_evap = m_evaporation * ds
        m_evaps.append(m_evap)

    return t_o, tss, tbs, s_c_surface, m_evaps


def calc_wet_surface_temperture(
    t_o, p, u, hc, m, h_heating_air, t_heating_air, limit_evaporation=False
):
    def calc_ts(ts):
        qh = h_heating_air * (t_heating_air - ts)
        qc = hc * (ts - t_o)
        q_sensible = WATER_SPECIFIC_HEAT * m * (ts - t_o)  # does not include this one
        rho_air = calc_air_density(t_o, p)
        k_h = hc / (rho_air * u * CP_AIR)
        n_s = calc_n(ts, p)
        n_o = calc_n(t_o, p)
        m_evaporation = k_h * rho_air * u * (n_s - n_o)
        if limit_evaporation:
            m_evaporation = min(m, k_h * rho_air * u * (n_s - n_o))
        q_evaporation = L_EVAPORATION * m_evaporation

        return abs(qh - qc - q_evaporation - q_sensible)

    ts = iteration_helpers.solve_minimize_f(calc_ts, [223, 323])
    return ts


def calc_dry_surface_temperture(t_o, hc, h_heating_air, t_heating_air):
    def calc_ts(ts):
        qh = h_heating_air * (t_heating_air - ts)
        qc = hc * (ts - t_o)
        return abs(qh - qc)

    ts = iteration_helpers.solve_minimize_f(calc_ts, [173, 473])
    return ts


def calc_t_total_water_drops_in_equilibrium(tk, p, u, lwc):
    n0 = calc_n(tk, p)
    rhoair = calc_air_density(tk, p)
    n_lwc = lwc / G_PER_KG / rhoair

    def f(tkt):
        ke = u ** 2 / 2
        nt = calc_n(tkt, p)
        dn = nt - n0
        qb = (
            ke
            - CP_AIR * (tkt - tk)
            - n_lwc
            * WATER_SPECIFIC_HEAT
            * (tkt - tk)  # assume that this was not included
            - min(dn, lwc * rhoair * G_PER_KG) * L_EVAPORATION
        )
        return abs(qb)

    tkt = iteration_helpers.solve_minimize_f(f, [223, 323])
    nt = calc_n(tkt, p)
    dn = nt - n0
    d_lwc = dn / rhoair * G_PER_KG
    lwc2 = max(0, lwc - d_lwc)
    return tkt, lwc2


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    plt.figure()
    plt.suptitle("NACA-TR-831 Figure 3 Comparison")

    t_o, tss, tbs, s_c = calc_dry_air_fig_3()
    t_o_f = tk_to_f(t_o)

    (line,) = plt.plot(
        s_c,
        [tk_to_f(_) - t_o_f for _ in tss],
        label="Calculated wing surface (python, laminar)",
    )
    (line2,) = plt.plot(
        s_c,
        [tk_to_f(_) - t_o_f for _ in tbs],
        label="Calculated hot air (python, laminar)",
    )
    t_o, tss_transition, tbs_transition, s_c = calc_dry_air_fig_3(
        hc_interpolator_transition
    )

    plt.plot(
        s_c,
        [tk_to_f(_) - t_o_f for _ in tss_transition],
        "--",
        c=line.get_color(),
        label="Calculated wing surface (python, transition)",
    )
    plt.plot(
        s_c,
        [tk_to_f(_) - t_o_f for _ in tbs_transition],
        "--",
        c=line2.get_color(),
        label="Calculated hot air (python, trasition)",
    )

    plt.plot(
        fig3_tb_s_c,
        fig3_tb,
        "o",
        fillstyle="none",
        label="Flight average measured hot air",
    )
    plt.plot(
        fig3_ts_s_c,
        fig3_ts,
        "x",
        fillstyle="none",
        label="Flight average wing measured surface",
    )

    plt.ylim(0, 280)
    plt.yticks(range(0, 280 + 20, 20))
    plt.xlim(0, 0.2)
    plt.xlabel("S/C")
    plt.ylabel("T - T_o, F")

    plt.gca().invert_xaxis()
    plt.grid()
    plt.legend()
    plt.savefig("naca_tr_831_fig3_comparison.png")

    plt.figure()
    plt.suptitle("NACA-TR-831 Figure 4 Comparison")

    t_o, tss, tbs, s_c_surface, m_evaps = calc_wet_air_fig_4()

    (line,) = plt.plot(
        s_c_surface,
        [tk_to_f(_) for _ in tss],
        label="Calculated wing surface (python, laminar)",
    )
    (line2,) = plt.plot(
        s_c_surface,
        [tk_to_f(_) for _ in tbs],
        label="Calculated hot air (python, laminar)",
    )
    t_o, tss_transition, tbs_transition, s_c_surface, m_evaps_ = calc_wet_air_fig_4(
        hc_interpolator_transition
    )
    plt.plot(
        s_c_surface,
        [tk_to_f(_) for _ in tss_transition],
        "--",
        c=line.get_color(),
        label="Calculated wing surface (python, transition)",
    )
    plt.plot(
        s_c_surface,
        [tk_to_f(_) for _ in tbs_transition],
        "--",
        c=line2.get_color(),
        label="Calculated hot air (python, transition)",
    )

    plt.plot(
        fig4_tb_s_c,
        fig4_tb,
        "o",
        fillstyle="none",
        label="Flight average measured hot air",
    )
    plt.plot(
        fig4_ts_s_c,
        fig4_ts,
        "x",
        fillstyle="none",
        label="Flight average measured wing surface",
    )

    plt.ylim(0, 280)
    plt.yticks(range(0, 280 + 20, 20))
    plt.xlim(0, 0.2)
    plt.xlabel("S/C")
    plt.ylabel("T, F")

    plt.gca().invert_xaxis()
    plt.grid()
    plt.legend()
    plt.savefig("naca_tr_831_fig4_comparison.png")

    plt.figure()
    plt.suptitle("NACA-TR-831 Figure 5 Comparison")

    t_o, tss, tbs, s_c_surface, m_evaps = calc_wet_air_fig_4(t_f=0)

    (line,) = plt.plot(
        s_c_surface,
        [tk_to_f(_) for _ in tss],
        label="Calculated wing surface (python, laminar)",
    )
    (line2,) = plt.plot(
        s_c_surface,
        [tk_to_f(_) for _ in tbs],
        label="Calculated hot air (python, laminar)",
    )

    plt.ylim(0, 280)
    plt.yticks(range(0, 280 + 40, 40))
    plt.xlim(0, 0.2)
    plt.xlabel("S/C")
    plt.ylabel("T, F")

    plt.gca().invert_xaxis()
    plt.grid()
    plt.legend()
    plt.savefig("naca_tr_831_fig5_comparison.png")

    sc = s_c_surface[:2] + s_c_surface[3::2]
    ms = m_evaps[:2] + [v1 + v2 for v1, v2 in zip(m_evaps[3::2], m_evaps[4::2])]

    plt.figure()
    tf = 29
    mvd = 10
    lwcs, tks = calc_figure_6(tf, mvd)
    plt.plot(lwcs, [tk_to_f(_) for _ in tks], label=f"{tf:.0f}F, {mvd} MVD")
    tf = 29
    lwcs = [0.1 * _ for _ in range(0, 20 + 1, 1)]
    mvd = 40
    lwcs, tks = calc_figure_6(tf, mvd, lwcs)
    plt.plot(lwcs, [tk_to_f(_) for _ in tks], label=f"{tf:.0f}F, {mvd} MVD")
    lwcs = [0.1 * _ for _ in range(0, 20 + 1, 1)]
    tf = 0
    mvd = 10
    lwcs, tks = calc_figure_6(tf, mvd, lwcs)
    plt.plot(lwcs, [tk_to_f(_) for _ in tks], label=f"{tf:.0f}F, {mvd} MVD")

    plt.ylim(0, 140)
    plt.yticks(range(0, 140 + 20, 20))
    plt.xlim(0)
    plt.xlabel("LWC, g/m^3")
    plt.ylabel("T heated surface, F")
    plt.grid()
    plt.legend()
    plt.savefig("naca_tr_831_fig6_comparison.png")

    from icinganalysis import markdown_table_helper

    t_o, tss, tbs, s_c_surface, m_evaps = calc_wet_air_fig_4()
    sc = s_c_surface[:2] + s_c_surface[2::2]
    sc0 = sc[1:]
    ms = m_evaps[:2] + [v1 + v2 for v1, v2 in zip(m_evaps[2::2], m_evaps[3::2])]
    rows = []
    for sc, sc0, mevap in zip(sc, sc0, ms):
        rows.append(
            [f"{sc:.4f} to {sc0:.4f}", f"{mevap*LBM_PER_KG*S_PER_HOUR/FT_PER_M:.2f}"]
        )

    rows.append(["Total", f"{sum(ms)*LBM_PER_KG*S_PER_HOUR/FT_PER_M:.2f}"])

    t = markdown_table_helper.make_markdown_table(["s/c", "Rate of evaporation"], rows)

    t_o, tss, tbs, s_c_surface, m_evaps = calc_wet_air_fig_4(t_f=0)
    sc = s_c_surface[:2] + s_c_surface[3::2]
    ms = m_evaps[:2] + [v1 + v2 for v1, v2 in zip(m_evaps[3::2], m_evaps[4::2])]

    t_o, tss, tbs, s_c_surface, m_evaps0 = calc_wet_air_fig_4(t_f=0)
    ms0 = m_evaps0[:2] + [v1 + v2 for v1, v2 in zip(m_evaps0[2::2], m_evaps0[3::2])]
    for i, m in enumerate(ms0):
        rows[i].insert(1, f"{m*LBM_PER_KG*S_PER_HOUR/FT_PER_M:.2f}")
    rows[-1].insert(1, f"{sum(ms0)*LBM_PER_KG*S_PER_HOUR/FT_PER_M:.2f}")
    t = markdown_table_helper.make_nice_width_markdown_table(
        [
            "s/c",
            "Rate of evaporation T=0F (lbm/hr-ft-LE)",
            "Rate of evaporation T=28.5F (lbm/hr-ft-LE)",
        ],
        rows,
    )
    print()
    print(t)
    print()
    with open("naca_tr_831_table_ii.md", "w") as fd:
        fd.writelines(t)

    plt.show()
