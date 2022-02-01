from math import log10
from icinganalysis.langmuir_cylinder_values import calc_k, calc_phi
from icinganalysis.langmuir_cylinder_values import (
    get_mids,
    langmuir_lwc_fractions,
    valid_distribution_ids,
)
from icinganalysis import langmuir_blodgett_table_ii
from icinganalysis import NACA_TR_1215_fig_24_conditions
from icinganalysis.NACA_TN_2903_compressibility import calc_delta_em
from icinganalysis.NACA_TN_2903_compressibility import data_fig_4
from scipy.interpolate import interp1d, interp2d

# fmt: off
data_table_iv_original = {  # k*phi
    0: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01),
        'ems_a': (.051, .205, .380, .566, .789, .885, .932, .963, .978),
        'ems_b': (.069, .204, .374, .555, .768, .870, .925, .961, .976),
        'ems_c': (.085, .211, .373, .549, .750, .854, .918, .957, .977),
        'ems_d': (.107, .225, .379, .542, .732, .836, .898, .951, .972),
        'ems_e': (.126, .241, .384, .536, .713, .815, .885, .940, .965),
    },
    200: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01),
        'ems_a': (.027, .135, .298, .493, .761, .874, .925, .960, .976),
        'ems_b': (.039, .138, .302, .486, .740, .859, .919, .959, .975),
        'ems_c': (.050, .146, .306, .482, .721, .846, .910, .955, .976),
        'ems_d': (.066, .165, .315, .480, .703, .826, .901, .948, .971),
        'ems_e': (.083, .182, .319, .477, .686, .805, .878, .938, .963),
    },
    1000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01),
        'ems_a': (.019, .109, .251, .460, .714, .830, .908, .953, .971),
        'ems_b': (.029, .109, .252, .452, .697, .816, .899, .953, .972),
        'ems_c': (.038, .122, .359, .423, .677, .800, .892, .949, .973),
        'ems_d': (.050, .138, .271, .477, .661, .783, .876, .943, .967),
        'ems_e': (.065, .154, .283, .447, .643, .763, .862, .933, .962),
    },

    3000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01),
        'ems_a': (.013, .085, .218, .409, .687, .815, .884, .945, .968),
        'ems_b': (.020, .090, .225, .416, .668, .797, .878, .940, .966),
        'ems_c': (.027, .100, .235, .410, .652, .785, .867, .938, .970),
        'ems_d': (.039, .111, .244, .415, .641, .766, .855, .921, .964),
        'ems_e': (.048, .130, .251, .413, .623, .746, .839, .918, .954),
    },
    10000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01),
        'ems_a': (.008, .057, .157, .350, .645, .778, .865, .920, .952),
        'ems_b': (.013, .060, .163, .356, .630, .764, .857, .920, .950),
        'ems_c': (.017, .072, .172, .357, .615, .748, .849, .918, .955),
        'ems_d': (.023, .083, .188, .362, .599, .731, .830, .909, .946),
        'ems_e': (.034, .092, .202, .368, .591, .713, .816, .899, .939),
    },
}

