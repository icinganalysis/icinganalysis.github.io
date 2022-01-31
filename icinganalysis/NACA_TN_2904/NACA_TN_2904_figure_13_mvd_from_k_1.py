from icinganalysis.air_properties import calc_pressure
from icinganalysis import langmuir_cylinder
from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement, multicylinder_naca_tn_2904


def c1(d_inch, mph, mvd, tk):
    mu_slug_ft_s = langmuir_cylinder.calc_air_viscosity(tk) / 14.5939 * 0.3048
    k = 4.088e-11 * (mvd**2*mph/mu_slug_ft_s/d_inch)
    return k


def d_inch_c1_from(k, mph, mvd, tk):
    mu_slug_ft_s = langmuir_cylinder.calc_air_viscosity(tk) / 14.5939 * 0.3048
    d_inch = 4.088e-11 * (mvd**2*mph/mu_slug_ft_s/k)
    return d_inch


def mvd_c1_from(k, l_inch, mph, tk):
    mu_slug_ft_s = langmuir_cylinder.calc_air_viscosity(tk) / 14.5939 * 0.3048
    mvd = (k / (4.088e-11 * (mph/mu_slug_ft_s/(2*l_inch))))**0.5
    return mvd


def calc_mvd_from_inv_k_for_L_1_inch(inv_k_for_L_1_inch, tk, u):
    mvd = langmuir_cylinder.calc_d_drop_from_k(1 / inv_k_for_L_1_inch, tk, u,
                                               2 * 1 * 0.0254,  # D = 2 * L * m/inch
                                               )
    return mvd


def calc_lwc_masses_to_match_total_mass(masses, d_cyls, length_cyls, tk, p, u, mvd, distribution="Langmuir A",
                                        time_in_icing=1):
    ems = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        distribution) for d in d_cyls]
    masses_calc = [1 / 1000 * em * u * time_in_icing * d * l for d, l, em in zip(d_cyls, length_cyls, ems)]
    lwc = sum(masses) / sum(masses_calc)
    masses_calc = [lwc / 1000 * em * u * time_in_icing * d * l for d, l, em in zip(d_cyls, length_cyls, ems)]
    return lwc, masses_calc


def get_data(inv_k_for_L_1_inch, masses, d_cyls, length_cyls, tk, p, u, distribution="Langmuir A"):
    mvd = calc_mvd_from_inv_k_for_L_1_inch(inv_k_for_L_1_inch, tk, u)
    lwc, masses_calc = calc_lwc_masses_to_match_total_mass(masses, d_cyls, length_cyls, tk, p, u, mvd, distribution)
    rss = multicylinder_naca_tn_2904.calc_rss_log_diff(masses, masses_calc)
    return lwc, mvd, rss


if __name__ == '__main__':

    # Figure 11 data
    em_lwcs = 0.0297, 0.0269, 0.0226, 0.0163
    d_cyls_inch = 0.125, 0.5, 1.25, 3
    d_cyls = [_ * 0.0254 for _ in d_cyls_inch]
    lengths_cyls = [1] * len(d_cyls)

    alt_ft = 10000
    tk = (9 + 459.67) / 1.8
    p = calc_pressure(alt_ft * 12 * 0.0254)
    mph = 200
    u = mph * 0.44704
    masses = [eml / 1000 * d * 0.0254 ** -2 for d, eml in zip(d_cyls, em_lwcs)]
    mass_ramp_up_ratios = 0.95, 0.9833, 1.0167, 1.05

    data = (
        ("Langmuir A", 0.165, [mass * ratio for mass, ratio in zip(masses, mass_ramp_up_ratios)]),
        ("Langmuir B", 0.210, masses),
        ("Langmuir E", 0.25, [mass * ratio for mass, ratio in zip(masses, reversed(mass_ramp_up_ratios))]),
    )

    for distribution, inv_k_for_L_1_inch_nominal, masses in data:
        lwc, mvd, rss = get_data(inv_k_for_L_1_inch_nominal, masses, d_cyls, lengths_cyls, tk, p, u, distribution)
        mvd_c1 = mvd_c1_from(1/inv_k_for_L_1_inch_nominal, 1, mph, tk)
        print(f"{lwc:.2f} {mvd_c1:.1f} {mvd:.1f} {rss:.3f} {sum(masses):.4f}")
