import matplotlib.pyplot as plt
from math import atan2, log
from scipy.interpolate import interp1d
import numpy as np

sqtr6 = 6 ** 0.5


def calc_cd_r_24(re_drop):
    return (
        1 + 0.197 * re_drop ** 0.63 + 2.6e-4 * re_drop ** 1.38
)  # equ. (22)


def calc_lambda_lambda_s_nasa(re_drop):
    if re_drop < 0.752:
        return 1
    # NASA/CR-2004-212875 equation (3.12)
    # representation of equ. (41)
    return 1 / (0.8388 + 0.001483 * re_drop + 0.1847 * re_drop ** 0.5)


def calc_lambda_lambda_s_ratio(re):
    if re == 0:
        return 1
    return 18 * (re ** (-2 / 3) - sqtr6 / re * atan2(re ** (1 / 3), sqtr6)
                 )  # DOT/FAA/CT88-8/1 equ. (2-10)


# fmt: off
_interp_ratio_rus = (0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2,
                     2.5, 3, 3.5, 4, 5, 6, 8, 10, 12, 14, 16, 18,
                     20, 25, 30, 35, 40, 50, 60, 80, 100, 120, 140,
                     160, 180, 200, 250, 300, 350, 400, 500, 600, 800, 1000,
                     1200, 1400, 1600, 1800, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 8000, 10000)
_interp_ratios = (1, .9956, .9911, .9832, .9652, .9493, .9342, .92, .9068, .895, .8842, .8744,
                  .8653, .8452, .8273, .812, .7978, .7734, .7527, .7185, .6905, .666, .644, .6242,
                  .6065, .5904, .5562, .5281, .5045, .4840, .4505, .4237, .3829, .3524, .3285,
                  .3090, .2928, .2789, .2668, .2424, .2234, .2080, .1953, .1752, .1597, .1373,
                  .1215, .1097, .1003, .0927, .0863, .0809, .0703, .0624, .0562, .0513, .0439, .0385, .0311, .0262)
# fmt: on

_ratio_interpolator = interp1d([log(_) for _ in _interp_ratio_rus], _interp_ratios)


def calc_ratio_langmuir_blodgett(re):
    return _ratio_interpolator(log(re) if re > 0 else log(0.01))

# fmt: off
_interp_cd_r_24_rus = (0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2,
                     2.5, 3, 3.5, 4, 5, 6, 8, 10, 12, 14, 16, 18,
                     20, 25, 30, 35, 40, 50, 60, 80, 100, 120, 140,
                     160, 180, 200, 250, 300, 350, 400, 500, 600, 800, 1000,
                     1200, 1400, 1600, 1800, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 8000, 10000,
                       12000,14000,16000,18000,20000,25000,30000,35000,40000,50000,60000,80000,
                       100000,120000,140000,160000,
                       )
_interp_cd_r_24 = (1,1.009,1.018,1.037,1.073,1.108,1.142,1.176,1.201,1.225,1.248,1.267,1.285,
                   1.332,1.374,1.412,1.447,1.513,1.572,1.678,1.782,1.901,2.009,2.109,2.198,
                   2.291,2.489,2.673,2.851,3.013,3.327,3.6,4.11,4.59,5.01,5.4,
                   5.76,6.16,6.52,7.38,8.26,9, 9.82,11.46,12.97,15.81,18.62,
                   21.3,24,26.9,29.8,32.7,40.4,47.8,55.6,63.7,80,96.8,130.6,166.3,
                   204, 243,285,325,365,470,574,674,778,980,1175,1552,
                   1905,2234,2549,2851,
                   )
# fmt: on


_cd_r_24_interpolator = interp1d([log(_) for _ in _interp_cd_r_24_rus], _interp_cd_r_24)


def calc_cd_r_24_langmuir_blodgett(re):
    # print('re', re)
    if re < 0.01:
        return 1
    if re > 160000:
        return 2851
    return _cd_r_24_interpolator(log(re) if re > 0 else log(0.01))


if __name__ == "__main__":

    rus_ = (20, 50, 100, 200, 500)

    rus = (0, .751, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)
    rs = np.logspace(-2, 4)
    lrs = [1/(1+0.1206*re**0.59 ) for re in rs]
    calc_ratios = []
    r2s = []
    for ru in rus:
        calc_ratios.append(calc_lambda_lambda_s_nasa(ru))
    rvs = []
    for ru in _interp_ratio_rus:
        r2s.append(calc_lambda_lambda_s_ratio(ru))
        rvs.append(calc_ratio_langmuir_blodgett(ru))

    plt.plot(_interp_ratio_rus, _interp_ratios, 'o', label='Table I values')
    plt.plot(_interp_ratio_rus, rvs, label='Interpolation of Table I')
    plt.plot(_interp_ratio_rus, r2s, '--', label='DOT/FAA/CT88-8/1 equ. (2-10)')
    plt.plot(rus, calc_ratios, ':', label="NASA/CR-2004-212875 equation (3.12)")
    plt.plot(rs, lrs, 'x', label='LTR-LT-92 Appendix A')

    plt.xscale('log')
    plt.xlabel('K')
    plt.ylabel("Droplet Range/Range_s")
    plt.legend()

    plt.figure()

    cd_r_24_ltr_lt_92 = [1 + 0.212*re**.6 + 2.6e-4*re**1.38 for re in _interp_cd_r_24_rus]

    plt.plot(_interp_cd_r_24_rus, _interp_cd_r_24, 'o', label='Table I values')
    plt.plot(_interp_cd_r_24_rus, [calc_cd_r_24_langmuir_blodgett(re) for re in _interp_cd_r_24_rus], label='Interpolation of Table I')
    plt.plot(_interp_cd_r_24_rus, [calc_cd_r_24(re) for re in _interp_cd_r_24_rus], '--', label="Equation (22)")
    plt.plot(_interp_cd_r_24_rus, cd_r_24_ltr_lt_92, 'x', label="LTR-LT-92 Appendix A")

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('K')
    plt.ylabel("Cd*Re/24")

    plt.legend()

    plt.show()
