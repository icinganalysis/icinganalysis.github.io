from scipy.interpolate import interp1d
from icinganalysis.water_properties import (
    RATIO_MOLECULAR_WEIGHTS,
    L_EVAPORATION,
    L_FREEZING,
    WATER_SPECIFIC_HEAT,
)
from icinganalysis.air_properties import CP_AIR, calc_pressure
from icinganalysis.units_helpers import (
    FT_PER_M,
    KNOTS_PER_MS,
    tf_to_k,
    tk_to_f,
    PSI_PER_PA,
    BTU_H_FT2_F_PER_W_M2_K,
    FT2_PER_M2,
    S_PER_HOUR,
    BTU_H_PER_W,
    LBM_PER_KG,
    MPH_PER_M_S,
)
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis.markdown_table_helper import make_nice_width_markdown_table
from icinganalysis.langmuir_blodgett_table_ii import calc_beta_o
from icinganalysis.langmuir_cylinder_values import calc_k, calc_phi, calc_re

CAL_PER_JOULE = 0.23900573614
G_PER_KG = 1000
CM_PER_M = 100


def calc_htc_rough(tk, p, u, d_cyl):
    k = (tk * 1.8 + 81) * 1e-7 / CAL_PER_JOULE * CM_PER_M
    re = calc_re(tk, p, u, d_cyl)
    nu = 0.082 * re ** 0.747  # NACA-TR-1215 (F12)
    hc = nu * k /d_cyl
    return hc


def calc_htc_lam(tk, p, u, d):
    k = (tk * 1.8 + 81) * 1e-7 / CAL_PER_JOULE * CM_PER_M
    reynolds = calc_re(tk, p, u, d)
    nu = 0.24 * reynolds ** 0.6
    return nu * k / d


def calc_htc_turb(tk, p, u, d):
    k = (tk * 1.8 + 81) * 1e-7 / CAL_PER_JOULE * CM_PER_M
    reynolds = calc_re(tk, p, u, d)
    nu = 0.024 * reynolds ** 0.805
    return nu * k / d


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


def calc_qc(tk, hc, t_surface=273.15):
    return hc * (t_surface - tk)


def calc_qc_messinger_units(tk, hc):
    hc_ = hc * BTU_H_FT2_F_PER_W_M2_K
    tf = tk_to_f(tk)
    qc = hc_ * (32 - tf)
    qc = qc / BTU_H_PER_W * FT2_PER_M2
    return qc


def calc_qv(u, hc, r=0.875):
    return hc * r * u ** 2 / 2 / CP_AIR


def calc_qv_messinger_units(u, hc, r=0.875):
    hc_ = hc * BTU_H_FT2_F_PER_W_M2_K
    v = u * FT_PER_M
    qv = hc_ * r * v ** 2 / 2 / 32.2 / 778 / 0.24
    qv = qv / BTU_H_PER_W * FT2_PER_M2
    return qv


def calc_qw(tk, wcr, t_surface=273.15):
    return wcr * WATER_SPECIFIC_HEAT * (t_surface - tk)


def calc_qw_messinger_units(tk, wcr):
    tf = tk_to_f(tk)
    rc = wcr * LBM_PER_KG * S_PER_HOUR / FT2_PER_M2
    cw = 1  # BTU/lbm-F
    qw = rc * cw * (32 - tf)
    qw = qw / BTU_H_PER_W * FT2_PER_M2

    return qw


def calc_qk(u, wcr):
    return wcr * u ** 2 / 2


def calc_qk_messinger_units(u, wcr):
    v = u * FT_PER_M
    rc = wcr * LBM_PER_KG * S_PER_HOUR / FT2_PER_M2
    qk = rc * v ** 2 / 2 / 32.2 / 778
    qk = qk / BTU_H_PER_W * FT2_PER_M2

    return qk


def calc_qe(tk, p, hc, t_surface=273.15):
    pvs = calc_vapor_p(t_surface)
    pv = calc_vapor_p(tk)
    n_s = RATIO_MOLECULAR_WEIGHTS * pvs / p
    n_o = RATIO_MOLECULAR_WEIGHTS * pv / p
    m_evap = 1.12 * hc / CP_AIR * (n_s - n_o)
    q_evap = m_evap * L_EVAPORATION
    return q_evap


