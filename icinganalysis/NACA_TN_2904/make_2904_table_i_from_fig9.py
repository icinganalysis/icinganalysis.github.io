from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement


ks = (.5, 1, 4, 16, 40)
print('    ', ks)
for phi in NACA_TN_2904_impingement.data_table_i:
    print(phi)
    for k, t in zip(
        NACA_TN_2904_impingement.data_table_i[phi]['ks'],
        NACA_TN_2904_impingement.data_table_i[phi]['theta'],
    ):
        theta = NACA_TN_2904_impingement.calc_theta_from_figure_9_data(k, phi)
        print('    ', k, f"{t:.3f} {theta:.3f}")
    # thetas = [NACA_TN_2904_impingement.calc_theta_from_figure_9_data(k, phi) for k in ks]
    # print(phi, thetas)
