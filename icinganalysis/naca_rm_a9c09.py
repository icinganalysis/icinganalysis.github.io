import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from icinganalysis import langmuir_blodgett_multicylinder
from icinganalysis import langmuir_blodgett_table_ii
from icinganalysis import langmuir_cylinder_values
from icinganalysis.langmuir_cylinder_values import valid_distribution_ids


def calc_mvd_for_theta_degree(theta_degree, tk, p, u, d_cylinder):
    def f(mvd_):
        theta_calc = max(
            0,
            langmuir_blodgett_table_ii.value_interpolator(
                langmuir_cylinder_values.calc_k(tk, u, mvd_, d_cylinder),
                langmuir_cylinder_values.calc_phi(tk, p, u, d_cylinder),
                "theta_degree",
            ),
        )
        return abs(theta_calc - theta_degree)

    solution = minimize_scalar(f, bounds=[1, 1000], method="bounded")
    mvd = float("nan")
    if solution.success:
        mvd = solution.x
    return mvd


d_cyls_A_inch = 0.125, 0.5, 1.25, 3
d_cyls_A = [_ * 0.0254 for _ in d_cyls_A_inch]
d_cyls_B_inch = 0.25, 1, 2.5, 6
d_cyls_B = [_ * 0.0254 for _ in d_cyls_B_inch]
d_cylinder_C = 5 * 0.0254
lengths_cyls = [5 * 0.0254] * len(d_cyls_A)  # assumed

# borrow values from NACA-TN-1393
lengths = [6 * 0.0254, 6 * 0.0254]  # apparent lengths from Figure 2
mvd = 10  # from the appendix
lwc = 0.5  # from the appendix
time = 60  # from the appendix
tk = 273.15 - 20  # assumed to be cold enough to freeze all water
p = 101325  # assumed
mph = (
    2.5 * 100 / 1.5
)  # inferred from table in appendix, "2.5 mph" and "1.5%", results in 166 mph, which is "reasonable"
u = mph * 0.44704
mvds = list(plt.np.arange(5, 47.5 + 2.5, 2.5))

# calculate max drop impingement differences for fixed cylinder C
diff_max_diameters = []
for mvd in mvds:
    theta_degree = max(
        0,
        langmuir_blodgett_table_ii.value_interpolator(
            langmuir_cylinder_values.calc_k(tk, u, mvd, d_cylinder_C),
            langmuir_cylinder_values.calc_phi(tk, p, u, d_cylinder_C),
            "theta_degree",
        ),
    )
    mvd_m_5 = float("nan")
    mvd_p_5 = float("nan")
    if theta_degree > 0:
        mvd_p_5 = calc_mvd_for_theta_degree(theta_degree + 5, tk, p, u, d_cylinder_C)
        if theta_degree - 5 > 0:
            mvd_m_5 = calc_mvd_for_theta_degree(
                theta_degree - 5, tk, p, u, d_cylinder_C
            )
    diff_max_diameters.append(max(abs(mvd_p_5 - mvd) / mvd, abs(mvd_m_5 - mvd) / mvd))


mass_ramp_up_ratios = 0.95, 0.9833, 1.0167, 1.05  # -/+ 5%, ramped up with diameter
mc = langmuir_blodgett_multicylinder.Multicylinder(d_cyls_A)
mc_B = langmuir_blodgett_multicylinder.Multicylinder(d_cyls_B)

print("this might take a while...")
plt.figure(figsize=(8, 4.8))
for dist in valid_distribution_ids:
    dists = []
    fds_up = []
    fds_down = []
    fds = []
    for mvd in mvds:
        masses = [
            langmuir_blodgett_multicylinder.langmuir_cylinder_values.calc_em_with_distribution_original(
                tk, p, u, mvd, d, dist
            )
            * lwc
            / 1000
            * u
            * d
            for d in d_cyls_A
        ]
        masses_ramped_up = [m * r for m, r in zip(masses, mass_ramp_up_ratios)]
        (
            lwc_ramped_up,
            mvd_ramped_up,
            dist_ramped_up,
            rss_ramped_up,
        ) = mc.find_lwc_mvd_dist(tk, u, p, masses_ramped_up)
        fds_up.append((abs(mvd_ramped_up - mvd) / mvd))
        masses_ramped_down = [
            m * r for m, r in zip(masses, reversed(mass_ramp_up_ratios))
        ]
        (
            lwc_ramped_down,
            mvd_ramped_down,
            dist_ramped_down,
            rss_ramped_down,
        ) = mc.find_lwc_mvd_dist(tk, u, p, masses_ramped_down)
        fds_down.append((abs(mvd_ramped_down - mvd) / mvd))
        fds.append(max(fds_up[-1], fds_down[-1]))
        dists.append(dist_ramped_up if fds_up[-1] > fds_down[-1] else dist_ramped_down)
    plt.plot(mvds, fds, label=f"Set A initial distribution {dist}")
    for m, f, d in zip(mvds, fds, dists):
        plt.text(m, f, d[-1])
