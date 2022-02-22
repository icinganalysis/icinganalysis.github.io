"""Interpolate cylinder impingement data in Table II of
Langmuir, Irving, and Blodgett, Katherine B.: A Mathematical Investigation of Water Droplet Trajectories.
Tech. Rep. No. 5418, Air Materiel Command, AAF, Feb. 19, 1946. (Contract No. W-33-038-ac-9151 with General Electric Co.)
"""
from scipy.interpolate import interp1d, interp2d
from math import log10, pi
from icinganalysis.langmuir_blodgett_table_i import calc_ratio_langmuir_blodgett, calc_cd_r_24_langmuir_blodgett

# fmt: off
table_II_original_data = {  # phi values as keys
    0: {
        'ks': (
            0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        'ems': (
            0.002, 0.018, 0.045, 0.129, 0.253, 0.358, 0.506, 0.696, 0.803, 0.864, 0.926, 0.954, 0.976, 0.983, 0.99,
            0.996, 0.998, 0.998),
        'betas': (
            0.048, 0.132, 0.202, 0.321, 0.439, 0.531, 0.66, 0.799, 0.868, 0.909, 0.952, 0.97, 0.984, 0.989, 0.994,
            0.997,
            0.998, 0.999),
        'theta_degree': (
            4.8, 12.8, 20, 32.5, 45.1, 54.5, 66.4, 77.3, 81.6, 84.3, 87.1, 88.2, 89.1, 89.4, 89.6, 89.9, 89.9, 89.9),
    },
    10: {
        'ks': (
            0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        'ems': (
            0.002, 0.015, 0.038, 0.106, 0.214, 0.314, 0.468, 0.655, 0.766, 0.832, 0.901, 0.935, 0.963, 0.973, 0.983,
            0.992, 0.995, 0.996),
        'betas': (
            0.044, 0.121, 0.186, 0.295, 0.404, 0.491, 0.616, 0.759, 0.844, 0.892, 0.939, 0.961, 0.978, 0.984, 0.991,
            0.995,
            0.997, 0.998),
        'theta_degree': (
            4.4, 11.8, 18.3, 29.7, 41.5, 50.5, 62.5, 74.2, 79.4, 82.2, 85.3, 86.9, 88.2, 88.7, 89.2, 89.6, 89.7, 89.8),
    },
    100: {
        'ks': (0.16, 0.25, 0.36, 0.64, 1, 1.96, 3.24, 6.25, 9, 16, 36, 64, 100, 196, 324, 625, 900,),
        'ems': (
            0.004, 0.029, 0.068, 0.181, 0.294, 0.475, 0.591, 0.721, 0.781, 0.855, 0.922, 0.951, 0.966, 0.98, 0.987,
            0.992, 0.994,),
        'betas': (
            0.065, 0.164, 0.246, 0.378, 0.478, 0.617, 0.705, 0.817, 0.861, 0.912, 0.955, 0.972, 0.981, 0.989, 0.993,
            0.996, 0.997,),
        'theta_degree': (
            6.4, 16.2, 24.5, 38.6, 49.2, 62.6, 70.1, 77, 79.7, 82.9, 86, 87.4, 88.2, 88.9, 89.2, 89.5, 89.7,),
    },
    1000: {
        'ks': (
            0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        'ems': (
            0.001, 0.009, 0.022, 0.062, 0.127, 0.203, 0.340, 0.542, 0.659, 0.737, 0.830, 0.880, 0.925, 0.942, 0.962,
            0.979, 0.986, 0.989),
        'betas': (
            0.048, 0.095, 0.146, 0.233, 0.323, 0.398, .513, 0.68, 0.778, 0.837, 0.901, 0.932, 0.959, 0.969, 0.98, 0.989,
            0.993, 0.995),
        'theta_degree': (
            3.5, 9.2, 14.2, 23.1, 32.3, 39.4, 50.1, 64, 71.6, 76.1, 80.8, 83.4, 85.9, 87, 87.8, 88.7, 89.1, 89.4),
    },
    10000: {
        'ks': (0.16, 0.25, 0.36, 0.64, 1, 1.96, 3.24, 6.25, 9, 16, 36, 64, 100, 196, 324, 625, 900),
        'ems': (
            0.001, 0.012, 0.03, 0.08, 0.148, 0.28, 0.394, 0.546, 0.62, 0.717, 0.82, 0.873, 0.904, 0.937, 0.954, 0.968,
            0.974),
        'betas': (
            0.044, 0.111, 0.168, 0.264, 0.343, 0.476, 0.58, 0.702, 0.759, 0.832, 0.901, 0.933, 0.951, 0.969, 0.977,
            0.985, 0.988),
        'theta_degree': (4.4, 10.8, 16.4, 26.3, 34, 45.6, 54, 63.4, 67.7, 73.7, 79.5, 82.4, 84.2, 85.9, 87, 87.9, 88.3),
    },
    1e5: {  # note that there is a typo "φ = 10^6" in the first part of Table II
        'ks': (
            0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        'ems': (
            0.0002, 0.002, 0.006, 0.019, 0.040, 0.067, 0.135, 0.276, 0.388, 0.475, 0.597, 0.673, 0.753, 0.792, 0.840,
            0.890, 0.917, 0.933),
        'betas': (
            0.019, 0.054, 0.083, 0.135, 0.192, 0.243, 0.33, 0.476, 0.582, 0.657, 0.756, 0.811, 0.866, 0.89, 0.919,
            0.947,
            0.961, 0.969),
        'theta_degree': (
            2.1, 5.3, 8.1, 13.2, 18.8, 23.9, 32.3, 44.5, 52.4, 53, 65.4, 69.9, 74.7, 77, 79.8, 83, 84.6, 85.5),
    },
    1e6: {
        'ks': (0.16, 0.25, 0.36, 0.64, 1, 1.96, 3.24, 6.25, 9, 16, 36, 64, 100, 196, 324, 625, 900,),
        'ems': (
            0.0002, 0.002, 0.006, 0.018, 0.033, 0.074, 0.123, 0.215, 0.271, 0.354, 0.46, 0.528, 0.582, 0.659, 0.71,
            0.773, 0.821,),
        'betas': (
            0.021, 0.054, 0.082, .122, .161, .236, .302, .393, .448, 0.531, 0.641, 0.711, 0.757, 0.814, 0.849, 0.887,
            0.906,),
        'theta_degree': (
            2.2, 5.3, 8, 12.8, 17, 23.4, 28.6, 36.2, 40.5, 47.4, 56.5, 62.3, 66.2, 71.1, 74.4, 77.6, 79.1),
    },
}
# fmt: on
# fmt: off
table_II_data = {  # phi values as keys, table II made non-jagged and added initial point
    0: {
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0000, 0.0020, 0.0180, 0.0450, 0.1290, 0.2530, 0.3580, 0.5060, 0.6960, 0.8030, 0.8640, 0.9260, 0.9540,
            0.9760, 0.9830, 0.9900, 0.9960, 0.9980, 0.9980),
        "betas": (
            0.0081, 0.0480, 0.1320, 0.2020, 0.3210, 0.4390, 0.5310, 0.6600, 0.7990, 0.8680, 0.9090, 0.9520, 0.9700,
            0.9840, 0.9890, 0.9940, 0.9970, 0.9980, 0.9990),
        "theta_degree": (
            1.2, 4.8, 12.8, 20.0, 32.5, 45.1, 54.5, 66.4, 77.3, 81.6, 84.3, 87.1, 88.2, 89.1, 89.4, 89.6, 89.9, 89.9,
            89.9),
    },
    10: {
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0008, 0.0020, 0.0150, 0.0380, 0.1060, 0.2140, 0.3140, 0.4680, 0.6550, 0.7660, 0.8320, 0.9010, 0.9350,
            0.9630, 0.9730, 0.9830, 0.9920, 0.9950, 0.9960),
        "betas": (
            0.0078, 0.0440, 0.1210, 0.1860, 0.2950, 0.4040, 0.4910, 0.6160, 0.7590, 0.8440, 0.8920, 0.9390, 0.9610,
            0.9780, 0.9840, 0.9910, 0.9950, 0.9970, 0.9980),
        "theta_degree": (
            1.0, 4.4, 11.8, 18.3, 29.7, 41.5, 50.5, 62.5, 74.2, 79.4, 82.2, 85.3, 86.9, 88.2, 88.7, 89.2, 89.6, 89.7,
            89.8),
    },
    100: {
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0000, 0.0014, 0.0126, 0.0310, 0.0842, 0.1755, 0.2662, 0.4224, 0.6135, 0.7252, 0.7964, 0.8755, 0.9152,
            0.9500, 0.9629, 0.9765, 0.9881, 0.9921, 0.9945),
        "betas": (
            0.0108, 0.0418, 0.1099, 0.1693, 0.2700, 0.3726, 0.4547, 0.5781, 0.7262, 0.8171, 0.8099, 0.9382, 0.9527,
            0.9714, 0.9792, 0.9870, 0.9936, 0.9961, 0.9972),
        "theta_degree": (
            1.1, 4.1, 10.8, 16.7, 27.0, 38.0, 46.8, 59.0, 71.4, 77.2, 80.4, 83.8, 85.7, 87.4, 88.0, 88.7, 89.3, 89.5,
            89.8),
    },
    1000: {
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0000, 0.0010, 0.0090, 0.0220, 0.0620, 0.1270, 0.2030, 0.3400, 0.5420, 0.6590, 0.7370, 0.8300, 0.8800,
            0.9250, 0.9420, 0.9620, 0.9790, 0.9860, 0.9890),
        "betas": (
            0.0313, 0.0480, 0.0950, 0.1460, 0.2330, 0.3230, 0.3980, 0.5130, 0.6800, 0.7780, 0.8370, 0.9010, 0.9320,
            0.9590, 0.9690, 0.9800, 0.9890, 0.9930, 0.9950),
        "theta_degree": (
            0.9, 3.5, 9.2, 14.2, 23.1, 32.3, 39.4, 50.1, 64.0, 71.6, 76.1, 80.8, 83.4, 85.9, 87.0, 87.8, 88.7, 89.1,
            89.4),
    },
    10000: {
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0000, 0.0001, 0.0045, 0.0129, 0.0369, 0.0771, 0.1302, 0.2373, 0.4186, 0.5511, 0.6395, 0.7462, 0.8086,
            0.8711, 0.8974, 0.9284, 0.9568, 0.9684, 0.9756),
        "betas": (
            0.0081, 0.0286, 0.0741, 0.1146, 0.1850, 0.2599, 0.3237, 0.4346, 0.6009, 0.7060, 0.7739, 0.8527, 0.8938,
            0.9319, 0.9472, 0.9646, 0.9784, 0.9852, 0.9887),
        "theta_degree": (
            1.0, 3.0, 7.3, 11.2, 18.1, 25.9, 32.2, 42.1, 55.6, 63.7, 68.9, 75.4, 78.9, 82.3, 83.8, 85.4, 87.2, 87.9,
            88.4),
    },
    1e5: {  # note that there is a typo "φ = 10^6" in the first part of Table II
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0003, 0.0002, 0.0020, 0.0060, 0.0190, 0.0400, 0.0670, 0.1350, 0.2760, 0.3880, 0.4750, 0.5970, 0.6730,
            0.7530, 0.7920, 0.8400, 0.8900, 0.9170, 0.9330),
        "betas": (
            0.0000, 0.0190, 0.0540, 0.0380, 0.1350, 0.1920, 0.2430, 0.3300, 0.4760, 0.5820, 0.6570, 0.7560, 0.8110,
            0.8660, 0.8900, 0.9190, 0.9470, 0.9610, 0.9690),
        "theta_degree": (
            6.4, 2.1, 5.3, 18.1, 13.2, 18.8, 23.9, 32.3, 44.5, 52.4, 53.0, 65.4, 69.9, 74.7, 77.0, 79.8, 83.0, 84.6,
            85.5),
    },
    1e6: {
        'ks': (
            0.125, 0.144, 0.196, 0.256, 0.4, 0.625, 0.9, 1.6, 3.6, 6.4, 10, 19.6, 32.4, 62.5, 90, 160, 360, 640, 1000),
        "ems": (
            0.0006, 0.0003, 0.0006, 0.0022, 0.0077, 0.0174, 0.0287, 0.0589, 0.1358, 0.2186, 0.2868, 0.3817, 0.4470,
            0.5252, 0.5693, 0.6367, 0.7199, 0.7758, 0.8371),
        "betas": (
            0.0038, 0.0136, 0.0357, 0.0558, 0.0895, 0.1202, 0.1510, 0.2115, 0.3162, 0.3965, 0.4636, 0.5593, 0.6273,
            0.7083, 0.7468, 0.7981, 0.8556, 0.8883, 0.9113),
        "theta_degree": (
            0.6, 1.5, 3.6, 5.5, 8.8, 12.6, 16.0, 21.4, 29.8, 36.5, 41.8, 49.8, 55.4, 62.1, 65.3, 69.7, 75.0, 77.7,
            79.5),
    },
}
# fmt: on

