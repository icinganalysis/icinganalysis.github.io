import matplotlib.pyplot as plt
from icinganalysis import multicylinder
from icinganalysis import langmuir_cylinder
from icinganalysis import NACA_TR_1215_impingement
from icinganalysis import multicylinder_naca_tr_1215

if __name__ == "__main__":

    # Figure 11
    em_lwcs = 0.0295, 0.0267, 0.0226, 0.0163
    d_cyls_inch = 0.125, 0.5, 1.25, 3
    d_cyls = [_ * 0.0254 for _ in d_cyls_inch]

    plt.figure(figsize=(5.3, 7.3))
    plt.plot(em_lwcs, d_cyls_inch, 'o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    plt.xlim(.001, .1)
    plt.ylim(.1, 100)
    plt.tight_layout()
    plt.savefig('naca_tn_2904_fig11_overlay.png', transparent=True)

    print(em_lwcs)

    mph = 200
    alt_ft = 10000
    tk = (9 + 459.67) / 1.8
    u = mph * 0.44704
    p = langmuir_cylinder.calc_pressure(alt_ft * 12 * 0.0254)
    mvd = 20
    distribution = "Langmuir B"

    k = langmuir_cylinder.calc_k(tk, u, mvd, 2*0.0254)
    print('k, 1/k', k, 1/k)

    k_phi = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    print('k_phi', k_phi)
    cdx = langmuir_cylinder.calc_d_cylinder_from_k(1, tk, u, mvd)
    print(cdx, cdx / 0.0254)

    d_cyl_m_k_1 = 10.1 * 0.0254
    mvdx = langmuir_cylinder.calc_d_drop_from_k(1, tk, u, d_cyl_m_k_1)
    print(mvdx)

    ems_lang_b = [NACA_TR_1215_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        "Langmuir B",
    ) for d in d_cyls]

    # ems_lang_b = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, "Langmuir B") for d in d_cyls]
    print(ems_lang_b)
    lwc = 0.55
    ems_lang_b_lwc_u_sq_inch_table_iii = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    print('ems_lang_b*lwc_u_sq_inch', ems_lang_b_lwc_u_sq_inch_table_iii)

    plt.figure()
    plt.suptitle(f'Nominal case MVD={mvd:.1f} LWC={lwc:.2f} {distribution}')
    plt.plot(em_lwcs, d_cyls_inch, 'o', label='Figure 11 data')
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    print('min(ds)', min(ds), min(d_cyls))
    ds_inch = [_ / 0.0254 for _ in ds]
    ems_lang_b = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, "Langmuir B") for d
                  in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    ems_lang_b_lwc_u_sq_inch_nominal = ems_lang_b_lwc_u_sq_inch
    plt.plot(ems_lang_b_lwc_u_sq_inch_nominal, ds_inch, label="Em calculated from\nFigure 6 interpolation")
    ems_lang_b = [langmuir_cylinder.calc_em_with_distribution(tk, p, u, mvd, d, "Langmuir B") for d in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, '--', label="Em calculated from\nLangmuir-Blodgett data interpolation")
    ems_lang_b = [NACA_TR_1215_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        "Langmuir B",
    ) for d in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, ':', label="Em calculated from\nTable IV interpolation")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    plt.xlim(.01, .06)
    plt.ylim(.1, 4)
    plt.grid(which='both')
    plt.legend(
        # loc='lower left'
    )
    plt.tight_layout()

    masses = [em_lwc * d for d, em_lwc in zip(d_cyls, em_lwcs)]
    masses = [em_lwc_u * d / 1000 * 0.0254 ** -2 for d, em_lwc_u in zip(d_cyls, em_lwcs)]
    print(masses)
    mc2 = multicylinder_naca_tr_1215.Multicylinder(d_cyls)
    vs = mc2.find_lwc_mvd_from_dist(tk, u, p, masses, distribution="Langmuir B")
    print(vs)
    vs = mc2.find_lwc_mvd_dist(tk, u, p, masses)
    print(vs)

    ds = plt.np.logspace(0.1 * min(d_cyls), 1.1 * max(d_cyls))
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    print('min(ds)', min(ds), min(d_cyls))
    ds_inch = [_ / 0.0254 for _ in ds]
    print(ds_inch[0], ds_inch[-1])

    mc = multicylinder.Multicylinder(d_cyls)
    lwc_lang, mvd_lang, best_distribution, rss = mc.find_lwc_mvd_dist(tk, u, p, masses)
    k_phi = multicylinder.calc_k_phi(tk, p, u, mvd_lang)
    print(lwc_lang, mvd_lang, best_distribution, rss, k_phi)
    lb_ems_lwcs = [
        langmuir_cylinder.calc_em_with_distribution(tk, p, u, mvd_lang, d,
                                                    best_distribution) * lwc_lang * u * 0.0254 ** 2 for
        d in ds]

    mc2 = multicylinder_naca_tr_1215.Multicylinder(d_cyls)
    lwc2, mvd2, best_distribution2, rss2 = mc2.find_lwc_mvd_dist(tk, u, p, masses)
    k_phi2 = multicylinder.calc_k_phi(tk, p, u, mvd2)
    print(lwc2, mvd2, best_distribution2, rss2, k_phi2)
    naca_ems_lwcs = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd2, d,
                                                                                     best_distribution2) * lwc2 * u * 0.0254 ** 2
                     for d in ds]

    em_lwcs_ramped_down = [m * em_lwc for m, em_lwc in zip((1.05, 1.0167, 0.9833, 0.95), em_lwcs)]
    em_lwcs_ramped_up = [m * em_lwc for m, em_lwc in zip((0.95, 0.9833, 1.0167, 1.05), em_lwcs)]
    # em_lwcs_ramped_down = [m * em_lwc for m, em_lwc in zip((1.05, 1., 1., 0.95), em_lwcs)]
    # em_lwcs_ramped_up = [m * em_lwc for m, em_lwc in zip((0.95, 1., 1., 1.05), em_lwcs)]
    masses_ramped_down = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_down)]
    masses_ramped_up = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_up)]
    lwc_ramped_up, mvd_ramped_up, best_distribution_ramped_up, rss = mc.find_lwc_mvd_dist(tk, u, p, masses_ramped_up)
    lb_ems_lwcs_ramped_up = [langmuir_cylinder.calc_em_with_distribution(tk, p, u, mvd_ramped_up, d,
                                                                         best_distribution_ramped_up) * lwc_ramped_up * u * 0.0254 ** 2
                             for d in ds]
    lwc_ramped_down, mvd_ramped_down, best_distribution_ramped_down, rss = mc.find_lwc_mvd_dist(tk, u, p,
                                                                                                masses_ramped_down)
    lb_ems_lwcs_ramped_down = [langmuir_cylinder.calc_em_with_distribution(tk, p, u, mvd_ramped_down, d,
                                                                           best_distribution_ramped_down) * lwc_ramped_down * u * 0.0254 ** 2
                               for d in ds]

    lwc2_ramped_down, mvd2_ramped_down, best_distribution2_ramped_down, rss2 = mc2.find_lwc_mvd_dist(tk, u, p,
                                                                                                     masses_ramped_down)
    naca_ems_lwcs_ramped_down = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd2_ramped_down, d,
                                                                        best_distribution2_ramped_down) * lwc2_ramped_down * u * 0.0254 ** 2
        for d in ds]
    lwc2_ramped_up, mvd2_ramped_up, best_distribution2_ramped_up, rss2 = mc2.find_lwc_mvd_dist(tk, u, p,
                                                                                               masses_ramped_up)
    naca_ems_lwcs_ramped_up = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd2_ramped_up, d,
                                                                        best_distribution2_ramped_up) * lwc2_ramped_up * u * 0.0254 ** 2
        for d in ds]

    # plt.figure(figsize=(5.25, 7.2))
    plt.figure(figsize=(9, 7.2))
    k_phi_calc = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    plt.suptitle(f'Nominal case MVD={mvd:.1f} LWC={lwc:.2f} {distribution}')
    plt.plot(em_lwcs, d_cyls_inch, 'o', label=f'Figure 11 data')
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    print('min(ds)', min(ds), min(d_cyls))
    ds_inch = [_ / 0.0254 for _ in ds]
    ems_lang_b = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, "Langmuir B") for d
                  in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    ems_lang_b_lwc_u_sq_inch_nominal = ems_lang_b_lwc_u_sq_inch
    plt.plot(ems_lang_b_lwc_u_sq_inch_nominal, ds_inch, label=f"Nominal\nMVD={mvd:.1f} LWC={lwc:.3f} Langmuir B")

    ems_lang_b_lwc_u_sq_inch_table_iii = [NACA_TR_1215_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        "Langmuir B",
    ) * lwc * u * 0.0254 ** 2 for d in ds]
    plt.plot(ems_lang_b_lwc_u_sq_inch_table_iii, ds_inch, '--', lw=1, label=f"Nominal with Table IV data\nMVD={mvd:.1f} LWC={lwc:.3f} Langmuir B")

    lwc2b, mvd2b, rss2b = mc2.find_lwc_mvd_from_dist(tk, u, p, masses, distribution="Langmuir B")
    naca_ems_lwcs_b = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(
            tk, p, u, mvd2b, d, "Langmuir B")
        * lwc2b * u * 0.0254 ** 2 for d in ds
    ]
    k_phi_2b = langmuir_cylinder.calc_k_phi(tk, p, u, mvd2b)
    k_phi_2 = langmuir_cylinder.calc_k_phi(tk, p, u, mvd2)
    # plt.plot(naca_ems_lwcs_b, ds_inch, label=f"NACA method best\nMVD={mvd2b:.1f} LWC={lwc2b:.3f} Langmuir B")
    # plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(
        loc='lower left'
    )
    plt.tight_layout()
    plt.savefig("naca_tn_2904_fig_13_nominals.png", transparent=True)

    plt.figure(figsize=(7.05, 7.2))
    k_phi_calc = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    plt.suptitle(f'Nominal case MVD={mvd:.1f} LWC={lwc:.2f} {distribution}')
    plt.plot(em_lwcs, d_cyls_inch, 'o', label=f'Figure 11 data')
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    print('min(ds)', min(ds), min(d_cyls))
    ds_inch = [_ / 0.0254 for _ in ds]
    ems_lang_b = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, "Langmuir B") for d
                  in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    ems_lang_b_lwc_u_sq_inch_nominal = ems_lang_b_lwc_u_sq_inch
    plt.plot(ems_lang_b_lwc_u_sq_inch_nominal, ds_inch, label=f"Nominal\nMVD={mvd:.1f} LWC={lwc:.3f} Langmuir B")

    lwc2b, mvd2b, rss2b = mc2.find_lwc_mvd_from_dist(tk, u, p, masses, distribution="Langmuir B")
    naca_ems_lwcs_b = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(
            tk, p, u, mvd2b, d, "Langmuir B")
        * lwc2b * u * 0.0254 ** 2 for d in ds
    ]
    k_phi_2b = langmuir_cylinder.calc_k_phi(tk, p, u, mvd2b)
    k_phi_2 = langmuir_cylinder.calc_k_phi(tk, p, u, mvd2)
    plt.plot(naca_ems_lwcs_b, ds_inch, label=f"NACA method best\nMVD={mvd2b:.1f} LWC={lwc2b:.3f} Langmuir B")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.001, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(
        loc='lower left'
    )
    plt.tight_layout()
    plt.savefig("naca_tn_2904_fig_13_nominal_bests.png", transparent=True)

    plt.figure(figsize=(9, 7.2))
    k_phi_calc = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    plt.suptitle(f'Nominal case MVD={mvd:.1f} LWC={lwc:.2f} {distribution}')
    plt.plot(em_lwcs, d_cyls_inch, 'o', label=f'Figure 11 data')
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    print('min(ds)', min(ds), min(d_cyls))
    ds_inch = [_ / 0.0254 for _ in ds]
    ems_lang_b = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, "Langmuir B") for d
                  in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_lang_b]
    ems_lang_b_lwc_u_sq_inch_nominal = ems_lang_b_lwc_u_sq_inch
    plt.plot(ems_lang_b_lwc_u_sq_inch_nominal, ds_inch, label=f"Nominal\nMVD={mvd:.1f} LWC={lwc:.3f} Langmuir B")

    lwc2b, mvd2b, rss2b = mc2.find_lwc_mvd_from_dist(tk, u, p, masses, distribution="Langmuir B")
    naca_ems_lwcs_b = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(
            tk, p, u, mvd2b, d, "Langmuir B")
        * lwc2b * u * 0.0254 ** 2 for d in ds
    ]
    k_phi_2b = langmuir_cylinder.calc_k_phi(tk, p, u, mvd2b)
    k_phi_2 = langmuir_cylinder.calc_k_phi(tk, p, u, mvd2)
    plt.plot(naca_ems_lwcs_b, ds_inch, label=f"NACA method best\nMVD={mvd2b:.1f} LWC={lwc2b:.3f} Langmuir B")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(
        loc='lower left'
    )
    plt.tight_layout()
    plt.savefig("naca_tn_2904_fig_13_nominal_bests2.png", transparent=True)

    plt.figure(figsize=(9, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o')
    plt.plot(ems_lang_b_lwc_u_sq_inch_nominal, ds_inch, "-",
             label=f"NACA Nominal\nMVD={20:.1f} LWC={0.55:.3f} Langmuir B")
    plt.plot(lb_ems_lwcs, ds_inch, '--',
             label=f"Langmuir method best\nMVD={mvd_lang:.1f} LWC={lwc_lang:.3f} {best_distribution}")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")

    # plt.plot(lb_ems_lwcs_ramped_up, ds_inch,
    #          label=f"Calculated Langmuir method best\nMVD={mvd_ramped_up:.1f} LWC={lwc_ramped_up:.3f} {best_distribution_ramped_up}")
    # plt.plot(lb_ems_lwcs_ramped_down, ds_inch,
    #          label=f"Calculated Langmuir method best\nMVD={mvd_ramped_down:.1f} LWC={lwc_ramped_down:.3f} {best_distribution_ramped_down}")
    # plt.plot(naca_ems_lwcs_ramped_down, ds_inch,
    #          label=f"NACA method best\nMVD={mvd2_ramped_down:.1f} LWC={lwc2_ramped_down:.3f} {best_distribution2_ramped_down}")
    # plt.plot(naca_ems_lwcs_ramped_up, ds_inch,
    #          label=f"NACA method best\nMVD={mvd2_ramped_up:.1f} LWC={lwc2_ramped_up:.3f} {best_distribution2_ramped_up}")

    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .5)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend()
    plt.savefig('naca_tn_2904_fig13a.png', transparent=True)

    plt.figure(figsize=(8, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(naca_ems_lwcs_ramped_up, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_up:.1f} LWC={lwc2_ramped_up:.3f} {best_distribution2_ramped_up}")
    plt.plot(lb_ems_lwcs_ramped_up, ds_inch, '--',
             label=f"Calculated Langmuir method best\nMVD={mvd_ramped_up:.1f} LWC={lwc_ramped_up:.3f} {best_distribution_ramped_up}")
    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .52)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='center right')
    plt.savefig('naca_tn_2904_fig13b.png', transparent=True)

    plt.figure(figsize=(8, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(naca_ems_lwcs_ramped_down, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_down:.1f} LWC={lwc2_ramped_down:.3f} {best_distribution2_ramped_down}")
    plt.plot(lb_ems_lwcs_ramped_down, ds_inch, '--',
             label=f"Langmuir method best\nMVD={mvd_ramped_down:.1f} LWC={lwc_ramped_down:.3f} {best_distribution_ramped_down}")
    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .1)
    plt.xlim(.004, .5)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='center right')
    plt.savefig('naca_tn_2904_fig13c.png', transparent=True)

    plt.figure(figsize=(8, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(naca_ems_lwcs_ramped_up, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_up:.1f} LWC={lwc2_ramped_up:.3f} {best_distribution2_ramped_up}")
    plt.plot(naca_ems_lwcs_ramped_down, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_down:.1f} LWC={lwc2_ramped_down:.3f} {best_distribution2_ramped_down}")
    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .1)
    plt.xlim(.004, .5)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='center right')
    plt.savefig('naca_tn_2904_fig13.png', transparent=True)

    plt.figure()
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.plot(naca_ems_lwcs_ramped_up, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_up:.1f} LWC={lwc2_ramped_up:.3f} {best_distribution2_ramped_up}")
    plt.plot(naca_ems_lwcs_ramped_down, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_down:.1f} LWC={lwc2_ramped_down:.3f} {best_distribution2_ramped_down}")
    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .1)
    plt.xlim(.004, .5)
    plt.ylim(.1, 10)
    plt.xlim(.01, .04)
    plt.ylim(.1, 4)
    plt.grid(which='both')
    plt.legend(loc='best')
    plt.savefig('naca_tn_2904_fig13_zoom.png', transparent=True)

    plt.figure()
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(lb_ems_lwcs, ds_inch, '-',
             label=f"Langmuir method best\nMVD={mvd_lang:.1f} LWC={lwc_lang:.3f} {best_distribution}")
    plt.plot(lb_ems_lwcs_ramped_up, ds_inch, '-',
             label=f"Langmuir method best\nMVD={mvd_ramped_up:.1f} LWC={lwc_ramped_up:.3f} {best_distribution_ramped_up}")
    plt.plot(lb_ems_lwcs_ramped_down, ds_inch, '-',
             label=f"Langmuir method best\nMVD={mvd_ramped_down:.1f} LWC={lwc_ramped_down:.3f} {best_distribution_ramped_down}")
    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .1)
    plt.xlim(.004, .5)
    plt.ylim(.1, 10)
    plt.xlim(.01, .04)
    plt.ylim(.1, 4)
    plt.grid(which='both')
    plt.legend(loc='best')
    plt.savefig('naca_tn_2904_fig13_zoom_lb.png', transparent=True)

    mvdp = (mvd_ramped_down - mvd_lang) / mvd_lang
    mvdm = (mvd_ramped_up - mvd_lang) / mvd_lang
    lwcp = (lwc_ramped_down - lwc_lang) / lwc_lang
    lwcm = (lwc_ramped_up - lwc_lang) / lwc_lang
    print(mvdp, lwcp)
    print(mvdm, lwcm)

    plt.figure()
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(naca_ems_lwcs, ds_inch, label=f"NACA method best\nMVD={mvd2:.1f} LWC={lwc2:.3f} {best_distribution2}")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', ms=10, mew=2, label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(naca_ems_lwcs_ramped_down, ds_inch,
             label=f"NACA method best\nMVD={mvd2_ramped_down:.1f} LWC={lwc2_ramped_down:.3f} {best_distribution2_ramped_down}")
    plt.plot(lb_ems_lwcs_ramped_down, ds_inch, '--',
             label=f"Calculated Langmuir method best\nMVD={mvd_ramped_down:.1f} LWC={lwc_ramped_down:.3f} {best_distribution_ramped_down}")
    plt.xscale('log')
    plt.xlim(0.01, 0.04)
    plt.yscale('log')
    plt.ylim(.1, 4)
    plt.xlim(.004, .1)
    plt.xlim(.01, .04)
    plt.ylim(.1, 4)
    plt.grid(which='both')
    plt.legend(loc='best')
    plt.savefig('naca_tn_2904_fig13c_zoom.png', transparent=True)

    plt.figure()
    print(mvd)
    lwc = .355
    distribution = "Langmuir B"
    # lb_ems_lwcs = [langmuir_cylinder.calc_em_with_distribution(tk, p, u, mvd_lang, d, best_distribution)*lwc_lang/1000*u for d in ds]
    ems_naca = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) * lwc / 1000 * u
        for d in ds]
    emx_naca = [NACA_TR_1215_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        distribution=distribution,
    ) * lwc / 1000 * u for d in ds]
    plt.plot(em_lwcs, d_cyls_inch, 's', label='Figure 11 data')
    plt.plot(ems_naca, ds_inch, label='Nominal NACA Langmuir B MVD=20 LWC=0.355')
    plt.plot(emx_naca, ds_inch, label='NACA Langmuir B MVD=20 LWC=0.355')
    masses = [em_lwc * d for d, em_lwc in zip(d_cyls, em_lwcs)]
    lwc2, mvd2, rss2 = mc2.find_lwc_mvd_from_dist(tk, u, p, masses, distribution=distribution)
    ems_naca_best_b = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) * lwc / 1000 * u
        for d in ds]

    plt.xscale('log')
    # plt.xlim(0.01, 0.04)
    plt.yscale('log')
    # plt.ylim(.1, 4)
    plt.grid(which='both')
    plt.legend()

    langs = {
        'Langmuir A': 'ems_a',
        'Langmuir B': 'ems_b',
        'Langmuir C': 'ems_c',
        'Langmuir D': 'ems_d',
        'Langmuir E': 'ems_e',
    }

    # plt.figure(figsize=(5, 7.4))
    plt.figure(figsize=(9.4, 7.2))
    k_phi = 10000
    d_cyl_inch_k_1 = 11.7
    d_cyl_m_k_1 = 11.7 * 0.0254
    mvd = langmuir_cylinder.calc_d_drop_from_k(1, tk, u, d_cyl_m_k_1)
    mvdx = langmuir_cylinder.calc_drop_diameter_micrometer_from_re_drop(k_phi ** 0.5, tk, p, u)
    print(mvd, mvdx)
    k_phix = langmuir_cylinder.calc_k_phi(tk, p, u, mvdx)
    k_phiy = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    print(k_phix, k_phiy)
    mvd = 20
    for distribution, tab in langs.items():
        inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(4))
        dcs = [langmuir_cylinder.calc_d_cylinder_from_phi(inv_k * k_phi, tk, p, u) for inv_k in inv_ks]
        emy = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) for d in
               dcs]
        ems = [NACA_TR_1215_impingement.ie(1 / inv_k, k_phi, distribution) for inv_k in inv_ks]

        line, = plt.plot(NACA_TR_1215_impingement.data_table_iii[10000][tab],
                         NACA_TR_1215_impingement.data_table_iii[10000]['inv_ks'], 'o', fillstyle='none',
                         label=f'Table III {distribution} points')
        plt.plot(ems, inv_ks, c=line.get_color(), lw=0.5,
                 # label=f'Table III {distribution} points interpolated'
                 )
        # plt.plot(emy, inv_ks, '--')

    plt.xscale('log')
    plt.xlim(0.008, 1)
    plt.yscale('log')
    plt.ylim(.01, 4)
    plt.grid(which='both')
    plt.xlabel("Em")
    plt.ylabel("1/K")
    plt.legend()
    plt.savefig("naca_2904_fig_12e.png", transparent=True)

    plt.figure(figsize=(9.43, 7.22))
    k_phi = 10000
    d_cyl_inch_k_1 = 11.7
    d_cyl_m_k_1 = 11.7 * 0.0254
    mvd = langmuir_cylinder.calc_d_drop_from_k(1, tk, u, d_cyl_m_k_1)
    mvdx = langmuir_cylinder.calc_drop_diameter_micrometer_from_re_drop(k_phi ** 0.5, tk, p, u)
    print(mvd, mvdx)
    k_phix = langmuir_cylinder.calc_k_phi(tk, p, u, mvdx)
    k_phiy = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    print(k_phix, k_phiy)
    mvd = 20
    for distribution, tab in (("Langmuir B", "ems_b"),):
        inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(4))
        dcs = [langmuir_cylinder.calc_d_cylinder_from_phi(inv_k * k_phi, tk, p, u) for inv_k in inv_ks]
        emy = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) for d in
               dcs]
        ems = [NACA_TR_1215_impingement.ie(1 / inv_k, k_phi, distribution) for inv_k in inv_ks]

        line, = plt.plot(NACA_TR_1215_impingement.data_table_iii[10000][tab],
                         NACA_TR_1215_impingement.data_table_iii[10000]['inv_ks'], 'o', fillstyle='none',
                         label=f'Table III {distribution} points')
        plt.plot(ems, inv_ks, c=line.get_color(), lw=0.5,
                 # label=f'Table III {distribution} points interpolated'
                 )
        # plt.plot(emy, inv_ks, '--')

    plt.xscale('log')
    plt.xlim(0.008, 1)
    plt.yscale('log')
    plt.ylim(.01, 4)
    plt.grid(which='both')
    plt.xlabel("Em")
    plt.ylabel("1/K")
    plt.legend()
    plt.savefig("naca_2904_fig_12eb.png", transparent=True)

    plt.figure(figsize=(9.46, 7.22))
    k_phi = 10000
    d_cyl_inch_k_1 = 11.7
    d_cyl_m_k_1 = 11.7 * 0.0254
    mvd = langmuir_cylinder.calc_d_drop_from_k(1, tk, u, d_cyl_m_k_1)
    mvdx = langmuir_cylinder.calc_drop_diameter_micrometer_from_re_drop(k_phi ** 0.5, tk, p, u)
    print(mvd, mvdx)
    k_phix = langmuir_cylinder.calc_k_phi(tk, p, u, mvdx)
    k_phiy = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    print(k_phix, k_phiy)
    mvd = 20
    for distribution, tab in (("Langmuir B", "ems_b"),):
        inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(4))
        dcs = [langmuir_cylinder.calc_d_cylinder_from_phi(inv_k * k_phi, tk, p, u) for inv_k in inv_ks]
        emy = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) for d in
               dcs]
        ems = [NACA_TR_1215_impingement.ie(1 / inv_k, k_phi, distribution) for inv_k in inv_ks]

        line, = plt.plot(NACA_TR_1215_impingement.data_table_iii[10000][tab],
                         NACA_TR_1215_impingement.data_table_iii[10000]['inv_ks'], 'o', fillstyle='none',
                         label=f'Table III {distribution} points')
        plt.plot(ems, inv_ks, c=line.get_color(), lw=0.5,
                 label=f'Table IV {distribution} points interpolated'
                 )
        plt.plot(emy, inv_ks, '--', lw=0.5, label=f"NACA method Figure 6 {distribution}")

    plt.xscale('log')
    plt.xlim(0.008, 1)
    plt.yscale('log')
    plt.ylim(.01, 4)
    plt.grid(which='both')
    plt.xlabel("Em")
    plt.ylabel("1/K")
    plt.legend()
    plt.savefig("naca_2904_fig_12ebiii.png", transparent=True)

    plt.figure(figsize=(9.43, 7.22))
    k_phi = 10000
    mvd = 20
    for distribution, tab in langs.items():
        inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(4))
        dcs = [langmuir_cylinder.calc_d_cylinder_from_phi(inv_k * k_phi, tk, p, u) for inv_k in inv_ks]
        emy = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) for d in
               dcs]
        plt.plot(emy, inv_ks, lw=0.5, label=distribution)

    plt.xscale('log')
    plt.xlim(0.008, 1)
    plt.yscale('log')
    plt.ylim(.01, 4)
    plt.grid(which='both')
    plt.xlabel("Em")
    plt.ylabel("1/K")
    plt.legend()
    plt.savefig("naca_2904_fig_12e2.png", transparent=True)

    plt.figure(figsize=(9.43, 7.22))
    k_phi = 10000
    mvd = 20
    for distribution, tab in (("Langmuir B", "ems_b"),):
        inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(4))
        dcs = [langmuir_cylinder.calc_d_cylinder_from_phi(inv_k * k_phi, tk, p, u) for inv_k in inv_ks]
        emy = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution) for d in
               dcs]
        plt.plot(emy, inv_ks, lw=0.5, label=distribution)

    plt.xscale('log')
    plt.xlim(0.008, 1)
    plt.yscale('log')
    plt.ylim(.01, 4)
    plt.grid(which='both')
    plt.xlabel("Em")
    plt.ylabel("1/K")
    plt.legend()
    plt.savefig("naca_2904_fig_12e2b.png", transparent=True)

    lwc = 0.55  # back to nominal
    plt.figure()
    # sensitivities for a range of drop sizes
    for mph in (400, 300, 200, 100):
        u = mph*0.44704
        mrps = []
        mvdps = []
        mvdms = []
        mvds = list(plt.np.arange(5, 30+2.5, 2.5))
        for mvd in mvds:
            phi = langmuir_cylinder.calc_phi(tk, p, u, min(d_cyls))
            if phi > 50000:
                mvdps.append(float('nan'))
                mvdms.append(float('nan'))
                continue
            # construct a Langmuir B
            ems = [
                NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution="Langmuir B")
                for d in d_cyls]
            ems_lwc_u = [e * lwc * u * 0.0254 ** 2 for e in ems]
            masses = [em_lwc_u * d / 1000 * 0.0254 ** -2 for d, em_lwc_u in zip(d_cyls, ems_lwc_u)]
            # best fits for +/-5%
            em_lwcs_ramped_down = [m * em_lwc for m, em_lwc in zip((1.05, 1.0167, 0.9833, 0.95), ems_lwc_u)]
            em_lwcs_ramped_up = [m * em_lwc for m, em_lwc in zip((0.95, 0.9833, 1.0167, 1.05), ems_lwc_u)]
            masses_ramped_down = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_down)]
            masses_ramped_up = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_up)]
            lwc_ramped_up, mvd_ramped_up, best_distribution_ramped_up, rss = mc2.find_lwc_mvd_dist(tk, u, p,
                                                                                                   masses_ramped_up)
            lwc_ramped_down, mvd_ramped_down, best_distribution_ramped_down, rss = mc2.find_lwc_mvd_dist(tk, u, p,
                                                                                                         masses_ramped_down)
            mvdp = (mvd_ramped_down - mvd) / mvd
            mvdm = (mvd_ramped_up - mvd) / mvd
            mrps.append(mvd_ramped_up)
            lwcp = (lwc_ramped_down - lwc) / lwc
            lwcm = (lwc_ramped_up - lwc) / lwc
            mvdps.append(-mvdp)
            mvdms.append(mvdm)
            plt.text(mvd, mvdm, best_distribution_ramped_up[-1])
            plt.text(mvd, -mvdp, best_distribution_ramped_down[-1])

        print(mrps)
        line, = plt.plot(mvds, mvdms, '--', label=f"Calculated MVD too large, {mph:.0f} mph")
        plt.plot(mvds, mvdps, '-', c=line.get_color(), label=f"Calculated MVD too small, {mph:.0f} mph")
    plt.plot([], [], ' ', label='Best fit distribution noted')
    plt.xlabel("MVD, micrometer")
    plt.xlim(0, 35)
    plt.ylabel("Possible fraction difference, abs(calc_mvd-MVD)/MVD")
    plt.ylim(0, .8)
    plt.legend()
    plt.savefig("naca_tn_2904_fig_14a.png")

    mph = 400
    u = mph * 0.44704
    mvd = 25
    ems = [
        NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, distribution="Langmuir B")
        for d in d_cyls]
    ems_lwc_u = [e * lwc * u * 0.0254 ** 2 for e in ems]
    masses = [em_lwc_u * d / 1000 * 0.0254 ** -2 for d, em_lwc_u in zip(d_cyls, ems_lwc_u)]
    # best fits for +/-5%
    em_lwcs_ramped_down = [m * em_lwc for m, em_lwc in zip((1.05, 1.0167, 0.9833, 0.95), ems_lwc_u)]
    em_lwcs_ramped_up = [m * em_lwc for m, em_lwc in zip((0.95, 0.9833, 1.0167, 1.05), ems_lwc_u)]
    masses_ramped_down = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_down)]
    masses_ramped_up = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_up)]
    lwc_ramped_up, mvd_ramped_up, best_distribution_ramped_up, rss_up = mc2.find_lwc_mvd_dist(tk, u, p,
                                                                                           masses_ramped_up)
    lwc_ramped_down, mvd_ramped_down, best_distribution_ramped_down, rss_down = mc2.find_lwc_mvd_dist(tk, u, p,
                                                                                                 masses_ramped_down)
    mvdp = (mvd_ramped_down - mvd) / mvd
    mvdm = (mvd_ramped_up - mvd) / mvd
    lwcp = (lwc_ramped_down - lwc) / lwc
    lwcm = (lwc_ramped_up - lwc) / lwc
    print(lwc_ramped_up, mvd_ramped_up, best_distribution_ramped_up, rss_up)
    print(lwc_ramped_down, mvd_ramped_down, best_distribution_ramped_down, rss_down)
    lwc_ramped_b, mvd_ramped_b, rss = mc2.find_lwc_mvd_from_dist(tk, u, p,masses_ramped_up, distribution="Langmuir B")
    print(lwc_ramped_b, mvd_ramped_b, "Langmuir B", rss)
    lwc_ramped_b, mvd_ramped_b, rss = mc2.find_lwc_mvd_from_dist(tk, u, p,masses_ramped_down, distribution="Langmuir B")
    print(lwc_ramped_b, mvd_ramped_b, "Langmuir B", rss)
    lwc_ramped_a, mvd_ramped_a, rss = mc2.find_lwc_mvd_from_dist(tk, u, p,masses_ramped_up, distribution="Langmuir A")
    print(lwc_ramped_a, mvd_ramped_a, "Langmuir A", rss)

    ks = [langmuir_cylinder.calc_k(tk, u, mvd_ramped_a, d) for d in d_cyls]
    print(ks)
    phi = langmuir_cylinder.calc_phi(tk, p, u, min(d_cyls))
    print(phi)

    # lwc_ramped_a, mvd_ramped_a, rss = mc2.find_lwc_mvd_from_dist(tk, u, p,masses_ramped_down, distribution="Langmuir A")
    # print(lwc_ramped_a, mvd_ramped_a, "Langmuir A", rss)

    plt.figure()
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'o')
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    print('min(ds)', min(ds), min(d_cyls))
    ds_inch = [_ / 0.0254 for _ in ds]
    emy = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd_ramped_up, d, "Langmuir E") * lwc_ramped_up * u * 0.0254 ** 2
           for d in ds]
    plt.plot(emy, ds_inch, label=f"{mvd:.2f} {mvd_ramped_up:.2f} {lwc_ramped_up:.3f}")
    emz = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd, d, "Langmuir E") * lwc * u * 0.0254 ** 2
           for d in ds]
    plt.plot(emz, ds_inch, ':')
    emz = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd_ramped_a, d, "Langmuir A") * lwc_ramped_a * u * 0.0254 ** 2
           for d in ds]
    plt.plot(emz, ds_inch, '--', label=f"{mvd:.2f} {mvd_ramped_a:.2f} {lwc_ramped_a:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    # plt.xlim(.01, .06)
    # plt.ylim(.1, 4)
    plt.grid(which='both')
    plt.legend(
        # loc='lower left'
    )
    plt.tight_layout()

    k_phi = langmuir_cylinder.calc_k_phi(tk, p, u, mvd_ramped_a)
    for d, d_inch in zip(d_cyls, d_cyls_inch):
        k = langmuir_cylinder.calc_k(tk, u, mvd_ramped_a, d)
        phi = langmuir_cylinder.calc_phi(tk, p, u, d)
        k_phi = langmuir_cylinder.calc_k_phi(tk, p, u, mvd_ramped_a)
        print(d, k, phi, k_phi)


    plt.figure()
    ks = [langmuir_cylinder.calc_k(tk, u, mvd_ramped_a, d) for d in ds]
    ems = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd_ramped_a, d, ) for d in ds]
    plt.plot(ks, ems)
    plt.xscale('log')


    plt.figure()
    ks = [langmuir_cylinder.calc_k(tk, u, mvd_ramped_a, d) for d in ds]
    ems = [NACA_TR_1215_impingement.calc_em_naca_tr_1215_with_distribution(tk, p, u, mvd_ramped_a, d, ) for d in ds]
    plt.plot(ds_inch, ems)
    plt.xscale('log')

    for mph in (400, 300, 200, 100):
        u = mph*.44704
        print(u,
        langmuir_cylinder.calc_phi(tk, p, u, min(d_cyls)),
        langmuir_cylinder.calc_phi(tk, p, u, max(d_cyls)),
              )




    plt.show()
