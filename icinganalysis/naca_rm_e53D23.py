"""
NACA-RM-E53D23
"""
from icinganalysis.NACA_TN_2904 import multicylinder_naca_tn_2904
from icinganalysis import langmuir_blodgett_multicylinder
from icinganalysis import langmuir_blodgett_multicylinder_k_phi_unique_mvd
from icinganalysis import air_properties
from icinganalysis import langmuir_cylinder_values
import matplotlib.pyplot as plt
from math import log10, pi


def calc_ave_d(d0, mass, length, ice_density=917):
    d_ave = 0.5 * (d0 + (4 * mass / (ice_density * pi * length) + d0 ** 2) ** 0.5)
    return d_ave


if __name__ == "__main__":
    # Table I and Table IV (same input values)
    u = 185 * 0.44704
    p = air_properties.calc_pressure(7000 * 0.3048)
    tk = -12.2 + 273.15  # using "Corrected temperature"
    icing_time = 216
    cylinder_diameters = [_ * 0.0254 for _ in (0.125, 0.5, 1.25, 3, 4.5)]
    lengths_cyls = [
        5.08 / 100 for _ in cylinder_diameters
    ]  # 5.08 cm from page 7, appears to agree with Figure 3
    masses = [
        _ / 1000 for _ in (1.1, 2.62, 4.52, 6.22, 7.06)
    ]  # original masses in grams
    ice_density = 850  # kg/m^3, page 7

    mc = multicylinder_naca_tn_2904.Multicylinder(cylinder_diameters, lengths_cyls)
    lwc, mvd, dist, rss = mc.find_lwc_mvd_dist(
        tk, u, p, masses, icing_time, ice_density
    )
    average_diameters = [
        calc_ave_d(d, m, l, ice_density)
        for d, m, l in zip(cylinder_diameters, masses, lengths_cyls)
    ]
    ems = [
        langmuir_cylinder_values.calc_em_with_distribution_original(
            tk, p, u, mvd, d, dist
        )
        for d in average_diameters
    ]
    k_phi = langmuir_cylinder_values.calc_k_phi(tk, p, u, mvd)
    print(k_phi)
    ks = [langmuir_cylinder_values.calc_k(tk, u, mvd, d) for d in average_diameters]

    plt.figure()
    for distribution in (
        "Langmuir A",
        "Langmuir B",
        "Langmuir C",
        "Langmuir D",
        "Langmuir E",
    ):
        lwc_, mvd_, rss_ = mc.find_lwc_mvd_from_dist(
            tk, u, p, masses, icing_time, distribution, ice_density
        )
        plt.plot(mvd_, lwc_, "+", ms=10, label=f"{distribution} RSS={rss_:.3f}")

    print(mvd, lwc, dist)
    plt.plot(
        mvd,
        lwc,
        "s",
        ms=10,
        fillstyle="none",
        label=f"Selected {distribution} RSS={rss_:.3f}",
    )
    plt.plot(
        13.7,
        0.3,
        "o",
        ms=10,
        fillstyle="none",
        label=f"NACA-RM-E53D23 Table I Langmuir E",
    )
    plt.plot(
        14.1,
        0.3,
        "o",
        ms=10,
        fillstyle="none",
        label=f"NACA-RM-E53D23 Table IV Langmuir E",
    )

    plt.xlim(0, 25)
    plt.ylim(0, 0.6)
    plt.xlabel("MVD")
    plt.ylabel("LWC")
    plt.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig("NACA-RM-53D23_mvd_lwc.png")

    ds = plt.np.logspace(log10(0.1 * 0.0254), log10(5 * 0.0254))
    inv_ks = [1 / langmuir_cylinder_values.calc_k(tk, u, mvd, d) for d in ds]
    ems_ = [
        langmuir_cylinder_values.calc_em_with_distribution_original(
            tk, p, u, mvd, d, dist
        )
        for d in ds
    ]

    plt.figure()
    plt.plot(inv_ks, ems_)

    plt.plot([1 / k for k in ks], ems, "o")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("1/K")
    plt.ylabel("Em")
    plt.tight_layout()
    plt.savefig("NACA-RM-53D23_fit.png")

    mc_langmuir = langmuir_blodgett_multicylinder.Multicylinder(
        cylinder_diameters, lengths_cyls
    )
    print(mc_langmuir.find_lwc_mvd_dist(tk, u, p, masses, icing_time, ice_density))
    mc_langmuir_k_phi_unique = langmuir_blodgett_multicylinder_k_phi_unique_mvd.Multicylinder(
        cylinder_diameters, lengths_cyls
    )
    print(
        mc_langmuir_k_phi_unique.find_lwc_mvd_dist(
            tk, u, p, masses, icing_time, ice_density
        )
    )

    plt.show()
