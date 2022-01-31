"""
reference:
NACA-TN-2904

Units:
tk: free-stream static temperature, K
p: air static pressure, Pa (N/m^2)
u: free-stream air speed, m/s
d_cylinder: cylinder diameter, m
d_drop: water drop diameter, micrometer (1e-6 m)
altitude: pressure altitude, m
"""
from math import log10, pi
from scipy.optimize import minimize, minimize_scalar
from icinganalysis import langmuir_cylinder
from icinganalysis.NACA_TN_2904.NACA_TN_2904_impingement import calc_em_from
from icinganalysis.air_properties import calc_altitude
from icinganalysis.langmuir_cylinder import calc_k, valid_distribution_ids

original_calc_em_with_distribution = calc_em_from
calc_em_with_distribution_to_use = calc_em_from


def calc_mass_average_em_diameter_with_distribution(initial_diameter, tk, p, u, lwc, mvd, time_in_icing=1, length=1,
                                                    distribution="Langmuir A", ice_density=None,
                                                    constrained_k_phi=None):
    final_diameter = initial_diameter
    prior_estimate_em = float("nan")  # note that this will force at least one iteration
    for i in range(10):
        if constrained_k_phi is None:
            k_phi = calc_k_phi(tk, p, u, mvd)
        else:
            k_phi = constrained_k_phi
        em_initial = calc_em_from(calc_k(tk, u, mvd, initial_diameter), k_phi,
                                                      distribution)
        mass_initial = (em_initial * lwc / 1000 * u * initial_diameter * length * time_in_icing)
        em_final = calc_em_from(calc_k(tk, u, mvd, initial_diameter), k_phi,
                                                    distribution)
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
        return float('nan'), float('nan'), float('nan')
        # raise ValueError(f"Poor convergence {delta_em}")
    return mass, em_average, average_diameter


def calc_rss_log_diff(masses, masses_1):
    vs = (sum(
        [
            (log10(m1) - log10(m2)) ** 2
            for m1, m2 in zip(masses, masses_1)
            if m1 > 0 and m2 > 0
        ]
    )
          ** 0.5)
    if not vs:  # no case with m1 > 0 and m2 > 0
        rss = float('nan')  # rss undefined
    else:  # at least one case with m1 > 0 and m2 > 0
        rss = (  # can evaluate the comparison
            sum(
                [
                    (log10(m1) - log10(m2)) ** 2
                    for m1, m2 in zip(masses, masses_1)
                    if m1 > 0 and m2 > 0
                ]
            )
            ** 0.5
        )
    return rss


