"""
Reproduce Figure 14 from NACA-TN-2904
"""


from icinganalysis import langmuir_cylinder
from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement, multicylinder_naca_tn_2904
import matplotlib.pyplot as plt

# Figure 11 data
em_lwcs = 0.0297, 0.0269, 0.0226, 0.0163
d_cyls_inch = 0.125, 0.5, 1.25, 3
d_cyls = [_ * 0.0254 for _ in d_cyls_inch]

alt_ft = 10000
tk = (9 + 459.67) / 1.8
p = langmuir_cylinder.calc_pressure(alt_ft * 12 * 0.0254)

mc = multicylinder_naca_tn_2904.Multicylinder(d_cyls)

base_distribution = "Langmuir B"
base_lwc = 0.55
mvds = list(plt.np.arange(5, 30 + 2.5, 2.5))
mphs = [400, 300, 200, 100]
mass_ramp_up_ratios = 0.95, 0.9833, 1.0167, 1.05
print("this might take a while...")
plt.figure()
for mph in mphs:
    u = mph * 0.44704
    fds_up = []
    fds_down = []
    dists_up = []
    dists_down = []
    for mvd in mvds:
        masses = [NACA_TN_2904_impingement.ie(
            langmuir_cylinder.calc_k(tk, u, mvd, d),
            langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
            base_distribution
        ) * base_lwc / 1000 * u * d for d in d_cyls]
        lwc_, mvd_, dist_, rss_ = mc.find_lwc_mvd_dist(tk, u, p, masses)
        masses_ramped_up = [mass * ratio for mass, ratio in zip(masses, mass_ramp_up_ratios)]
        lwc_ramped_up, mvd_ramped_up, dist_ramped_up, rss_ramped_up = mc.find_lwc_mvd_dist(
            tk, u, p, masses_ramped_up, guess_mvd=mvd)
        fds_up.append((abs(mvd_ramped_up - mvd) / mvd))
        dists_up.append(dist_ramped_up)
        masses_ramped_down = [mass * ratio for mass, ratio in zip(masses, reversed(mass_ramp_up_ratios))]
        lwc_ramped_down, mvd_ramped_down, dist_ramped_down, rss_ramped_down = mc.find_lwc_mvd_dist(tk, u, p,
                                                                                                   masses_ramped_down,
                                                                                                   guess_mvd=mvd)
        fds_down.append((abs(mvd_ramped_down - mvd) / mvd))
        dists_down.append(dist_ramped_down)
    line, = plt.plot(mvds, fds_down, label=f"MPH={mph:.0f}")
    for m, v, t in zip(mvds, fds_down, dists_down):
        plt.text(m, v, t[-1], c=line.get_color())
    plt.plot(mvds, fds_up, '--', c=line.get_color())
    for m, v, t in zip(mvds, fds_up, dists_up):
        plt.text(m, v, t[-1], c=line.get_color())
plt.plot([], [], '-', c='k', label="Lower limit error (MVD to small)")
plt.plot([], [], '--', c='k', label="Upper limit error (MVD to large)")
plt.xlim(0, 35)
plt.ylim(0, max(0.8, plt.ylim()[1]))
plt.xlabel('MVD, micrometer')
plt.ylabel('Maximum possible error (MVD_calc-MVD)/MVD')
plt.legend(loc="center left")
plt.savefig('NACA_TN_2904_Figure_14a_calc.png', transparent=True)

