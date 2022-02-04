"""
NASA-CR-4257

"""
from icinganalysis import langmuir_cylinder_values
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
    )  # might be the opposite of the expected, but that's what figure 6.6 uses
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


d_cyl = 4 * 0.0254
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
        's_cm': (-7.2, -6.3, -5.6, -4.8, -4, -3.3, -2.6, -1.8, -1,
                 0,
                 0.7, 1.5, 2.3, 3.1, 4, 4.8, 5.5, 6.2),
        'beta': (
            0, 0.01, 0.04, 0.135, 0.285, 0.415, 0.47, 0.52, 0.54,
            0.52,
            0.517, 0.47, 0.405, 0.3, 0.15, 0.05, 0.01, 0),
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

plt.plot(d_test["figure_6.6a"]["s_cm"], d_test["figure_6.6a"]["beta"], "o")
plt.plot(
    d_theory["figure_6.6a"]["s_cm"], d_theory["figure_6.6a"]["beta"],
)
plt.grid()

print(calc_em_h(d_test["figure_6.6a"]["s_cm"], d_test["figure_6.6a"]["beta"]))
print(calc_em_h(d_test["figure_6.6b"]["s_cm"], d_test["figure_6.6b"]["beta"]))
print(
    calc_em_h(d_test["figure_6.6a"]["s_cm"], d_test["figure_6.6a"]["beta"])
    / 2
    / 100
    / d_test["figure_6.6a"]["d_cyl"]
)
print(
    calc_em_h(d_theory["figure_6.6a"]["s_cm"], d_theory["figure_6.6a"]["beta"])
    / 2
    / 100
    / d_theory["figure_6.6a"]["d_cyl"]
)

s_upper, beta_upper, s_lower, beta_lower = get_uppers_lowers(
    d_test["figure_6.6a"]["s_cm"], d_test["figure_6.6a"]["beta"]
)
print(calc_em_h(s_upper, beta_upper) / 100 / d_test["figure_6.6a"]["d_cyl"])
print(calc_em_h(s_lower, beta_lower) / 100 / d_test["figure_6.6a"]["d_cyl"])

u = 80.25
tk = 273.15 + 7.9
p = 95720
mvd = 20.36

em_calc = langmuir_cylinder_values.calc_em(tk, p, u, mvd, d_cyl)

em_dist = sum(
    [
        w * langmuir_cylinder_values.calc_em(tk, p, u, r * mvd, d_cyl)
        for w, r in zip(
        d_test["figure_6.6a"]["lwc_fractions"],
        d_test["figure_6.6a"]["d_ratio_mids"],
    )
    ]
)
print(em_dist)

print(em_calc)

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
    name, em_average, em_lower, em_upper, em_mvd, em_dist = get_em_stats(d_test[case])
    em_theory = get_em_stats(d_theory[case])[1]
    # fmt:off
    row_text = f"{case} {d_test[case]['mvd']:.2f} {em_average:.3f} {em_lower:.3f} " \
        f"{em_upper:.3f} {em_theory:.3f} {em_dist:.3f} {phi:.0f} {k_mvd:.2f}"
    # fmt:on
    print('row_text.split', row_text.split(" "))
    rows.append(row_text.split(" "))

print(make_markdown_table(header, rows))

cols = list(zip(*rows))
print(rows)
print(cols)
mvd, em_test, em_test_lower, em_test_upper, em_calc_breer, em_calc_lb, phi, k = [
    [float(_) for _ in col] for col in cols[1:]
]

plt.figure()
plt.plot(k, em_test, "_", c="k", ms=14, label="Test data")
plt.plot(k, em_test_lower, "_", c="k", ms=14)
plt.plot(k, em_test_upper, "_", c="k", ms=14)
plt.text(k[0], em_test[0], " figure_6.6a")
plt.text(k[1], em_test[1], " figure_6.6b")
plt.plot(k, em_calc_breer, "x", label="Calculated (Breer)")
(line,) = plt.plot(k, em_calc_lb, "+", label="Calculated (Langmuir-Blodgett)")