# fmt: off
data_table_iv_augmented = {  # k*phi
    0: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, 0.0001),
        'ems_a': (.000, .051, .205, .380, .566, .789, .885, .932, .963, .978, .99, .999),
        'ems_b': (.000, .069, .204, .374, .555, .768, .870, .925, .961, .976, .99, .999),
        'ems_c': (.000, .085, .211, .373, .549, .750, .854, .918, .957, .977, .99, .999),
        'ems_d': (.000, .107, .225, .379, .542, .732, .836, .898, .951, .972, .99, .999),
        'ems_e': (.000, .126, .241, .384, .536, .713, .815, .885, .940, .965, .99, .999),
    },
    200: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, .0001),
        'ems_a': (.000, .027, .135, .298, .493, .761, .874, .925, .960, .976, .99, .999),
        'ems_b': (.000, .039, .138, .302, .486, .740, .859, .919, .959, .975, .99, .999),
        'ems_c': (.000, .050, .146, .306, .482, .721, .846, .910, .955, .976, .99, .999),
        'ems_d': (.000, .066, .165, .315, .480, .703, .826, .901, .948, .971, .99, .999),
        'ems_e': (.000, .083, .182, .319, .477, .686, .805, .878, .938, .963, .99, .999),
    },
    1000: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, .0001),
        'ems_a': (.000, .019, .109, .251, .460, .714, .830, .908, .953, .971, .99, .999),
        'ems_b': (.000, .029, .109, .252, .452, .697, .816, .899, .953, .972, .99, .999),
        'ems_c': (.000, .038, .122, .359, .423, .677, .800, .892, .949, .973, .99, .999),
        'ems_d': (.000, .050, .138, .271, .477, .661, .783, .876, .943, .967, .99, .999),
        'ems_e': (.000, .065, .154, .283, .447, .643, .763, .862, .933, .962, .99, .999),
    },

    3000: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, .0001),
        'ems_a': (.000, .013, .085, .218, .409, .687, .815, .884, .945, .968, .99, .999),
        'ems_b': (.000, .020, .090, .225, .416, .668, .797, .878, .940, .966, .99, .999),
        'ems_c': (.000, .027, .100, .235, .410, .652, .785, .867, .938, .970, .99, .999),
        'ems_d': (.000, .039, .111, .244, .415, .641, .766, .855, .921, .964, .99, .999),
        'ems_e': (.000, .048, .130, .251, .413, .623, .746, .839, .918, .954, .99, .999),
    },
    10000: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, .0001),
        'ems_a': (.000, .008, .057, .157, .350, .645, .778, .865, .920, .952, .99, .999),
        'ems_b': (.000, .013, .060, .163, .356, .630, .764, .857, .920, .950, .99, .999),
        'ems_c': (.000, .017, .072, .172, .357, .615, .748, .849, .918, .955, .99, .999),
        'ems_d': (.000, .023, .083, .188, .362, .599, .731, .830, .909, .946, .99, .999),
        'ems_e': (.000, .034, .092, .202, .368, .591, .713, .816, .899, .939, .99, .999),
    },
    50000: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, .0001),
        'ems_a': (.000, 0.005, 0.038, 0.105, 0.254, 0.534, 0.714, 0.825, 0.901, 0.939, 1.000, 1.),
        'ems_b': (.000, 0.010, 0.043, 0.112, 0.255, 0.520, 0.699, 0.815, 0.898, 0.936, 0.998, .999),
        'ems_c': (.000, 0.015, 0.050, 0.120, 0.260, 0.511, 0.684, 0.803, 0.893, 0.934, 0.996, .999),
        'ems_d': (.000, 0.022, 0.062, 0.135, 0.271, 0.506, 0.670, 0.789, 0.886, 0.930, 0.994, .999),
        'ems_e': (.000, 0.031, 0.075, 0.149, 0.281, 0.499, 0.654, 0.773, 0.875, 0.924, 0.992, .999),
    },
    200000: {
        'inv_ks': (8, 4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001, .0001),
        'ems_a': (0.000, 0.005, 0.038, 0.105, 0.223, 0.445, 0.643, 0.783, 0.879, 0.925, 0.996, 1.00),
        'ems_b': (0.001, 0.010, 0.043, 0.112, 0.225, 0.436, 0.628, 0.769, 0.874, 0.922, 0.994, 1.00),
        'ems_c': (0.002, 0.015, 0.050, 0.120, 0.231, 0.432, 0.614, 0.756, 0.868, 0.918, 0.992, 1.00),
        'ems_d': (0.005, 0.022, 0.062, 0.135, 0.242, 0.432, 0.603, 0.742, 0.860, 0.914, 0.990, 1.00),
        'ems_e': (0.010, 0.031, 0.075, 0.149, 0.254, 0.430, 0.591, 0.725, 0.848, 0.906, 0.987, 1.00),
    },
}


