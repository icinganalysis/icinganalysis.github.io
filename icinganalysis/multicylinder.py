"""
reference:
Langmuir, Irving, and Blodgett, Katherine B.: A Mathematical Investigation of Water Droplet Trajectories.
Tech. Rep. No. 5418, Air Materiel Command, AAF, Feb. 19, 1946. (Contract No. W-33-038-ac-9151 with General Electric Co.)

Units:
tk: free-stream static temperature, K
p: air static pressure, Pa (N/m^2)
u: free-stream air speed, m/s
d_cylinder: cylinder diameter, m
d_drop: water drop diameter, micrometer (1e-6 m)
altitude: pressure altitude, m
"""
from math import log10, pi
from scipy.optimize import minimize
from icinganalysis import langmuir_cylinder
from icinganalysis.air_properties import calc_altitude

original_calc_em_with_distribution = langmuir_cylinder.calc_em_with_distribution
calc_em_with_distribution_to_use = langmuir_cylinder.calc_em_with_distribution


def calc_mass_average_em_diameter_with_distribution(
    initial_diameter,
    tk,
    p,
    u,
    lwc,
    mvd,
    time_in_icing=1,
    length=1,
    distribution="Langmuir A",
    ice_density=None,
    calc_em_with_distribution_to_use=calc_em_with_distribution_to_use
):
    final_diameter = initial_diameter
    prior_estimate_em = float("nan")  # note that this will force at least one iteration
    # print(distribution, lwc, mvd)
    for i in range(10):
        em_initial = calc_em_with_distribution_to_use(tk, p, u, mvd, initial_diameter, distribution)
        mass_initial = (em_initial * lwc / 1000 * u * initial_diameter * length * time_in_icing)
        em_final = calc_em_with_distribution_to_use(tk, p, u, mvd, final_diameter, distribution)
        mass_final = em_final * lwc / 1000 * u * final_diameter * length * time_in_icing
        mass = (mass_initial + mass_final) / 2
        if ice_density is None:
            volume = 0
        else:
            volume = mass / ice_density
        final_diameter = ((4 / pi * volume) + initial_diameter ** 2) ** 0.5
        average_diameter = (initial_diameter + final_diameter) / 2
        em_average = mass / (lwc / 1000 * u * average_diameter * length * time_in_icing)
        delta_em = abs(em_average - prior_estimate_em)
        if delta_em < 0.001:
            break
        prior_estimate_em = em_average
    else:
        raise ValueError(f"Poor convergence {delta_em}")
    return mass, em_average, average_diameter


