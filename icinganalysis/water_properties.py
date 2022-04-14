"""
NASA/CR-2004-212875 equations (as noted) implemented in SI units (kg, m, K, s, N)
"""
from math import log10
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar

WATER_SPECIFIC_HEAT = 4220  # J/kg-K
L_FREEZING = 334640  # J/kg (A.20)
L_EVAPORATION = 2500900  # J/kg
RATIO_MOLECULAR_WEIGHTS = 0.622  # water to air
T_MP = 273.15
WATER_DENSITY = 1000  # kg/m^3
PA_PER_MM_HG = 133.322
ICE_BULK_DENSITY = 917  # kg/m^3


def calc_vapor_p_psi(tk):  # (A.8) and (A.9)
    dt = (tk - 273.15) * 1.8
    pv = 0.088586 + (
        dt
        * (
            3.5748e-3
            + (
                dt
                * (
                    6.3964e-5
                    + (
                        dt
                        * (
                            6.5919e-7
                            + (
                                dt
                                * (
                                    4.1880e-9
                                    + (dt * (1.5613e-11 + (dt * (2.6169e-14))))
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    return pv


def calc_vapor_p(tk):  # (A.8) and (A.9)
    dt = tk - 273.15
    pv = 610.78 + (
        dt
        * (
            44.365
            + (
                dt
                * (
                    1.4289
                    + (
                        dt
                        * (
                            2.6506e-2
                            + (
                                dt
                                * (3.0312e-4 + (dt * (2.0341e-6 + (dt * (6.1368e-9)))))
                            )
                        )
                    )
                )
            )
        )
    )
    return pv


def calc_diffusivity_water_vapor(tk, p):  # (A.4)
    return 2.11e-5 * (tk / 273.15) ** 1.94 * 101320 / p


def calc_vapor_pressure_gg(tk):
    """
    http://cires1.colorado.edu/~voemel/vp.html
    https://en.wikipedia.org/wiki/Goff%E2%80%93Gratch_equation
    :param tk:
    :return: saturated liquid water vapor pressure, Pa
    """
    PA_PER_H_PA = 100  # ratio Pa / hPa
    vp = PA_PER_H_PA * 10 ** (
        -7.90298 * (373.15 / tk - 1)
        + 5.02808 * log10(373.15 / tk)
        - 1.3816e-7 * (10 ** (11.344 * (1 - tk / 373.15)) - 1)
        + 8.1328e-3 * (10 ** (-3.49149 * (373.15 / tk - 1)) - 1)
        + log10(1013.246)
    )
    return vp


def calc_vapor_pressure_over_ice_gg(tk):
    """
    http://cires1.colorado.edu/~voemel/vp.html
    https://en.wikipedia.org/wiki/Goff%E2%80%93Gratch_equation
    :param tk:
    :return: saturated liquid water vapor pressure, Pa
    """
    PA_PER_H_PA = 100  # ratio Pa / hPa
    vp = PA_PER_H_PA * 10 ** (
        -9.09718 * (273.16 / tk - 1)
        -3.56654 * log10(273.16 / tk)
        +0.876793 * (1-tk/273.16)
        + log10(6.1071)
    )
    return vp


_smithsonian_tables_130_1933 = (  # TC, pv_mm_hg
    -50, .029,
    -45, .054,
    -40, .096,
    -35, .169,
    -30, .288,
    -25, .480,
    -24, .530,
    -23, .585,
    -22, .646,
    -21, .712,
    -20, .783,
    -19, .862,
    -18, .947,
    -17, 1.041,
    -16, 1.142,
    -15, 1.252,
    -14, 1.373,
    -10, 1.964,
    -5, 3.025,
    0, 4.58,
    5, 6.54,
    10, 9.21,
    15, 12.79,
    20, 17.55,
    25, 23.78,
    30, 31.86,
    35, 42.23,
    40, 55.40,
    45, 71.97,
    50, 92.6,
    55, 118.2,
    60, 149.6,
)
_tcs = _smithsonian_tables_130_1933[::2]
_tks = [_+273.15 for _ in _tcs]
_pvs_mm_hg = _smithsonian_tables_130_1933[1::2]
_pvs = [PA_PER_MM_HG*_ for _ in _pvs_mm_hg]
_log_tks = [log10(_) for _ in _tks]
_log_pvs = [log10(_) for _ in _pvs]
_log_pv_interpolator = interp1d(_log_tks, _log_pvs, kind='cubic')


def vapor_p_smithsonian_tables_1934(tk):
    """
    While not noted in the source,
    (https://babel.hathitrust.org/cgi/pt?id=wu.89055210611&view=1up&seq=237&skin=2021)
    this follows the vapor pressure over ice line at
    temperatures below 0C (273.15K)
    :param tk:
    :return:
    """
    pv = 10 ** _log_pv_interpolator(log10(tk))
    return pv


def find_tk_for_pv(pv, pv_function=calc_vapor_pressure_gg):

    def f(tk):
        return abs(pv-pv_function(tk))

    solution = minimize_scalar(f, bounds=[223.15, 333.15], method='bounded')
    tk = float('nan')
    if solution.success:
        tk = solution.x
    return tk


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.plot(_tks, _pvs)
    tks = [_+273.15 for _ in range(-40, 60+1, 1)]
    pvs = [vapor_p_smithsonian_tables_1934(tk) for tk in tks]
    plt.plot(tks, pvs, '--')
    pvs = [calc_vapor_pressure_gg(_) for _ in tks]
    plt.plot(tks, pvs, '-.')
    tks = [_+273.15 for _ in range(-40, 0+1, 1)]
    pvs = [calc_vapor_pressure_over_ice_gg(_) for _ in tks]
    plt.plot(tks, pvs, ':')
    plt.show()