data_fig_6 = {  # phi
    0: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320, 500, 10000),
        'ems': (0, .0515, .205, .38, .74, .92, .96, .99, .992, .9999),
    },
    100: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320, 500, 10000),
        'ems': (0, .0365, .155, .31, .685, .875, .925, .98, .985, .998),
    },
    1000: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320, 500, 10000),
        'ems': (0, .026, .1175, .25, .615, .83, .89, .97, .978, .993),
    },
    10000: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320, 500, 10000),
        'ems': (0, .014, .073, .155, .48, .755, .845, .955, .966, .99),
    },
    50000: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320, 500, 10000),
        'ems': (0, .007, .04, .105, .38, .68, .795, .94, .955, .987),
    }
}

data_fig_6a = {  # phi
    0: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320),
        'ems': (0, .0515, .205, .38, .74, .92, .96, .99),
    },
    100: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320),
        'ems': (0, .0365, .155, .31, .685, .875, .925, .98),
    },
    1000: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320),
        'ems': (0, .026, .1175, .25, .615, .83, .89, .97),
    },
    10000: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320),
        'ems': (0, .014, .073, .155, .48, .755, .845, .955),
    },
    50000: {
        'ks': (.125, .25, .5, 1, 4, 16, 40, 320),
        'ems': (0, .007, .04, .105, .38, .68, .795, .94),
    }
}
# fmt: on

l10phi_for_phi_0 = 0

log10_ks = [log10(k) for k in data_fig_6[0]["ks"]]
log10_phis = [log10(_) if _ > 0 else l10phi_for_phi_0 for _ in data_fig_6]
phis = [_ for _ in data_fig_6]
zs = [data_fig_6[_]["ems"] for _ in data_fig_6]

_em_interpolator_log10 = interp2d(log10_ks, log10_phis, zs, kind="cubic")


def calc_em_naca_tn_2904_from_figure6_data(k, phi, include_compressibility=False):
    partial_em = float(
        max(
            0,
            _em_interpolator_log10(
                log10(k), log10(phi) if phi > 0 else l10phi_for_phi_0,
            ),
        )
    )
    delta_em = 0
    if include_compressibility:
        delta_em = calc_delta_em(k, phi)
    return float(partial_em + delta_em)


def calc_em_naca_tn_2904_from_with_distribution_fig6_data(
    k, phi, distribution="Langmuir A", include_compressibility=False
):
    mids = get_mids(distribution)
    em = 0
    for d_drop_ratio, w in zip(mids, langmuir_lwc_fractions):
        em_partial = calc_em_naca_tn_2904_from_figure6_data(
            k * d_drop_ratio ** 2, phi, include_compressibility
        )
        em += w * em_partial
    return min(1, max(em, 0))


def calc_em_naca_tn_2904_fig_6_data(tk, p, u, mvd, d_cylinder, include_compressibility=False):
    return calc_em_naca_tn_2904_from_figure6_data(
        calc_k(tk, u, mvd, d_cylinder),
        calc_phi(tk, p, u, d_cylinder),
        include_compressibility,
    )


def calc_em_naca_tn_2904_with_distribution_fig6_data(
    tk, p, u, mvd, d_cylinder, distribution="Langmuir A", include_compressibility=False
):
    mids = get_mids(distribution)
    em = 0
    for d_drop_ratio, w in zip(mids, langmuir_lwc_fractions):
        em += w * calc_em_naca_tn_2904_fig_6_data(
            tk, p, u, mvd * d_drop_ratio, d_cylinder, include_compressibility
        )
    return em


l10phi_for_k_phi_0 = 0