# plt.figure()
# mass_ramp_up_ratios = 0.9, 0.9667, 1.0333, 1.1
# for mph in mphs:
#     u = mph * 0.44704
#     fds_up = []
#     fds_down = []
#     dists_up = []
#     dists_down = []
#     for mvd in mvds:
#         masses = [NACA_TN_2904_impingement.ie(
#             langmuir_cylinder.calc_k(tk, u, mvd, d),
#             langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
#             base_distribution
#         ) * base_lwc / 1000 * u * d for d in d_cyls]
#         lwc_, mvd_, dist_, rss_ = mc.find_lwc_mvd_dist(tk, u, p, masses)
#         masses_ramped_up = [mass * ratio for mass, ratio in zip(masses, mass_ramp_up_ratios)]
#         lwc_ramped_up, mvd_ramped_up, dist_ramped_up, rss_ramped_up = mc.find_lwc_mvd_dist(
#             tk, u, p, masses_ramped_up, guess_mvd=mvd)
#         fds_up.append((abs(mvd_ramped_up - mvd) / mvd))
#         dists_up.append(dist_ramped_up)
#         masses_ramped_down = [mass * ratio for mass, ratio in zip(masses, reversed(mass_ramp_up_ratios))]
#         lwc_ramped_down, mvd_ramped_down, dist_ramped_down, rss_ramped_down = mc.find_lwc_mvd_dist(tk, u, p,
#                                                                                                    masses_ramped_down,
#                                                                                                    guess_mvd=mvd)
#         fds_down.append((abs(mvd_ramped_down - mvd) / mvd))
#         dists_down.append(dist_ramped_down)
#     line, = plt.plot(mvds, fds_down, label=f"MPH={mph:.0f}")
#     for m, v, t in zip(mvds, fds_down, dists_down):
#         plt.text(m, v, t[-1], c=line.get_color())
#     plt.plot(mvds, fds_up, '--', c=line.get_color())
#     for m, v, t in zip(mvds, fds_up, dists_up):
#         plt.text(m, v, t[-1], c=line.get_color())
# plt.plot([], [], '-', c='k', label="Lower limit error (MVD to small)")
# plt.plot([], [], '--', c='k', label="Upper limit error (MVD to large)")
# plt.xlim(0, 35)
# plt.ylim(0, max(0.8, plt.ylim()[1]))
# plt.xlabel('MVD, micrometer')
# plt.ylabel('Maximum possible error (MVD_calc-MVD)/MVD')
# plt.legend(loc="center left")
# plt.savefig('NACA_TN_2904_Figure_14b_calc_.png', transparent=True)
#
# plt.figure()
# mass_ramp_up_ratios = 0.9, 0.9667, 1.0333, 1.1
# for mph in mphs:
#     u = mph * 0.44704
#     fds_up = []
#     fds_down = []
#     dists_up = []
#     dists_down = []
#     for mvd in mvds:
#         masses = [NACA_TN_2904_impingement.ie(
#             langmuir_cylinder.calc_k(tk, u, mvd, d),
#             langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
#             base_distribution
#         ) * base_lwc / 1000 * u * d for d in d_cyls]
#         lwc_, mvd_, dist_, rss_ = mc.find_lwc_mvd_dist(tk, u, p, masses)
#         masses_ramped_up = [mass * ratio for mass, ratio in zip(masses, mass_ramp_up_ratios)]
#         lwc_ramped_up, mvd_ramped_up, dist_ramped_up, rss_ramped_up = mc.find_lwc_mvd_dist(
#             tk, u, p, masses_ramped_up, guess_mvd=mvd)
#         fds_up.append((abs(mvd_ramped_up - mvd) / mvd))
#         dists_up.append(dist_ramped_up)
#         masses_ramped_down = [mass * ratio for mass, ratio in zip(masses, reversed(mass_ramp_up_ratios))]
#         lwc_ramped_down, mvd_ramped_down, dist_ramped_down, rss_ramped_down = mc.find_lwc_mvd_dist(tk, u, p,
#                                                                                                    masses_ramped_down,
#                                                                                                    guess_mvd=mvd)
#         fds_down.append((abs(mvd_ramped_down - mvd) / mvd))
#         dists_down.append(dist_ramped_down)
#     line, = plt.plot(mvds, fds_down, label=f"MPH={mph:.0f}")
#     for m, v, t in zip(mvds, fds_down, dists_down):
#         plt.text(m, v, t[-1], c=line.get_color())
#     plt.plot(mvds, fds_up, '--', c=line.get_color())
#     for m, v, t in zip(mvds, fds_up, dists_up):
#         plt.text(m, v, t[-1], c=line.get_color())
# plt.plot([], [], '-', c='k', label="Lower limit error (MVD to small)")
# plt.plot([], [], '--', c='k', label="Upper limit error (MVD to large)")
# plt.xlim(0, 35)
# plt.ylim(0, 1.05)
# plt.xlabel('MVD, micrometer')
# plt.ylabel('Maximum possible error (MVD_calc-MVD)/MVD')
# plt.legend(loc="center left")
# plt.savefig('NACA_TN_2904_Figure_14b_calc.png', transparent=True)

plt.show()