log10_ks = [log10(_) for _ in table_II_data[0]['ks']]
log10_phis = [log10(_) if _ > 0 else -1 for _ in table_II_data]
zs = [table_II_data[_]['ems'] for _ in table_II_data]
_em_interpolator = interp2d(log10_ks, log10_phis, zs,
                            kind='cubic'
                            )
zs = [table_II_data[_]['betas'] for _ in table_II_data]
_beta_interpolator = interp2d(log10_ks, log10_phis, zs, kind='cubic')
zs = [table_II_data[_]['theta_degree'] for _ in table_II_data]
_theta_degree_interpolator = interp2d(log10_ks, log10_phis, zs, kind='cubic')


def calc_em(k, phi):
    return max(0, _em_interpolator(log10(k), log10(phi) if phi > 0 else -1))


def calc_beta_o(k, phi):
    return max(0, _beta_interpolator(log10(k), log10(phi) if phi > 0 else -1))


def calc_theta_degree(k, phi):
    return max(0, _theta_degree_interpolator(log10(k), log10(phi) if phi > 0 else -1))


def lt_ltr_92_em(k, phi):
    re = (k * phi) ** 0.5
    ratio = 1 / (1 + 0.1206 * re ** 0.59)
    ko = 0.125 + (k - 0.125) * ratio
    em = 0.457 * (log10(8 * ko)) ** 1.634
    if ko < 0.125:
        return 0
    # if k > 3:  # what Appendix A says, but it does not work well
    if em > 0.5:  # what Langmuir-Blodgett uses
        cd_r_24_ltr_lt_92 = 1 + 0.212 * re ** .6 + 2.6e-4 * re ** 1.38
        he = pi / 2 + 0.121 * re ** 0.6 + 0.754e-4 * re ** 1.38
        em = k / (k + he)
    return em


