"""
NASA-CR-4257

"""
from math import pi, degrees, radians
from statistics import mean, stdev
from icinganalysis.langmuir_blodgett_table_ii import value_interpolator
from icinganalysis import langmuir_cylinder_values
from icinganalysis.NACA_TN_2904.NACA_TN_2904_impingement import calc_em_from as naca_tn_2904_calc_em_from
from icinganalysis.NACA_TN_2904.NACA_TN_2904_impingement import calc_em as naca_tn_2904_calc_em
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def make_markdown_table(header, rows):
    text = "|".join(header) + "\n"
    text += "|".join(["---"] * len(header)) + "\n"
    for row in rows:
        text += "|".join([str(_) for _ in row]) + "\n"
    return text


def calc_em_h(s, beta):
    em = sum(
        (
            (s2 - s1) * (b1 + b2) / 2
            for s1, s2, b1, b2 in zip(s[:-1], s[1:], beta[:-1], beta[1:])
        )
    )
    return em


def get_uppers_lowers(s, beta):
    """
    will add a point at s=0 if there is not one
    """
    if 0 not in s:
        s = list(s)
        beta = list(beta)
        b0 = max(0, min(1, interp1d(s, beta, fill_value="extrapolate")(0)))
        i0s = [i for i, sv in enumerate(s) if sv < 0]
        i0 = 0
        if i0s:
            i0 = i0s[-1] + 1
        s.insert(i0, 0)
        beta.insert(i0, b0)
    s_upper, beta_upper = tuple(
        zip(*[(s, b) for s, b in zip(s, beta) if s <= 0])
    )  # might be the opposite of what you expect, but that's what figure 6.6 uses
    s_lower, beta_lower = tuple(zip(*[(s, b) for s, b in zip(s, beta) if s >= 0]))
    return s_upper, beta_upper, s_lower, beta_lower


def get_em_stats(case_data):
    name = case_data["name"]
    d_cyl = case_data["d_cyl"]
    mvd = case_data["mvd"]
    u = case_data["u"]
    p = case_data["p"]
    tk = case_data["tk"]
    lwc_fractions = case_data["lwc_fractions"]
    d_ratio_mids = case_data["d_ratio_mids"]
    s_cm = case_data["s_cm"]
    beta = case_data["beta"]
    em_average = calc_em_h(s_cm, beta) / 100 / d_cyl
    s_upper, beta_upper, s_lower, beta_lower = get_uppers_lowers(s_cm, beta)
    em_lower = calc_em_h(s_lower, beta_lower) * 2 / 100 / d_cyl
    em_upper = calc_em_h(s_upper, beta_upper) * 2 / 100 / d_cyl
    em_mvd = langmuir_cylinder_values.calc_em(tk, p, u, mvd, d_cyl)
    em_dist = sum(
        [
            w * langmuir_cylinder_values.calc_em(tk, p, u, r * mvd, d_cyl)
            for w, r in zip(lwc_fractions, d_ratio_mids)
        ]
    )
    return name, em_average, em_lower, em_upper, em_mvd, em_dist