log10_ks = [log10(inv_k) for inv_k in data_table_iv_augmented[0]["inv_ks"]]
log10_phis = [log10(_) if _ > 0 else l10phi_for_phi_0 for _ in data_table_iv_augmented]
k_phis = [_ for _ in data_table_iv_augmented]
zsa = [data_table_iv_augmented[_]["ems_a"] for _ in data_table_iv_augmented]
_em_interpolator_k_phi_a_log10 = interp2d(log10_ks, log10_phis, zsa, kind="cubic")
zsb = [data_table_iv_augmented[_]["ems_b"] for _ in data_table_iv_augmented]
_em_interpolator_k_phi_b_log10 = interp2d(log10_ks, log10_phis, zsb, kind="cubic")
zsc = [data_table_iv_augmented[_]["ems_c"] for _ in data_table_iv_augmented]
_em_interpolator_k_phi_c_log10 = interp2d(log10_ks, log10_phis, zsc, kind="cubic")
zsd = [data_table_iv_augmented[_]["ems_d"] for _ in data_table_iv_augmented]
_em_interpolator_k_phi_d_log10 = interp2d(log10_ks, log10_phis, zsd, kind="cubic")
zse = [data_table_iv_augmented[_]["ems_e"] for _ in data_table_iv_augmented]
_em_interpolator_k_phi_e_log10 = interp2d(log10_ks, log10_phis, zse, kind="cubic")
_k_phi_interpolators = {
    "Langmuir A": _em_interpolator_k_phi_a_log10,
    "Langmuir B": _em_interpolator_k_phi_b_log10,
    "Langmuir C": _em_interpolator_k_phi_c_log10,
    "Langmuir D": _em_interpolator_k_phi_d_log10,
    "Langmuir E": _em_interpolator_k_phi_e_log10,
}

kind = "linear"
kind = "quadratic"
kind = "cubic"
_k_interps = {
    "Langmuir A": (
        interp1d(
            log10_ks,
            data_table_iv_augmented[0]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[1000]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[3000]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[10000]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[50000]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200000]["ems_a"],
            kind,
            fill_value="extrapolate",
        ),
    ),
    "Langmuir B": (
        interp1d(
            log10_ks,
            data_table_iv_augmented[0]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[1000]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[3000]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[10000]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[50000]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200000]["ems_b"],
            kind,
            fill_value="extrapolate",
        ),
    ),
    "Langmuir C": (
        interp1d(
            log10_ks,
            data_table_iv_augmented[0]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[1000]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[3000]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[10000]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[50000]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200000]["ems_c"],
            kind,
            fill_value="extrapolate",
        ),
    ),
    "Langmuir D": (
        interp1d(
            log10_ks,
            data_table_iv_augmented[0]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[1000]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[3000]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[10000]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[50000]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200000]["ems_d"],
            kind,
            fill_value="extrapolate",
        ),
    ),
    "Langmuir E": (
        interp1d(
            log10_ks,
            data_table_iv_augmented[0]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[1000]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[3000]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[10000]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[50000]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
        interp1d(
            log10_ks,
            data_table_iv_augmented[200000]["ems_e"],
            kind,
            fill_value="extrapolate",
        ),
    ),
}

lkphis = [
    log10(_) for _ in (10 ** l10phi_for_k_phi_0, 200, 1000, 3000, 10000, 50000, 200000)
]


def ie(k, k_phi, distribution="Langmuir A"):
    ems = [ki(log10(1 / k)) for ki in _k_interps[distribution]]

    _ip = interp1d(
        lkphis,
        ems,
        kind="linear",
        # kind='quadratic',
        fill_value="extrapolate",
        # fill_value=float('nan'),
        bounds_error=False,
    )
    return _ip(log10(k_phi) if k_phi > 0 else l10phi_for_k_phi_0)


def calc_em(tk, p, u, mvd, cylinder_diameter, distribution="Langmuir A"):
    k = calc_k(tk, u, mvd, cylinder_diameter)
    k_phi = k * calc_phi(tk, p, u, cylinder_diameter)
    em = min(1, max(0, calc_em_from(k, k_phi, distribution)))
    return em


def calc_em_from(k, k_phi, distribution="Langmuir A"):
    em = min(1, max(0, ie(k, k_phi, distribution)))
    return em


interpolators = {
    phi: interp1d(
        [log10(k) for k in d["ks"]], d["ems"], "cubic", fill_value="extrapolate"
    )
    for phi, d in data_fig_6.items()
}


def make_markdown_table(header, rows):
    text = "|".join(header) + "\n"
    text += "|".join(["---"] * len(header)) + "\n"
    for row in rows:
        text += "|".join([str(_) for _ in row]) + "\n"
    return text


