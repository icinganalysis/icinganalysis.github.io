from scipy.interpolate import interp1d
from icinganalysis import air_properties
from icinganalysis.iteration_helpers import (
    solve_minimize_f,
    trim_extra_x_y_zeros,
    get_x_y_split_at_x_value,
)
from icinganalysis import langmuir_cylinder_values
from icinganalysis.naca_tn_1472_data import (
    get_beta_interpolator_for_condition,
    u_ratio_interpolator,
    q_h_interp,
    s_c_tks,
    tks,
    tk_surface_interp,
    interp_wet_dry_ratio,
    s_c_h,
    h,
    h_interp,
    q_h_interp_8e,
    tk_surface_interp_8e,
    s_c_h_8e,
    h_8e,
    calc_k_airfoil,
    q_dry_fig23_interpolator,
    q_dry_fig23_recalc_interpolator,
    q_dry_fig26_interpolator,
    q_total_fig26_interpolator,
    h_turb_fig25_interpolator,
    h_measured_fig25_interpolator,
    s_c_h_fig25,
    h_turb_fig25,
    h_measured_fig25,
    f_wet_interpolator,
    get_scs_betas,
)


from icinganalysis.units_helpers import (
    MPH_PER_M_S,
    G_PER_KG,
    BTU_H_PER_W,
    BTU_H_FT2_F_PER_W_M2_K,
    M_PER_FT,
    FT_PER_M,
    tf_to_k,
    tk_to_f,
    LBM_PER_KG,
    S_PER_HOUR,
)
from icinganalysis import water_properties


calc_vapor_p = water_properties.calc_vapor_p


def calc_h_btu(h):
    return [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h]


def calc_q_btu(q):
    return [_ * BTU_H_PER_W / (FT_PER_M ** 2) for _ in q]


def calc_table_i_condition_5(r=0.84):
    u = 157 / MPH_PER_M_S
    p = air_properties.calc_pressure(9010 / FT_PER_M)
    tk = tf_to_k(24)
    lwc = 0.32
    mvd = 9
    distribution = "Langmuir C"
    chord = 8 * M_PER_FT
    k = calc_k_airfoil(tk, u, mvd, chord)
    print(f"MVD {mvd}, K {k}")
    bi = get_beta_interpolator_for_condition(tk, u, mvd, chord, distribution)

    hs = []
    tos = []
    tos_wet = []
    h_drys = []
    urs = []
    betas = []
    svs = plt.np.linspace(
        -0.12, 0.59, int((0.59 - -0.12) * 100 * 4)
    )  # 0.0025 s/c spacing
    hs_wet = []
    q_convs = []
    q_evaps = []
    q_water_sensible = []
    qhs = []

    for sc in svs:
        u_ratio = u_ratio_interpolator(abs(sc))
        urs.append(u_ratio)
        tko_wet = calc_tko_equation_18(tk, u, p, u_ratio)
        beta = bi(sc)
        betas.append(beta)
        qh = q_h_interp_8e(sc)
        ts = tk_surface_interp(sc)
        tko = tk + u ** 2 / 2 / air_properties.CP_AIR * (1 - u_ratio ** 2 * (1 - r))
        x = calc_x_equation_22(ts, tko, p)
        m_dot = beta * lwc / G_PER_KG * u
        tk_surface = tk_surface_interp_8e(sc)

        def calc_apparent_h(h):
            return abs(
                qh
                - (
                    m_dot * water_properties.WATER_SPECIFIC_HEAT * (tk_surface - tk)
                    + h * x * (tk_surface - tko_wet)
                )
            )

        h = solve_minimize_f(calc_apparent_h, [1, 1000])
        hs_wet.append(h)

        def calc_h_dry(h):
            return abs(qh - (h * (tk_surface - tko)))

        h_dry = solve_minimize_f(calc_h_dry, [1, 1000])
        h_drys.append(h_dry)

        if m_dot > 0:
            hs.append(h)
        else:
            hs.append(h_dry)

        tos.append(tko)
        tos_wet.append(tko_wet)
        q_convs.append(hs[-1] * (tk_surface - tko_wet))
        q_evaps.append(hs[-1] * (x - 1) * (tk_surface - tko_wet))
        q_water_sensible.append(
            m_dot * water_properties.WATER_SPECIFIC_HEAT * (tk_surface - tk)
        )
        qhs.append(qh)
    return (
        svs,
        hs,
        tos,
        tos_wet,
        h_drys,
        urs,
        betas,
        hs_wet,
        q_convs,
        q_evaps,
        q_water_sensible,
        qhs,
    )