# fmt: off
delta_em_interpolator = interp1d(  # Table V em, delta_em values
    (0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5),
    (0, 0, 0.005, 0.013, 0.02, 0.023, 0.02, 0.015, 0.010, 0.005,
     -0.010  # added point
     )
)
# fmt: on


def calc_em_langmuir_blodgett(k, phi):
    re = (k * phi) ** 0.5
    ratio = calc_ratio_langmuir_blodgett(re)
    ko = 0.125 + (k - 0.125) * ratio
    if ko < 0.125:
        return 0
    em = 0.466 * (log10(8 * ko)) ** 2  # equ. (33)
    if k > 1.1 and phi < 10:  # Hmm, this part does not seem to do much...
        em = ko / (ko + pi / 2)  # equ. (34)
    if em > 0.5:
        cd_r_24 = calc_cd_r_24_langmuir_blodgett(re)
        he = 1 + 0.5708 * cd_r_24 - 0.73e-4 * re ** 1.38  # equ. (43)
        em = k / (k + he)  # equ. (42)
    else:
        delta_em = delta_em_interpolator(em)  # Table V corrections
        em += delta_em
    return em

# fmt: off
table_XI_data = {  # K*phi values as keys
    0: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.04, 0.187, 0.385, 0.56, 0.761, 0.864, 0.927, 0.97, 0.984),
        'em_b': (0.059, 0.192, 0.372, 0.548, 0.747, 0.852, 0.918, 0.963,),
        'em_c': (0.078, 0.202, 0.372, 0.536, 0.731, 0.837, 0.906, 0.959,),
        'em_d': (0.1, 0.216, 0.371, 0.53, 0.716, 0.821, 0.894, 0.951,),
        'em_e': (0.12, 0.233, 0.376, 0.523, 0.699, 0.803, 0.878, 0.942,),
    },
    20: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.03, 0.137, 0.326, 0.522, 0.729, 0.843, 0.916, 0.963, 0.983),
        'em_b': (0.044, 0.148, 0.319, 0.505, 0.714, 0.829, 0.902, 0.956,),
        'em_c': (0.059, 0.163, 0.32, 0.494, 0.699, 0.813, 0.892, 0.952,),
        'em_d': (0.077, 0.18, 0.328, 0.49, 0.682, 0.797, 0.878, 0.942,),
        'em_e': (0.099, 0.201, 0.336, 0.485, 0.668, 0.779, 0.861, 0.933,),
    },
    200: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.021, 0.101, 0.271, 0.478, 0.694, 0.822, 0.904, 0.961, 0.983),
        'em_b': (0.031, 0.116, 0.272, 0.46, 0.679, 0.807, 0.892, 0.955,),
        'em_c': (0.044, 0.131, 0.277, 0.452, 0.665, 0.791, 0.879, 0.948,),
        'em_d': (0.061, 0.151, 0.289, 0.45, 0.65, 0.775, 0.865, 0.938,),
        'em_e': (0.08, 0.172, 0.306, 0.448, 0.638, 0.758, 0.846, 0.925,),
    },
    1000: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.0150, 0.076, 0.226, 0.42, 0.656, 0.796, 0.886, 0.951, 0.985),
        'em_b': (0.0231, 0.0906, 0.2301, 0.409, 0.644, 0.781, 0.873, 0.943,),
        'em_c': (0.0335, 0.107, 0.237, 0.406, 0.629, 0.764, 0.86, 0.937,),
        'em_d': (0.0481, 0.124, 0.251, 0.409, 0.615, 0.747, 0.845, 0.927,),
        'em_e': (0.0660, 0.146, 0.267, 0.411, 0.605, 0.729, 0.826, 0.913,),
    },
    3000: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.011, 0.06, 0.186, 0.373, 0.624, 0.767, 0.87, 0.943, 0.971),
        'em_b': (0.0171, 0.072, 0.193, 0.366, 0.606, 0.751, 0.856, 0.935,),
        'em_c': (0.0256, 0.087, 0.204, 0.365, 0.593, 0.735, 0.841, 0.925,),
        'em_d': (0.039, 0.105, 0.22, 0.371, 0.582, 0.719, 0.826, 0.914,),
        'em_e': (0.054, 0.131, 0.249, 0.39, 0.58, 0.711, 0.807, 0.898,),
    },
    10000: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.009, 0.044, 0.149, 0.314, 0.582, 0.736, 0.848, 0.932, 0.965),
        'em_b': (0.0125, 0.0541, 0.155, 0.313, 0.556, 0.715, 0.83, 0.921,),
        'em_c': (0.0193, 0.0677, 0.167, 0.318, 0.546, 0.7, 0.816, 0.914,),
        'em_d': (0.0296, 0.083, 0.185, 0.327, 0.536, 0.684, 0.799, 0.898,),
        'em_e': (0.0426, 0.1036, 0.203, 0.336, 0.532, 0.668, 0.781, 0.88,),
    },
}
# fmt: on