def make_table_iii():
    k_phi = 3000
    distribution = "Langmuir C"
    for i, inv_k in enumerate(data_table_iv_augmented[k_phi]["inv_ks"]):
        phi = k_phi * inv_k
        emc = calc_em_naca_tn_2904_from_figure6_data(1 / inv_k, phi)
        emy = ie(1 / inv_k, k_phi, distribution)
        k0 = 1 / inv_k
        ems = 0
        emz = 0
        for dr, w in zip(get_mids(distribution), langmuir_lwc_fractions):
            k = k0 * dr ** 2
            ems += w * calc_em_naca_tn_2904_from_figure6_data(k, k_phi / k0)
            # emz +=
        print(
            k_phi,
            phi,
            inv_k,
            distribution,
            ems,
            emy,
            data_table_iv_augmented[k_phi]["ems_c"][i],
        )
    k_phi = 50000
    for distribution in valid_distribution_ids:
        ems = []
        for i, inv_k in enumerate(data_table_iv_augmented[0]["inv_ks"]):
            k = 1 / inv_k
            phi = k_phi / k
            k0 = k
            em = 0
            for dr, w in zip(get_mids(distribution), langmuir_lwc_fractions):
                k = k0 * dr ** 2
                em += w * calc_em_naca_tn_2904_from_figure6_data(k, k_phi / k0)
            ems.append(em)
        print(f"{distribution} ems 50000 ", ", ".join([f"{_:.3f}" for _ in ems]))
    k_phi = 200000
    for distribution in valid_distribution_ids:
        ems = []
        for i, inv_k in enumerate(data_table_iv_augmented[0]["inv_ks"]):
            k = 1 / inv_k
            phi = k_phi / k
            k0 = k
            em = 0
            for dr, w in zip(get_mids(distribution), langmuir_lwc_fractions):
                k = k0 * dr ** 2
                em += w * calc_em_naca_tn_2904_from_figure6_data(k, k_phi / k0)
            ems.append(em)
        print(f"{distribution} ems 200000 ", ", ".join([f"{_:.3f}" for _ in ems]))


def make_table_i():
    print("Table I")
    header = ("Phi", "K", "E NACA", "E Langmuir", "Table III")
    print()
    phi = 0
    print(phi)
    rows = []
    for i, k in enumerate((0.25, 0.5, 1, 4, 16, 40, 320)):
        em = calc_em_naca_tn_2904_from_figure6_data(k, phi)
        em_langmuir_blodgett = langmuir_blodgett_table_ii.calc_em(k, phi)
        emx = calc_em_from(k, k * phi)
        print(k, em, em_langmuir_blodgett)
        row = (
            f"{phi:.0f}",
            f"{k:.2f}",
            f"{em:.3f}",
            f"{float(em_langmuir_blodgett):.3f}",
            f"{emx:.3f}",
        )
        rows.append(row)
    print()
    phi = 100
    for i, k in enumerate((0.5, 1, 4, 16)):
        em = calc_em_naca_tn_2904_from_figure6_data(k, phi)
        em_langmuir_blodgett = langmuir_blodgett_table_ii.calc_em(k, phi)
        emx = ie(k, k * phi)
        print(k, em, em_langmuir_blodgett)
        row = (
            f"{phi:.0f}",
            f"{k:.2f}",
            f"{em:.3f}",
            f"{float(em_langmuir_blodgett):.3f}",
            f"{emx:.3f}",
        )
        rows.append(row)
    phi = 1000
    for i, k in enumerate((0.5, 1, 4, 16)):
        em = calc_em_naca_tn_2904_from_figure6_data(k, phi)
        em_langmuir_blodgett = langmuir_blodgett_table_ii.calc_em(k, phi)
        emx = ie(k, k * phi)
        print(k, em, em_langmuir_blodgett)
        row = (
            f"{phi:.0f}",
            f"{k:.2f}",
            f"{em:.3f}",
            f"{float(em_langmuir_blodgett):.3f}",
            f"{emx:.3f}",
        )
        rows.append(row)
    phi = 10000
    for i, k in enumerate((0.5, 1, 4, 16)):
        em = calc_em_naca_tn_2904_from_figure6_data(k, phi)
        em_langmuir_blodgett = langmuir_blodgett_table_ii.calc_em(k, phi)
        emx = ie(k, k * phi)
        print(k, em, em_langmuir_blodgett)
        row = (
            f"{phi:.0f}",
            f"{k:.2f}",
            f"{em:.3f}",
            f"{float(em_langmuir_blodgett):.3f}",
            f"{emx:.3f}",
        )
        rows.append(row)
    phi = 50000
    for i, k in enumerate((0.5, 1, 4, 16, 320)):
        em = calc_em_naca_tn_2904_from_figure6_data(k, phi)
        em_langmuir_blodgett = langmuir_blodgett_table_ii.calc_em(k, phi)
        emx = ie(k, k * phi)
        print(k, em, em_langmuir_blodgett)
        row = (
            f"{phi:.0f}",
            f"{k:.2f}",
            f"{em:.3f}",
            f"{float(em_langmuir_blodgett):.3f}",
            f"{emx:.3f}",
        )
        rows.append(row)

    text = make_markdown_table(header, rows)
    print(text)