def calc_qe_messinger_units(tk, p, hc):
    t_surface = 273.15
    psia = p * PSI_PER_PA
    hc_btu = hc * BTU_H_FT2_F_PER_W_M2_K
    pvs_psia = calc_vapor_p(t_surface) * PSI_PER_PA
    pv_psia = calc_vapor_p(tk) * PSI_PER_PA
    L_EVAP = 1075  # BTU/lbm
    m_evap = hc_btu * 2.9 * (pvs_psia - pv_psia) / psia
    q_evap = L_EVAP * m_evap
    q_evap = q_evap / BTU_H_PER_W * FT2_PER_M2
    return q_evap


def calc_qf(wcr, n):
    return wcr * n * L_FREEZING


def calc_n_unlimited(tk, p, u, hc, wcr, r=0.875):
    qc = calc_qc(tk, hc)
    qe = calc_qe(tk, p, hc)
    qv = calc_qv(u, hc, r)
    qk = calc_qk(u, wcr)
    qw = calc_qw(tk, wcr)
    q_partial_sum = qc + qe + qw - qk - qv
    n = q_partial_sum / (wcr * L_FREEZING)

    return n


def calc_heat_terms_unlimited(tk, p, u, hc, wcr, r=0.875):
    qc = calc_qc(tk, hc)
    qe = calc_qe(tk, p, hc)
    qv = calc_qv(u, hc, r)
    qk = calc_qk(u, wcr)
    qw = calc_qw(tk, wcr)
    q_partial_sum = qc + qe + qw - qk - qv
    n = q_partial_sum / (wcr * L_FREEZING)
    qfreeze = n*wcr * L_FREEZING

    return qc, qe, qv, qk, qw, qfreeze, n


def calc_ts_n(tk, p, u, hc, wcr, r=0.875, t_surface=273.15):
    n = calc_n_unlimited(tk, p, u, hc, wcr, r)
    if 0 <= n <= 1:
        ts = 273.15
        return ts, float(n)
    n = max(0, min(1, n))

    def q_diff(ts):
        qc = calc_qc(tk, hc, ts)
        qe = calc_qe(tk, p, hc, ts)
        qv = calc_qv(u, hc, r)
        qk = calc_qk(u, wcr)
        qw = calc_qw(tk, wcr, ts)
        qf = n * wcr * L_FREEZING
        return abs(qc + qe + qw - qk - qv - qf)

    ts = solve_minimize_f(q_diff, [243.15, 373.15])

    return float(ts), float(n)


def find_lwc_critical_lam(tk, p, u, beta, d_cyl, r=0.875):
    hc = calc_htc_lam(tk, p, u, d_cyl)
    return find_lwc_critical_n1(tk, p, u, hc, beta, r)


def find_lwc_critical_turb(tk, p, u, beta, d_cyl, r=0.875):
    hc = calc_htc_turb(tk, p, u, d_cyl)
    return find_lwc_critical_n1(tk, p, u, hc, beta, r)


def find_lwc_critical_rough(tk, p, u, beta, d_cyl, r=0.875):
    hc = calc_htc_rough(tk, p, u, d_cyl)
    return find_lwc_critical_n1(tk, p, u, hc, beta, r)


def find_lwc_critical_n1(tk, p, u, hc, beta, r=0.875):
    ts = 273.15
    qc = calc_qc(tk, hc, ts)
    qe = calc_qe(tk, p, hc, ts)
    qv = calc_qv(u, hc, r)
    n = 1

    def q_diff(lwc):
        wcr = lwc / G_PER_KG * beta * u
        qk = calc_qk(u, wcr)
        qw = calc_qw(tk, wcr, ts)
        qf = n * wcr * L_FREEZING
        return abs(qc + qe + qw - qk - qv - qf)

    lwc = solve_minimize_f(q_diff, [0, 20])
    return lwc