def calc_tko_equation_18(tk, u, p, u_ratio=1, r=0.84):
    alt = air_properties.calc_altitude(p)
    wet_dry_ratio = interp_wet_dry_ratio(tk, alt)
    tko = (
        tk
        + u ** 2
        / 2
        / air_properties.CP_AIR
        * (1 - u_ratio ** 2 * (1 - r))
        * wet_dry_ratio
    )
    return tko


def calc_x_equation_22(ts, tko, p):
    e = calc_vapor_p(tko)
    es = calc_vapor_p(ts)
    x = (
        1
        + water_properties.L_EVAPORATION
        / air_properties.CP_AIR
        * (es - e)
        / (ts - tko)
        * water_properties.RATIO_MOLECULAR_WEIGHTS
        / p
    )
    return x


def calc_table_i_condition_1(r=0.84):
    u = 167 / MPH_PER_M_S
    p = air_properties.calc_pressure(9100 * M_PER_FT)
    tk = tf_to_k(24)
    lwc = 0.38
    mvd = 10
    distribution = "Langmuir C"
    chord = 8 * M_PER_FT
    bi = get_beta_interpolator_for_condition(tk, u, mvd, chord, distribution)
    hs = []
    tos = []
    tos_wet = []
    h_drys = []
    urs = []
    betas = []
    svs = plt.np.linspace(
        -0.12, 0.59, (int((0.59 - -0.12) * 100) + 1) * 4
    )  # 0.0025 s/c spacing
    hs_wet = []

    for sc in svs:
        u_ratio = u_ratio_interpolator(abs(sc))
        urs.append(u_ratio)
        tko_wet = calc_tko_equation_18(tk, u, p, u_ratio)
        beta = bi(sc)
        betas.append(beta)
        qh = q_h_interp(sc)
        ts = tk_surface_interp(sc)
        tko = tk + u ** 2 / 2 / air_properties.CP_AIR * (1 - u_ratio ** 2 * (1 - r))
        x = calc_x_equation_22(ts, tko, p)
        m_dot = beta * lwc / G_PER_KG * u
        tk_surface = tk_surface_interp(sc)

        def calc_apparent_h_error(h):
            return abs(
                qh
                - (
                    m_dot * water_properties.WATER_SPECIFIC_HEAT * (tk_surface - tk)
                    + h * x * (tk_surface - tko_wet)
                )
            )

        h = solve_minimize_f(calc_apparent_h_error, [1, 1000])
        hs_wet.append(h)

        h_dry = qh / (tk_surface - tko)
        h_drys.append(h_dry)

        if m_dot > 0:
            hs.append(h)
        else:
            hs.append(h_dry)

        tos.append(tko)
        tos_wet.append(tko_wet)
    return svs, hs, tos, tos_wet, h_drys, urs, betas, hs_wet


def calc_fig_23_hs(r=0.84):
    u = 157 / MPH_PER_M_S
    tk = tf_to_k(24)
    svs = plt.np.linspace(
        -0.12, 0.59, int(((0.59 - -0.12) * 100 + 1) * 4)
    )  # 0.0025 s/c spacing
    hs = []
    hs_recalc = []
    for sc in svs:
        ts = tk_surface_interp(sc)
        q_dry = q_dry_fig23_interpolator(sc)
        u_ratio = u_ratio_interpolator(abs(sc))
        tko = tk + u ** 2 / 2 / air_properties.CP_AIR * (1 - u_ratio ** 2 * (1 - r))
        h = q_dry / (ts - tko)
        hs.append(h)
        q_dry = q_dry_fig23_recalc_interpolator(sc)
        h = q_dry / (ts - tko)
        hs_recalc.append(h)
    return svs, hs, hs_recalc


