"""
reference:
Langmuir, Irving, and Blodgett, Katherine B.: A Mathematical Investigation of Water Droplet Trajectories.
Tech. Rep. No. 5418, Air Materiel Command, AAF, Feb. 19, 1946. (Contract No. W-33-038-ac-9151 with General Electric Co.)

Units:
tk: free-stream static temperature, K
p: air static pressure, Pa (N/m^2)
u: free-stream air speed, m/s
d_cylinder: cylinder diameter, m
d_drop: water drop diameter, micrometer (1e-6 m)
altitude: pressure altitude, m
"""
from math import atan, log, log10, degrees
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar
import numpy as np

langmuir_a_mids = 1, 1, 1, 1, 1, 1, 1
langmuir_b_mids = 0.56, 0.72, 0.84, 1.0, 1.17, 1.32, 1.49
langmuir_c_mids = 0.42, 0.61, 0.77, 1, 1.25, 1.51, 1.81
langmuir_d_mids = 0.31, 0.52, 0.71, 1, 1.37, 1.74, 2.22
langmuir_e_mids = 0.23, 0.44, 0.65, 1, 1.48, 2.00, 2.71
langmuir_lwc_fractions = 0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05

from langmuir_blodgett_table_ii import calc_em

from langmuir_blodgett_table_i import calc_cd_r_24_langmuir_blodgett as calc_cd_r_24
from langmuir_blodgett_table_i import calc_ratio_langmuir_blodgett as calc_lambda_lambda_s
em_interpolator_to_use = calc_em


def calc_em_with_distribution(tk, p, u, mvd, diameter, distribution="Langmuir A"):
    """
    This is the more technically correct implementation that should be used for most cases,
    other than reproducing AAF TR 5418 values.

    As noted in NACA-TR-1215, Langmuir-Blodgett used an approximation where
    the k*phi value for the MVD drop size is used for all drop size bins.
    To be more technically correct, each drop size bin should have a unique k*phi value.
    The "calc_em_with_distribution_k_phi_mvd" implements the approximation and
    reproduces AAF TR 5418 Table XI values.

    Even so, the two versions yield only slightly different values.
    """
    mids = {
        "langmuir a": langmuir_a_mids,
        "langmuir b": langmuir_b_mids,
        "langmuir c": langmuir_c_mids,
        "langmuir d": langmuir_d_mids,
        "langmuir e": langmuir_e_mids,
    }.get(distribution.lower(), None)
    if mids is None:
        raise ValueError(
            f"{distribution} is not recognized as a Langmuir distribution type"
        )
    em = 0
    for d_drop_ratio, w in zip(mids, langmuir_lwc_fractions):
        k = calc_k(tk, u, mvd * d_drop_ratio, diameter)
        phi = calc_phi(tk, p, u, diameter)
        delta_em = em_interpolator_to_use(k, phi)
        em += w * delta_em
    return em


def calc_em_with_distribution_k_phi_mvd(tk, p, u, mvd, diameter, distribution="Langmuir A"):
    """
    This will reproduce Table XI distribution values, but as noted in NACA-TR-1215
    this is an approximation.

    The k*phi value for the MVD drop size is used for all drop size bins.
    To be more technically correct, each drop size bin should have a unique k*phi value,
    "calc_em_with_distribution" implements the more technically correct version,
    and that is what is recommended for uses other that reproducing AAF TR 5418 values.

    Even so, the two versions yield only slightly different values.
    """
    mids = {
        "langmuir a": langmuir_a_mids,
        "langmuir b": langmuir_b_mids,
        "langmuir c": langmuir_c_mids,
        "langmuir d": langmuir_d_mids,
        "langmuir e": langmuir_e_mids,
    }.get(distribution.lower(), None)
    if mids is None:
        raise ValueError(
            f"{distribution} is not recognized as a Langmuir distribution type"
        )
    em = 0
    k_phi = calc_k(tk, u, mvd, diameter) * calc_phi(tk, p, u, diameter)
    for d_drop_ratio, w in zip(mids, langmuir_lwc_fractions):
        k = calc_k(tk, u, mvd * d_drop_ratio, diameter)
        phi = k_phi / k
        delta_em = em_interpolator_to_use(k, phi)
        em += w * delta_em
    return em