ks = plt.np.logspace(-1, 2)
ems = [langmuir_cylinder_values.calc_em_from(k, phi[0]) for k in ks]
ems = [
    sum(
        [
            w * langmuir_cylinder_values.calc_em_from(k * r ** 2, phi[0])
            for w, r in zip(
            d_test["figure_6.6a"]["lwc_fractions"],
            d_test["figure_6.6a"]["d_ratio_mids"],
        )
        ]
    )
    for k in ks
]
plt.plot(
    ks,
    ems,
    "--",
    c=line.get_color(),
    label=f"Figure 6.6a distribution Em_calc Phi={phi[0]:.0f}",
)
ems = [
    sum(
        [
            w * langmuir_cylinder_values.calc_em_from(k * r ** 2, phi[1])
            for w, r in zip(
            d_test["figure_6.6b"]["lwc_fractions"],
            d_test["figure_6.6b"]["d_ratio_mids"],
        )
        ]
    )
    for k in ks
]
plt.plot(
    ks,
    ems,
    ":",
    c=line.get_color(),
    label=f"Figure 6.6b distribution Em_calc Phi={phi[1]:.0f}",
)
plt.xscale("log")
plt.legend()

ems = []
for case in repeats_a:
    d_cyl = d_test[repeats_a[case]['data_name']]['d_cyl']
    em_h_cm = calc_em_h(repeats_a[case]['s_cm'], repeats_a[case]['beta'])
    em = em_h_cm / 100 / d_cyl
    s_upper, beta_upper, s_lower, beta_lower = get_uppers_lowers(repeats_a[case]['s_cm'], repeats_a[case]['beta'])
    em_h_cm = calc_em_h(s_upper, beta_upper)
    em_upper = em_h_cm *2 / 100 / d_cyl
    em_h_cm = calc_em_h(s_lower, beta_lower)
    em_lower = em_h_cm *2 / 100 / d_cyl
    ems.append((case, em, em_upper, em_lower))
    print(case, em, em_upper, em_lower)

case, em, em_upper, em_lower = list(zip(*ems))
em_ave = sum(em)/len(em)

header = "Case", "Em", "Em_upper", "Em_lower"
rows = []
for case, em, em_upper, em_lower in zip(case, em, em_upper, em_lower):
    vs = (em-em_ave)/em_ave, (em_upper-em_ave)/em_ave, (em_lower-em_ave)/em_ave,
    row = [case] + [f"{v*100:+.1f}%" for v in vs]
    rows.append(row)
print(f"figure_6.6a Em_ave={em_ave:.3f}")
print("repeats:")
print(make_markdown_table(header, rows))
print()

ems = []
for case in repeats_b:
    d_cyl = d_test[repeats_b[case]['data_name']]['d_cyl']
    em_h_cm = calc_em_h(repeats_b[case]['s_cm'], repeats_b[case]['beta'])
    em = em_h_cm / 100 / d_cyl
    s_upper, beta_upper, s_lower, beta_lower = get_uppers_lowers(repeats_b[case]['s_cm'], repeats_b[case]['beta'])
    em_h_cm = calc_em_h(s_upper, beta_upper)
    em_upper = em_h_cm *2 / 100 / d_cyl
    em_h_cm = calc_em_h(s_lower, beta_lower)
    em_lower = em_h_cm *2 / 100 / d_cyl
    ems.append((case, em, em_upper, em_lower))
    print(case, em, em_upper, em_lower)

case, em, em_upper, em_lower = list(zip(*ems))
em_ave = sum(em)/len(em)

header = "Case", "Em", "Em_upper", "Em_lower"
rows = []
for case, em, em_upper, em_lower in zip(case, em, em_upper, em_lower):
    vs = (em-em_ave)/em_ave, (em_upper-em_ave)/em_ave, (em_lower-em_ave)/em_ave,
    row = [case] + [f"{v*100:+.1f}%" for v in vs]
    rows.append(row)
print(f"figure_6.6b Em_ave={em_ave:.3f}")
print("repeats:")
print(make_markdown_table(header, rows))
print()

plt.show()