langs_table_iv = {
    "Langmuir A": "ems_a",
    "Langmuir B": "ems_b",
    "Langmuir C": "ems_c",
    "Langmuir D": "ems_d",
    "Langmuir E": "ems_e",
}


def make_table_iv():
    print()
    print("Comparison to Table IV values for Em with Distribution")
    for k_phi in (0, 200, 1000, 3000, 10000):
        print()
        iks = []
        diffs = []
        phis = []
        ks = []
        print("Distribution|A|A|B|B|C|C|D|D|E|E|")
        print("---|---|---|---|---|---|---|---|---|---|---|")
        print(
            f"K*Phi={k_phi}, 1/K|Calc Em|Table IV|Calc Em|Table IV|Calc Em|Table IV|Calc Em|Table IV|Calc Em|Table IV|"
        )
        for i, inv_k in enumerate(data_table_iv_augmented[k_phi]["inv_ks"]):
            print(f"{inv_k}", end="|")
            for dist, tab in langs_table_iv.items():
                ema = data_table_iv_augmented[k_phi][tab][i]
                emc = calc_em_naca_tn_2904_from_with_distribution_fig6_data(
                    1 / inv_k, k_phi * inv_k, dist, False
                )
                # emc = ie(1/inv_k, k_phi, dist)
                diff = emc - ema
                print(f"{float(emc):.3f}|{ema:.3f}", end="|")
                iks.append(inv_k)
                diffs.append(diff)
                phis.append(k_phi * inv_k)
                ks.append(1 / inv_k)
            print()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    d_cyls = [_ * 0.0254 for _ in (0.125, 0.5, 1, 3, 6)]
    p = 90000
    tk = 263.15
    u = 90
    mvd = 20
    phis_typical = [calc_phi(tk, p, u, _) for _ in d_cyls]
    ks_typical = [calc_k(tk, u, mvd, _) for _ in d_cyls]
    k_phis_typical = [calc_k(tk, u, mvd, _) * calc_phi(tk, p, u, _) for _ in d_cyls]
    inv_ks_typical = [1 / calc_k(tk, u, mvd, _) for _ in d_cyls]
    ems_typical = [calc_em_naca_tn_2904_fig_6_data(tk, p, u, mvd, _) for _ in d_cyls]
    print("phis_typical", phis_typical)
    print("k_phis_typical", k_phis_typical)
    print("ks_typical", ks_typical)

    plt.figure(figsize=(7.35, 5.62))
    plt.suptitle("Fig 6")
    plt.plot([], [], " ", label="Phi")
    for phi in data_fig_6:
        (line,) = plt.plot(
            data_fig_6[phi]["ks"],
            data_fig_6[phi]["ems"],
            "o",
            fillstyle="none",
            label=phi,
        )
        ks = plt.np.logspace(log10(0.125), 3)
        ems = [calc_em_naca_tn_2904_from_figure6_data(k, phi) for k in ks]
        # emx = [ie(k, k*phi) for k in ks]
        plt.plot(ks, ems, "-", c=line.get_color(), lw=0.5)
        # plt.plot(ks, emx, '--', lw=3, c=line.get_color())
    plt.xscale("log")
    plt.xlabel("K")
    plt.xlim(0.1, 1000)
    plt.ylabel("Em")
    plt.ylim(0, 1.5)
    plt.legend()
    plt.savefig("naca_tn_2904_Fig6overlay.png", transparent=True)

    plt.figure(figsize=(7.35, 5.62))
    plt.suptitle("Fig 6")
    plt.plot([], [], " ", label="Phi")
    for phi in data_fig_6:
        # line, = plt.plot(data_fig_6[phi]['ks'], data_fig_6[phi]['ems'], 'o', fillstyle='none', label=phi)
        ks = plt.np.logspace(log10(0.125), 3)
        ems = [calc_em_naca_tn_2904_from_figure6_data(k, phi) for k in ks]
        plt.plot(ks, ems, "-", c=line.get_color(), lw=0.5, label=phi)

    for k_phi in data_table_iv_augmented:
        if k_phi > 10000:
            continue
        ks = [1 / inv_k for inv_k in data_table_iv_augmented[k_phi]["inv_ks"]]
        (line,) = plt.plot(
            ks,
            data_table_iv_augmented[k_phi]["ems_a"],
            "o",
            fillstyle="none",
            label=f"Table IV k_phi={k_phi}",
        )
        emx = [calc_em_naca_tn_2904_from_figure6_data(k, k_phi / k) for k in ks]
        plt.plot(ks, emx, "+", fillstyle="none", c=line.get_color())

    plt.plot([], [], "+", c="k", label="calc")
    plt.xscale("log")
    plt.xlabel("K")
    plt.xlim(0.1, 1000)
    plt.ylabel("Em")
    plt.ylim(0, 1.5)
    plt.legend()
    plt.savefig("naca_tn_2904_Fig6overlayt4.png", transparent=True)

    plt.figure()
    plt.suptitle("Fig 4")
    plt.plot([], [], " ", label="Phi")
    for phi in data_fig_6:
        (line,) = plt.plot(
            data_fig_6[phi]["ks"], data_fig_6[phi]["ems"], "o", label=phi
        )
        ks = plt.np.logspace(log10(0.125), 4)
        ems = [calc_em_naca_tn_2904_from_figure6_data(k, phi) for k in ks]
        plt.plot(ks, ems, "--", c=line.get_color())

    for condition in NACA_TR_1215_fig_24_conditions.conditions_data.values():
        print(condition)
        ks_typical = [calc_k(tk, u, mvd, _) for _ in condition["d_cyls_m"]]
        ems_typical = [
            calc_em_naca_tn_2904_fig_6_data(tk, p, u, mvd, _) for _ in condition["d_cyls_m"]
        ]
        plt.plot(ks_typical, ems_typical, "s-", fillstyle="none")

    plt.plot([], [], "--", c="k", label="Interpolation")
    plt.plot([], [], "s-", c="k", label="Figure 24 multicylinder conditions")
    plt.xscale("log")
    plt.xlabel("K")
    plt.ylabel("Em")
    plt.legend()
    plt.savefig("naca-tn-2904_figure_6.png")

    plt.figure()
    plt.suptitle("NACA-TN-2904 Table IV Data")
    plt.plot([], [], " ", label="K*Phi")
    for k_phi in data_table_iv_augmented:
        (line,) = plt.plot(
            data_table_iv_augmented[k_phi]["inv_ks"],
            data_table_iv_augmented[k_phi]["ems_a"],
            "o",
            fillstyle="none",
            label=k_phi,
        )
        print([1 / _ for _ in data_table_iv_augmented[k_phi]["inv_ks"]])
        print([k_phi * _ for _ in data_table_iv_augmented[k_phi]["inv_ks"]])
        print()
        inv_ks = plt.np.logspace(-3, log10(8))
        ems = [calc_em_naca_tn_2904_from_figure6_data(1 / _, k_phi * _) for _ in inv_ks]
        plt.plot(inv_ks, ems, "-", c=line.get_color())
    plt.plot(
        [], [], "-", c="k", label="Calculated with\nNACA-TR-1215 Figure 4 correlations"
    )
    plt.xscale("log")
    plt.xlabel("1/K")
    plt.ylabel("Em")
    plt.legend()
    plt.savefig("naca-tn-2904_table_iv.png")

    d_cyls = [_ * 0.0254 for _ in (0.125, 0.5, 1, 3, 6)]
    p = 90000
    tk = 263.15
    u = 90
    mvd = 20
    phis_typical = [calc_phi(tk, p, u, _) for _ in d_cyls]
    ks_typical = [calc_k(tk, u, mvd, _) for _ in d_cyls]
    k_phis_typical = [calc_k(tk, u, mvd, _) * calc_phi(tk, p, u, _) for _ in d_cyls]
    inv_ks_typical = [1 / calc_k(tk, u, mvd, _) for _ in d_cyls]
    ems_typical = [calc_em_naca_tn_2904_fig_6_data(tk, p, u, mvd, _) for _ in d_cyls]
    print("phis_typical", phis_typical)
    print("k_phis_typical", k_phis_typical)
    print("ks_typical", ks_typical)

    plt.figure(figsize=(7, 7))
    plt.suptitle("NACA-TN-2904 Table IV Data")
    plt.plot([], [], " ", label="K*Phi")
    for k_phi in data_table_iv_augmented:
        (line,) = plt.plot(
            data_table_iv_augmented[k_phi]["inv_ks"],
            data_table_iv_augmented[k_phi]["ems_a"],
            "o",
            fillstyle="none",
            label=k_phi,
        )
        print([1 / _ for _ in data_table_iv_augmented[k_phi]["inv_ks"]])
        print([k_phi * _ for _ in data_table_iv_augmented[k_phi]["inv_ks"]])
        print()
        inv_ks = plt.np.logspace(-3, log10(8))
        ems = [calc_em_naca_tn_2904_from_figure6_data(1 / _, k_phi * _) for _ in inv_ks]
        plt.plot(inv_ks, ems, "-", c=line.get_color())
        ems = [langmuir_blodgett_table_ii.calc_em(1 / _, k_phi * _) for _ in inv_ks]
        plt.plot(inv_ks, ems, ":", c=line.get_color())
    plt.plot(
        [], [], "-", c="k", label="Calculated with\nNACA-TR-1215 Figure 4 correlations"
    )
    plt.plot(
        [], [], ":", c="k", label="Calculated with\nLangmuir-Blodgett correlations"
    )

    for condition in NACA_TR_1215_fig_24_conditions.conditions_data.values():
        print(condition)
        inv_ks_typical = [1 / calc_k(tk, u, mvd, _) for _ in condition["d_cyls_m"]]
        ems_typical = [
            calc_em_naca_tn_2904_fig_6_data(tk, p, u, mvd, _) for _ in condition["d_cyls_m"]
        ]
        plt.plot(inv_ks_typical, ems_typical, "s-", fillstyle="none")

    plt.xscale("log")
    plt.xlabel("1/K")
    plt.ylabel("Em")
    plt.legend()
    plt.savefig("naca-tr-1215_table_iii_langmuir_comparison.png")

    plt.figure()
    phis = list(data_fig_6.keys())
    phis[0] = 10 ** l10phi_for_phi_0
    phis_log10 = [
        log10(phi) if phi > 10 ** l10phi_for_phi_0 else l10phi_for_phi_0
        for phi in list(interpolators.keys())
    ]
    plt.plot([], [], " ", label="k")
    vs = []
    for k in data_fig_6[0]["ks"]:
        ems = [interp(log10(k)) for interp in interpolators.values()]
        plt.plot(phis, ems, "-+", label=k)
    plt.xscale("log")
    plt.xlabel("phi")
    plt.legend()

    plt.figure()
    for phi in data_fig_4:
        plt.plot(data_fig_4[phi]["ks"], data_fig_4[phi]["delta_em"], label=phi)
    plt.xscale("log")
    plt.legend()

    print(calc_delta_em(20, 10))
    make_table_i()
    make_table_iii()
    make_table_iv()

    plt.show()
