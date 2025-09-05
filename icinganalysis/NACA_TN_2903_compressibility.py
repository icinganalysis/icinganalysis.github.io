from math import log10
from scipy.interpolate import interp2d, RectBivariateSpline
import numpy as np

data_fig_4 = {  # phi
    0: {
        'ks': (.1, 1, 4, 5, 7, 10, 20, 100, 1000),
        'delta_em': (0, .0010, .0048, .0050, .0048, .004, .002, .0005, 0)
    },
    100: {
        'ks': (.1, 1, 4, 5, 7, 10, 20, 100, 1000),
        'delta_em': (0, .0045, .0100, .0105, .0100, .007, .004, .001, 0)
    },
    1000: {
        'ks': (.1, 1, 4, 5, 7, 10, 20, 100, 1000),
        'delta_em': (0, .0065, .0175, .0175, .0160, .011, .0055, .0022, 0)
    },
    10000: {
        'ks': (.1, 1, 4, 5, 7, 10, 20, 100, 1000),
        'delta_em': (0, .0100, .0235, .0240, .0200, .015, .008, .003, 0)
    },
    50000: {
        'ks': (.1, 1, 4, 5, 7, 10, 20, 100, 1000),
        'delta_em': (0, .0120, .0290, .0300, .0280, .020, .01, .0035, 0)
    },
}

l10phi_for_phi_0 = 0

# _delta_em_interp = interp2d(
#     [log10(k) for k in data_fig_4[0]['ks']],
#     [log10(phi) if phi > 10 ** l10phi_for_phi_0 else l10phi_for_phi_0 for phi in data_fig_4],
#     [data_fig_4[phi]['delta_em'] for phi in data_fig_4]
# )

_delta_em_interp = lambda lk, lphi: RectBivariateSpline([log10(k) for k in data_fig_4[0]['ks']],
    [log10(phi) if phi > 10 ** l10phi_for_phi_0 else l10phi_for_phi_0 for phi in data_fig_4],
    np.array([data_fig_4[phi]['delta_em'] for phi in data_fig_4]).T, kx=3, ky=3)(
        lk, lphi
    ).T[0, 0]


def calc_delta_em(k, phi):
    delta_em = _delta_em_interp(log10(k), log10(phi) if phi > 10 ** l10phi_for_phi_0 else l10phi_for_phi_0)
    return delta_em
