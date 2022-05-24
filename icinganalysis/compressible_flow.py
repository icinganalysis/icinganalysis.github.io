"""
A review of compressible flow equations may be found at
https://www.grc.nasa.gov/WWW/k-12/airplane/shortc.html
"""

from icinganalysis import air_properties
from icinganalysis.iteration_helpers import solve_minimize_f

gamma = air_properties.GAMMA_AIR
gp1d2gm1 = (gamma + 1) / (2 * (gamma - 1))  # 3.0
gdgm1 = gamma / (gamma - 1)  # gdgm1
inv_gm1 = 1 / (gamma - 1)  # 2.5
gm1d2 = (gamma - 1) / 2  # 0.2
gp1d2 = (gamma + 1) / 2  # 1.2
gd2 = gamma / 2  # 0.7


def calc_sonic_airspeed(tk):
    sonic_airspeed = (gamma * air_properties.R_AIR * tk) ** 0.5
    return sonic_airspeed


def calc_mach(u, tk):
    sonic_airspeed = calc_sonic_airspeed(tk)
    return u / sonic_airspeed


def calc_u(mach, tk):
    return mach * calc_sonic_airspeed(tk)


def calc_mach_from_t_total(u, t_total):
    t = t_total - u ** 2 / (gamma * air_properties.R_AIR)
    mach = calc_mach(u, t)
    return mach


def calc_limited_pl_p_ratio(mach, pl_p):
    """
    Calculate a limited ratio that will not violate pl > 0 or local mach calculation constraints.
    When using Cp values at Mach values other than the one the Cp values were determined at,
    calculated pl / p ratios can result in pl <= 0,
    or the local mach calculation being a non-real number,
    due to the term ((pl_p) ** (-1 / gdgm1) * (1 + gm1d2 * mach ** 2) - 1) being less than 0.

    :param mach: free stream Mach
    :param pl_p: ratio of local p to free stream p
    :return: limited ratio pl/p
    """
    pl_p = max(1e-25, min(pl_p, calc_pl_p_max(mach)))
    return pl_p


def calc_mach_local(mach, pl_p, limit_pl_p_ratio=True):
    """
    Calculate the local Mach number
    :param mach:
    :param pl_p:
    :param limit_pl_p_ratio:
    :return:
    """
    if limit_pl_p_ratio:
        pl_p = calc_limited_pl_p_ratio(mach, pl_p)
    mach_l = (((pl_p) ** (-1 / gdgm1) * (1 + gm1d2 * mach ** 2) - 1) * 1 / gm1d2) ** 0.5
    return mach_l


def calc_t_recovery(tk_static, u, r=1):
    mach = calc_mach(u, tk_static)
    tr = tk_static * (1 + r * gm1d2 * mach ** 2)
    return tr


def calc_a_a_star(mach):
    """
    Calculate the area change ratio where isentropic flow will reach Mach 1

    :param mach: initial Mach
    :return: area change ratio for Mach 1
    """
    return 1 / mach * ((1 + gm1d2 * mach ** 2) ** gp1d2gm1) * gp1d2 ** -gp1d2gm1


def calc_mach2_subsonic(a1, mach1, a2):
    """
    Find the subsonic Mach value at point 2.
    Note that there can also be a supersonic solution.
    :param a1: initial flow area
    :param mach1: initial Mach
    :param a2: final area
    :return: Mach at point 2
    """
    a_star = a1 / calc_a_a_star(mach1)

    def calc_diff(mach2):
        return abs(a_star - a2 / calc_a_a_star(mach2))

    mach2 = solve_minimize_f(calc_diff, [0, 1])
    return mach2


def calc_limited_pressure_coefficient(pressure_coefficient, mach):
    """
    Calculate a Cp value that will not violate pl > 0 or local mach calculation constraints.
    When using Cp values at Mach values other than the one the Cp values were determined at,
    calculated pl / p ratios can result in pl <= 0,
    or the local mach calculation being a non-real number,
    due to the term ((pl_p) ** (-1 / gdgm1) * (1 + gm1d2 * mach ** 2) - 1) being less than 0.

    :param pressure_coefficient: pressure coefficient, Cp=(pl/p-1)/(0.7*mach**2)
    :param mach: Mach number
    :return: limited Cp value
    """
    pressure_coefficient = max(
        calc_cp_min(mach), min(pressure_coefficient, calc_cp_max(mach))
    )
    return pressure_coefficient


def calc_pl_p(mach, pressure_coefficient, limit_pressure_coefficient=True):
    if limit_pressure_coefficient:
        pressure_coefficient = calc_limited_pressure_coefficient(
            pressure_coefficient, mach
        )
    pl_p = 1 + gd2 * mach ** 2 * pressure_coefficient
    return pl_p


def calc_cp_max(mach):
    """Calculate the maximum Cp value that does not the constraint
    ((pl_p) ** (-1 / gdgm1) * (1 + gm1d2 * mach ** 2) - 1) > 0

    """
    cp = ((1 / (1 + gm1d2 * mach ** 2)) ** -gdgm1 - 1) / (gd2 * mach ** 2)
    return cp


def calc_cp_min(mach):
    """Calculate the minimum Cp value for pl > 0"""
    return -1 / (gd2 * mach ** 2) + 1e-10  # keep minimum pl slightly above zero


def calc_pl_p_max(mach):
    """
    Calculate a limited ratio that will not violate local mach calculation constraints.
    Prevent local mach calculation being a non-real number,
    due to the term ((pl_p) ** (-1 / gdgm1) * (1 + gm1d2 * mach ** 2) - 1) being less than 0.
    :param mach: Mach number
    :return: limited pressure ratio
    """
    return (1 / (1 + gm1d2 * mach ** 2)) ** -gdgm1


if __name__ == "__main__":
    tk = 273.15
    c = (air_properties.GAMMA_AIR * air_properties.R_AIR * tk) ** 0.5
    print(c)

    mach = 0.5
    print(mach, calc_cp_max(mach), calc_cp_min(mach))

    cp = 2
    print(
        cp,
        calc_limited_pressure_coefficient(cp, mach),
        calc_pl_p(mach, calc_limited_pressure_coefficient(cp, mach)),
    )
    cp = 0
    print(
        cp,
        calc_limited_pressure_coefficient(cp, mach),
        calc_pl_p(mach, calc_limited_pressure_coefficient(cp, mach)),
    )
    cp = -10
    print(
        cp,
        calc_limited_pressure_coefficient(cp, mach),
        calc_pl_p(mach, calc_limited_pressure_coefficient(cp, mach)),
    )
    cp_limited = calc_limited_pressure_coefficient(cp, mach)
    print(calc_pl_p(mach, cp_limited))
    print(gp1d2)
    print(calc_pl_p_max(mach))