plt.xlim(5, 50)
plt.ylim(0, 1)
# plt.xlabel("MVD, micrometer")
# plt.ylabel("Maximum measurement error fraction, (MVD_calc-MVD)/MVD")
plt.legend()
plt.savefig("naca_rm_a9c09_fig2_a.png", transparent=True)

plt.figure(figsize=(8, 4.8))
dist = "Langmuir A"
# for dist in valid_distribution_ids:
for dist in ("Langmuir A",):
    dists = []
    fds_up = []
    fds_down = []
    fds = []
    for mvd in mvds:
        masses = [
            langmuir_blodgett_multicylinder.langmuir_cylinder_values.calc_em_with_distribution_original(
                tk, p, u, mvd, d, dist
            )
            * lwc
            / 1000
            * u
            * d
            for d in d_cyls_A
        ]
        masses_ramped_up = [m * r for m, r in zip(masses, mass_ramp_up_ratios)]
        (
            lwc_ramped_up,
            mvd_ramped_up,
            dist_ramped_up,
            rss_ramped_up,
        ) = mc.find_lwc_mvd_dist(tk, u, p, masses_ramped_up)
        fds_up.append((abs(mvd_ramped_up - mvd) / mvd))
        masses_ramped_down = [
            m * r for m, r in zip(masses, reversed(mass_ramp_up_ratios))
        ]
        (
            lwc_ramped_down,
            mvd_ramped_down,
            dist_ramped_down,
            rss_ramped_down,
        ) = mc.find_lwc_mvd_dist(tk, u, p, masses_ramped_down)
        fds_down.append((abs(mvd_ramped_down - mvd) / mvd))
        fds.append(max(fds_up[-1], fds_down[-1]))
        dists.append(dist_ramped_up if fds_up[-1] > fds_down[-1] else dist_ramped_down)
    plt.plot(mvds, fds, label=f"MVD Set A")
    # for m, f, d in zip(mvds, fds, dists):
    #     plt.text(m, f, d[-1])
    dists = []
    fds_up = []
    fds_down = []
    fds = []
    for mvd in mvds:
        masses = [
            langmuir_blodgett_multicylinder.langmuir_cylinder_values.calc_em_with_distribution_original(
                tk, p, u, mvd, d, dist
            )
            * lwc
            / 1000
            * u
            * d
            for d in d_cyls_B
        ]
        masses_ramped_up = [m * r for m, r in zip(masses, mass_ramp_up_ratios)]
        (
            lwc_ramped_up,
            mvd_ramped_up,
            dist_ramped_up,
            rss_ramped_up,
        ) = mc_B.find_lwc_mvd_dist(tk, u, p, masses_ramped_up)
        fds_up.append((abs(mvd_ramped_up - mvd) / mvd))
        masses_ramped_down = [
            m * r for m, r in zip(masses, reversed(mass_ramp_up_ratios))
        ]
        (
            lwc_ramped_down,
            mvd_ramped_down,
            dist_ramped_down,
            rss_ramped_down,
        ) = mc_B.find_lwc_mvd_dist(tk, u, p, masses_ramped_down)
        fds_down.append((abs(mvd_ramped_down - mvd) / mvd))
        fds.append(max(fds_up[-1], fds_down[-1]))
        dists.append(dist_ramped_up if fds_up[-1] > fds_down[-1] else dist_ramped_down)
    plt.plot(mvds, fds, label=f"MVD Set B")
    # for m, f, d in zip(mvds, fds, dists):
    #     plt.text(m, f, d[-1])
    plt.plot(mvds, diff_max_diameters, "--", label="Maximum drop diameter Cylinder C")

plt.xlim(5, 50)
plt.ylim(0, 1)
# plt.xlabel("MVD or Maximum drop diameter, micrometer")
# plt.ylabel("Maximum measurement error fraction, (dia_calc-dia)/dia")
plt.legend()
plt.savefig("naca_rm_a9c09_fig2.png", transparent=True)

plt.show()
