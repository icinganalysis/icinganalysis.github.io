import simple_csv_reader
from scipy.interpolate import interp1d
import numpy as np

from icinganalysis import langmuir_cylinder_values, langmuir_blodgett_table_ii

header, rows = simple_csv_reader.simple_csv_reader(r'cyl_beta2-43.csv')
columns = list(zip(*rows))
d = {k: v for k, v in zip(header, columns)}

lkos = np.log(d['ko'])
_beta_interp_extrapolate = interp1d(lkos, d['cyl_beta'],
                                    bounds_error=False, fill_value='extrapolate')
_beta_interp = interp1d(lkos, d['cyl_beta'],
                        bounds_error=False, fill_value=float('nan'))


def get_beta_extrapolate(ko):
    b = max(0, min(1, _beta_interp_extrapolate(np.log(ko))))
    return b


def get_beta(ko):
    b = _beta_interp(np.log(ko))
    b = max(0, b)
    return b


if __name__ == '__main__':


    ks = np.geomspace(0.01, 10)

    import matplotlib.pyplot as plt

    bs = [get_beta_extrapolate(_) for _ in ks]
    plt.plot(ks, bs, '--')
    bs = [get_beta(_) for _ in ks]
    plt.plot(ks, bs)
    plt.plot(d['ko'], d['cyl_beta'], '+')
    plt.xscale('log')
    plt.ylim(0, 1)
    header, rows = simple_csv_reader.simple_csv_reader(
        'table_2_7_a.csv')

    from icinganalysis import read_nasa_cr_2004_212875_data
    from icinganalysis import units_helpers

    diameter = 0.2
    p = 101000
    for case, u, mvd, lwc, tc, n, *_ in rows:
        print(case, u, mvd, lwc, tc, n)
        t = units_helpers.tc_to_k(tc)

        k = langmuir_cylinder_values.calc_k(t, u, mvd, diameter)
        re_drop = langmuir_cylinder_values.calc_re_d_drop(t, p, u, mvd)
        lr = langmuir_cylinder_values.calc_lambda_lambda_s(re_drop)
        phi = langmuir_cylinder_values.calc_phi(t, p, u, diameter)
        kol = langmuir_cylinder_values.calc_ko_cylinder(t, p, u, mvd, diameter)
        kol2 = langmuir_cylinder_values.calc_ko_cylinder(t, p, u, mvd, diameter * 2)
        bl = langmuir_blodgett_table_ii.calc_beta_o(k, phi)
        plt.plot(kol, bl, '^', fillstyle='none', label='Ko_langmuir_cylinder_radius')
        plt.plot(kol2, bl, 'v', fillstyle='none', label='Ko_langmuir_cylinder_diameter')

        # (k_o, beta_o, ac_calc, no_calc, b_calc, phi, theta, re_a, we_l, mach_calc
        #  ) = read_nasa_cr_2004_212875_data.get_nasa_cr_2004_212875_params_standard_units(
        #     t, p, u, mvd, lwc, diameter, 1, False
        # )
        # plt.plot(k_o, beta_o, 'x')
        # (k_o2, beta_ox, ac_calc, no_calc, b_calc, phi, theta, re_a, we_l, mach_calc
        #  ) = read_nasa_cr_2004_212875_data.get_nasa_cr_2004_212875_params_standard_units(
        #     t, p, u, mvd, lwc, diameter, 1, True
        # )
        # plt.plot(k_o, beta_ox, '*')
        k = read_nasa_cr_2004_212875_data.calc_k_cylinder_from(u, t, mvd, diameter)
        range_ratio = read_nasa_cr_2004_212875_data.calc_range_parameter_from(u, t, mvd, p)
        k_oc = k * range_ratio
        k = read_nasa_cr_2004_212875_data.calc_k_cylinder_from(u, t, mvd, diameter / 2)
        range_ratio = read_nasa_cr_2004_212875_data.calc_range_parameter_from(u, t, mvd, p)
        k_oc_d2 = k * range_ratio
        #
        plt.plot(k_oc, bl, 'x')
        plt.plot(k_oc_d2, bl, '<')

    tc = 7.9
    u = 80.25
    mvd = 20.36
    diameter_inch = 4
    diameter = units_helpers.inch_to_m(diameter_inch)
    p = 95720
    t = units_helpers.tc_to_k(tc)
    beta = 0.53
    (k_o, beta_o, ac_calc, no_calc, b_calc, phi, theta, re_a, we_l, mach_calc
     ) = read_nasa_cr_2004_212875_data.get_nasa_cr_2004_212875_params_standard_units(
        t, p, u, mvd, lwc, diameter, 1, True
    )
    c_for_beta_calc = diameter
    if True:
        c_for_beta_calc = diameter * 0.5
    k = read_nasa_cr_2004_212875_data.calc_k_cylinder_from(u, t, mvd, c_for_beta_calc)
    range_ratio = read_nasa_cr_2004_212875_data.calc_range_parameter_from(u, t, mvd, p)
    k_oc = k * range_ratio

    print(k_o)
    plt.plot(k_o, beta, 'o', fillstyle='none')
    plt.plot(k_oc, beta, 's', fillstyle='none')

    kom = k_o
    bm = beta

    tc = 8.2
    u = 81.02
    mvd = 16.45
    diameter_inch = 4
    diameter = units_helpers.inch_to_m(diameter_inch)
    p = 95650
    t = units_helpers.tc_to_k(tc)
    beta = 0.43
    (k_o, beta_o, ac_calc, no_calc, b_calc, phi, theta, re_a, we_l, mach_calc
     ) = read_nasa_cr_2004_212875_data.get_nasa_cr_2004_212875_params_standard_units(
        t, p, u, mvd, lwc, diameter, 1, True
    )
    c_for_beta_calc = diameter
    if True:
        c_for_beta_calc = diameter * 0.5
    k = read_nasa_cr_2004_212875_data.calc_k_cylinder_from(u, t, mvd, c_for_beta_calc)
    range_ratio = read_nasa_cr_2004_212875_data.calc_range_parameter_from(u, t, mvd, p)
    k_oc = k * range_ratio
    kom2 = k_o
    bm2 = beta

    print(k_o)
    plt.plot(k_o, beta, 'o', fillstyle='none')
    plt.plot(k_oc, beta, 's', fillstyle='none')
    plt.legend()

    diameter = 0.2
    t = 273.15-26
    p = 101325
    u = 70
    lwc=0.7

    ds = np.geomspace(5, 200)
    kols = [langmuir_cylinder_values.calc_ko_cylinder(t, p, u, _, diameter) for _ in ds]
    lr = langmuir_cylinder_values.calc_lambda_lambda_s(re_drop)
    phi = langmuir_cylinder_values.calc_phi(t, p, u, diameter)
    bls = [langmuir_blodgett_table_ii.calc_beta_o(langmuir_cylinder_values.calc_k(t, u, _, diameter), phi) for _ in ds]
    kos_conventional_dia = [
        langmuir_cylinder_values.calc_lambda_lambda_s(langmuir_cylinder_values.calc_re_d_drop(t, p, u, _))
        * langmuir_cylinder_values.calc_k(t, u, _, diameter * 2)
        for _ in ds
    ]
    kos_conventional_rad = [
        langmuir_cylinder_values.calc_lambda_lambda_s(langmuir_cylinder_values.calc_re_d_drop(t, p, u, _))
        * langmuir_cylinder_values.calc_k(t, u, _, diameter)
        for _ in ds
    ]
    mvd = 20
    k = langmuir_cylinder_values.calc_k(t, u, mvd, diameter)
    ko = langmuir_cylinder_values.calc_ko_cylinder(t, p, u, mvd, diameter)
    beta = langmuir_blodgett_table_ii.calc_beta_o(langmuir_cylinder_values.calc_k(t, u, mvd, diameter), phi)
    print(ko, beta)

    plt.figure(figsize=(9, 7))
    plt.plot(kols, bls, lw=2, label='Ko Langmuir cylinder radius')
    plt.plot(kos_conventional_dia, bls, ':', label='Ko equation 2-8 cylinder diameter')
    plt.plot(kos_conventional_rad, bls, '-.', label='Ko equation 2-8 cylinder radius')
    plt.plot(d['ko'], d['cyl_beta'], '--', label='Figure 2-43 Cylinder (Ko equation 2-8 cylinder radius?)')
    plt.plot(kom, bm, 'o', label="NASA-CR-4257 figure 6.6(a) Ko Langmuir cylinder radius")
    plt.plot(kom2, bm2, 'o', label="NASA-CR-4257 figure 6.6(b) Ko Langmuir cylinder radius")
    plt.plot(ko, beta, 's', fillstyle='none', label=f'Expected value Table 2-5 beta={beta[0]:.3f}')
    kox = (
        langmuir_cylinder_values.calc_lambda_lambda_s(
            langmuir_cylinder_values.calc_re_d_drop(t, p, u, mvd))
        * langmuir_cylinder_values.calc_k(t, u, mvd, diameter/2)
    )
    from icinganalysis.similarity import manual_of_scaling_methods
    by = manual_of_scaling_methods.calc_beta_o(kox)
    bx = interp1d(kos_conventional_rad, [float(_) for _ in bls])(ko)
    plt.plot(ko, bx, 's', label=f"Apparent value used in Table 2-5 beta={bx:.3f}")
    print(bx, by)

    plt.plot(k_o, beta_o, 'x')
    (k_o2, beta_ox, ac_calc, no_calc, b_calc, phi, theta, re_a, we_l, mach_calc
     ) = read_nasa_cr_2004_212875_data.get_nasa_cr_2004_212875_params_standard_units(
        t, p, u, mvd, lwc, diameter, 1, True)
    # plt.plot(k_o2, beta_ox, '<')
    print('k_o2, beta_ox', k_o2, beta_ox, no_calc, no_calc*beta/bx)

    from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement
    phi = NACA_TN_2904_impingement.calc_phi(t, p, u, diameter)
    bns = [
    NACA_TN_2904_impingement.calc_beta(NACA_TN_2904_impingement.calc_k(t, u, _, diameter), phi, 0) for _ in ds
    ]
    plt.plot(kols, bns, label="NACA_TN_2904 beta (plotted with Ko Langmuir cylinder radius)")


    k = NACA_TN_2904_impingement.calc_k(t, u, mvd, diameter)
    phi = NACA_TN_2904_impingement.calc_phi(t, p, u, diameter)
    betan = NACA_TN_2904_impingement.calc_beta(k, phi, 0)
    print('betan', betan)


    plt.xscale('log')
    plt.xlim(0.01, 10)
    plt.ylim(0, 1)
    plt.xlabel('"Ko" (see legend)')
    plt.ylabel('Beta max')
    plt.legend(loc='upper left')



    plt.figure()
    ems = [
        min(1, NACA_TN_2904_impingement.calc_em(t, p, u, _, diameter) )
        for _ in ds]
    plt.plot(kols, ems, '--')
    theta_ms = [
        min(np.pi/2, NACA_TN_2904_impingement.calc_theta_naca_tn_2904_from_table_i_data(NACA_TN_2904_impingement.calc_k(t, u, _, diameter), phi))
        for _ in ds]
    plt.plot(kols, theta_ms, ':')
    bs = [np.pi/2*e/m for e, m in zip(ems, theta_ms)]
    plt.plot(kols, bs)
    plt.xscale('log')




    plt.show()