def calc_air_viscosity_recent(tk):
    """
    Calculate the dynamic viscosity of air 
    :param tk: temperature, K
    :return: dynamic viscosity of air, Pa-s (N-s/m^2) 
    """

    return (1.458e-6 * tk ** (3 / 2)) / (tk + 110.4)


def calc_air_viscosity(tk):
    """
    Calculate the dynamic viscosity of air
    :param tk: temperature, K
    :return: dynamic viscosity of air, Pa-s (N-s/m^2)
    """

    return 2.48e-7 * tk ** 0.7542  # equ. (13)


def calc_air_density_recent(tk, p):
    return p / (287.05 * tk)


def calc_air_density(tk, p):
    return 0.3484 / 100 * p / tk  # equ. (15)


def calc_pressure(altitude):
    p = 101325 * (1 - 2.25577e-5 * altitude) ** 5.25588
    return p


def calc_altitude(pressure):
    return (1 - (pressure / 101325) ** (1 / 5.25588)) / 2.25577e-5


def calc_re(tk, p, u, length):
    return u * length * calc_air_density(tk, p) / calc_air_viscosity(tk)  # equ. (9)


def calc_re_d_drop(tk, p, u, drop_diameter_micrometer):
    return u * drop_diameter_micrometer / 1000000 * calc_air_density(tk, p) / calc_air_viscosity(tk)  # equ. (9)


def calc_drop_diameter_micrometer_from_re_drop(re, tk, p, u):  # equ. (9), re-arranged
    drop_diameter_micrometer = re * 1000000 * calc_air_viscosity(tk) / (u * calc_air_density(tk, p))
    return drop_diameter_micrometer


def calc_range_stokes(tk, u, drop_diameter_micrometer):
    lambda_s = (
        2
        / 9
        * 1000
        * (drop_diameter_micrometer / 1000000 / 2) ** 2
        * u
        / calc_air_viscosity(tk)
    )  # equ. (11)
    return lambda_s


def calc_k(tk, u, drop_diameter_micrometer, d_cylinder):
    c = d_cylinder / 2
    k = (
        2
        / 9
        * 1000
        * (drop_diameter_micrometer / 1000000 / 2) ** 2
        * u
        / calc_air_viscosity(tk)
        / c
    )  # equ. (12)
    return k


def calc_d_cylinder_from_k(k, tk, u, d_drop):
    return 2 * 2 / 9 * 1000 * (d_drop / 1000000 / 2) ** 2 * u / calc_air_viscosity(tk) / k  # equ. (12), re-arranged


def calc_d_drop_from_k(k, tk, u, d_cylinder):
    drop_diameter_micrometer = 1000000 * 2 * (k / (
        2*
        2
        / 9
        * 1000
        * u
        / calc_air_viscosity(tk)
        / d_cylinder
    ))**0.5  # equ. (12), re-arranged
    return drop_diameter_micrometer


def calc_phi(tk, p, u, d_cylinder):
    c = d_cylinder / 2
    phi = (
        18 * calc_air_density(tk, p) ** 2 * u * c / (1000 * calc_air_viscosity(tk))
    )  # equ. (25)
    return phi


def calc_d_cylinder_from_phi(phi, tk, p, u):
    d_cylinder = (phi * 2 * 1000 * calc_air_viscosity(tk) / (18 * calc_air_density(tk, p) ** 2 * u)
                  )  # equ. (25), re-arranged
    return d_cylinder


def calc_ko_cylinder(tk, p, u, drop_diameter_micrometer, d_cylinder):
    re_drop = calc_re(tk, p, u, drop_diameter_micrometer / 1000000)
    lambda_lambda_s = calc_lambda_lambda_s(re_drop)
    k = calc_k(tk, u, drop_diameter_micrometer, d_cylinder)
    ko = 0.125 + lambda_lambda_s * (k - 0.125)
    return ko