def calc_figure_26_(r=0.84):
    u = 167 / MPH_PER_M_S
    p = air_properties.calc_pressure(12000 * M_PER_FT)
    tk = tf_to_k(20)
    lwc = 0.5
    mvd = 25
    distribution = "Langmuir E"
    chord = 8 * M_PER_FT
    bi = get_beta_interpolator_for_condition(tk, u, mvd, chord, distribution)
    svs = plt.np.linspace(
        0, 0.18, int(((0.18 - 0) * 100 + 1) * 4)
    )  # 0.0025 s/c spacing
    hs = []
    tos = []
    tos_wet = []
    h_drys = []
    urs = []
    betas = []
    hs_wet = []
    q_convs = []
    q_evaps = []
    q_water_sensible = []
    qhs = []
    tss = []
    m_dots = []

    for sc in svs:
        u_ratio = u_ratio_interpolator(abs(sc))
        urs.append(u_ratio)
        tko_wet = calc_tko_equation_18(tk, u, p, u_ratio)
        beta = bi(sc)
        betas.append(beta)
        m_dot = beta * lwc / G_PER_KG * u
        m_dots.append(m_dot)
        qh = q_total_fig26_interpolator(sc)
        tko = tk + u ** 2 / 2 / air_properties.CP_AIR * (1 - u_ratio ** 2 * (1 - r))

        def calc_ts(ts):
            x = calc_x_equation_22(ts, tko, p)
            if m_dot <= 0:
                x = 1 + (x - 1) * 0.5
            h = q_dry_fig26_interpolator(sc) / (ts - tko)
            # h = max(100, h)
            qw = m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
            qe = h * (x - 1) * (ts - tko_wet)
            qc = h * (ts - tko_wet)
            q_tot = qw + qc + qe
            # print('    ', ts, h, x, q_tot, qh, qh-q_tot)

            return abs(
                qh
                - (
                    m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
                    + h * x * (ts - tko_wet)
                )
            )

        ts = solve_minimize_f(calc_ts, [273.15, 323.15])
        tss.append(ts)
        h = q_dry_fig26_interpolator(sc) / (ts - tko)
        x = calc_x_equation_22(ts, tko, p)
        if m_dot <= 0:
            x = 1 + (x - 1) * 0.5

        hs.append(h)

        tos.append(tko)
        tos_wet.append(tko_wet)
        q_convs.append(hs[-1] * (ts - tko_wet))
        q_evaps.append(hs[-1] * (x - 1) * (ts - tko_wet))
        q_water_sensible.append(
            m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
        )
        qhs.append(qh)
    print(
        "sum m_dots",
        sum(m_dots) * 0.0025 * chord,
        sum(m_dots) * 0.0025 * chord * LBM_PER_KG / FT_PER_M * 3600,
    )
    return (
        svs,
        hs,
        tos,
        tos_wet,
        h_drys,
        urs,
        betas,
        hs_wet,
        q_convs,
        q_evaps,
        q_water_sensible,
        qhs,
        tss,
    )


