import matplotlib.pyplot as plt
from icinganalysis import langmuir_cylinder
from icinganalysis import NACA_TN_2904_impingement
from icinganalysis import  multicylinder_naca_tn_2904_table_iv


def c1(d_inch, mph, mvd, tk):
    mu_slug_ft_s = langmuir_cylinder.calc_air_viscosity(tk) / 14.5939 * 0.3048
    k = 4.088e-11 * (mvd**2*mph/mu_slug_ft_s/d_inch)
    return k


def d_inch_c1_from(k, mph, mvd, tk):
    mu_slug_ft_s = langmuir_cylinder.calc_air_viscosity(tk) / 14.5939 * 0.3048
    d_inch = 4.088e-11 * (mvd**2*mph/mu_slug_ft_s/k)
    return d_inch


def mvd_c1_from(k, d_inch, mph, tk):
    mu_slug_ft_s = langmuir_cylinder.calc_air_viscosity(tk) / 14.5939 * 0.3048
    mvd = (k / (4.088e-11 * (mph/mu_slug_ft_s/d_inch)))**0.5
    return mvd


if __name__ == "__main__":

    # Figure 11
    em_lwcs = 0.0297, 0.0269, 0.0226, 0.0163
    # em_lwcs = 0.0300, 0.0267, 0.0226, 0.0163
    d_cyls_inch = 0.125, 0.5, 1.25, 3
    d_cyls = [_ * 0.0254 for _ in d_cyls_inch]

    print(em_lwcs)

    mph = 200
    alt_ft = 10000
    tk = (9 + 459.67) / 1.8
    u = mph * 0.44704
    p = langmuir_cylinder.calc_pressure(alt_ft * 12 * 0.0254)



    # K=1 fits from graphic analysis
    k1_d_cyl_inch = 8.3, 9.9, 11.7
    mvds = [langmuir_cylinder.calc_d_drop_from_k(1, tk, u, d*0.0254) for d in k1_d_cyl_inch]
    print(mvds)
    kphis = [langmuir_cylinder.calc_k_phi(tk, p, u, mv) for mv in mvds]
    print(kphis)



    mvd = 20
    distribution = "Langmuir B"
    mvd_nom = 20
    lwc_nom = 0.55
    dist_nom = "Langmuir B"

    k = langmuir_cylinder.calc_k(tk, u, mvd, 2 * 0.0254)
    print('k, 1/k', k, 1 / k)

    k_phi = langmuir_cylinder.calc_k_phi(tk, p, u, mvd)
    print('k_phi', k_phi)
    cdx = langmuir_cylinder.calc_d_cylinder_from_k(1, tk, u, mvd)
    print(cdx, cdx / 0.0254)

    d_cyl_m_k_1 = 10.1 * 0.0254
    mvdx = langmuir_cylinder.calc_d_drop_from_k(1, tk, u, d_cyl_m_k_1)
    print(mvdx)
    em_indicated_nom = [el/(u*0.0254**2)/lwc_nom for el in em_lwcs]

    ems_nom = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_nom, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom),
        "Langmuir B",
    ) for d in d_cyls]

    print(ems_nom)
    lwc = 0.55
    # ems_lang_b = [e * lwc for e in ems_lang_b]
    ems_lwc_nom_u_sq_inch_table_iv = [e * lwc_nom * u * 0.0254 ** 2 for e in ems_nom]
    print('ems_lang_b*lwc_u_sq_inch', ems_lwc_nom_u_sq_inch_table_iv)
    rss_nominal = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs, ems_lwc_nom_u_sq_inch_table_iv)
    print(em_lwcs)
    print(ems_nom)
    print(ems_lwc_nom_u_sq_inch_table_iv)
    print('rss_nominal', rss_nominal)

    masses = [em_lwc_u * d / 1000 * 0.0254 ** -2 for d, em_lwc_u in zip(d_cyls, em_lwcs)]
    mc3 = multicylinder_naca_tn_2904_table_iv.Multicylinder(d_cyls)

    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    ds_inch = [_ / 0.0254 for _ in ds]
    print(ds_inch[0], ds_inch[-1])
    lwc3, mvd3, best_distribution3, rss3 = mc3.find_lwc_mvd_dist(tk, u, p, masses)

    naca3_ems_lwcs = [NACA_TN_2904_impingement.calc_em_naca_tn_2904_with_distribution(tk, p, u, mvd3, d,
                                                                                     best_distribution3) * lwc3 * u * 0.0254 ** 2
                     for d in ds]

    naca3_ems_lwcs = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd3, d),
        # langmuir_cylinder.calc_phi(tk, p, u, d),  # !!! error, should use calc_k_phi !!!
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        best_distribution3) * lwc3 * u * 0.0254 ** 2
                     for d in ds]

    plt.figure()
    plt.suptitle(f'Nominal case MVD={mvd:.1f} LWC={lwc:.2f} {distribution} RSS {rss_nominal}')
    plt.plot(em_lwcs, d_cyls_inch, 'o', label='Figure 11 data')
    ds = plt.np.logspace(plt.np.log10(0.1 * min(d_cyls)), plt.np.log10(5 * max(d_cyls)))
    ds_inch = [_ / 0.0254 for _ in ds]
    ems_nom = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd, d),
        # langmuir_cylinder.calc_phi(tk, p, u, d),  # !!! error, should use calc_k_phi !!!
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd),
        "Langmuir B",
    ) for d in ds]
    ems_lang_b_lwc_u_sq_inch = [e * lwc * u * 0.0254 ** 2 for e in ems_nom]
    plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, ':', label="Em calculated from\nTable IV interpolation")
    plt.plot(naca3_ems_lwcs, ds_inch, '--', label=f"NACA Table IV method best\nMVD={mvd3:.1f} LWC={lwc3:.3f} {best_distribution3} {rss3:.3f}")
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

    em_lwcs_ramped_down = [m * em_lwc for m, em_lwc in zip((1.05, 1.0167, 0.9833, 0.95), em_lwcs)]
    em_lwcs_ramped_up = [m * em_lwc for m, em_lwc in zip((0.95, 0.9833, 1.0167, 1.05), em_lwcs)]
    masses_ramped_down = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_down)]
    masses_ramped_up = [em_lwc * d / 1000 * 0.0254 ** -2 for d, em_lwc in zip(d_cyls, em_lwcs_ramped_up)]



    lwc3_ramped_down, mvd3_ramped_down, best_distribution3_ramped_down, rss3_ramped_down = mc3.find_lwc_mvd_dist(tk, u, p,
                                                                                                     masses_ramped_down)
    naca3_ems_lwcs_ramped_down = [
        NACA_TN_2904_impingement.ie(langmuir_cylinder.calc_k(tk, u, mvd3_ramped_down, d),
                                    langmuir_cylinder.calc_k_phi(tk, p, u, mvd3_ramped_down),
                                    best_distribution3_ramped_down) * lwc3_ramped_down * u * 0.0254 ** 2
        for d in ds]
    lwc3_ramped_up, mvd3_ramped_up, best_distribution3_ramped_up, rss3_ramped_up = mc3.find_lwc_mvd_dist(tk, u, p,
                                                                                               masses_ramped_up)

    print('best_distribution3_ramped_up', best_distribution3_ramped_up)
    print(mvd3_ramped_up)

    naca3_ems_lwcs_ramped_up = [
        NACA_TN_2904_impingement.ie(langmuir_cylinder.calc_k(tk, u, mvd3_ramped_up, d),
                                    langmuir_cylinder.calc_k_phi(tk, p, u, mvd3_ramped_up),
                                    best_distribution3_ramped_up) * lwc3_ramped_up * u * 0.0254 ** 2
        for d in ds]


    print(rss3_ramped_down, mvd3_ramped_down)
    print(rss3_ramped_up, mvd3_ramped_up)

    plt.figure(figsize=(8, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(naca3_ems_lwcs, ds_inch, label=f"NACA Table IV method best\nMVD={mvd3:.1f} LWC={lwc3:.3f} {best_distribution3} {rss3:.3f}")
    plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, ':', label="Em calculated from\nTable IV interpolation")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(naca3_ems_lwcs_ramped_up, ds_inch,
             label=f"NACA method best\nMVD={mvd3_ramped_up:.1f} LWC={lwc3_ramped_up:.3f} {best_distribution3_ramped_up} {rss3_ramped_up:.3f}")
    plt.plot(naca3_ems_lwcs_ramped_down, ds_inch,
             label=f"NACA method best\nMVD={mvd3_ramped_down:.1f} LWC={lwc3_ramped_down:.3f} {best_distribution3_ramped_down} {rss3_ramped_down:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .04)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='best')
    plt.savefig('naca_tn_2904_fig13_iv_zoom_no_k_for_k_phi_error.png', transparent=True)


    mvd_nom_up = 25
    lwc_nom_up = 0.52
    dist_nom_up = "Langmuir B"
    ems_nom_up = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_nom_up, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom_up),
        dist_nom_up,
    ) for d in ds]
    em_lwcs_nom_up = [e * lwc_nom_up * u * 0.0254 ** 2 for e in ems_nom_up]
    rss_nom_up = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs, em_lwcs_nom_up)
    em_indicated_ramped_up = [el/(u*0.0254**2)/lwc_nom_up for el in em_lwcs_ramped_up]

    mvd_nom_down = 17
    lwc_nom_down = 0.57
    dist_nom_down = "Langmuir E"
    ems_nom_down = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_nom_down, d),
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom_down),
        dist_nom_down,
    ) for d in ds]
    em_lwcs_nom_down = [e * lwc_nom_down * u * 0.0254 ** 2 for e in ems_nom_down]
    rss_nom_down = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs, em_lwcs_nom_down)
    em_indicated_ramped_down = [el/(u*0.0254**2)/lwc_nom_down for el in em_lwcs_ramped_down]

    plt.figure(figsize=(8, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(naca3_ems_lwcs, ds_inch, label=f"NACA Table IV method best\nMVD={mvd3:.1f} LWC={lwc3:.3f} {best_distribution3} {rss3:.3f}")
    plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, ':', label="Em calculated from\nTable IV interpolation")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(naca3_ems_lwcs_ramped_up, ds_inch,
             label=f"NACA method best\nMVD={mvd3_ramped_up:.1f} LWC={lwc3_ramped_up:.3f} {best_distribution3_ramped_up} {rss3_ramped_up:.3f}")
    plt.plot(em_lwcs_nom_up, ds_inch,
             label=f"NACA nominal up\nMVD={mvd_nom_up:.1f} LWC={lwc_nom_up:.3f} {dist_nom_up} {rss_nom_up:.3f}")
    plt.plot(em_lwcs_nom_down, ds_inch,
             label=f"NACA nominal down\nMVD={mvd_nom_down:.1f} LWC={lwc_nom_down:.3f} {dist_nom_down} {rss_nom_down:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .04)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='best')

    plt.figure(figsize=(8, 7.9))
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch,
             label=f"NACA nominal\nMVD={mvd_nom:.1f} LWC={lwc_nom:.3f} {dist_nom} {rss_nominal:.3f}")
    plt.plot(em_lwcs_nom_down, ds_inch,
             label=f"NACA nominal down\nMVD={mvd_nom_down:.1f} LWC={lwc_nom_down:.3f} {dist_nom_down} {rss_nom_down:.3f}")
    plt.plot(em_lwcs_nom_up, ds_inch,
             label=f"NACA nominal up\nMVD={mvd_nom_up:.1f} LWC={lwc_nom_up:.3f} {dist_nom_up} {rss_nom_up:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .04)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='best')


    k_phi = 10000
    dps = [langmuir_cylinder.calc_d_cylinder_from_k(1/inv_k, tk, u, mvd_nom) for inv_k in
           NACA_TN_2904_impingement.data_table_iv_original[k_phi]['inv_ks']]
    dps_inch = [_/0.0254 for _ in dps]
    em_lwc_us_dps_bs = [e * u * lwc_nom * 0.0254 ** 2 for e in NACA_TN_2904_impingement.data_table_iv_original[k_phi]['ems_b']]

    plt.figure(figsize=(5, 7.9)) # fig 13 overlay
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    line, = plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch,
             label=f"NACA nominal\nMVD={mvd_nom:.1f} LWC={lwc_nom:.3f}\n{dist_nom} {rss_nominal:.3f}")
    plt.plot(em_lwcs_nom_down, ds_inch,
             label=f"NACA nominal down\nMVD={mvd_nom_down:.1f} LWC={lwc_nom_down:.3f}\n{dist_nom_down} {rss_nom_down:.3f}")
    plt.plot(em_lwcs_nom_up, ds_inch,
             label=f"NACA nominal up\nMVD={mvd_nom_up:.1f} LWC={lwc_nom_up:.3f}\n{dist_nom_up} {rss_nom_up:.3f}")
    plt.plot(em_lwc_us_dps_bs, dps_inch, 'x', c= line.get_color(),
             label=f'Table IV points Langmuir B\nMVD={mvd_nom:.1f} LWC={lwc_nom:.3f}')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_13_overlay.png', transparent=True)

    plt.figure(figsize=(5.4, 8)) # fig 13 overlay
    plt.plot(em_lwcs, d_cyls_inch, 'o', label="Figure 11 data")
    line, = plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, '--',
             label=f"NACA nominal\nMVD={mvd_nom:.1f} LWC={lwc_nom:.3f}\n{dist_nom} {rss_nominal:.3f}")
    plt.plot(em_lwc_us_dps_bs, dps_inch, 'x', c= line.get_color(),
             label=f'Table IV points Langmuir B\nMVD={mvd_nom:.1f} LWC={lwc_nom:.3f}')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_13_overlay_b_only.png', transparent=True)

    mvdx = langmuir_cylinder.calc_drop_diameter_micrometer_from_re_drop(10000**0.5, tk, p, u)
    plt.figure(figsize=(10.5, 7.9)) # fig 13 overlay
    plt.plot(em_lwcs, d_cyls_inch, 'o', fillstyle='none', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    line, = plt.plot(ems_lang_b_lwc_u_sq_inch, ds_inch, '--',
             label=f"NACA nominal\nMVD={mvd_nom:.1f} LWC={lwc_nom:.3f}\n{dist_nom} RSS={rss_nominal:.3f}")
    plt.plot(em_lwc_us_dps_bs, dps_inch, 'x', c= line.get_color(),
             label=f'Table IV points Langmuir B\nat nominal K*Phi=10000\nMVD={mvdx:.2f} LWC={lwc_nom:.3f}')
    plt.plot(naca3_ems_lwcs, ds_inch, label=f"Calculated best fit\nMVD={mvd3:.1f} LWC={lwc3:.3f}\n{best_distribution3} RSS={rss3:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_13_overlay_b_only_wide.png', transparent=True)

    es = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_nom, d),  # !!!
        langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom_up),
        dist_nom_up) for d in ds]
    em_lwc_us_dps_as = [e * u * lwc_nom_up * 0.0254 ** 2 for e in es]
    rss_a = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs_ramped_up, em_lwc_us_dps_as)

    plt.figure(figsize=(10.5, 7.9)) # fig 13 overlay
    plt.plot(em_lwcs, d_cyls_inch, 'o', fillstyle='none', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    line, = plt.plot(em_lwc_us_dps_as, ds_inch, '--',
             label=f"NACA nominal K*Phi=10000\nMVD={mvdx:.1f} LWC={lwc_nom_up:.3f}\n{dist_nom_up} RSS={rss_a:.3f}")
    plt.plot(em_lwcs_nom_up, ds_inch, ':',
             label=f"NACA nominal\nMVD={mvd_nom_up:.1f} LWC={lwc_nom_up:.3f} {dist_nom_up} {rss_nom_up:.3f}")
    plt.plot(naca3_ems_lwcs_ramped_up, ds_inch,
             label=f"NACA method best\nMVD={mvd3_ramped_up:.1f} LWC={lwc3_ramped_up:.3f}\n{best_distribution3_ramped_up} {rss3_ramped_up:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_13_overlay_a_only_wide.png', transparent=True)

    plt.figure(figsize=(10.5, 7.9)) # fig 13 overlay
    lwcx = lwc_nom_down
    # lwcx = 0.62
    em_lwcs_nom_downx = [_*lwcx/lwc_nom_down for _ in em_lwcs_nom_down]
    rss_ex = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs_ramped_down, em_lwcs_nom_down)
    plt.plot(em_lwcs, d_cyls_inch, 'o', fillstyle='none', label="Figure 11 data")
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'x', label="Figure 11 data ramped\nfrom -5% to +5%")
    plt.plot(em_lwcs_ramped_down, d_cyls_inch, '+', label="Figure 11 data ramped\nfrom +5% to -5%")
    plt.plot(em_lwcs_nom_downx, ds_inch, ':',
             label=f"NACA nominal\nMVD={mvd_nom_down:.1f} LWC={lwcx:.3f} {dist_nom_down} {rss_ex:.3f}")
    plt.plot(naca3_ems_lwcs_ramped_down, ds_inch,
             label=f"NACA method best\nMVD={mvd3_ramped_down:.1f} LWC={lwc3_ramped_down:.3f}\n{best_distribution3_ramped_down} {rss3_ramped_down:.3f}")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, .1)
    plt.ylim(.1, 10)
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_13_overlay_e_only_wide.png', transparent=True)

    # fig12e overlay
    plt.figure(figsize=(5.7, 7.7))
    k_phi = 10000
    inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(6), 1000)
    for dist, tab in NACA_TN_2904_impingement.langs_table_iv.items():

        ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
        line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} interpolated")

        plt.plot(
            NACA_TN_2904_impingement.data_table_iv_original[k_phi][tab],
            NACA_TN_2904_impingement.data_table_iv_original[k_phi]['inv_ks'],
            'o', fillstyle='none',
            c=line.get_color(),
            label=f'Table IV {dist}'
        )

    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.008, 1)
    plt.ylim(.01, 6)
    plt.legend()
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_12e_overlay.png', transparent=True)

    plt.figure(figsize=(5.7, 7.7))
    k_phi = 10000
    inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(6), 1000)
    dts = (('Langmuir B', 'ems_b'),)
    for dist, tab in dts:

        ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
        line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} interpolated")

        plt.plot(
            NACA_TN_2904_impingement.data_table_iv_original[k_phi][tab],
            NACA_TN_2904_impingement.data_table_iv_original[k_phi]['inv_ks'],
            'o', fillstyle='none',
            c=line.get_color(),
            label=f'Table IV {dist}'
        )

    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.008, 1)
    plt.ylim(.01, 6)
    plt.legend()
    plt.grid(which='both')
    plt.legend(loc='lower left')
    plt.savefig('naca_tn_2904_fig_12e_overlay_langmuir_b_only.png', transparent=True)


    plt.figure(figsize=(5.7, 7.7))
    inv_ks = plt.np.logspace(plt.np.log10(.01), plt.np.log10(6), 1000)
    dist = 'Langmuir E'
    k_phi = 10000
    ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
    line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} K*Phi={k_phi:.0f}")
    inv_ks_d_cyl = [1/langmuir_cylinder.calc_k(tk, u, mvd_nom, d) for d in d_cyls]
    ems_d_cyls = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks_d_cyl]
    plt.plot(ems_d_cyls, inv_ks_d_cyl, '+', c=line.get_color())
    k_phi = kphis[0]
    ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
    line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} K*Phi={k_phi:.0f}")
    inv_ks_d_cyl = [1/langmuir_cylinder.calc_k(tk, u, mvds[0], d) for d in d_cyls]
    ems_d_cyls = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks_d_cyl]
    plt.plot(ems_d_cyls, inv_ks_d_cyl, '+', c=line.get_color())

    k_phi_nom_down = langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom_down)
    ems = [NACA_TN_2904_impingement.ie(1 / inv_k, k_phi_nom_down, dist) for inv_k in inv_ks]
    line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} K*Phi={k_phi_nom_down:.0f}")
    inv_ks_d_cyl = [1/langmuir_cylinder.calc_k(tk, u, mvd_nom_down, d) for d in d_cyls]
    ems_d_cyls = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi_nom_down, dist) for inv_k in inv_ks_d_cyl]
    print(inv_ks_d_cyl)
    print(ems_d_cyls)
    print(mvd_nom_down)
    plt.plot(ems_d_cyls, inv_ks_d_cyl, '+', c=line.get_color())
    plt.plot([],[],'+',c='k',label='Cylinder calculated Em values for K*Phi value')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.008, 1)
    plt.ylim(.01, 6)
    plt.xlabel('Em')
    plt.ylabel('1/K')
    plt.legend()
    plt.grid(which='both')
    plt.legend(loc='lower left')

    plt.figure(figsize=(5.7, 7.7))
    inv_ks = plt.np.logspace(plt.np.log10(.007), plt.np.log10(6), 1000)
    dist = 'Langmuir A'
    k_phi = 10000
    ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
    line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} K*Phi={k_phi:.0f}")
    inv_ks_d_cyl = [1/langmuir_cylinder.calc_k(tk, u, mvd_nom, d) for d in d_cyls]
    ems_d_cyls = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks_d_cyl]
    plt.plot(ems_d_cyls, inv_ks_d_cyl, '+', c=line.get_color())
    lwc_c, mvd_c, rss_c = mc3.find_lwc_mvd_from_dist(tk, u, p, masses_ramped_up, distribution=dist,
                                    constrained_k_phi=k_phi)
    em_indicated = [el/(u*0.0254**2)/lwc_c for el in em_lwcs]
    rss_indicated = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_indicated, ems_d_cyls)
    plt.plot(em_indicated, inv_ks_d_cyl, 'o', c=line.get_color(), fillstyle='none', label=f"{k_phi:.0f} {mvd_nom:.1f} {rss_indicated:.3f}")

    k_phi = kphis[-1]
    ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
    line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} K*Phi={k_phi:.0f}")
    inv_ks_d_cyl = [1/langmuir_cylinder.calc_k(tk, u, mvds[-1], d) for d in d_cyls]
    ems_d_cyls = [NACA_TN_2904_impingement.ie(1/inv_k, k_phi, dist) for inv_k in inv_ks_d_cyl]
    plt.plot(ems_d_cyls, inv_ks_d_cyl, '+', c=line.get_color())
    lwc_c, mvd_c, rss_c = mc3.find_lwc_mvd_from_dist(tk, u, p, masses_ramped_up, distribution=dist,
                                    constrained_k_phi=k_phi)
    em_indicated = [el/(u*0.0254**2)/lwc_nom_up for el in em_lwcs_ramped_up]
    rss_indicated = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_indicated, ems_d_cyls)
    plt.plot(em_indicated, inv_ks_d_cyl, 'o', c=line.get_color(), fillstyle='none', label=f"{k_phi:.0f} {mvds[-1]:.1f} {rss_indicated:.3f}")
    print(em_indicated)

    print(lwc_c, mvd_c, rss_c)
    print(langmuir_cylinder.calc_k_phi(tk, p, u, mvd_c))
    print(kphis[-1])

    k_phi_nom_up = langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom_up)
    k_phi = k_phi_nom_up
    ems = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks]
    line, = plt.plot(ems, inv_ks, lw=0.5, label=f"{dist} K*Phi={k_phi:.0f}")
    inv_ks_d_cyl = [1/langmuir_cylinder.calc_k(tk, u, mvd_nom_up, d) for d in d_cyls]
    ems_d_cyls = [NACA_TN_2904_impingement.ie(1/inv_k,k_phi, dist) for inv_k in inv_ks_d_cyl]

    plt.plot(ems_d_cyls, inv_ks_d_cyl, '+', c=line.get_color())
    plt.plot([],[],'+',c='k',label='Cylinder calculated Em values for K*Phi value')
    lwc_c, mvd_c, rss_c = mc3.find_lwc_mvd_from_dist(tk, u, p, masses_ramped_up, distribution=dist,
                                    constrained_k_phi=k_phi)
    em_indicated = [el/(u*0.0254**2)/lwc_c for el in em_lwcs_ramped_up]
    rss_indicated = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_indicated, ems_d_cyls)
    plt.plot(em_indicated, inv_ks_d_cyl, 'o', c=line.get_color(), fillstyle='none', label=f"{k_phi:.0f} {mvd_nom_up:.1f} {rss_indicated:.3f}")
    print(mvd_nom, mvds[-1], mvd_nom_up)
    print(em_indicated)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.1, 1)
    plt.ylim(.007, .4)
    plt.xlabel('Em')
    plt.ylabel('1/K')
    plt.legend()
    plt.grid(which='both')
    plt.legend(loc='lower left')

    plt.figure(figsize=(10, 7.9))
    dist = 'Langmuir A'
    plt.plot(em_lwcs_ramped_up, d_cyls_inch, 'o', c='k', fillstyle='none')
    inv_ks = plt.np.logspace(plt.np.log10(.007), plt.np.log10(6), 1000)
    ds = [langmuir_cylinder.calc_d_cylinder_from_k(1/inv_k, tk, u, mvd_nom_up) for inv_k in inv_ks]
    ds_inch = [_/0.0254 for _ in ds]
    k_phi = 10000
    lwcx = lwc_nom_up
    lwcx = 0.495
    ems = [NACA_TN_2904_impingement.ie(1/inv_k, k_phi, dist) for inv_k in inv_ks]
    ems_lwc_calc = [e * lwcx * u * 0.0254 ** 2 for e in ems]
    line, = plt.plot(ems_lwc_calc, ds_inch, lw=0.5)
    em_lwcs_d_cyls = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_nom_up, d),
        k_phi, dist,
    ) * lwcx * u * 0.0254 ** 2 for d in d_cyls]
    rss = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs_ramped_up, em_lwcs_d_cyls)
    plt.plot(em_lwcs_d_cyls, d_cyls_inch, '+', c=line.get_color(),
             label=f"Constrained K*Phi={k_phi:.0f}\n{dist} {lwcx:.3f} {mvd_nom_up:.2f} {rss:.3f}")

    k_phi = kphis[-1]
    lwc_c, mvd_c, rss_c = mc3.find_lwc_mvd_from_dist(tk, u, p, masses_ramped_up, distribution=dist,
                                    constrained_k_phi=k_phi)
    mvd_cx = mvd_c
    mvd_c = mvds[-1]
    ds = [langmuir_cylinder.calc_d_cylinder_from_k(1/inv_k, tk, u, mvd_c) for inv_k in inv_ks]
    ds_inch = [_/0.0254 for _ in ds]
    ems = [NACA_TN_2904_impingement.ie(1/inv_k, k_phi, dist) for inv_k in inv_ks]
    ems_lwc_calc = [e * lwc_c * u * 0.0254 ** 2 for e in ems]
    line, = plt.plot(ems_lwc_calc, ds_inch, lw=0.5)
    em_lwcs_d_cyls = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_c, d),
        k_phi, dist,
    ) * lwc_c * u * 0.0254 ** 2 for d in d_cyls]
    rss = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs_ramped_up, em_lwcs_d_cyls)
    plt.plot(em_lwcs_d_cyls, d_cyls_inch, '+', c=line.get_color(),
             label=f"K*Phi={k_phi:.0f} Nominal\n{dist} {lwc_c:.3f} {mvd_c:.2f} {mvd_cx:.2f} {rss:.3f}")


    k_phi = langmuir_cylinder.calc_k_phi(tk, p, u, mvd3_ramped_up)
    ds = [langmuir_cylinder.calc_d_cylinder_from_k(1/inv_k, tk, u, mvd3_ramped_up) for inv_k in inv_ks]
    ds_inch = [_/0.0254 for _ in ds]
    ems = [NACA_TN_2904_impingement.ie(1/inv_k, k_phi, best_distribution3_ramped_up) for inv_k in inv_ks]
    ems_lwc_calc = [e * lwc3_ramped_up * u * 0.0254 ** 2 for e in ems]
    line, = plt.plot(ems_lwc_calc, ds_inch, lw=0.5)
    em_lwcs_d_cyls = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd3_ramped_up, d),
        k_phi, best_distribution3_ramped_up,
    ) * lwc3_ramped_up * u * 0.0254 ** 2 for d in d_cyls]
    rss = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs_ramped_up, em_lwcs_d_cyls)
    plt.plot(em_lwcs_d_cyls, d_cyls_inch, '+', c=line.get_color(),
             label=f"K*Phi={k_phi:.0f} Calculated best fit\n{best_distribution3_ramped_up} {lwc3_ramped_up:.3f} {mvd3_ramped_up:.2f} {rss:.3f}")

    k_phi = langmuir_cylinder.calc_k_phi(tk, p, u, mvd_nom_up)
    lwc_nom_up = 0.505
    ds = [langmuir_cylinder.calc_d_cylinder_from_k(1/inv_k, tk, u, mvd_nom_up) for inv_k in inv_ks]
    ds_inch = [_/0.0254 for _ in ds]
    ems = [NACA_TN_2904_impingement.ie(1/inv_k, k_phi, dist) for inv_k in inv_ks]
    ems_lwc_calc = [e * lwc_nom_up * u * 0.0254 ** 2 for e in ems]
    line, = plt.plot(ems_lwc_calc, ds_inch, lw=0.5)
    em_lwcs_d_cyls = [NACA_TN_2904_impingement.ie(
        langmuir_cylinder.calc_k(tk, u, mvd_nom_up, d),
        k_phi, dist,
    ) * lwc_nom_up * u * 0.0254 ** 2 for d in d_cyls]
    rss = multicylinder_naca_tn_2904_table_iv.calc_rss_log_diff(em_lwcs_ramped_up, em_lwcs_d_cyls)
    plt.plot(em_lwcs_d_cyls, d_cyls_inch, '+', c=line.get_color(),
             label=f"K*Phi={k_phi:.0f} Nom\n{dist} {lwc_nom_up:.3f} {mvd_nom_up:.2f} {rss:.3f}")

    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(.004, 0.1)
    plt.ylim(0.1,10)
    plt.xlabel('Em*LWC*u, g/s/in^2')
    plt.ylabel('Cylinder diameter, inch')
    plt.legend()
    plt.grid(which='both')
    plt.legend(loc='lower left')

    plt.savefig('nada_tn_2904_13x.png', transparent=True)


    inv_k_L_1 = [.165, .21, .25]
    mvds = [langmuir_cylinder.calc_d_drop_from_k(1/inv_k, tk, u, 2*0.0254) for inv_k in inv_k_L_1]
    print(mvds)

    inv_k_L_1 = [
        0.165289256198347,
    0.2,
        0.227272727272727,
    ]
    mvds = [langmuir_cylinder.calc_d_drop_from_k(1/inv_k, tk, u, 2*0.0254) for inv_k in inv_k_L_1]
    print(mvds)

    k = langmuir_cylinder.calc_k(tk, u, 20, 1*0.0254)
    print(k)
    k= c1(1, u/0.44704, 20, tk)
    print(k)
    d_inch = d_inch_c1_from(k, u/0.44704, 20, tk)
    print(d_inch)

    mvd = mvd_c1_from(k, 1, u/0.44704, tk)
    print(mvd)
    inv_k_L_1 = [.165, .21, .25]
    mvds = [mvd_c1_from(1/inv_k, 2, u/0.44704, tk) for inv_k in inv_k_L_1]
    print(mvds)
    rs = [_/mvds[1] for _ in mvds]
    print(rs)
    print([_**2 for _ in rs])
    print([mvds[1]*_**2 for _ in rs])

    plt.show()
