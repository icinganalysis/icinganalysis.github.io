from math import log10
from scipy.interpolate import interp1d, interp2d

# fmt: off
data_table_iv = {  # k*phi
    0: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001),
        'ems_a': (.051, .205, .380, .566, .789, .885, .932, .963, .978, .999),
        'ems_b': (.069, .204, .374, .555, .768, .870, .925, .961, .976, .999),
        'ems_c': (.085, .211, .373, .549, .750, .854, .918, .957, .977, .999),
        'ems_d': (.107, .225, .379, .542, .732, .836, .898, .951, .972, .999),
        'ems_e': (.126, .241, .384, .536, .713, .815, .885, .940, .965, .999),
    },
    200: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001),
        'ems_a': (.027, .135, .298, .493, .761, .874, .925, .960, .976, .999),
        'ems_b': (.039, .138, .302, .486, .740, .859, .919, .959, .975, .999),
        'ems_c': (.050, .146, .306, .482, .721, .846, .910, .955, .976, .999),
        'ems_d': (.066, .165, .315, .480, .703, .826, .901, .948, .971, .999),
        'ems_e': (.083, .182, .319, .477, .686, .805, .878, .938, .963, .999),
    },
    1000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001),
        'ems_a': (.019, .109, .251, .460, .714, .830, .908, .953, .971, .999),
        'ems_b': (.029, .109, .252, .452, .697, .816, .899, .953, .972, .999),
        'ems_c': (.038, .122, .359, .423, .677, .800, .892, .949, .973, .999),
        'ems_d': (.050, .138, .271, .477, .661, .783, .876, .943, .967, .999),
        'ems_e': (.065, .154, .283, .447, .643, .763, .862, .933, .962, .999),
    },

    3000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001),
        'ems_a': (.013, .085, .218, .409, .687, .815, .884, .945, .968, .999),
        'ems_b': (.020, .090, .225, .416, .668, .797, .878, .940, .966, .999),
        'ems_c': (.027, .100, .235, .410, .652, .785, .867, .938, .970, .999),
        'ems_d': (.039, .111, .244, .415, .641, .766, .855, .921, .964, .999),
        'ems_e': (.048, .130, .251, .413, .623, .746, .839, .918, .954, .999),
    },
    10000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001),
        'ems_a': (.008, .057, .157, .350, .645, .778, .865, .920, .952, .999),
        'ems_b': (.013, .060, .163, .356, .630, .764, .857, .920, .950, .999),
        'ems_c': (.017, .072, .172, .357, .615, .748, .849, .918, .955, .999),
        'ems_d': (.023, .083, .188, .362, .599, .731, .830, .909, .946, .999),
        'ems_e': (.034, .092, .202, .368, .591, .713, .816, .899, .939, .999),
    },
    50000: {
        'inv_ks': (4, 2, 1, 0.5, .2, .1, .05, .02, .01, .001),
        'ems_a': (0.005, 0.038, 0.105, 0.254, 0.534, 0.714, 0.825, 0.901, 0.939, 1.000),
        'ems_b': (0.010, 0.043, 0.112, 0.255, 0.520, 0.699, 0.815, 0.898, 0.936, 0.998),
        'ems_c': (0.015, 0.050, 0.120, 0.260, 0.511, 0.684, 0.803, 0.893, 0.934, 0.996),
        'ems_d': (0.022, 0.062, 0.135, 0.271, 0.506, 0.670, 0.789, 0.886, 0.930, 0.994),
        'ems_e': (0.031, 0.075, 0.149, 0.281, 0.499, 0.654, 0.773, 0.875, 0.924, 0.992),
    },
}

l10phi_for_phi_0 = 0

l10phi_for_k_phi_0 = 1