# make a non-jagged version of Table II
phi_em_ints = {
    phi: interp1d(
        [log10(_) for _ in table_II_original_data[phi]["ks"]],
        table_II_original_data[phi]["ems"],
        kind="quadratic",
        fill_value="extrapolate",
    )
    for phi in table_II_data
}

phi_beta_ints = {
    phi: interp1d(
        [log10(_) for _ in table_II_original_data[phi]["ks"]],
        table_II_original_data[phi]["betas"],
        kind="quadratic",
        fill_value="extrapolate",
    )
    for phi in table_II_data
}

phi_theta_ints = {
    phi: interp1d(
        [log10(_) for _ in table_II_original_data[phi]["ks"]],
        table_II_original_data[phi]["theta_degree"],
        kind="quadratic",
        fill_value="extrapolate",
    )
    for phi in table_II_data
}


def value_interpolator(k, phi, v='ems'):
    phis = list(table_II_original_data.keys())
    if phi <= phis[2]:
        phis = phis[:4]
    elif phi <= phis[3]:
        phis = phis[1:5]
    elif phi <= phis[4]:
        phis = phis[2:6]
    else:
        phis = phis[3:7]
    interpolator_selected = {'ems': phi_em_ints, 'betas': phi_beta_ints, 'theta_degree': phi_theta_ints}[v]
    eks = [interpolator_selected[_](log10(k)) for _ in phis]
    xs = [log10(_) if _ > 0 else -1 for _ in phis]
    value = interp1d(xs, eks, kind="quadratic", fill_value="extrapolate")(
        log10(phi) if phi > 0 else -1
    )
    return value


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from numpy import logspace

    for phi in table_II_data:
        print(phi)
        ks = table_II_data[0]['ks']
        ems = [value_interpolator(k, phi, 'ems') for k in ks]
        betas = [value_interpolator(k, phi, 'betas') for k in ks]
        theta_degree = [value_interpolator(k, phi, 'theta_degree') for k in ks]
        print('"ems":', '(' + ', '.join([f"{max(0, float(_)):.4f}" for _ in ems]) + '),')
        print('"betas":', '(' + ', '.join([f"{max(0, float(_)):.4f}" for _ in betas]) + '),')
        print('"theta_degree":', '(' + ', '.join([f"{max(0, float(_)):.1f}" for _ in theta_degree]) + '),')

    plt.figure()
    plt.suptitle('Verify interpolation in Table II data')
    for phi in table_II_original_data:
        ks = table_II_original_data[phi]['ks']
        line, = plt.plot(ks, table_II_original_data[phi]['ems'], 'o', label=f"Table II data phi={phi:.0f}")
        em_calcs = [calc_em(k, phi) for k in ks]
        plt.plot(ks, em_calcs, '--', c=line.get_color())

    plt.plot([], [], '--', c='k', label='interpolated')
    plt.xscale('log')
    plt.xlabel('K')
    plt.ylabel('Em')
    plt.legend()

    plt.figure()
    plt.suptitle('Comparison to Table XI data')
    for k_phi in table_XI_data:
        inv_ks = table_XI_data[k_phi]['inv_ks']
        ems = [calc_em(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        line, = plt.plot(inv_ks, ems, 'o', label=f'Table XI data k*phi={k_phi:.0f}')
        inv_ks = logspace(-2.5, log10(8), 100)
        ems = [calc_em(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        plt.plot(inv_ks, ems, '-', c=line.get_color())
        ems2 = [calc_em_langmuir_blodgett(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        plt.plot(inv_ks, ems2, '--', c=line.get_color())
        ems3 = [lt_ltr_92_em(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        plt.plot(inv_ks, ems3, ':', c=line.get_color())

    plt.plot([], [], '-', c='k', label='Calculated from Table II interpolation')
    plt.plot([], [], '--', c='k', label='Calculated from Langmuir-Blodgett')
    plt.plot([], [], ':', c='k', label='Calculated from LTR-LT-92 equations')
    plt.xscale('log')
    plt.xlabel('1/K')
    plt.ylabel('Em')
    plt.legend()

    plt.figure()
    plt.suptitle('Comparison to Table XI data')
    for k_phi in table_XI_data:
        inv_ks = table_XI_data[k_phi]['inv_ks']
        ems = [calc_em(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        line, = plt.plot(inv_ks, ems, 'o', label=f'Table XI data k*phi={k_phi:.0f}')
        inv_ks = logspace(-2.5, log10(8), 100)
        ems = [calc_em(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        plt.plot(inv_ks, ems, '-', c=line.get_color())
        ems2 = [calc_em_langmuir_blodgett(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        plt.plot(inv_ks, ems2, '--', c=line.get_color())
        ems3 = [lt_ltr_92_em(1 / inv_k, k_phi * inv_k) for inv_k in inv_ks]
        plt.plot(inv_ks, ems3, ':', c=line.get_color())

    plt.plot([], [], '-', c='k', label='Calculated from Table II interpolation')
    plt.plot([], [], '--', c='k', label='Calculated from Langmuir-Blodgett')
    plt.plot([], [], ':', c='k', label='Calculated from LTR-LT-92 equations')
    plt.xscale('log')
    plt.xlabel('1/K')
    plt.yscale('log')
    plt.ylabel('Em')
    plt.ylim(0.001, 1)
    plt.legend()

    plt.show()
