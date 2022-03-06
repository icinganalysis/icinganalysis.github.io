"""
NASA/CR-2004-212875 equations (as noted) implemented in SI units (kg, m, K, s, N)
"""
from math import log10

WATER_SPECIFIC_HEAT = 4220  # J/kg-K
L_FREEZING = 334640  # J/kg (A.20)
L_EVAPORATION = 2500900  # J/kg
RATIO_MOLECULAR_WEIGHTS = 0.622  # water to air
T_MP = 273.15


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