# fmt:off
d_test = {
    'figure_6.6a': {
        'name': 'figure_6.6a',
        'd_cyl': 4 * 0.0254,
        'mvd': 20.36,
        'u': 80.25,
        'p': 95720,
        'tk': 273.15 + 7.9,
        'lwc_fractions': (0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05),
        'd_ratio_mids': (0.277, .446, .6617, 1, 1.5865, 2.2943, 3.2542),
        's_cm': (-7.2, -6.3, -5.6, -4.8, -4, -3.3, -2.6, -1.8, -1, 0, 0.7, 1.5, 2.3, 3.1, 4, 4.8, 5.5, 6.2),
        'beta': (0, 0.01, 0.04, 0.135, 0.285, 0.415, 0.47, 0.52, 0.54, 0.52, 0.517, 0.47, 0.405, 0.3, 0.15, 0.05, 0.01, 0),
    },
    'figure_6.6b': {
        'name': 'figure_6.6b',
        'd_cyl': 4 * 0.0254,
        'mvd': 16.45,
        'u': 81.02,
        'p': 95650,
        'tk': 273.15 + 8.2,
        'lwc_fractions': (0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05),
        'd_ratio_mids': (0.3161, 0.4981, 0.6872, 1, 1.3737, 1.9614, 2.8288),
        's_cm': (-6.2, -5.5, -4.6, -3.8, -3, -2.3, -1.6, -0.7, 0.1, 1.05, 1.8, 2.6, 3.4, 4.2, 5, 5.6),
        'beta': (0, 0.01, 0.045, 0.135, 0.255, 0.35, 0.405, 0.43, 0.42, 0.39, 0.315, 0.2, 0.095, 0.03, 0.01, 0),
    },
}
d_theory = {
    'figure_6.6a': {
        'name': 'figure_6.6a',
        'd_cyl': 4 * 0.0254,
        'mvd': 20.36,
        'u': 80.25,
        'p': 95720,
        'tk': 273.15 + 7.9,
        'lwc_fractions': (0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05),
        'd_ratio_mids': (0.277, .446, .6617, 1, 1.5865, 2.2943, 3.2542),
        's_cm': (-7.2, -6.3, -5.5, -4.3, -3, -2.3, -1.1, 0, 1.1, 2.3, 3, 4.3, 5.5, 6.3, 7.2),
        'beta': (0, 0.01, 0.04, 0.16, 0.3, 0.4, 0.5, 0.52, 0.5, 0.4, 0.3, 0.16, 0.04, 0.01, 0),
    },
    'figure_6.6b': {
        'name': 'figure_6.6b',
        'd_cyl': 4 * 0.0254,
        'mvd': 16.45,
        'u': 81.02,
        'p': 95650,
        'tk': 273.15 + 8.2,
        'lwc_fractions': (0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05),
        'd_ratio_mids': (0.3161, 0.4981, 0.6872, 1, 1.3737, 1.9614, 2.8288),
        's_cm': (-6.2, -5.5, -4.6, -3, -1.8, -1.3, -0.7, 0, 0.7, 1.3, 1.8, 3, 4.6, 5.5, 6.2),
        'beta': (0, 0.01, 0.045, 0.22, 0.34, 0.4, 0.43, 0.445, 0.43, 0.4, 0.34, 0.22, 0.045, 0.01, 0),
    },
}

repeats_a = {
    'figure_6_3_a_run_a': {
        'data_name': 'figure_6.6a',
        's_cm': (
            -7.2, -6.5, -6, -5.3, -4.8, -3.8, -3, -2.7, -2.4, -1.8, -1.1, -0.6, 0, 0.5, 1.1, 2.2, 3, 3.5, 4.1, 4.7, 5.1,
            5.6),
        'beta': (
            0, 0.01, 0.03, 0.1, 0.2, 0.4, 0.47, 0.495, 0.495, 0.515, 0.52, 0.527, 0.515, 0.495, 0.49, 0.4, 0.3, 0.2,
            0.1, 0.04, 0.018, 0),
    },
    'figure_6_3_a_run_b': {
        'data_name': 'figure_6.6a',
        's_cm': (
            -6.8, -6, -5.3, -5, -4.6, -4.1, -3.7, -3.1, -2.5, -1.8, -1.3, -0.6, -0.1, 0, 0.8, 1.5, 2.2, 2.9, 3.4, 3.6,
            4.2, 4.8, 5.3, 5.75, 6, 6.4),
        'beta': (
            0, 0.005, 0.03, 0.06, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.56, 0.535, 0.536, 0.55, 0.5, 0.465, 0.4, 0.35,
            0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0),
    },
}