def calc_figure_26(r=0.84):
    u = 167 / MPH_PER_M_S
    p = air_properties.calc_pressure(12000 * M_PER_FT)
    tk = tf_to_k(20)
    lwc = 0.5
    mvd = 25
    distribution = "Langmuir E"
    chord = 8 * M_PER_FT
    # h_chord = 0.12  # NACA0012 at 0 AOA
    # h_upper_chord = h_chord / 2  # upper surface only
    bi = get_beta_interpolator_for_condition(tk, u, mvd, chord, distribution)

    s23, h23, h23_recalc = calc_fig_23_hs()
    hint = interp1d(s23, h23)

    svs = plt.np.linspace(0, 0.18, int((0.18 - 0) * 100 * 4) + 1)  # 0.0025 s/c spacing
    hs = []
    tos = []
    tos_wet = []
    h_drys = []
    urs = []
    betas = []
    hs_wet = []
    q_convs = []
    q_evaps = []
    q_water_sensible = []
    qhs = []
    tss = []
    m_dots = []

    for sc in svs:
        u_ratio = u_ratio_interpolator(abs(sc))
        urs.append(u_ratio)
        tko_wet = calc_tko_equation_18(tk, u, p, u_ratio)
        beta = bi(sc)
        betas.append(beta)
        m_dot = beta * lwc / G_PER_KG * u
        m_dots.append(m_dot)
        qh = q_total_fig26_interpolator(sc)
        tko = tk + u ** 2 / 2 / air_properties.CP_AIR * (1 - u_ratio ** 2 * (1 - r))
        h = hint(sc)

        def calc_ts(ts):
            x = calc_x_equation_22(ts, tko, p)
            # if m_dot <= 0:
            if sc >= 0.108:
                x = 1 + (x - 1) * 0.5
            qw = m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
            qe = h * (x - 1) * (ts - tko_wet)
            qc = h * (ts - tko_wet)
            q_tot = qw + qc + qe

            return abs(
                qh
                - (
                    m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
                    + h * x * (ts - tko_wet)
                )
            )

        ts = solve_minimize_f(calc_ts, [223.15, 373.15])
        tss.append(ts)
        h = q_dry_fig26_interpolator(sc) / (ts - tko)
        x = calc_x_equation_22(ts, tko, p)
        if sc >= 0.108:
            x = 1 + (x - 1) * 0.5

        hs.append(h)

        tos.append(tko)
        tos_wet.append(tko_wet)
        q_convs.append(hs[-1] * (ts - tko_wet))
        q_evaps.append(hs[-1] * (x - 1) * (ts - tko_wet))
        q_water_sensible.append(
            m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
        )
        qhs.append(qh)

    print(
        "sum m_dots",
        sum(m_dots) * 0.0025 * chord,
        sum(m_dots) * 0.0025 * chord * LBM_PER_KG / FT_PER_M * 3600,
    )

    return (
        svs,
        hs,
        tos,
        tos_wet,
        h_drys,
        urs,
        betas,
        hs_wet,
        q_convs,
        q_evaps,
        q_water_sensible,
        qhs,
        tss,
    )