def calc_n_messinger_units(tk, p, u, hc, wcr, r=0.875):
    qc = calc_qc_messinger_units(tk, hc)
    qe = calc_qe_messinger_units(tk, p, hc)
    qv = calc_qv_messinger_units(u, hc, r)
    qk = calc_qk_messinger_units(u, wcr)
    qw = calc_qw_messinger_units(tk, wcr)
    q_partial_sum = qc + qe + qw - qk - qv
    n = q_partial_sum / (wcr * L_FREEZING)

    return n


def calc_theta_1(p, b):
    t_surface = 273.15
    pvs = calc_vapor_p(t_surface)
    return (
        t_surface * (1 + b / WATER_SPECIFIC_HEAT)
        + L_EVAPORATION * 0.7 / CP_AIR * pvs / p
    )


def calc_theta2(tk, p, b, n):
    pv = calc_vapor_p(tk)
    return (
        tk * (1 + b / WATER_SPECIFIC_HEAT)
        + L_EVAPORATION * 0.7 / CP_AIR * pv / p
        + L_FREEZING * n * b / WATER_SPECIFIC_HEAT
    )


def calc_theta_3(u, b, r=0.875):
    return (r / CP_AIR + b / WATER_SPECIFIC_HEAT) * (u ** 2 / 2)


def calc_n_with_b(tk, p, u, b, r=0.875):
    hc = 1  # arbitrary, just need for ratio b = wcr * cpw / hc
    wcr = hc * b / WATER_SPECIFIC_HEAT
    return calc_n_unlimited(tk, p, u, hc, wcr, r)


def calc_n_with_b_messinger_units(tk, p, u, b, r=0.875):
    hc = 1  # arbitrary, just need for ratio b = wcr * cpw / hc
    wcr = hc * b / WATER_SPECIFIC_HEAT
    return calc_n_messinger_units(tk, p, u, hc, wcr, r)


# fmt: off
d_fig10b_bs = (
    0, 0,
    100, 0.39,
    200, 0.68,
    300, 0.94,
    400, 1.14,
    500, 1.26,
    600, 1.35,
    700, 1.4,
    800, 1.43,
    900, 1.42,
    1000, 1.37,
)
# fmt: on
_ks = d_fig10b_bs[::2]
_bs = d_fig10b_bs[1::2]
cyl_knots_bs_interpolator = interp1d(_ks, _bs)