class Multicylinder:
    def __init__(self, diameters, lengths=None, calc_em_with_distribution_to_use=calc_em_with_distribution_to_use):
        self.diameters = diameters
        if lengths is None:
            lengths = [1] * len(self.diameters)  # assume unit length
        self.lengths = lengths
        self.calc_em_with_distribution_to_use = calc_em_with_distribution_to_use

    def calc_ems_fixed_diameters(self, tk, ms, p, mvd, distribution="Langmuir A"):
        ems = []
        for d, length in zip(self.diameters, self.lengths):
            em = self.calc_em_with_distribution_to_use(tk, p, ms, mvd, d, distribution)
            ems.append(em)
        return ems

    def calc_masses_average_ems_diameters(
        self,
        tk,
        p,
        ms,
        lwc,
        mvd,
        time_in_icing=1,
        distribution="Langmuir A",
        ice_density=None,
    ):
        ems = []
        masses = []
        average_diameters = []
        for diameter, length in zip(self.diameters, self.lengths):
            (mass, em, dia,) = calc_mass_average_em_diameter_with_distribution(
                diameter,
                tk,
                p,
                ms,
                lwc,
                mvd,
                time_in_icing,
                length,
                distribution,
                ice_density,
                calc_em_with_distribution_to_use=self.calc_em_with_distribution_to_use
            )
            masses.append(mass)
            ems.append(em)
            average_diameters.append(dia)
        return masses, ems, average_diameters

    def find_lwc_mvd_from_dist(
        self,
        tk,
        ms,
        p,
        masses,
        time_in_icing=1,
        distribution="Langmuir A",
        ice_density=None,
    ):
        def f_log10_rss(x):
            mvd, lwc = x
            calculated_masses = []
            for diameter, length in zip(self.diameters, self.lengths):
                (mass, em, dia,) = calc_mass_average_em_diameter_with_distribution(
                    diameter,
                    tk,
                    p,
                    ms,
                    lwc,
                    mvd,
                    time_in_icing,
                    length,
                    distribution,
                    ice_density,
                    calc_em_with_distribution_to_use=self.calc_em_with_distribution_to_use
                )
                calculated_masses.append(mass)
            rss = (
                sum(
                    [
                        (log10(m1) - log10(m2)) ** 2
                        for m1, m2 in zip(masses, calculated_masses)
                        if m1 > 0 and m2 > 0
                    ]
                )
                ** 0.5
            )
            return rss

        mvd_lwc_solution = minimize(
            f_log10_rss, x0=(10, 0.5), bounds=[(1, 1000), (0.01, 10)]  # assumed x0
        )
        mvd, lwc = mvd_lwc_solution.x
        rss = f_log10_rss((mvd, lwc))
        if not mvd_lwc_solution.success:
            if rss > 1e-6:  # good enough, whether or not the solver thinks so...
                lwc, mvd, rss = float("nan"), float("nan"), float("nan")

        return lwc, mvd, rss

    def find_lwc_mvd_dist(
        self, tk, ms, p, masses, time_in_icing=1, ice_density=None, use_log_rss=True,
    ):
        distribution_results = []
        for dist in (
            "Langmuir A",
            "Langmuir B",
            "Langmuir C",
            "Langmuir D",
            "Langmuir E",
        ):
            distribution_results.append(
                (
                    self.find_lwc_mvd_from_dist(
                        tk, ms, p, masses, time_in_icing, dist, ice_density
                    ),
                    dist,
                )
            )
        distribution_results.sort(key=lambda _: _[0][-1])  # sort by rss values
        (lwc, mvd, rss), dist = distribution_results[
            0
        ]  # select the one with the lowest rss
        return lwc, mvd, dist, rss


def calc_k_phi(tk, p, u, drop_diameter_micrometer):  # equ. (50)
    k_phi = (
                2
                * langmuir_cylinder.calc_air_density(tk, p)
                * u
                * drop_diameter_micrometer
                / 1000000
                / 2
                / langmuir_cylinder.calc_air_viscosity(tk)
            ) ** 2
    return k_phi