repeats_b = {
    'figure_6_3_b_run_6b': {
        'data_name': 'figure_6.6b',
        's_cm': (-7.3, -7, -6.5, -6, -5.4, -4.5, -3.9, -3.2, -2.7, -1.8, -1, -0.5, 0, 1, 1.5, 2.2, 2.9, 3.4, 4, 4.4),
        'beta': (
            0, 0.005, 0, 0, 0.025, 0.1, 0.2, 0.3, 0.35, 0.4, 0.41, 0.42, 0.41, 0.35, 0.3, 0.2, 0.1, 0.05, 0.018, 0),
    },
    'figure_6_3_b_run_5c': {
        'data_name': 'figure_6.6b',
        's_cm': (
            -6.2, -5.9, -5.6, -5.2, -4.8, -4, -3.6, -2.9, -2.2, -1.7, -1, -0.6, -0.4, 0, 0.8, 1.5, 2.1, 2.7, 3.4, 4,
            4.5, 5,
            5.7, 6, 6.3),
        'beta': (
            0.02, 0.02, 0.005, 0.005, 0.015, 0.06, 0.1, 0.2, 0.3, 0.35, 0.4, 0.42, 0.42, 0.41, 0.4, 0.35, 0.3, 0.2, 0.1,
            0.045, 0.02, 0.01, 0, 0.01, 0.02),
    },
    'figure_6_3_b_run_6c': {
        'data_name': 'figure_6.6b',
        's_cm': (
            -6, -5.2, -4.8, -4.1, -3.8, -3.2, -2.6, -1.8, -0.65, 0, 0.5, 1.1, 1.6, 2.1, 2.6, 3.1, 3.8, 4.3, 5, 5.5),
        'beta': (
            0, 0.005, 0.015, 0.06, 0.1, 0.2, 0.3, 0.4, 0.455, 0.45, 0.453, 0.43, 0.4, 0.35, 0.3, 0.2, 0.1, 0.05, 0.01,
            0),
    },
}
# fmt:on


