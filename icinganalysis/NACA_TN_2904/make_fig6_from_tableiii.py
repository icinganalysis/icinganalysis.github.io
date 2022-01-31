from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement
from icinganalysis.NACA_TN_2904.NACA_TN_2904_impingement import calc_em_from
import matplotlib.pyplot as plt


td = NACA_TN_2904_impingement.data_table_iv_original
for k_phi in td:
    print(k_phi)

fd = NACA_TN_2904_impingement.data_fig_6a
for phi in fd:
    line, = plt.plot(fd[phi]['ks'], fd[phi]['ems'], 'o', label=f"Phi={phi}")
    k_phis = [k*phi for k in fd[phi]['ks']]
    # for k, k_phi, em in zip(fd[phi]['ks'], k_phis, fd[phi]['ems']):
    #     plt.text(k, em, f"{k} {k_phi:.0f}")
    ks = plt.np.logspace(plt.np.log10(min(fd[phi]['ks'])), plt.np.log10(max(fd[phi]['ks'])))
    print(min(fd[phi]['ks']), max(fd[phi]['ks']))
    # print(min(ks), max(ks))
    ems_calc = [calc_em_from(k, k*phi) for k in ks]
    # print(phi, max(k_phis))
    plt.plot(ks, ems_calc, c=line.get_color())
    # for k, k_phi, em in zip(fd[phi]['ks'], k_phis, ems_calc):
    #     plt.text(k, em, f"{k} {k_phi:.0f}")
for k_phi in td:
    print(k_phi)
    ks = [1/inv_k for inv_k in td[k_phi]['inv_ks']]
    ems_calc = [calc_em_from(1/inv_k, k_phi) for inv_k in td[k_phi]['inv_ks']]
    phis = [k_phi*inv_k for inv_k in td[k_phi]['inv_ks']]
    plt.plot(ks, ems_calc, 'o', fillstyle='none', c='k')
    for k, phi, em in zip(ks, phis, ems_calc):
        plt.text(k, em, f"{1/k:.3f} {k_phi}")
plt.plot([], [], 'o', fillstyle='none', c='k', label='Table IV points (1/K, K*Phi noted)')
plt.plot([], [], '-', fillstyle='none', c='k', label='Interpolated from Table IV points')

plt.xscale('log')
plt.legend()

plt.show()