# fmt: off
d_table_i = (  # run, type, mph, lwc, mvd, twet, ttotal, beta, b, n_calc, t_calc, t_measured
    '1', 'A', 244, 0.64, 6.8, 6.8, 14.5, .18, .275, 1, 31.1, 31,
    '2-A', 'A', 252, .7, 9.7, 4.6, 13.2, .31, .527, .65, 32, 34,
    '2-B', 'A', 252, 2, 7.6, 4.6, 13.2, .22, 1.065, .402, 32, 31,
    '2-C', 'A', 252, .26, 10.5, 4.6, 13.2, .335, .211, 1, 26.3, 27,
    '3', 'A', 235, 1.1, 8.5, 10.1, 16.8, .25, .645, .46, 32, 33,
    '4', 'A', 226, .32, 12, 0.9, 8.3, .375, .276, 1, 25.8, 25,
    '5', 'A', 227, .27, 20.7, 4.1, 11, .59, .367, .9, 32, 30,
    '6-A', 'N', 221, .27, 9.8, 5.4, 11.7, .29, .178, 1, 23.4, 22,
    '6-B', 'N', 207, .27, 10, 6.2, 11.5, .29, .17, 1, 23.3, 21,
    '7', 'A', 220, .5, 18.2, 6.7, 13.3, .53, .603, .535, 32, 32,
    '8', 'A', 210, .81, 17.1, 17.9, 22.7, .5, .9, .237, 32, 33,
    '9', 'N', 238, .7, 16.4, 12.8, 19, .495, .796, .35, 32, 33,
    '10', 'N', 234, .16, 13.8, 2.5, 10, .44, .165, 1, 20.4, 20,
    '11', 'N', 228, .43, 13.2, 20.8, 26.5, .41, .407, .282, 32, 31,
    '12-A', 'N', 243, .17, 8.9, 0.8, 9.0, .27, .107, 1, 16, 16,
    '12-B', 'N', 243, .145, 10, -0.2, 7.7, .32, .111, 1, 16.2, 18,
    '13', 'A', 238, .34, 13, 7.7, 14.7, .415, .334, .83, 32, 31,
    '14', 'N', 232, .34, 16, 15.7, 22, .49, .388, .475, 32, 32,
)
# fmt: on
runs = d_table_i[::12]
types = d_table_i[1::12]
mphs = d_table_i[2::12]
lwcs = d_table_i[3::12]
mvds = d_table_i[4::12]
twets = d_table_i[5::12]
ttotals = d_table_i[6::12]
wcrs_calcs = d_table_i[7::12]
bs_calcs = d_table_i[8::12]
ns_calcs = d_table_i[9::12]
ts_calcs = d_table_i[10::12]
ts_measureds = d_table_i[11::12]

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    b = 0.2
    p = calc_pressure(20000 / FT_PER_M)
    u = 450 / KNOTS_PER_MS
    tk = tf_to_k(0)
    print(tk, p, u)

    print("n_calc=", calc_n_with_b(tk, p, u, b))

    knots = plt.np.linspace(1, 1000, 1000)
    us = [_ / KNOTS_PER_MS for _ in knots]
    ns = [calc_n_with_b(tk, p, _, b) for _ in us]

    print()
    print()
    print()
    hc = 1  # arbitrary, just need for ratio b = wcr * cpw / hc
    wcr = hc * b / WATER_SPECIFIC_HEAT
    print(calc_qk(u, wcr))
    print(calc_qk_messinger_units(u, wcr))
    print(calc_qc(tk, hc))
    print(calc_qc_messinger_units(tk, hc))
    print(calc_qv(u, hc))
    print(calc_qv_messinger_units(u, hc))
    print(calc_qw(tk, wcr))
    print(calc_qw_messinger_units(tk, wcr))
    print()
    print()
    print()

    print(min(us), max(us))
    print(min(knots), max(knots))

    plt.figure()
    plt.plot(knots, ns)
    ns = [calc_n_with_b_messinger_units(tk, p, _, b) for _ in us]
    plt.plot(knots, ns, "--")

    ts, ns = zip(*[calc_ts_n(tk, p, _, hc, wcr) for _ in us])
    plt.plot(knots, ns, ":")

    plt.figure()
    plt.suptitle("Figure 10a conditions, b=0.2")
    ks, tsfn = zip(*[(k, tk_to_f(_)) for k, _, n in zip(knots, ts, ns) if 0 < n < 1])
    plt.plot(ks, tsfn, label="0 <= n <= 1")
    tsf = [tk_to_f(_) for _ in ts]
    plt.plot(knots, tsf, "--", label="Calculated surface temperature")

    plt.xlabel("Free Stream Airspeed, Knots")
    plt.xlim(0, 1000)
    plt.ylabel("Surface Temperature, F")
    plt.ylim(0, 80)
    plt.legend()
    plt.tight_layout()
    plt.savefig("messinger_figure10a_calc.png")

    ts_v0 = 14.1
    v_n0 = 439
    v_n1 = 570
    ts_v1000 = 66

    ts_v0_calc = 15.3
    v_n0_calc = 431
    v_n1_calc = 561
    ts_v1000_calc = 66.6

    print()
    print("Figure 10a conditions, b=0.2")
    text = make_nice_width_markdown_table(
        ["Source", "Ts@V=0, F", "V@n=0, knots", "V@n=1, knots", "Ts@V=1000, F"],
        [
            ["Messinger Figure 10a", ts_v0, v_n0, v_n1, ts_v1000],
            ["Calculated", ts_v0_calc, v_n0_calc, v_n1_calc, ts_v1000_calc],
        ],
    )
    print()
    print(text)

    plt.figure()
    plt.suptitle("Figure 10a conditions, b=0.5")
    b = 0.5

    ts_v0 = 28.2
    v_n0 = 185
    v_n1 = 587
    ts_v1000 = 66

    ts_v0_calc = 30
    v_n0_calc = 179
    v_n1_calc = 576
    ts_v1000_calc = 66.1

    hc = 1  # arbitrary, just need for ratio b = wcr * cpw / hc
    wcr = hc * b / WATER_SPECIFIC_HEAT
    knots = plt.np.linspace(1, 1000, 1000)
    us = [_ / KNOTS_PER_MS for _ in knots]

    lwc = 0.5
    mvd = 15
    d_cyl = 3 * 0.0254

    betas = [
        calc_beta_o(calc_k(tk, _, mvd, d_cyl), calc_phi(tk, p, _, d_cyl)) for _ in us
    ]
    wcrs = [
        lwc
        / 1000
        * _
        * calc_beta_o(calc_k(tk, _, mvd, d_cyl), calc_phi(tk, p, _, d_cyl))
        for _ in us
    ]

    reynolds = [calc_re(tk, p, _, d_cyl) for _ in us]

    ts, ns = zip(*[calc_ts_n(tk, p, _, hc, wcr) for _ in us])
    tfs = [tk_to_f(_) for _ in ts]
    ks, tsfn = zip(*[(k, tk_to_f(_)) for k, _, n in zip(knots, ts, ns) if 0 < n < 1])
    plt.plot(ks, tsfn, label="0 <= n <= 1")
    plt.plot(knots, tfs, "--", label="Calculated surface temperature")

    plt.xlabel("Free Stream Airspeed, Knots")
    plt.xlim(0, 1000)
    plt.ylabel("Surface Temperature, F")
    plt.ylim(0, 80)
    plt.legend()
    plt.tight_layout()
    plt.savefig("messinger_figure10a_calc_b0_5.png")

    print()
    print("Figure 10a conditions, b=0.5")
    text = make_nice_width_markdown_table(
        ["Source", "Ts@V=0, F", "V@n=0, knots", "V@n=1, knots", "Ts@V=1000, F"],
        [
            ["Messinger Figure 10a", ts_v0, v_n0, v_n1, ts_v1000],
            ["Calculated", ts_v0_calc, v_n0_calc, v_n1_calc, ts_v1000_calc],
        ],
    )
    print()
    print(text)

    plt.figure()
    rcs = [_ * LBM_PER_KG * S_PER_HOUR / FT2_PER_M2 for _ in wcrs]
    bs = [cyl_knots_bs_interpolator(_) for _ in knots]
    fcs = [(1 * r_) / b_ for b_, r_ in zip(bs, rcs)]
    plt.plot(knots, fcs)
    plt.plot(knots, bs, "--")

    plt.figure()
    plt.suptitle("Figure 10b, 3 inch diameter cylinder")
    plt.plot(knots, betas, label="MVD 15, Langmuir A")
    plt.ylim(0, 1)
    plt.xlabel("Free Stream Airspeed, Knots")
    plt.xlim(0, 1000)
    plt.ylabel("Beta")
    plt.legend()
    plt.savefig("messinger_fig10b_beta.png")

    plt.figure()
    hcs = [calc_htc_lam(tk, p, _, d_cyl) for _ in us]
    hcs_turb = [calc_htc_turb(tk, p, _, d_cyl) for _ in us]
    hcs_btu = [_ * BTU_H_FT2_F_PER_W_M2_K for _ in hcs]
    hcs_turb_btu = [_ * BTU_H_FT2_F_PER_W_M2_K for _ in hcs_turb]
    plt.plot(reynolds, fcs, label="Calculated from Figure 10b values, beta cylinder")
    plt.plot(reynolds, hcs_btu, "--", label="nu = 0.24 * reynolds ** 0.6")
    plt.plot(reynolds, hcs_turb_btu, ":", label="nu = 0.024 * reynolds ** 0.805")
    plt.xscale("log")
    plt.xlabel("Reynolds Number (based on cylinder diameter)")
    plt.yscale("log")
    plt.ylabel("Heat transfer coefficient, BTU/h-ft^2-F")
    plt.legend()
    plt.savefig("messinger_fig10b_hcs.png")

    plt.figure()
    plt.suptitle("Figure 10b, 3 inch diameter cylinder")
    bs2 = [rc * 1 / fc for rc, fc in zip(rcs, hcs_btu)]
    bs2_turb = [rc * 1 / fc for rc, fc in zip(rcs, hcs_turb_btu)]
    plt.plot(knots, bs, label="Figure 10b values")
    plt.plot(knots, bs2, "--", label="nu = 0.24 * reynolds ** 0.6")
    plt.plot(knots, bs2_turb, ":", label="nu = 0.024 * reynolds ** 0.805")
    plt.xlabel("Free Stream Airspeed, Knots")
    plt.xlim(0, 1000)
    plt.ylabel("b = wcr * cpw / hc")
    plt.ylim(0,)
    plt.legend()
    plt.savefig("messinger_fig10b_bs.png")

    ts2, ns2 = zip(
        *[calc_ts_n(tk, p, _, hc_, wcr_) for _, hc_, wcr_ in zip(us, hcs, wcrs)]
    )
    tfs2 = [tk_to_f(_) for _ in ts2]
    ts2_turb, ns2_turb = zip(
        *[calc_ts_n(tk, p, _, hc_, wcr_) for _, hc_, wcr_ in zip(us, hcs_turb, wcrs)]
    )
    tfs2_turb = [tk_to_f(_) for _ in ts2_turb]

    plt.figure()
    plt.suptitle("Figure 10b, Stagnation point of a 3 inch diameter cylinder")
    plt.plot(knots, tfs, "--", label="b = 0.5")
    plt.plot(knots, tfs2, "-", label="nu = 0.24 * reynolds ** 0.6")
    plt.plot(knots, tfs2_turb, ":", label="nu = 0.024 * reynolds ** 0.805")
    plt.xlabel("Free Stream Airspeed, Knots")
    plt.xlim(0, 1000)
    plt.ylabel("Surface Temperature, F")
    plt.ylim(0, 80)
    plt.legend()
    plt.savefig("messinger_fig10b_ts.png")

    d_cyl = 3.75 * 0.0254
    altitude = 8200 / FT_PER_M
    p = calc_pressure(altitude)
    rows = []
    d_rows = []
    for (run, type, mph, lwc, mvd, twet, ttotal, beta, b, n, ts, ts_measured) in zip(
        *(iter(d_table_i),) * 12
    ):
        u = mph / MPH_PER_M_S
        u2 = 93 / MPH_PER_M_S
        tk_total = tf_to_k(ttotal)
        tk = tk_total - u ** 2 / 2 / CP_AIR
        tk_wet = tf_to_k(twet)
        tf = tk_to_f(tk)
        reynolds = calc_re(tk, p, u, d_cyl)
        print("reynolds", reynolds)
        beta_calc = calc_beta_o(calc_k(tk, u, mvd, d_cyl), calc_phi(tk, p, u, d_cyl))
        hc = calc_htc_lam(tk, p, u, d_cyl)
        wcr = beta_calc * lwc / G_PER_KG * u
        b_calc = wcr * WATER_SPECIFIC_HEAT / hc
        ts_calc, n_calc = calc_ts_n(tk, p, u, hc, wcr)
        ts_calc_wet, n_calc_wet = calc_ts_n(tk_wet, p, u, hc, wcr)
        hc_turb = calc_htc_turb(tk, p, u, d_cyl)
        ts_calc_turb, n_calc_turb = calc_ts_n(tk, p, u, hc_turb, wcr)
        ts_calc_turb_wet, n_calc_turb_wet = calc_ts_n(tk_wet, p, u, hc_turb, wcr)
        print(
            mvd,
            beta,
            beta_calc,
            b,
            b_calc,
            ts_measured,
            ts,
            tk_to_f(ts_calc),
            n,
            n_calc,
            tf,
            twet,
        )
        rows.append(
            (
                run,
                mph,
                lwc,
                mvd,
                f"{tf:.1f}",
                n,
                f"{n_calc:.2f}",
                ts_measured,
                f"{tk_to_f(ts_calc):.1f}",
            )
        )
        d_rows.append(
            (
                run,
                ttotal,
                lwc,
                n,
                n_calc,
                ts_measured,
                tk_to_f(ts_calc),
                tf,
                twet,
                n_calc_wet,
                tk_to_f(ts_calc_wet),
                n_calc_turb,
                tk_to_f(ts_calc_turb),
                n_calc_turb_wet,
                tk_to_f(ts_calc_turb_wet),
                ts,
                hc,
                hc_turb,
            )
        )

    print()
    print("Table 1")
    text = make_nice_width_markdown_table(
        [
            "Run",
            "Airspeed, mph",
            "LWC",
            "MVD",
            "T_static, F",
            "Messinger calculated n",
            "Python calculated n",
            "Measured T_surface, F",
            "Calculated T_surface, F",
        ],
        rows,
    )
    print(text)
    print()

    plt.figure()
    for (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) in d_rows:
        (line,) = plt.plot(ttotal, n, "+", ms=14)
        plt.plot(ttotal, n_calc, "o", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(ttotal, n_calc2, "s", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot((ttotal, ttotal), (n_calc, n_calc2), ":", c=line.get_color())
        plt.text(ttotal, n + 0.005, run)
    plt.plot([], [], "+", c="k", ms=14, label="Calculated (Messinger) (run ID noted)")
    plt.plot(
        [],
        [],
        "o",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) (using T_static)",
    )
    plt.plot(
        [],
        [],
        "s",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) (using T_wet)",
    )
    plt.xlabel("Ttotal, F")
    plt.xlim(5, 30)
    plt.ylabel("Stagnation line freezing fraction, n")
    plt.ylim((0, 1.2))
    plt.legend()
    plt.savefig("messinger_table1_n.png")

    plt.figure()
    for (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) in d_rows:
        (line,) = plt.plot(ttotal, n, "+", ms=14)
        plt.plot(ttotal, n_calc_turb, "o", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(
            ttotal, n_calc_turb_wet, "s", fillstyle="none", c=line.get_color(), ms=12
        )
        plt.plot(
            (ttotal, ttotal), (n_calc_turb_wet, n_calc_turb), ":", c=line.get_color()
        )
        plt.text(ttotal, n + 0.005, run)
    plt.plot([], [], "+", c="k", ms=14, label="Calculated (Messinger) (run ID noted)")
    plt.plot(
        [],
        [],
        "o",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) Turbulent (using T_static)",
    )
    plt.plot(
        [],
        [],
        "s",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) Turbulent (using T_wet)",
    )
    plt.xlabel("Ttotal, F")
    plt.xlim(5, 30)
    plt.ylabel("Stagnation line freezing fraction, n")
    plt.ylim((0, 1.2))
    plt.legend()
    plt.savefig("messinger_table1_n_turb.png")

    plt.figure()
    for (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) in d_rows:
        (line,) = plt.plot(ttotal, tsm, "+", ms=14)
        plt.plot(ttotal, ts, "^", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(ttotal, ts_calc, "o", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(ttotal, ts_calc2, "s", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot((ttotal, ttotal), (ts_calc, ts_calc2), ":", c=line.get_color())
        plt.text(ttotal, tsm + 0.05, run)
    plt.plot([], [], "+", c="k", ms=14, label="Measured (run ID noted)")
    plt.plot(
        [], [], "^", fillstyle="none", c="k", ms=12, label="Calculated (Messinger)"
    )
    plt.plot(
        [],
        [],
        "o",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) (using T_static)",
    )
    plt.plot(
        [],
        [],
        "s",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) (using T_wet)",
    )
    plt.xlabel("Ttotal, F")
    plt.xlim(5, 30)
    plt.ylabel("Tsurface, F")
    plt.ylim(10, 40)
    plt.legend()
    plt.savefig("messinger_table1_ts.png")

    plt.figure()
    for (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) in d_rows:
        (line,) = plt.plot(ttotal, tsm, "+", ms=14)
        plt.plot(
            ttotal, ts_calc_turb_wet, "o", fillstyle="none", c=line.get_color(), ms=12
        )
        plt.plot(ttotal, ts_calc_turb, "s", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(
            (ttotal, ttotal), (ts_calc_turb_wet, ts_calc_turb), ":", c=line.get_color()
        )
        plt.text(ttotal, tsm + 0.05, run)
    plt.plot([], [], "+", c="k", ms=14, label="Measured (run ID noted)")
    plt.plot(
        [],
        [],
        "o",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) Turbulent (using T_static)",
    )
    plt.plot(
        [],
        [],
        "s",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) Turbulent (using T_wet)",
    )
    plt.xlabel("Ttotal, F")
    plt.xlim(5, 30)
    plt.ylabel("Tsurface, F")
    plt.ylim(10, 40)
    plt.legend()
    plt.savefig("messinger_table1_ts_turbulent.png")

    plt.figure()
    for (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) in d_rows:
        (line,) = plt.plot(ttotal, twet, "+", ms=12)
        plt.plot(ttotal, tf, "o", fillstyle="none", c=line.get_color(), ms=12)
        plt.text(ttotal, twet + 0.05, run)
        plt.plot((ttotal, ttotal), (twet, tf), ":", c=line.get_color())
    plt.plot([], [], "+", c="k", ms=12, label="Twet (run ID noted)")
    plt.plot([], [], "o", fillstyle="none", c="k", ms=12, label="Tstatic")
    plt.xlabel("Ttotal, F")
    plt.xlim(5, 30)
    plt.ylabel("T, F")
    plt.ylim(-5, 25)
    plt.legend()
    plt.savefig("messinger_table1_twet.png")

    plt.figure()
    (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) = zip(*d_rows)
    plt.plot(ttotal, hc, "+", label="nu = 0.24 * reynolds ** 0.6")
    plt.plot(ttotal, hc_turb, "x", label="nu = 0.024 * reynolds ** 0.805")
    plt.xlabel("Ttotal, F")
    plt.xlim(5, 30)
    plt.ylabel("T, F")
    plt.ylim(0)
    plt.legend()

    plt.figure()
    plt.plot(ts_measureds, ts_calcs, '+')
    plt.plot((16, 34), (15, 34))

    plt.figure()
    for (
        run,
        ttotal,
        lwc,
        n,
        n_calc,
        tsm,
        ts_calc,
        tf,
        twet,
        n_calc2,
        ts_calc2,
        n_calc_turb,
        ts_calc_turb,
        n_calc_turb_wet,
        ts_calc_turb_wet,
        ts,
        hc,
        hc_turb,
    ) in d_rows:
        (line,) = plt.plot(tsm, tsm, "+", ms=14)
        plt.plot(tsm, ts, "^", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(tsm, ts_calc, "o", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot(tsm, ts_calc2, "s", fillstyle="none", c=line.get_color(), ms=12)
        plt.plot((tsm, tsm), (ts_calc, ts_calc2), ":", c=line.get_color())
        plt.text(tsm, tsm + 0.05, run)
    plt.plot([], [], "+", c="k", ms=14, label="Measured (run ID noted)")
    plt.plot(
        [], [], "^", fillstyle="none", c="k", ms=12, label="Calculated (Messinger)"
    )
    plt.plot(
        [],
        [],
        "o",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) (using T_static)",
    )
    plt.plot(
        [],
        [],
        "s",
        fillstyle="none",
        c="k",
        ms=12,
        label="Calculated (Python) (using T_wet)",
    )
    plt.plot((15, 35), (15, 35), ':')
    plt.xlabel("Tsurface measured, F")
    plt.xlim(14, 36)
    plt.xticks((15, 20, 25, 30, 35))
    plt.ylabel("Tsurface, F")
    plt.ylim(14, 36)
    plt.yticks((15, 20, 25, 30, 35))
    plt.legend()
    plt.savefig("messinger_table1_ts_ts.png")

    plt.show()