# fmt: off
delta_em_interpolator = interp1d(  # Table V em, delta_em values
    (0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5),
    (0, 0, 0.005, 0.013, 0.02, 0.023, 0.02, 0.015, 0.010, 0.005,
     -0.010  # added point
     )
)
# fmt: on


def calc_em(tk, p, u, drop_diameter_micrometer, d_cylinder):
    k = calc_k(tk, u, drop_diameter_micrometer, d_cylinder)
    ko = calc_ko_cylinder(tk, p, u, drop_diameter_micrometer, d_cylinder)
    if ko < 0.125:
        return 0
    phi = calc_phi(tk, p, u, d_cylinder)
    em = 0.466 * (log10(8 * ko)) ** 2  # equ. (33)
    if k > 1.1 and phi < 10:
        em = ko / (ko + 3.14159 / 2)  # equ. (34)
    else:
        if em > 0.5:
            re_drop = calc_re(tk, p, u, drop_diameter_micrometer / 1000000)
            cd_r_24 = calc_cd_r_24(re_drop)
            he = 1 + 0.5708 * cd_r_24 - 0.73e-4 * re_drop ** 1.38  # equ. (43)
            k = calc_k(tk, u, drop_diameter_micrometer, d_cylinder)
            em = k / (k + he)  # equ. (42)
        else:
            delta_em = delta_em_interpolator(em)
            em += delta_em
    return em


def calc_theta_impingement(tk, p, u, drop_diameter_micrometer, d_cylinder):
    k = calc_k(tk, u, drop_diameter_micrometer, d_cylinder)
    ko = calc_ko_cylinder(tk, p, u, drop_diameter_micrometer, d_cylinder)
    if ko < 0.125:
        return 0
    phi = calc_phi(tk, p, u, d_cylinder)
    theta = atan(1.70 * (k - 0.125) ** 0.76)
    em = 0.466 * (log10(8 * ko)) ** 2  # equ. (33)
    if k > 10 and phi <= 10:
        # if phi > 0:
        theta = atan(k)
    if phi > 10:
        theta = atan(1.70 * (ko - 0.125) ** 0.76)
        # re_drop = calc_re(tk, p, u, drop_diameter_micrometer / 1000000)
        # cd_r_24 = 1 + 0.197 * re_drop ** 0.63 + 2.6e-4 * re_drop ** 1.38  # equ. (22)
        # ho = 0.358 + 0.615 * cd_r_24 - 0.51e-4 * re_drop ** 1.38  # equ. (45)
        # theta = atan(ko/ho)  # equ (44)
        if k > 10:
            re_drop = calc_re(tk, p, u, drop_diameter_micrometer / 1000000)
            cd_r_24 = (
                1 + 0.197 * re_drop ** 0.63 + 2.6e-4 * re_drop ** 1.38
            )  # equ. (22)
            cd_r_24 = calc_cd_r_24(re_drop)
            ho = 0.358 + 0.615 * cd_r_24 - 0.51e-4 * re_drop ** 1.38  # equ. (45)
            theta = atan(k / ho)  # equ (44)
        # else:
        #     theta = atan(1.70 * (ko - 0.125) ** 0.76)
    return degrees(theta)


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