class Multicylinder:
    def __init__(self, diameters, lengths=None):
        self.diameters = diameters
        if lengths is None:
            lengths = [1] * len(self.diameters)  # assume unit length
        self.lengths = lengths
        self.calc_em_with_distribution_to_use = calc_em_from

    def calc_ems_fixed_diameters(self, tk, ms, p, mvd, distribution="Langmuir A"):
        ems = []
        for d, length in zip(self.diameters, self.lengths):

            # k = calc_k(tk, ms, mvd, d)
            # k_phi = calc_k_phi(tk, p, ms, mvd)



            em = self.calc_em_with_distribution_to_use(calc_k(tk, ms, mvd, d), calc_k_phi(tk, p, ms, mvd), distribution)


            # print('     mvd, k, k_phi, em', mvd, k, k_phi, em)


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
        constrained_k_phi=None,
    ):
        ems = []
        masses = []
        average_diameters = []
        for diameter, length in zip(self.diameters, self.lengths):
            (mass, em, dia,) = calc_mass_average_em_diameter_with_distribution(diameter, tk, p, ms, lwc, mvd,
                                                                               time_in_icing, length, distribution,
                                                                               ice_density,
                                                                               constrained_k_phi=constrained_k_phi)
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
        constrained_k_phi=None,
        guess_lwc=0.5,
        guess_mvd=10,
    ):
        def f_log10_rss(x):
            mvd, lwc = x
            calculated_masses = []
            for diameter, length in zip(self.diameters, self.lengths):
                (mass, em, dia,) = calc_mass_average_em_diameter_with_distribution(diameter, tk, p, ms, lwc, mvd,
                                                                                   time_in_icing, length, distribution,
                                                                                   ice_density,
                                                                                   constrained_k_phi=constrained_k_phi)
                calculated_masses.append(mass)
            rss = calc_rss_log_diff(masses, calculated_masses)
            return rss


        mvd_lwc_solution = minimize(
            f_log10_rss, x0=(guess_mvd, guess_lwc), bounds=[(1, 1000), (0.01, 10)]  # assumed x0
        )
        mvd, lwc = mvd_lwc_solution.x
        rss = f_log10_rss((mvd, lwc))
        if not mvd_lwc_solution.success:
            lwc, mvd, rss = self.alternative_find_lwc_mvd_from_dist(
                tk, ms, p, masses, time_in_icing, distribution, ice_density,
                constrained_k_phi,guess_lwc, guess_mvd
            )

        if rss != rss:  # float('nan')
            lwc, mvd, rss = float("nan"), float("nan"), float("nan")

        elif not mvd_lwc_solution.success:
            # lwc, mvd, rss = float("nan"), float("nan"), float("nan")
            if rss > 1:  # good enough, whether or not the solver thinks so...
                lwc, mvd, rss = float("nan"), float("nan"), float("nan")

        return lwc, mvd, rss

    def alternative_find_lwc_mvd_from_dist(
        self,
        tk,
        ms,
        p,
        masses,
        time_in_icing=1,
        distribution="Langmuir A",
        ice_density=None,
        constrained_k_phi=None,
        guess_lwc=0.5,
        guess_mvd=10,
    ):
        def f_log10_rss(mvd):
            lwc = 1
            calculated_masses = []
            # print(tk, ms, p, mvd, distribution)
            ems = self.calc_ems_fixed_diameters(tk, ms, p, mvd, distribution)
            for diameter, length, em in zip(self.diameters, self.lengths, ems):
                mass = em * lwc / 1000 * ms * time_in_icing * diameter * length
                calculated_masses.append(mass)
            # print(calculated_masses)
            lwc = sum(masses) / sum(calculated_masses)
            calculated_masses = [lwc*_ for _ in calculated_masses]
            rss = calc_rss_log_diff(masses, calculated_masses)
            # print('    ', mvd, lwc, rss)
            return rss


        mvd_solution = minimize_scalar(
            f_log10_rss, bounds=(1, 1000), method='Bounded'  # assumed x0
        )
        mvd = mvd_solution.x

        calc_masses, _, _ = self.calc_masses_average_ems_diameters(
            tk, p, ms, 1, mvd, time_in_icing, distribution, ice_density, constrained_k_phi
        )
        lwc = sum(masses) / sum(calc_masses)
        calc_masses = [lwc * _ for _ in calc_masses]
        rss = calc_rss_log_diff(masses, calc_masses)

        if rss != rss:  # float('nan')
            lwc, mvd, rss = float("nan"), float("nan"), float("nan")

        elif not mvd_solution.success:
            # lwc, mvd, rss = float("nan"), float("nan"), float("nan")
            if rss > 1:  # good enough, whether or not the solver thinks so...
                lwc, mvd, rss = float("nan"), float("nan"), float("nan")

        return lwc, mvd, rss


    def find_lwc_mvd_dist(
        self, tk, ms, p, masses, time_in_icing=1, ice_density=None,
        constrained_k_phi=None,
        guess_lwc=0.5,
        guess_mvd=10,
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
                        tk, ms, p, masses, time_in_icing, dist, ice_density,
                        constrained_k_phi=constrained_k_phi,
                        guess_lwc=guess_lwc,
                        guess_mvd=guess_mvd,
                    ),
                    dist,
                )
            )
        distribution_results.sort(key=lambda _: _[0][-1])  # sort by rss values
        (lwc, mvd, rss), dist = distribution_results[
            0
        ]  # select the one with the lowest rss
        return lwc, mvd, dist, rss

    def find_lwc_mvd_dist_all_sorted(
        self, tk, ms, p, masses, time_in_icing=1, ice_density=None,
        constrained_k_phi=None,
        guess_lwc=0.5,
        guess_mvd=10,
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
                        tk, ms, p, masses, time_in_icing, dist, ice_density,
                        constrained_k_phi=constrained_k_phi,
                        guess_lwc=guess_lwc,
                        guess_mvd=guess_mvd,
                    ),
                    dist,
                )
            )
        distribution_results.sort(key=lambda _: _[0][-1])  # sort by rss values

        rows = []
        for (lwc, mvd, rss), dist in distribution_results:
            rows.append((lwc, mvd, dist, rss))
        cols = tuple(zip(*rows))
        return cols


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
    # plt.xlim(0.01, 1)
    plt.xlabel("1/K")
    plt.yscale("log")
    plt.ylim(0.1, 1)
    plt.ylabel("Em")
    plt.legend()
    plt.savefig('Calculation_with_k_phi_unique_for_each_drop_size_bin.png')

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
    for dist in valid_distribution_ids:
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