log10_ks = [log10(inv_k) for inv_k in data_table_iv[0]['inv_ks']]
log10_phis = [log10(_) if _ > 0 else l10phi_for_phi_0 for _ in data_table_iv]
k_phis = [_ for _ in data_table_iv]
zsa = [data_table_iv[_]['ems_a'] for _ in data_table_iv]
_em_interpolator_k_phi_a_log10 = interp2d(log10_ks, log10_phis, zsa, kind='cubic')
zsb = [data_table_iv[_]['ems_b'] for _ in data_table_iv]
_em_interpolator_k_phi_b_log10 = interp2d(log10_ks, log10_phis, zsb, kind='cubic')
zsc = [data_table_iv[_]['ems_c'] for _ in data_table_iv]
_em_interpolator_k_phi_c_log10 = interp2d(log10_ks, log10_phis, zsc, kind='cubic')
zsd = [data_table_iv[_]['ems_d'] for _ in data_table_iv]
_em_interpolator_k_phi_d_log10 = interp2d(log10_ks, log10_phis, zsd, kind='cubic')
zse = [data_table_iv[_]['ems_e'] for _ in data_table_iv]
_em_interpolator_k_phi_e_log10 = interp2d(log10_ks, log10_phis, zse, kind='cubic')
_k_phi_interpolators = {
    'Langmuir A': _em_interpolator_k_phi_a_log10,
    'Langmuir B': _em_interpolator_k_phi_b_log10,
    'Langmuir C': _em_interpolator_k_phi_c_log10,
    'Langmuir D': _em_interpolator_k_phi_d_log10,
    'Langmuir E': _em_interpolator_k_phi_e_log10,
}

kind = 'linear'
# kind = 'cubic'
_k_interps = {
    'Langmuir A': (
        interp1d(log10_ks, data_table_iv[0]['ems_a'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[200]['ems_a'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[1000]['ems_a'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[3000]['ems_a'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[10000]['ems_a'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[50000]['ems_a'], kind, fill_value='extrapolate'),
    ),
    'Langmuir B': (
        interp1d(log10_ks, data_table_iv[0]['ems_b'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[200]['ems_b'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[1000]['ems_b'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[3000]['ems_b'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[10000]['ems_b'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[50000]['ems_b'], kind, fill_value='extrapolate'),
    ),
    'Langmuir C': (
        interp1d(log10_ks, data_table_iv[0]['ems_c'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[200]['ems_c'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[1000]['ems_c'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[3000]['ems_c'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[10000]['ems_c'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[50000]['ems_c'], kind, fill_value='extrapolate'),
    ),
    'Langmuir D': (
        interp1d(log10_ks, data_table_iv[0]['ems_d'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[200]['ems_d'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[1000]['ems_d'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[3000]['ems_d'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[10000]['ems_d'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[50000]['ems_d'], kind, fill_value='extrapolate'),
    ),
    'Langmuir E': (
        interp1d(log10_ks, data_table_iv[0]['ems_e'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[200]['ems_e'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[1000]['ems_e'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[3000]['ems_e'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[10000]['ems_e'], kind, fill_value='extrapolate'),
        interp1d(log10_ks, data_table_iv[50000]['ems_e'], kind, fill_value='extrapolate'),
    ),
}

lkphis = [log10(_) for _ in (10, 200, 1000, 3000, 10000, 50000)]


def ie(k, k_phi, distribution='Langmuir A'):
    ems = [ki(log10(1 / k)) for ki in _k_interps[distribution]]
    _ip = interp1d(lkphis, ems, kind='linear',
                   # fill_value='extrapolate'
                   fill_value=float('nan'),
                   bounds_error=False,
                   )
    return _ip(log10(k_phi) if k_phi > 0 else l10phi_for_k_phi_0)




def make_table_iv():
    langs_table_iv = {
        'Langmuir A': 'ems_a',
        'Langmuir B': 'ems_b',
        'Langmuir C': 'ems_c',
        'Langmuir D': 'ems_d',
        'Langmuir E': 'ems_e',
    }
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
            f"K*Phi={k_phi}, 1/K|Calc Em|Table IV|Calc Em|Table IV|Calc Em|Table IV|Calc Em|Table IV|Calc Em|Table IV|")
        for i, inv_k in enumerate(data_table_iv[k_phi]['inv_ks']):
            print(f"{inv_k}", end='|')
            for dist, tab in langs_table_iv.items():
                ema = data_table_iv[k_phi][tab][i]
                emc = ie(1 / inv_k, k_phi, dist)
                diff = emc - ema
                print(f"{float(emc):.3f}|{ema:.3f}", end='|')
                iks.append(inv_k)
                diffs.append(diff)
                phis.append(k_phi * inv_k)
                ks.append(1 / inv_k)
            print()


make_table_iv()