def calc_figure_26_h_fig25(
    r=0.84, h_interpolator=h_turb_fig25_interpolator, f_wet=None
):
    u = 167 / MPH_PER_M_S
    p = air_properties.calc_pressure(12000 * M_PER_FT)
    tk = tf_to_k(20)
    lwc = 0.5
    mvd = 25
    distribution = "Langmuir E"
    chord = 8 * M_PER_FT
    bi = get_beta_interpolator_for_condition(tk, u, mvd, chord, distribution)

    for mid in langmuir_cylinder_values.get_mids(distribution):
        print(mid * mvd, calc_k_airfoil(tk, u, mid * mvd, chord))

    svs = plt.np.linspace(0, 0.18, int((0.18 - 0) / 0.0025) + 1)  # 0.0025 s/c spacing
    hs = []
    tos = []
    tos_wet = []
    h_drys = []
    urs = []
    betas = []
    hs_wet = []
    q_convs = []
    q_evaps = []
    q_water_sensible = []
    qhs = []
    tss = []
    m_dots = []
    m_dot_evaps = []
    f_wet_to_use = 1

    for sc in svs:
        u_ratio = u_ratio_interpolator(abs(sc))
        urs.append(u_ratio)
        tko_wet = calc_tko_equation_18(tk, u, p, u_ratio)
        beta = bi(sc)
        betas.append(beta)
        m_dot = beta * lwc / G_PER_KG * u
        m_dots.append(m_dot)
        qh = q_total_fig26_interpolator(sc)
        tko = tk + u ** 2 / 2 / air_properties.CP_AIR * (1 - u_ratio ** 2 * (1 - r))
        h = h_interpolator(sc)

        def calc_ts(ts):
            x = calc_x_equation_22(ts, tko, p)
            if m_dot <= 0:
                x = 1 + (x - 1) * f_wet_to_use
            qw = m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
            qe = h * (x - 1) * (ts - tko_wet)
            qc = h * (ts - tko_wet)

            return abs(
                qh
                - (
                    m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
                    + h * x * (ts - tko_wet)
                )
            )

        ts = solve_minimize_f(calc_ts, [223.15, 333.15])
        tss.append(ts)
        tos.append(tko)
        tos_wet.append(tko_wet)
        x = calc_x_equation_22(ts, tko, p)
        if m_dot <= 0:
            x = 1 + (x - 1) * f_wet_to_use
        q_convs.append(h * (ts - tko_wet))
        q_evaps.append(h * (x - 1) * (ts - tko_wet))
        m_dot_evap = q_evaps[-1] / water_properties.L_EVAPORATION
        m_dot_evaps.append(m_dot_evap)
        if m_dot <= 0 and f_wet_to_use == 1:
            if f_wet is None:
                sum_water_catch = sum(m_dots) * 0.0025 * chord
                sum_evaps = sum(m_dot_evaps) * 0.0025 * chord
                f_wet_calc = f_wet_interpolator((sum_water_catch - sum_evaps))
                f_wet_to_use = f_wet_calc
                print(
                    "    ",
                    sc,
                    sum_water_catch,
                    sum_evaps,
                    (sum_water_catch - sum_evaps),
                    f_wet_calc,
                )
                print(
                    "    ",
                    sc,
                    sum_water_catch * LBM_PER_KG * S_PER_HOUR / FT_PER_M,
                    sum_evaps * LBM_PER_KG * S_PER_HOUR / FT_PER_M,
                    (sum_water_catch - sum_evaps) * LBM_PER_KG * S_PER_HOUR / FT_PER_M,
                    f_wet_calc,
                )
            else:
                f_wet_to_use = f_wet
        q_water_sensible.append(
            m_dot * water_properties.WATER_SPECIFIC_HEAT * (ts - tk)
        )

        h = q_dry_fig26_interpolator(sc) / (ts - tko)

        hs.append(h)

        qhs.append(qh)

    print(
        "sum m_dots",
        sum(m_dots) * 0.0025 * chord,
        sum(m_dots) * 0.0025 * chord * LBM_PER_KG / FT_PER_M * 3600,
    )

    return (
        svs,
        hs,
        tos,
        tos_wet,
        h_drys,
        urs,
        betas,
        hs_wet,
        q_convs,
        q_evaps,
        q_water_sensible,
        qhs,
        tss,
        m_dots,
        m_dot_evaps,
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sh, h_calc, tos, tos_wet, h_drys, urs, betas, hs_wet = calc_table_i_condition_1()

    s = plt.np.linspace(-0.12, 0.59, 1000)
    qs = [q_h_interp(_) for _ in s]

    plt.figure()
    plt.plot(sh, betas)
    plt.ylim(0)

    plt.figure()
    plt.plot(sh, urs)
    plt.ylim(0)

    plt.figure()
    plt.plot(s_c_tks, tks, "+")
    tks = [tk_surface_interp(_) for _ in s]
    plt.plot(s, tks)
    plt.plot(sh, tos, label="tko")
    plt.plot(sh, tos_wet, "--", label="tko_wet")

    plt.plot((sh[0], sh[-1]), (tf_to_k(24), tf_to_k(24)), "-", label="ambient")

    plt.xlabel("S/C")
    plt.ylabel("T, K")
    plt.legend()

    plt.figure()
    plt.plot(s_c_h, h, "+", ms=10, label="Figure 8a values")
    hs = [h_interp(_) for _ in s]
    # plt.plot(s, hs)

    sb, _ = trim_extra_x_y_zeros(sh, betas)
    sb_min = min(sb[1:])
    sb_max = max(sb[:-1])

    hx = [q_h_interp(_) / (tk_surface_interp(_) - 273.15) for _ in s]
    plt.plot(sh, h_calc, "-", label="Calculated")
    si, hi = zip(*[(s_, h_) for s_, h_ in zip(sh, h_calc) if sb_min <= s_ <= sb_max])
    plt.plot(si, hi, "--", fillstyle="none", c="b", label="Nodes with impingement")
    plt.plot(sh, hs_wet, ":", label="Calculated h_wet")
    plt.ylim(0)
    plt.xlabel("S/C")
    plt.ylabel("HC, W/m^2-K")
    plt.legend()

    plt.figure()
    plt.plot(
        s_c_h,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h],
        "+",
        ms=10,
        label="Figure 8a values",
    )
    plt.plot(sh, [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h_calc], "-", label="Calculated")
    sb, _ = trim_extra_x_y_zeros(sh, betas)
    sb_min = min(sb[1:])
    sb_max = max(sb[:-1])
    si, hi = zip(*[(s_, h_) for s_, h_ in zip(sh, h_calc) if sb_min <= s_ <= sb_max])
    plt.plot(
        si,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in hi],
        "--",
        fillstyle="none",
        c="b",
        label="Nodes with impingement",
    )
    plt.ylim(0)
    plt.xlabel("S/C")
    plt.ylabel("HC, BTU/ft^2-h-F")
    plt.legend()
    plt.savefig("naca_tn_1472_fig8a.png")

    (
        sh_8e,
        h_calc_8e,
        tos,
        tos_wet,
        h_drys,
        urs,
        betas,
        hs_wet,
        q_convs,
        q_evaps,
        q_water_sensible,
        qhs,
    ) = calc_table_i_condition_5()
    plt.figure()
    plt.plot(
        s_c_h_8e,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h_8e],
        "+",
        ms=10,
        label="Figure 8e values",
    )
    plt.plot(
        sh_8e, [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h_calc_8e], "-", label="Calculated"
    )
    sb, _ = trim_extra_x_y_zeros(sh_8e, betas)
    sb_min = min(sb[1:])
    sb_max = max(sb[:-1])
    si, hi = zip(
        *[(s_, h_) for s_, h_ in zip(sh_8e, h_calc_8e) if sb_min <= s_ <= sb_max]
    )
    plt.plot(
        si,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in hi],
        "--",
        fillstyle="none",
        c="b",
        label="Nodes with impingement",
    )
    sd, hd = zip(
        *[
            (s_, h_)
            for s_, h_ in zip(sh_8e, h_drys)
            if sb_min - 0.005 <= s_ <= sb_max + 0.005
        ]
    )
    plt.plot(sd, [_ * BTU_H_FT2_F_PER_W_M2_K for _ in hd], ":", label="Calculated Dry")
    plt.ylim(0)
    plt.xlabel("S/C")
    plt.ylabel("HC, BTU/ft^2-h-F")
    plt.legend()
    plt.savefig("naca_tn_1472_fig8e.png")

    plt.figure()
    plt.plot(
        sh_8e, [_ * BTU_H_PER_W / (FT_PER_M ** 2) for _ in qhs], label="q measured"
    )
    plt.plot(
        sh_8e,
        [_ * BTU_H_PER_W / (FT_PER_M ** 2) for _ in q_convs],
        label="q_dry_convection",
    )
    plt.plot(sh_8e, [_ * BTU_H_PER_W / (FT_PER_M ** 2) for _ in q_water_sensible])
    qwet = [sum(vs) for vs in zip(q_convs, q_evaps, q_water_sensible)]
    x, y, _, _ = get_x_y_split_at_x_value(sh_8e, qwet, 0.2)
    plt.plot(x, [_ * BTU_H_PER_W / (FT_PER_M ** 2) for _ in y], "--x", label="q_wet")
    plt.ylim(0, 2200)
    plt.legend()

    (
        svs_f26,
        hs_f26,
        tos_f26,
        tos_wet_f26,
        h_drys_f26,
        urs_f26,
        betas_f26,
        hs_wet_f26,
        q_convs_f26,
        q_evaps_f26,
        q_water_sensible_f26,
        qhs_f26,
        tss_f26,
        m_dots_f26,
        m_dot_evaps_f26,
    ) = calc_figure_26_h_fig25(0.89)

    QE = sum(q_evaps_f26) * 0.0025 * 8 / FT_PER_M
    print(
        "QE",
        QE,
        QE * BTU_H_PER_W / FT_PER_M,
        QE / water_properties.L_EVAPORATION * LBM_PER_KG / FT_PER_M * 3600,
    )

    (
        svs_f26_h25_measured,
        hs_f26_h25_measured,
        tos_f26_h25_measured,
        tos_wet_f26_h25_measured,
        h_drys_f26_h25_measured,
        urs_f26_h25_measured,
        betas_f26_h25_measured,
        hs_wet_f26_h25_measured,
        q_convs_f26_h25_measured,
        q_evaps_f26_h25_measured,
        q_water_sensible_f26_h25_measured,
        qhs_f26_h25_measured,
        tss_f26_h25_measured,
        m_dots_f26_h25_measured,
        m_dot_evaps_f26_h25_measured,
    ) = calc_figure_26_h_fig25(0.84, h_measured_fig25_interpolator)

    QE = sum(q_evaps_f26_h25_measured) * 0.0025 * 8 / FT_PER_M
    print(
        "QE",
        QE,
        QE * BTU_H_PER_W / FT_PER_M,
        QE / water_properties.L_EVAPORATION * LBM_PER_KG / FT_PER_M * 3600,
    )

    plt.figure()

    (line,) = plt.plot(
        s_c_h, [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h], ":+", label="Figure 8a icing"
    )
    # plt.plot(
    #     sh,
    #     [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h_calc],
    #     "-",
    #     c=line.get_color(),
    #     label="Calculated h 8a",
    # )
    (line,) = plt.plot(
        s_c_h_8e,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h_8e],
        ":x",
        label="Figure 8e icing",
    )
    # plt.plot(
    #     sh_8e,
    #     [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h_calc_8e],
    #     "-",
    #     c=line.get_color(),
    #     label="Calculated h 8e",
    # )
    s23, h23, h23_recalc = calc_fig_23_hs()
    plt.plot(
        s23,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h23],
        "--",
        c="k",
        label="Figure 23 dry",
    )
    plt.plot(
        s23,
        [_ * BTU_H_FT2_F_PER_W_M2_K for _ in h23_recalc],
        "-.",
        c="k",
        label="Figure 23 dry recalculated",
    )

    # plt.plot(svs_f26, calc_h_btu(hs_f26), label="Figure 26")
    plt.plot(
        s_c_h_fig25, calc_h_btu(h_measured_fig25), label="Figure 25 measured dry air"
    )
    plt.plot(s_c_h_fig25, calc_h_btu(h_turb_fig25), label="Figure 25 dry air turbulent")

    print(svs_f26[1] - svs_f26[0])

    plt.ylim(0)
    plt.xlabel("S/C")
    plt.ylabel("Heat transfer coefficient, BTU/ft^2-h-F")
    plt.legend()
    plt.savefig("naca_tn_1472_hc_comparison.png")

    plt.figure()
    plt.plot(
        svs_f26_h25_measured,
        [tk_to_f(_) for _ in tss_f26_h25_measured],
        label="With Figure 25 measured dry HC",
    )
    plt.plot(
        svs_f26,
        [tk_to_f(_) for _ in tss_f26],
        "--",
        label="With Figure 25 estimated HC",
    )
    plt.xlim(0)
    plt.ylim(0)
    plt.xlabel("S/C")
    plt.ylabel("t_surface, F")
    plt.legend()
    plt.savefig("naca_tn_1472_fig26_t_surface.png")

    plt.figure()
    sand_pile_q_evap = [sum(vs) for vs in zip(q_convs_f26, q_evaps_f26)]
    sand_pile_q_total = [
        sum(vs) for vs in zip(q_convs_f26, q_evaps_f26, q_water_sensible_f26)
    ]
    plt.plot(
        svs_f26,
        calc_q_btu(sand_pile_q_total),
        label="q_total = q_conv + q_evap + q_water_sensible",
    )
    plt.plot(svs_f26, calc_q_btu(sand_pile_q_evap), "--", label="q_conv + q_evap")
    plt.plot(svs_f26, calc_q_btu(q_convs_f26), "-.", label="q_conv")
    plt.ylim(0, 4000)
    plt.yticks(range(0, 4000 + 400, 400))
    plt.xlim(0, 0.24)
    plt.xticks(plt.np.arange(0, 0.24 + 0.02, 0.02))
    plt.xlabel("S/C")
    plt.ylabel("Heat transfer coefficient, BTU/ft^2-h-F")
    plt.grid()
    plt.legend()
    plt.savefig("naca_tn_1472_fig26.png")

    plt.figure()
    plt.suptitle("With Figure 25 measured dry HC")
    sand_pile_q_evap = [
        sum(vs) for vs in zip(q_convs_f26_h25_measured, q_evaps_f26_h25_measured)
    ]
    sand_pile_q_total = [
        sum(vs)
        for vs in zip(
            q_convs_f26_h25_measured,
            q_evaps_f26_h25_measured,
            q_water_sensible_f26_h25_measured,
        )
    ]
    plt.plot(
        svs_f26,
        calc_q_btu(sand_pile_q_total),
        label="q_total = q_conv + q_evap + q_water_sensible",
    )
    plt.plot(svs_f26, calc_q_btu(sand_pile_q_evap), "--", label="q_conv + q_evap")
    plt.plot(svs_f26, calc_q_btu(q_convs_f26_h25_measured), "-.", label="q_conv")
    plt.ylim(0, 4000)
    plt.yticks(range(0, 4000 + 400, 400))
    plt.xlim(0, 0.24)
    plt.xticks(plt.np.arange(0, 0.24 + 0.02, 0.02))
    plt.xlabel("S/C")
    plt.ylabel("Heat transfer coefficient, BTU/ft^2-h-F")
    plt.grid()
    plt.legend()

    plt.figure()
    x, y = trim_extra_x_y_zeros(svs_f26, betas_f26)
    plt.plot(*trim_extra_x_y_zeros(svs_f26, betas_f26))
    plt.xlim(0)
    plt.ylim(0, 1)
    plt.xlabel("S/C")
    plt.ylabel("Beta")

    (
        svs_f26_fwet_3,
        hs_f26_fwet_3,
        tos_f26_fwet_3,
        tos_wet_f26_fwet_3,
        h_drys_f26_fwet_3,
        urs_f26_fwet_3,
        betas_f26_fwet_3,
        hs_wet_f26_fwet_3,
        q_convs_f26_fwet_3,
        q_evaps_f26_fwet_3,
        q_water_sensible_f26_fwet_3,
        qhs_f26_fwet_3,
        tss_f26_fwet_3,
        m_dots_f26v,
        m_dot_evaps_f26_fwet_3,
    ) = calc_figure_26_h_fig25(0.89, f_wet=0.3)

    QE = sum(q_evaps_f26_fwet_3) * 0.0025 * 8 / FT_PER_M
    print(
        "QE",
        QE,
        QE * BTU_H_PER_W / FT_PER_M,
        QE / water_properties.L_EVAPORATION * LBM_PER_KG / FT_PER_M * 3600,
    )

    plt.show()
