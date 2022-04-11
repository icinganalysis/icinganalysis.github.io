from scipy.interpolate import interp1d
from math import log10


def tf_to_k(tf):
    return (tf + 459.67) / 1.8


def tk_to_f(tk):
    return tk * 1.8 - 459.67


_d = (  # Tc, Pa https://en.wikipedia.org/wiki/Ethanol_(data_page)
    -31.3,
    133.3,
    -2.3,
    1333,
    19,
    5333,
    43.9,
    13332,
    63.5,
    53329,
    78.4,
    101315,
    97.5,
    202650,
)
tcs = _d[::2]
pvs = _d[1::2]
tks = [_ + 273.15 for _ in tcs]
log_tks = [log10(_) for _ in tks]
log_pvs = [log10(_) for _ in pvs]
_log_pv_interp = interp1d(log_tks, log_pvs, kind="cubic")


def calc_p_vapor(tk):
    return 10 ** _log_pv_interp(log10(tk))


MOLECULAR_MASS = 0.04606844  # kg/mol
L_EVAPORATION = 42.3 / MOLECULAR_MASS * 1000  # kJ/mol / kg/mol * J/kJ = J/kg
DENSITY = 803  # kg/m^3

# fmt: off
_d_mp = (  # mass fraction, Tc https://en.wikipedia.org/wiki/Ethanol_(data_page)
    0, 0,
    0.025, -1,
    .048, -2,
    .068, -3,
    .113, -5,
    .1378, -6.1,
    .164, -7.5,
    .175, -8.7,
    .18, -9.4,
    .203, -10.6,
    .2211, -12.2,
    .242, -14,
    .267, -16,
    .3, -18.9,
    .338, -23.6,
    .39, -28.7,
    .463, -33.9,
    .561, -41,
    .719, -51.3,
    1, -114.3,
)
# fmt: on
mf = _d_mp[::2]
tcs = _d_mp[1::2]
tks_mp = [_ + 273.15 for _ in tcs]
_mp_interpolator = interp1d(mf, tks_mp)


def interp_mp(fraction):
    return _mp_interpolator(fraction)


if __name__ == "__main__":
    from icinganalysis.iteration_helpers import generate_even_odd_pairs

    # fmt: off
    naca_arr_5g13_table_ii = (  # Tf, kg_ethanol/kg_water
        23, .124,
        25.5, .092,
        23.0, .124,
        26.3, .07,
        23, .124,
        26.6, .075,
        18, .184,
        22.1, .135,
        10.6, .270,
        15.8, .212,
    )
    # fmt: on

    print("NACA-ARR-5G13 Table II")
    rows = []
    for tf, conc in generate_even_odd_pairs(naca_arr_5g13_table_ii):
        mf = conc / (1 + conc)
        tk = interp_mp(mf)
        tf_mp = tk_to_f(tk)
        rows.append([conc, f"{tf:.1f}", f"{tf_mp:.1f}"])

    header = [
        "Ethanol concentration, kg/kg_water",
        "T_surface, F",
        "Calculated freezing point, F",
    ]
    from icinganalysis import markdown_table_helper

    text = markdown_table_helper.make_nice_width_markdown_table(header, rows)
    print(text)
    # a reasonable match