if __name__ == "__main__":

    header = (
        "Case",
        "MVD",
        "Em_test",
        "Em_test_lower",
        "Em_test_upper",
        "Em_calc_Breer",
        "Em_calc_LB",
        "Phi",
        "K_mvd",
    )

    rows = []
    for case in d_test:
        d_cyl = d_test[case]["d_cyl"]
        mvd = d_test[case]["mvd"]
        u = d_test[case]["u"]
        p = d_test[case]["p"]
        tk = d_test[case]["tk"]
        phi = langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl)
        k_mvd = langmuir_cylinder_values.calc_k(tk, u, mvd, d_cyl)
        name, em_average, em_lower, em_upper, em_mvd, em_dist = get_em_stats(
            d_test[case]
        )
        em_theory = get_em_stats(d_theory[case])[1]
        # fmt:off
        row_text = f"{case} {d_test[case]['mvd']:.2f} {em_average:.3f} {em_lower:.3f} " \
            f"{em_upper:.3f} {em_theory:.3f} {em_dist:.3f} {phi:.0f} {k_mvd:.2f}"
        # fmt:on
        rows.append(row_text.split(" "))

    print(make_markdown_table(header, rows))

    cols = list(zip(*rows))
    mvd, em_test, em_test_lower, em_test_upper, em_calc_breer, em_calc_lb, phi, ks_mvd = [
        [float(_) for _ in col] for col in cols[1:]
    ]
    variance = [0.1 * _ for _ in em_test]  # 10% variation from Conclusions
    plt.figure()
    eba = plt.errorbar(
        ks_mvd[0],
        em_test[0],
        yerr=variance[0],
        linestyle="",
        marker="o",
        capsize=4,
        mew=3,
        label="Test data MVD=20.36 (+/-10% repeatability)",
    )
    ebb = plt.errorbar(
        ks_mvd[1],
        em_test[1],
        yerr=variance[1],
        linestyle="",
        marker="o",
        capsize=4,
        mew=3,
        label="Test data MVD=16.45 (+/-10% repeatability)",
    )
    plt.text(ks_mvd[0], em_test[0], "  Figure_6.6a MVD=20.36")
    plt.text(ks_mvd[1], em_test[1], "  Figure_6.6b MVD=16.45")
    (line,) = plt.plot(
        ks_mvd,
        em_calc_lb,
        "s",
        fillstyle="none",
        ms=12,
        mew=2,
        label="Calculated (Langmuir-Blodgett)",
    )
    plt.plot(
        ks_mvd,
        em_calc_breer,
        "x",
        fillstyle="none",
        ms=12,
        mew=2,
        label="Calculated (Breer)",
    )

    ks = plt.np.logspace(-1, 2)
    ems_ks = [
        sum(
            [
                w * langmuir_cylinder_values.calc_em_from(k_ * r ** 2, phi[0])
                for w, r in zip(
                    d_test["figure_6.6a"]["lwc_fractions"],
                    d_test["figure_6.6a"]["d_ratio_mids"],
                )
            ]
        )
        for k_ in ks
    ]
    plt.plot(
        ks,
        ems_ks,
        "--",
        c=eba[0].get_color(),
        label=f"Calculated from measured distribution MVD={mvd[0]}",
    )
    ems_ks = [
        sum(
            [
                w * langmuir_cylinder_values.calc_em_from(k_ * r ** 2, phi[1])
                for w, r in zip(
                    d_test["figure_6.6b"]["lwc_fractions"],
                    d_test["figure_6.6b"]["d_ratio_mids"],
                )
            ]
        )
        for k_ in ks
    ]
    plt.plot(
        ks,
        ems_ks,
        ":",
        c=ebb[0].get_color(),
        label=f"Calculated from measured distribution MVD={mvd[1]}",
    )
    plt.xscale("log")
    plt.xlabel("K (based on MVD)")
    plt.ylim(0, 1)
    plt.ylabel("Em")

    plt.legend()
    plt.savefig("nasa_cr_4257_fig6_6_comparison.png")

    ems = []
    all_ems = []
    ave_ems = []
    for case in repeats_a:
        d_cyl = d_test[repeats_a[case]["data_name"]]["d_cyl"]
        em_h_cm = calc_em_h(repeats_a[case]["s_cm"], repeats_a[case]["beta"])
        em = em_h_cm / 100 / d_cyl
        s_upper, beta_upper, s_lower, beta_lower = get_uppers_lowers(
            repeats_a[case]["s_cm"], repeats_a[case]["beta"]
        )
        em_h_cm = calc_em_h(s_upper, beta_upper)
        em_upper = em_h_cm * 2 / 100 / d_cyl
        em_h_cm = calc_em_h(s_lower, beta_lower)
        em_lower = em_h_cm * 2 / 100 / d_cyl
        ems.append((case, em, em_upper, em_lower))
        all_ems.extend(ems[-1][1:])
        ave_ems.append(em)

    case, em, em_upper, em_lower = list(zip(*ems))
    em_ave = sum(em) / len(em)
    em_dev_a = stdev([float(_) for _ in all_ems])
    em_dev_av = stdev([float(_) for _ in ave_ems])
    print('fig6.3a em ave dev', em_dev_av, em_dev_av / mean([float(_) for _ in ave_ems]))

    header = "Case", "Em", "Em_upper", "Em_lower"
    rows = []
    for case, em, em_upper, em_lower in zip(case, em, em_upper, em_lower):
        vs = (
            (em - em_ave) / em_ave,
            (em_upper - em_ave) / em_ave,
            (em_lower - em_ave) / em_ave,
        )
        row = [case] + [f"{v*100:+.1f}%" for v in vs]
        rows.append(row)
    print()
    print(f"figure_6.6a Em_ave={em_ave:.3f} {em_dev_a:.4f}")
    print("repeats:")
    print(make_markdown_table(header, rows))
    print()

    ems = []
    all_ems = []
    ave_ems = []
    for case in repeats_b:
        d_cyl = d_test[repeats_b[case]["data_name"]]["d_cyl"]
        em_h_cm = calc_em_h(repeats_b[case]["s_cm"], repeats_b[case]["beta"])
        em = em_h_cm / 100 / d_cyl
        s_upper, beta_upper, s_lower, beta_lower = get_uppers_lowers(
            repeats_b[case]["s_cm"], repeats_b[case]["beta"]
        )
        em_h_cm = calc_em_h(s_upper, beta_upper)
        em_upper = em_h_cm * 2 / 100 / d_cyl
        em_h_cm = calc_em_h(s_lower, beta_lower)
        em_lower = em_h_cm * 2 / 100 / d_cyl
        ems.append((case, em, em_upper, em_lower))
        all_ems.extend(ems[-1][1:])
        ave_ems.append(em)

    case, em, em_upper, em_lower = list(zip(*ems))
    em_ave = sum(em) / len(em)
    em_dev_b = stdev([float(_) for _ in all_ems])
    em_dev_av = stdev([float(_) for _ in ave_ems])
    print('fig6.3b em ave dev', em_dev_av, em_dev_av / mean([float(_) for _ in ave_ems]))

    header = "Case", "Em", "Em_upper", "Em_lower"
    rows = []
    for case, em, em_upper, em_lower in zip(case, em, em_upper, em_lower):
        vs = (
            (em - em_ave) / em_ave,
            (em_upper - em_ave) / em_ave,
            (em_lower - em_ave) / em_ave,
        )
        row = [case] + [f"{v*100:+.1f}%" for v in vs]
        rows.append(row)
    print(f"figure_6.6b Em_ave={em_ave:.3f} {em_dev_b:.4f}")
    print("repeats:")
    print(make_markdown_table(header, rows))
    print()

    plt.figure()
    ks = plt.np.logspace(-1, 2)
    for repeats, drop_diam_max in zip((repeats_a, repeats_b), (4.25 * 20.36, 77.7)):
        thetas = []
        for case in repeats:
            d_cyl = d_test[repeats[case]["data_name"]]["d_cyl"]
            s_min = repeats[case]["s_cm"][0] / 100
            s_max = repeats[case]["s_cm"][-1] / 100
            theta_min = 360 * s_min / (pi * d_cyl)
            theta_max = 360 * s_max / (pi * d_cyl)
            theta_min = degrees(
                s_min / (d_cyl / 2)
            )  # OK, I think that I get the degrees function now...
            theta_max = degrees(s_max / (d_cyl / 2))
            thetas.append(abs(theta_min))
            thetas.append(abs(theta_max))
            data_name = repeats[case]["data_name"]
            d_cyl = d_test[data_name]["d_cyl"]
            mvd = d_test[data_name]["mvd"]
            u = d_test[data_name]["u"]
            p = d_test[data_name]["p"]
            tk = d_test[data_name]["tk"]
            theta_calc_degree = value_interpolator(
                langmuir_cylinder_values.calc_k(tk, u, drop_diam_max, d_cyl),
                langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl),
                "theta_degree",
            )
            k_mvd = langmuir_cylinder_values.calc_k(tk, u, mvd, d_cyl)

        eba = plt.plot(
            [k_mvd] * len(thetas),
            thetas,
            "_",
            ms=12,
            mew=3,
            label=f"Test data MVD={mvd}",
        )
        theta_calcs_degrees = [
            value_interpolator(
                k * (drop_diam_max / mvd) ** 2,
                langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl),
                "theta_degree",
            )
            for k in ks
        ]
        plt.plot(
            ks,
            theta_calcs_degrees,
            "--",
            c=eba[0].get_color(),
            label=f"Calculated with maximum drop diameter from measured distribution MVD={mvd}",
        )

    plt.xscale("log")
    plt.xlabel("K (based on MVD)")
    plt.ylabel("Theta impingement maximum, degrees")
    plt.ylim(0, 90)
    plt.yticks(range(0, 90 + 10, 10))
    plt.legend()
    plt.savefig("nasa_cr_4257_theta_comparison.png")

    plt.figure()
    ks = plt.np.logspace(-1, 2)
    ks_naca_tn_2904 = plt.np.logspace(plt.np.log10(.25), 2)  # stay in 1/k range NACA-TN-2904 of Table IV
    for repeats in (repeats_a, repeats_b):
        ems_test = []
        for case in repeats:
            data_name = repeats[case]["data_name"]
            d_cyl = d_test[data_name]["d_cyl"]
            mvd = d_test[data_name]["mvd"]
            u = d_test[data_name]["u"]
            p = d_test[data_name]["p"]
            tk = d_test[data_name]["tk"]
            s_cm = repeats[case]["s_cm"]
            beta = repeats[case]["beta"]
            em_test = calc_em_h(s_cm, beta) / 100 / d_cyl
            ems_test.append(em_test)

            k_mvd = langmuir_cylinder_values.calc_k(tk, u, mvd, d_cyl)

        eba = plt.plot(
            [k_mvd] * len(ems_test),
            ems_test,
            "_",
            ms=12,
            mew=3,
            label=f"Test data MVD={mvd}",
        )
        ems_calc = [
            sum(
                [
                    w
                    * langmuir_cylinder_values.calc_em_from(
                        k * r ** 2, langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl)
                    )
                    for w, r in zip(
                        d_test[data_name]["lwc_fractions"],
                        d_test[data_name]["d_ratio_mids"],
                    )
                ]
            )
            for k in ks
        ]
        plt.plot(
            ks,
            ems_calc,
            "--",
            c=eba[0].get_color(),
            label=f"Calculated from measured distribution MVD={mvd}",
        )
        ems_calc_naca_tn_2904 = [
            sum(
                [
                    w * naca_tn_2904_calc_em_from(
                        k * r ** 2, k*langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl))
                    for w, r in zip(
                        d_test[data_name]["lwc_fractions"],
                        d_test[data_name]["d_ratio_mids"],
                    )
                ]
            )
            for k in ks_naca_tn_2904
        ]
        plt.plot(
            ks_naca_tn_2904,
            ems_calc_naca_tn_2904,
            ":",
            c=eba[0].get_color(),
            label=f"NACA-TN-2904 from measured distribution MVD={mvd}",
        )
    plt.plot(
        ks_mvd,
        em_calc_breer,
        "x",
        fillstyle="none",
        ms=12,
        mew=2,
        label="Calculated (Breer)",
    )

    plt.xscale("log")
    # plt.xlim(1, 3)
    plt.xlabel("K (based on MVD)")
    plt.ylabel("Em")
    plt.ylim(0, 1)
    plt.legend()
    plt.savefig("nasa_cr_4257_em_comparison.png")

    plt.figure(figsize=(8, 8))
    mvds = list(range(5, 40+1, 1))
    ks_naca_tn_2904 = plt.np.logspace(plt.np.log10(.25), 2)  # stay in 1/k range NACA-TN-2904 of Table IV
    for repeats in (repeats_a, repeats_b):
        ems_test = []
        for case in repeats:
            data_name = repeats[case]["data_name"]
            d_cyl = d_test[data_name]["d_cyl"]
            mvd = d_test[data_name]["mvd"]
            u = d_test[data_name]["u"]
            p = d_test[data_name]["p"]
            tk = d_test[data_name]["tk"]
            s_cm = repeats[case]["s_cm"]
            beta = repeats[case]["beta"]
            em_test = calc_em_h(s_cm, beta) / 100 / d_cyl
            ems_test.append(em_test)

            k_mvd = langmuir_cylinder_values.calc_k(tk, u, mvd, d_cyl)

        eba = plt.plot(
            [mvd] * len(ems_test),
            ems_test,
            "_",
            ms=12,
            mew=3,
            label=f"Test data MVD={mvd}",
        )
        ems_calc = [
            sum(
                [
                    w
                    * langmuir_cylinder_values.calc_em(tk, p, u, r*mvd_, d_cyl)
                    for w, r in zip(
                        d_test[data_name]["lwc_fractions"],
                        d_test[data_name]["d_ratio_mids"],
                    )
                ]
            )
            for mvd_ in mvds
        ]
        plt.plot(
            mvds,
            ems_calc,
            "--",
            c=eba[0].get_color(),
            label=f"Langmuir-Blodgett calculated from distribution MVD={mvd}",
        )
        ems_calc_naca_tn_2904 = [
            sum(
                [
                    w * naca_tn_2904_calc_em(tk, p, u, r*mvd_, d_cyl)
                    for w, r in zip(
                        d_test[data_name]["lwc_fractions"],
                        d_test[data_name]["d_ratio_mids"],
                    )
                ]
            )
            for mvd_ in mvds
        ]
        plt.plot(
            mvds,
            ems_calc_naca_tn_2904,
            ":",
            c=eba[0].get_color(),
            label=f"NACA-TN-2904 calculated from distribution MVD={mvd}",
        )
    plt.plot(
        (20.36, 16.45),
        em_calc_breer,
        "x",
        fillstyle="none",
        ms=12,
        mew=2,
        label="Calculated (Breer)",
    )

    plt.xlim(10, 25)
    plt.xlabel("MVD, micrometer")
    plt.ylabel("Em")
    plt.ylim(0, 0.6)
    plt.legend(loc='upper left')
    plt.savefig("nasa_cr_4257_em_comparison_mvd.png")

    print(radians(5)*(d_cyl/2))
    print(radians(90)*(d_cyl/2))

    plt.show()