table_X_data = {
    "em*lwc": (0.118, 0.0808, 0.0603, 0.025),  # g/m^3
    "average_dia_cm": (0.43, 2.6, 5.09, 15),
}

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from numpy import logspace

    print('Average cylinder diameters, inch: ', [_ / 2.54 for _ in table_X_data["average_dia_cm"]])  # page 379
    tk = 268  # page 381
    air_density = 1.101  # page 381
    u = 207 * 0.44704  # page 381
    ds = [_ / 100 for _ in table_X_data["average_dia_cm"]]  # page 379

    inv_ks = logspace(-2, 1)

    lengths = [0.1] * len(ds)  # page 379
    time_in_icing = 1  # second, unit of mass_rates
    ice_density = None  # suppress ice growth calculation, as average cylinder diameters were already determined
    mass_rates = [
        m / 1000 * u * d * l for m, d, l in zip(table_X_data["em*lwc"], ds, lengths)
    ]  # kg/s
    p = 1.101 / (0.3484 / 100 / tk)

    alt = calc_altitude(p)
    print("alt", alt, alt / 0.3048)
    mc = Multicylinder(ds, lengths)

    print("u", u)
    print("mass_rates", mass_rates)

    lwc, mvd, dist, rss = mc.find_lwc_mvd_dist(tk, u, p, mass_rates, time_in_icing, ice_density)
    k_phi = calc_k_phi(tk, p, u, mvd)
    d_cyl = [langmuir_cylinder.calc_d_cylinder_from_k(1 / inv_k, tk, u, mvd) for inv_k in inv_ks]
    ems = [langmuir_cylinder.calc_em(tk, p, u, mvd, d) for d in d_cyl]

    inv_kcs = [1 / langmuir_cylinder.calc_k(tk, u, mvd, d) for d in ds]
    apparent_ems = [m / lwc for m in table_X_data["em*lwc"]]
    print()
    print(f"Calculation with k*phi unique for each drop size bin\nMVD={mvd:.1f} {dist} Kφ(mvd)={k_phi:.0f}")
    print("apparent_ems", apparent_ems)

    plt.figure()
    plt.suptitle(
        f"Calculation with k*phi unique for each drop size bin\nMVD={mvd:.1f} a={mvd / 2:.2f} {dist} Kφ(mvd)={k_phi:.0f}")
    plt.plot(inv_ks, ems, label="calculated Em")
    plt.plot(
        inv_kcs,
        apparent_ems,
        "^",
        fillstyle="none",
        label="apparent Em based on measured mass, average diameter",
    )
    plt.xscale("log")
    plt.xlim(0.01, 1)
    plt.xlabel("1/K")
    plt.yscale("log")
    plt.ylim(0.1, 1)
    plt.ylabel("Em")
    plt.legend()
    plt.savefig('Calculation_with_k_phi_unique_for_each_drop_size_bin.png')

    #  "Monkey-patch" in the "calc_em_with_distribution_k_phi_mvd" method
    langmuir_cylinder.calc_em_with_distribution = langmuir_cylinder.calc_em_with_distribution_k_phi_mvd
    lwc, mvd, dist, rss = mc.find_lwc_mvd_dist(tk, u, p, mass_rates, time_in_icing, ice_density)
    k_phi = calc_k_phi(tk, p, u, mvd)
    d_cyl = [langmuir_cylinder.calc_d_cylinder_from_k(1 / inv_k, tk, u, mvd) for inv_k in inv_ks]
    ems = [langmuir_cylinder.calc_em(tk, p, u, mvd, d) for d in d_cyl]

    inv_kcs = [1 / langmuir_cylinder.calc_k(tk, u, mvd, d) for d in ds]
    apparent_ems = [m / lwc for m in table_X_data["em*lwc"]]
    print()
    print(f"Calculation with k*phi(mvd)=constant\nMVD={mvd:.1f} {dist} Kφ(mvd)={k_phi:.0f}")
    print("apparent_ems", apparent_ems)

    plt.figure()
    plt.suptitle(f"Calculation with k*phi(mvd)=constant\nMVD={mvd:.1f} a={mvd / 2:.2f} {dist} Kφ(mvd)={k_phi:.0f}")
    plt.plot(inv_ks, ems, label="calculated Em")
    plt.plot(
        inv_kcs,
        apparent_ems,
        "^",
        fillstyle="none",
        label="apparent Em based on measured mass, average diameter",
    )
    plt.xscale("log")
    plt.xlim(0.01, 1)
    plt.xlabel("1/K")
    plt.yscale("log")
    plt.ylim(0.1, 1)
    plt.ylabel("Em")
    plt.legend()
    plt.savefig('Calculation_with_k_phi_constant_for_each_drop_size_bin.png')

    plt.figure()
    plt.plot(table_X_data["average_dia_cm"], table_X_data["em*lwc"], 'o', label='Data from Cunningham')
    plt.xscale('log')
    plt.xlim(.1, 100)
    plt.xlabel('Cylinder average diameter, cm')
    plt.ylabel('Em*LWC, g/m^3')
    plt.ylim(.01, 1)
    plt.yscale('log')
    plt.legend()
    plt.savefig('Cunningham_data.png')

    plt.figure()
    k_phi = 10000
    mvd = langmuir_cylinder.calc_drop_diameter_micrometer_from_re_drop(k_phi ** 0.5, tk, p, u)
    d_cyl = [langmuir_cylinder.calc_d_cylinder_from_k(1 / inv_k, tk, u, mvd) for inv_k in inv_ks]
    for dist in (
        "Langmuir A",
        "Langmuir B",
        "Langmuir C",
        "Langmuir D",
        "Langmuir E",
    ):
        ems = [langmuir_cylinder.calc_em_with_distribution(tk, p, u, mvd, d, dist) for d in d_cyl]
        plt.plot(inv_ks, ems, label=f'Kφ(mvd)={k_phi:.0f} {dist}')
    plt.xscale('log')
    plt.xlim(.01, 10)
    plt.xlabel('1/K')
    plt.ylabel('Em')
    plt.ylim(.01, 1)
    plt.yscale('log')
    plt.legend()
    plt.savefig('k_phi_10000.png')

    plt.show()