# fmt: off
table_VIII_data = {  # phi values as keys
    5000: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.01, 0.052, 0.169, 0.346, 0.61, 0.754, 0.861, 0.94, 0.968),
    },
    10000: {
        'inv_ks': (4, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01),
        'em_a': (0.009, 0.044, 0.149, 0.314, 0.582, 0.736, 0.848, 0.932, 0.965),
        'em_b': (0.0125, 0.054, 0.155, 0.313, 0.556, 0.715, 0.83, 0.921,),
        'em_c': (0.019, 0.068, 0.167, 0.318, 0.546, 0.7, 0.816, 0.914,),
        'em_d': (0.03, 0.083, 0.185, 0.327, 0.536, 0.683, 0.799, 0.898,),
        'em_e': (0.043, 0.104, 0.203, 0.336, 0.532, 0.668, 0.781, 0.88,),
    },
}
# fmt: on


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    # use the "Presentation of Data" example values
    alt = 1900  # m
    t = -10  # C
    tk = 273.15 + t
    p = calc_pressure(alt)
    d_cylinder = 0.1  # arbitrary size

    inv_ks_for_interpolation = np.logspace(-2.1, log10(5))

    em_types = {
        "em_a": "A",
        "em_b": "B",
        "em_c": "C",
        "em_d": "D",
        "em_e": "E",
    }
    for k_phi in table_XI_data:
        plt.figure(figsize=(8, 6))
        plt.suptitle(f"Kφ={k_phi:.0f}")
        print("k_phi", k_phi)
        for em_type in ["em_a", "em_b", "em_c", "em_d", "em_e"]:
            ks = [1 / _ for _ in table_XI_data[k_phi]["inv_ks"]]
            x, y = tuple(
                zip(
                    *tuple(
                        zip(
                            table_XI_data[k_phi]["inv_ks"],
                            table_XI_data[k_phi][em_type],
                        )
                    )
                )
            )  # make same length
            (line,) = plt.plot(x, y, "o")
            ems_calc = []
            for inv_k in inv_ks_for_interpolation:
                k = 1/inv_k
            # for k in ks:
                phi = k_phi / k
                match_phi_with_u_result = minimize_scalar(  # find an airspeed to match phi
                    lambda _: abs(
                        calc_phi(tk, p, _, d_cylinder)
                        - max(phi, 0.1)  # use 0.1 to approximate phi=0
                    ),
                    bounds=(0, 1000000),
                    method="bounded",
                )
                if not match_phi_with_u_result.success:
                    raise ValueError(tk, p, d_cylinder, phi, match_phi_with_u_result)
                u = match_phi_with_u_result.x

                match_phi_with_u_result = minimize_scalar(  # find a drop size to match k
                    lambda _: abs(calc_k(tk, u, _, d_cylinder) - k),
                    bounds=(0, 1000000),
                    method="bounded",
                )
                if not match_phi_with_u_result.success:
                    raise ValueError(tk, u, d_cylinder, k, match_phi_with_u_result)
                drop_diameter_micrometer = match_phi_with_u_result.x
                ems_calc.append(
                    calc_em_with_distribution_k_phi_mvd(
                        tk,
                        p,
                        u,
                        drop_diameter_micrometer,
                        d_cylinder,
                        distribution=f"Langmuir {em_types[em_type]}",
                    )
                )
            plt.plot(
                inv_ks_for_interpolation,
                ems_calc,
                c=line.get_color(),
                label=f"Calculated {em_types[em_type]}",
            )
        plt.plot([], [], "o", c="k", label="Table XI values")

        plt.xscale("log")
        plt.xlabel("1/K")
        plt.ylim(0, 1)
        plt.ylabel("Em")
        plt.legend()
        plt.savefig(f"calculation_verification_table_XI_k_phi={k_phi:.0f}.png")

    for k_phi in table_XI_data:
        plt.figure(figsize=(8, 6))
        plt.suptitle(f"Kφ={k_phi:.0f}")
        for em_type in ["em_a", "em_b", "em_c", "em_d", "em_e"]:
            ks = [1 / _ for _ in table_XI_data[k_phi]["inv_ks"]]
            x, y = tuple(
                zip(
                    *tuple(
                        zip(
                            table_XI_data[k_phi]["inv_ks"],
                            table_XI_data[k_phi][em_type],
                        )
                    )
                )
            )  # make same length
            (line,) = plt.plot(x, y, "o")
            ems_calc = []
            for inv_k in inv_ks_for_interpolation:
                k = 1/inv_k
            # for k in ks:
                phi = k_phi / k
                match_phi_with_u_result = minimize_scalar(  # find an airspeed to match phi
                    lambda _: abs(
                        calc_phi(tk, p, _, d_cylinder)
                        - max(phi, 0.1)  # use 0.1 to approximate phi=0
                    ),
                    bounds=(0.01, 1000000),
                    method="bounded",
                )
                if not match_phi_with_u_result.success:
                    raise ValueError(tk, p, d_cylinder, phi, match_phi_with_u_result)
                u = match_phi_with_u_result.x

                match_phi_with_u_result = minimize_scalar(  # find a drop size to match k
                    lambda _: abs(calc_k(tk, u, _, d_cylinder) - k),
                    bounds=(0.01, 1000000),
                    method="bounded",
                )
                if not match_phi_with_u_result.success:
                    raise ValueError(tk, u, d_cylinder, k, match_phi_with_u_result)
                drop_diameter_micrometer = match_phi_with_u_result.x
                ems_calc.append(
                    calc_em_with_distribution_k_phi_mvd(
                        tk,
                        p,
                        u,
                        drop_diameter_micrometer,
                        d_cylinder,
                        distribution=f"Langmuir {em_types[em_type]}",
                    )
                )
            plt.plot(
                inv_ks_for_interpolation,
                ems_calc,
                c=line.get_color(),
                label=f"Calculated {em_types[em_type]}",
            )
        plt.plot([], [], "o", c="k", label="Table XI values")

        plt.xscale("log")
        plt.xlabel("1/K")
        plt.yscale("log")
        plt.ylabel("Em")
        plt.legend()
        plt.savefig(f"calculation_verification_table_XI_k_phi={k_phi:.0f}_log.png")
    for k_phi in table_XI_data:
        plt.figure(figsize=(8, 6))
        plt.suptitle(f"Kφ={k_phi:.0f}")
        print("k_phi", k_phi)
        for em_type in ["em_a", "em_b", "em_c", "em_d", "em_e"]:
            ks = [1 / _ for _ in table_XI_data[k_phi]["inv_ks"]]
            ems_calc_k_phi_mvd = []
            ems_calc = []
            for inv_k in inv_ks_for_interpolation:
                k = 1/inv_k
            # for k in ks:
                phi = k_phi / k
                match_phi_with_u_result = minimize_scalar(  # find an airspeed to match phi
                    lambda _: abs(
                        calc_phi(tk, p, _, d_cylinder)
                        - max(phi, 0.1)  # use 0.1 to approximate phi=0
                    ),
                    bounds=(0, 1000000),
                    method="bounded",
                )
                if not match_phi_with_u_result.success:
                    raise ValueError(tk, p, d_cylinder, phi, match_phi_with_u_result)
                u = match_phi_with_u_result.x

                match_phi_with_u_result = minimize_scalar(  # find a drop size to match k
                    lambda _: abs(calc_k(tk, u, _, d_cylinder) - k),
                    bounds=(0, 1000000),
                    method="bounded",
                )
                if not match_phi_with_u_result.success:
                    raise ValueError(tk, u, d_cylinder, k, match_phi_with_u_result)
                drop_diameter_micrometer = match_phi_with_u_result.x
                ems_calc.append(
                    calc_em_with_distribution(
                        tk,
                        p,
                        u,
                        drop_diameter_micrometer,
                        d_cylinder,
                        distribution=f"Langmuir {em_types[em_type]}",
                    )
                )
                ems_calc_k_phi_mvd.append(
                    calc_em_with_distribution_k_phi_mvd(
                        tk,
                        p,
                        u,
                        drop_diameter_micrometer,
                        d_cylinder,
                        distribution=f"Langmuir {em_types[em_type]}",
                    )
                )
            line, = plt.plot(
                inv_ks_for_interpolation,
                ems_calc,
                label=f"Calculated with NACA-TR-1215 unique bin k*phi values {em_types[em_type]}",
            )
            plt.plot(
                inv_ks_for_interpolation,
                ems_calc_k_phi_mvd, '--', c=line.get_color(),
                # label=f"Calculated with K*Phi from MVD {em_types[em_type]}",
            )
        plt.plot([], [], '--', c='k',
        label=f"Calculated with K*Phi from MVD",
        )
        plt.xscale("log")
        plt.xlabel("1/K")
        plt.ylim(0, 1)
        # plt.yscale('log')
        plt.ylabel("Em")
        plt.legend()
        plt.savefig(f"compare_em_distribution_with_and_without_k_phi_mvd_k_phi={k_phi:.0f}.png")

    plt.show()
