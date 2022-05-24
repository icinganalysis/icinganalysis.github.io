"""
iads1dmp "Icing Analysis Developmental Software 1 Dimensional Multi-Phase" code

An homage to AEDC1DMP, and python lower case naming convention

The AEDC1DMP is described in:
Schulz, R. J.: Second Report for Research and Modeling of Water Particles in Adverse Weather Simulation Facilities. TASK REPORT 97-03, AEDC, July, 1998, https://apps.dtic.mil/sti/pdfs/ADA364922.pdf
"""
from math import pi
from scipy.interpolate import interp1d
from icinganalysis.air_properties import (
    CP_AIR,
    GAMMA_AIR,
    R_AIR,
    calc_air_density,
    calc_air_viscosity,
    calc_air_thermal_conductivity,
)
from icinganalysis.compressible_flow import calc_mach, calc_mach_from_t_total, calc_a_a_star, calc_mach2_subsonic
from icinganalysis.iteration_helpers import solve_minimize_f, take_by
from icinganalysis.units_helpers import (
    FT_PER_M,
    MICROMETERS_PER_METER,
    PSI_PER_PA,
    G_PER_KG,
)
from icinganalysis.water_properties import (
    WATER_DENSITY,
    WATER_SPECIFIC_HEAT,
    calc_vapor_p,
    find_tk_for_pv,
    RATIO_MOLECULAR_WEIGHTS,
    L_EVAPORATION,
)

gamma = GAMMA_AIR
gp1d2gm1 = (gamma + 1) / (2 * (gamma - 1))  # 3.0
gdgm1 = gamma / (gamma - 1)  # 3.5
inv_gm1 = 1 / (gamma - 1)  # 2.5
gm1d2 = (gamma - 1) / 2  # 0.2
gp1d2 = (gamma + 1) / 2  # 0.7

# fmt: off
d_fig14 = (
    0, 15.6,
    2, 15.6,
    2.5, 15.53,
    3, 15.47,
    3.5, 15.3,
    4, 15.1,
    4.5, 14.8,
    16, 7.25,
    17, 6.6,
    18, 6,
    19, 5.7,
    20, 5.4,
    21, 5.2,
    22, 5,
    23, 4.85,
    24, 4.7,
    25, 4.58,
    26, 4.48,
    27, 4.4,
    28, 4.35,
    29, 4.29,
    30, 4.24,
    31, 4.19,
    32, 4.16,
    33, 4.15,
    34, 4.14,
    45.5, 4.14,
)
# fmt: on
distance_fig14 = [_ / FT_PER_M for _ in d_fig14[::2]]
area_fig_14 = [pi * (_ / FT_PER_M) ** 2 for _ in d_fig14[1::2]]
mach_initial_nominal_fig14 = 0.0188


area_fig_14_interpolator = interp1d(
    distance_fig14, area_fig_14, kind="linear", fill_value="extrapolate"
)

# fmt: off
d_fig15 = (
    0, 20.8, 15.6, 15.6,
    2.5, 21, 21, 18,
    5, 24, 24, 21,
    7.5, 30, 29.5, 23.5,
    10, 39, 38, 28,
    12.5, 55, 52, 37,
    15, 79, 72, 50,
    17.5, 123, 113, 72,
    20, 173, 160, 104,
    22.5, 210, 199, 135,
    25, 242, 230, 162,
    27.5, 268, 258, 187,
    30, 287, 277, 208,
    32.5, 300, 291, 227,
    35, 304, 300, 241,
    37.5, 304, 302, 252,
    40, 304, 303, 260,
    42.5, 304, 304, 266,
    45, 304, 304, 271,
)
# fmt: on
distance_ft_fig15, v_air_fig15, v_50_fig15, v_500_fig15 = zip(*take_by(d_fig15, 4))
distance_fig15 = [_ / FT_PER_M for _ in distance_ft_fig15]
u_air_fig15 = [_ / FT_PER_M for _ in v_air_fig15]
u_50_fig15 = [_ / FT_PER_M for _ in v_50_fig15]
u_500_fig15 = [_ / FT_PER_M for _ in v_500_fig15]
t_total = 500 / 1.8
mach_initial_calculated_fig14 = calc_mach_from_t_total(u_air_fig15[0], t_total)

# fmt: off
d_fig16 = (
    0, 500, 633, 633,
    2.5, 500, 493, 559,
    5, 500, 493, 540,
    7.5, 500, 493, 528,
    10, 500, 493, 520,
    12.5, 500, 493, 514,
    15, 500, 493, 510,
    17.5, 499, 492.5, 508,
    20, 498, 492, 506.5,
    22.5, 497, 491.5, 505,
    25, 495, 491, 504,
    27.5, 494, 490.5, 503,
    30, 492, 490, 502,
    32.5, 492, 489.5, 501.5,
    35, 492, 489, 501,
    37.5, 492, 489, 500.5,
    40, 492, 489, 500,
    42.5, 492, 489, 499.5,
    45, 492, 489, 499,
)
# fmt: on
distance_ft_fig16, t_air_rankine_fig16, t_50_rankine_fig16, t_500_rankine_fig16 = zip(
    *take_by(d_fig16, 4)
)
distance_fig16 = [_ / FT_PER_M for _ in distance_ft_fig16]
tk_air_fig16 = [_ / 1.8 for _ in t_air_rankine_fig16]
tk_50_fig16 = [_ / 1.8 for _ in t_50_rankine_fig16]
tk_500_fig16 = [_ / 1.8 for _ in t_500_rankine_fig16]

# fmt: off
d_fig17 = (
    0, 500,
    2.5, 489.5,
    5, 487.2,
    7.5, 486,
    10, 485,
    12.5, 484.4,
    15, 484.1,
    17.5, 484,
    20, 483.9,
    22.5, 483.8,
    25, 483.7,
    27.5, 483.6,
    30, 483.5,
    32.5, 483.4,
    35, 483.3,
    37.5, 483.2,
    40, 483.1,
    42.5, 483,
    45, 482.9,
)
# fmt: on
distance_fig17 = [_ / FT_PER_M for _ in d_fig17[::2]]
d_drop_fig17 = d_fig17[1::2]

# fmt: off
d_fig17_continued = (
    0, 50,
    1, 48.2,
    2, 48,
    3, 47.85,
    4, 47.7,
    5, 47.55,
    6, 47.4,
    7, 47.25,
    8, 47.15,
    9, 47.05,
    10, 46.95,
    11, 46.85,
    12, 46.75,
    13, 46.68,
    14, 46.61,
    15, 46.54,
    16, 46.48,
    17, 46.43,
    18, 46.38,
    19, 46.35,
    20, 46.32,
    21, 46.3,
    22, 46.28,
    23, 46.26,
    24, 46.24,
    25, 46.22,
    26, 46.21,
    27, 46.201,
    28, 46.192,
    29, 46.183,
    30, 46.174,
    31, 46.165,
    32, 46.155,
    33, 46.146,
    34, 46.14,
    35, 46.134,
    36, 46.137,
    37, 46.131,
    38, 46.135,
    39, 46.139,
    40, 46.132,
    41, 46.136,
    42, 46.13,
    43, 46.133,
    44, 46.137,
    45, 46.131,
    46, 46.134,
)
# fmt: on
distance_fig17_continued = [_ / FT_PER_M for _ in d_fig17_continued[::2]]
d_drop_fig17_continued = d_fig17_continued[1::2]


def calc_ru(tk, p, u, drop_radius):
    """equation (9)"""
    return (
        2
        * (drop_radius / MICROMETERS_PER_METER)
        * calc_air_density(tk, p)
        * u
        / calc_air_viscosity(tk)
    )


def calc_cd_r_24_approx(re_relative):
    """equation (22)"""
    return 1 + 0.197 * re_relative ** 0.63 + 2.6e-4 * re_relative ** 1.38


def calc_u_fig14(x):
    area = area_fig_14_interpolator(x)
    t_total = tk_air_fig16[0]
    mach = calc_mach2_subsonic(area_fig_14[0], mach_initial_nominal_fig14, area)
    tk = t_total / (1 + gm1d2 * mach ** 2)
    return mach * (gamma * R_AIR * tk) ** 0.5


def integrate_drop(
    tk_total,
    p_total,
    d_drop,
    v_drop,
    t_drop,
    initial_position,
    final_position,
    rh=1.0,
    lwc=1.0,
    u_function_of_x=calc_u_fig14,
    tau=0.0001,
    n_max=1000000,
):
    xs = [initial_position]
    vs = [v_drop]
    u = u_function_of_x(xs[-1])
    tk = tk_total - u ** 2 / 2 / CP_AIR
    us = [u]
    t_drops = [t_drop]
    d_drops = [d_drop]
    rhs = [rh]
    tks = [tk]
    lwcs = [lwc]
    t_totals = [tk_total]

    for i in range(n_max):
        mach = calc_mach_from_t_total(u, t_totals[-1])
        tk = tk_total / (1 + gm1d2 * mach ** 2)
        p = p_total / (1 + gm1d2 * mach ** 2) ** gdgm1
        (
            x2,
            v2,
            t_drop2,
            d_drop2,
            rh2,
            lwc2,
            t_total2,
        ) = increment_drop_position_adapt_tau(
            tks[-1],
            p,
            u_function_of_x,
            vs[-1],
            d_drops[-1],
            t_drops[-1],
            tau,
            xs[-1],
            rhs[-1],
            lwcs[-1],
        )

        if (
            d_drop2 != d_drop2
        ):  # float('nan'), drop evaporated, cannot continue the integration
            break

        if x2 <= xs[-1]:
            raise ValueError(
                f"Integration error, try a smaller tau value, x2 <= xs[-1], tau={tau}, x2={x2} xs[-1]={xs[-1]}"
            )

        if x2 > final_position:
            u = u_function_of_x(final_position)
            t_drop2 = t_drops[-1] + (t_drop2 - t_drops[-1]) * (
                final_position - xs[-1]
            ) / (x2 - xs[-1])
            d_drop2 = d_drops[-1] + (d_drop2 - d_drops[-1]) * (
                final_position - xs[-1]
            ) / (x2 - xs[-1])
            t_total2 = t_totals[-1] + (t_total2 - t_totals[-1]) * (
                final_position - xs[-1]
            ) / (x2 - xs[-1])
            tk = t_total2 - u ** 2 / 2 / CP_AIR
            rh2 = rhs[-1] + (rh2 - rhs[-1]) * (final_position - xs[-1]) / (x2 - xs[-1])
            lwc2 = lwcs[-1] + (lwc2 - lwcs[-1]) * (final_position - xs[-1]) / (
                x2 - xs[-1]
            )
        xs.append(x2)
        vs.append(v2)
        u = u_function_of_x(x2)
        t_drops.append(t_drop2)
        d_drops.append(d_drop2)
        us.append(u)
        tks.append(tk)
        rhs.append(rh2)
        lwcs.append(lwc2)
        t_totals.append(t_total2)
        if x2 > final_position:
            xs[-1] = final_position
            break
    else:
        raise ValueError(
            f"Did not complete integration, try increasing n_max or tau,\nx={xs[-1]}, target final position={final_position}, tau={tau}, n_max={n_max}"
        )
    return xs, vs, us, t_drops, d_drops, tks, rhs, lwcs, t_totals


def increment_drop_position_adapt_tau(
    tk, p, u_function_of_x, v_drop, d_drop, t_drop, d_tau, position, rh=1.0, lwc=1
):
    position2, v_drop2, t_drop2, d_drop2, rh2, lwc2, t_total2 = increment_drop_position(
        tk,
        p,
        u_function_of_x(position),
        v_drop,
        d_drop,
        t_drop,
        d_tau,
        position,
        rh,
        lwc,
    )
    if abs(t_drop - t_drop2) > 1:
        tau = d_tau / 10
        mach = calc_mach(u_function_of_x(position), tk)
        position2, v_drop2, t_drop2, d_drop2, rh2, lwc2 = (
            position,
            v_drop,
            t_drop,
            d_drop,
            rh,
            lwc,
        )
        for i in range(10):
            (
                position2,
                v_drop2,
                t_drop2,
                d_drop2,
                rh2,
                lwc2,
                t_total2,
            ) = increment_drop_position(
                tk,
                p,
                u_function_of_x(position2),
                v_drop2,
                d_drop2,
                t_drop2,
                tau,
                position2,
                rh2,
                lwc2,
            )
            mach2 = calc_mach_from_t_total(u_function_of_x(position2), t_total2)
            tk = t_total2 * (1 + gm1d2 * mach2 ** 2)
            p = p * (1 + gm1d2 * mach ** 2) ** gdgm1 / (1 + gm1d2 * mach2 ** 2) ** gdgm1

    return position2, v_drop2, t_drop2, d_drop2, rh2, lwc2, t_total2


def increment_drop_position(
    tk, p, u, v_drop, d_drop, t_drop, d_tau, position, rh=1.0, lwc=1
):
    r = 0.8  # NACA-TN-3024, "Note that a recovery coefficient of 0.8 is used; this is no more than a representative average figure based on many data reported in the literature."
    mach = calc_mach(u, tk)
    re_relative = calc_ru(tk, p, abs(u - v_drop), d_drop / 2)
    mach_relative = calc_mach(abs(u - v_drop), tk)
    t_static_local_drop_relative = (
        tk * (1 + gm1d2 * mach ** 2) / (1 + gm1d2 * mach_relative ** 2)
    )  # after equation 1 in NACA-TN-3024
    t_recovery_local_drop_relative = t_static_local_drop_relative * (
        1 + r * gm1d2 * mach_relative ** 2
    )  # after equation 1 in NACA-TN-3024

    cd_r_24 = calc_cd_r_24_approx(re_relative)
    f = (
        cd_r_24
        * 6
        * pi
        * (u - v_drop)
        * d_drop
        / MICROMETERS_PER_METER
        / 2
        * calc_air_viscosity(tk)
    )
    mass = pi / 6 * (d_drop / MICROMETERS_PER_METER) ** 3 * WATER_DENSITY
    if mass <= 0:
        position2, v_drop2, t_drop, d_drop2, rh2, lwc2, t_total2 = (
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
        )
        return position2, v_drop2, t_drop, d_drop2, rh2, lwc2, t_total2
    n = lwc / G_PER_KG / mass
    accel = f / mass
    delta_v = accel * d_tau
    v_drop2 = v_drop + delta_v
    position2 = position + v_drop * d_tau + delta_v / 2 * d_tau

    nu = 2 + 0.2464 * (0.71) ** (1 / 3) * re_relative ** 0.6393  # NACA-TN-3024, page 10
    hc = nu * calc_air_thermal_conductivity(tk) / (d_drop / MICROMETERS_PER_METER)
    nue = 2 + 0.33 * re_relative ** 0.56  # NACA-TN-3024, page 11
    hce = nue * calc_air_thermal_conductivity(tk) / (d_drop / MICROMETERS_PER_METER)

    pv = rh * calc_vapor_p(tk)
    pvs = calc_vapor_p(t_drop)
    me = 1.12 * hce * RATIO_MOLECULAR_WEIGHTS / CP_AIR * (pvs / p - pv / p)
    qe = me * L_EVAPORATION
    surface_area = 4 * pi * (d_drop / 2 / MICROMETERS_PER_METER) ** 2
    qc = surface_area * hc * (t_recovery_local_drop_relative - t_drop) * d_tau
    q = surface_area * (hc * (t_recovery_local_drop_relative - t_drop) - qe) * d_tau
    delta_mass = me * surface_area * d_tau
    mass2 = mass - delta_mass
    if mass2 < 0:
        mass2 = 0
    d_drop2 = (mass2 * 6 / pi / WATER_DENSITY) ** (1 / 3) * MICROMETERS_PER_METER
    dt = q / (mass * WATER_SPECIFIC_HEAT)
    t_drop += dt

    rho = p / (R_AIR * tk)
    lwc2 = lwc - (delta_mass * n * G_PER_KG)
    vapor_mass = pv / (R_AIR / RATIO_MOLECULAR_WEIGHTS * tk)
    vapor_mass2 = vapor_mass + delta_mass * n
    pv2 = vapor_mass2 * (R_AIR / RATIO_MOLECULAR_WEIGHTS * tk)

    t_total = tk * (1 + gm1d2 * mach ** 2)
    t_total2 = t_total - qc * n / rho / CP_AIR
    tk2 = t_total2 / (1 + gm1d2 * mach ** 2)
    rh2 = pv2 / calc_vapor_p(tk2)

    return position2, v_drop2, t_drop, d_drop2, rh2, lwc2, t_total2


if __name__ == "__main__":
    p_total = 2047 / 144 / PSI_PER_PA
    t_total = 500 / 1.8
    rh = 0.547
    x_start = 0
    x_finish = 46 / FT_PER_M
    mass_ratio_water_air = 0.00018  # Table II LF "load factor"

    u0 = u_air_fig15[0]
    mach = calc_mach_from_t_total(u0, t_total)
    tk = t_total / (1 + gm1d2 * mach ** 2)
    p = p_total / (1 + gm1d2 * mach ** 2) ** gdgm1
    rho_air = calc_air_density(tk, p)
    lwc = rho_air * mass_ratio_water_air * G_PER_KG
    print("lwc", lwc)

    import matplotlib.pyplot as plt

    d_drop = 500
    v_drop0 = u_500_fig15[0]
    t_drop_start = tk_500_fig16[0]
    taus = 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001
    all_final_vs = []
    for tau in taus:
        xs, vs, us, t_drops, d_drops, tks, rhs, lwcs, t_totals = integrate_drop(
            t_total,
            p_total,
            d_drop,
            v_drop0,
            t_drop_start,
            x_start,
            x_finish,
            rh,
            lwc,
            tau=tau,
        )
        all_final_vs.append(
            (
                xs[-1],
                vs[-1],
                us[-1],
                t_drops[-1],
                d_drops[-1],
                tks[-1],
                rhs[-1],
                lwcs[-1],
                t_totals[-1],
            )
        )

    plt.figure()
    (xs, vs, us, t_drops, d_drops, tks, rhs, lwcs, t_totals) = zip(*all_final_vs)
    plt.plot(taus, t_drops, "--+", label="Drop diameter=500 micrometer")
    plt.xlabel("Dimensionless time step tau")
    plt.xscale("log")
    plt.ylabel("T drop final")
    plt.ylim(min(260, plt.ylim()[0]), max(280, plt.ylim()[1]))
    plt.legend()
    plt.savefig("iads1dmp_tau_sensitivity.png")

    d_drop = 50
    v_drop0 = u_50_fig15[0]
    t_drop_start = tk_50_fig16[0]
    xs, vs, us, t_drops, d_drops, tks, rhs, lwcs, t_totals = integrate_drop(
        t_total, p_total, d_drop, v_drop0, t_drop_start, x_start, x_finish, rh, lwc
    )

    d_drop = 500
    v_drop0 = u_500_fig15[0]
    t_drop_start = tk_500_fig16[0]
    (
        xs500,
        vs500,
        us500,
        t_drops500,
        d_drops500,
        tks500,
        rhs500,
        lwcs500,
        t_totals500,
    ) = integrate_drop(
        t_total, p_total, d_drop, v_drop0, t_drop_start, x_start, x_finish, rh, lwc
    )

    plt.figure()
    plt.suptitle("TASK REPORT 97-03, Reference Case 2")
    (line,) = plt.plot(xs, vs, label="Calculated 50 micrometer")
    plt.plot(
        distance_fig15,
        u_50_fig15,
        "^",
        fillstyle="none",
        c=line.get_color(),
        label="Figure 15 50 micrometer",
    )
    (line,) = plt.plot(xs500, vs500, label="Calculated 500 micrometer")
    plt.plot(
        distance_fig15,
        u_500_fig15,
        "s",
        fillstyle="none",
        c=line.get_color(),
        label="Figure 15 500 micrometer",
    )
    (line,) = plt.plot(xs, us, "--", label="Calculated air")
    plt.plot(
        distance_fig15,
        u_air_fig15,
        "o",
        fillstyle="none",
        c=line.get_color(),
        label="Figure 15 air",
    )
    plt.xlim(0)
    plt.ylim(0)
    plt.xlabel("Distance, m")
    plt.ylabel("Velocity, m/s")
    plt.legend()
    plt.savefig("iads1dmp_velocity.png")

    plt.figure()
    plt.suptitle("TASK REPORT 97-03, Reference Case 2")
    (line,) = plt.plot(xs, t_drops, label="Calculated drop temperature 50 micrometer")
    plt.plot(
        distance_fig16,
        tk_50_fig16,
        "^",
        fillstyle="none",
        c=line.get_color(),
        label="Figure 15 50 micrometer",
    )
    t_vaps = [find_tk_for_pv(rh * calc_vapor_p(t)) for rh, t in zip(rhs, tks)]
    plt.plot(
        xs,
        t_vaps,
        ":",
        c=line.get_color(),
        label="Saturated vapor temperature 50 micrometer",
    )
    (line,) = plt.plot(
        xs500, t_drops500, label="Calculated drop temperature 500 micrometer"
    )
    plt.plot(
        distance_fig16,
        tk_500_fig16,
        "s",
        fillstyle="none",
        c=line.get_color(),
        label="Figure 15 500 micrometer",
    )
    t_vaps500 = [find_tk_for_pv(rh * calc_vapor_p(t)) for rh, t in zip(rhs500, tks500)]
    plt.plot(
        xs500,
        t_vaps500,
        ":",
        c=line.get_color(),
        label="Saturated vapor temperature 500 micrometer",
    )
    (line,) = plt.plot(xs, tks, "--", label="Calculated air T_static")
    plt.plot(
        distance_fig16,
        tk_air_fig16,
        "o",
        fillstyle="none",
        c=line.get_color(),
        label="Figure 15 air",
    )

    plt.plot(xs, t_totals, "-.", label="Total temperature 50 micrometer")

    plt.xlabel("Distance, m")
    plt.ylabel("Temperature, K")
    plt.ylim(min(plt.ylim()[0], 260))
    plt.yticks(range(260, 370, 10))
    plt.legend()
    plt.savefig("iads1dmp_temperature.png")

    plt.figure()
    plt.suptitle("TASK REPORT 97-03, Reference Case 2")
    (line,) = plt.plot(xs, d_drops, label="Calculated 50 micrometer")
    plt.plot(
        distance_fig17_continued,
        d_drop_fig17_continued,
        "^",
        ms=10,
        fillstyle="none",
        c=line.get_color(),
        label="Figure 17 values 50 micrometer",
    )
    (line,) = plt.plot(xs500, d_drops500, label="Calculated 500 micrometer")
    plt.plot(
        distance_fig17,
        d_drop_fig17,
        "s",
        ms=14,
        fillstyle="none",
        c=line.get_color(),
        label="Figure 17 values 500 micrometer",
    )
    plt.ylim(0)
    plt.xlabel("Distance, m")
    plt.ylabel("Drop diameter, micrometer")
    plt.legend()
    plt.savefig("iads1dmp_drop_size.png")

    plt.figure()
    plt.suptitle("TASK REPORT 97-03, Reference Case 2")
    (line,) = plt.plot(xs, d_drops, label="Calculated 50 micrometer")
    plt.plot(
        distance_fig17_continued,
        d_drop_fig17_continued,
        "^",
        ms=10,
        fillstyle="none",
        c=line.get_color(),
        label="Figure 17 values 50 micrometer",
    )
    plt.ylim(0)
    plt.xlabel("Distance, m")
    plt.ylabel("Drop diameter, micrometer")
    plt.legend()
    plt.savefig("iads1dmp_drop_size50.png")

    plt.figure()
    plt.suptitle("TASK REPORT 97-03, Reference Case 2")
    plt.plot(xs, rhs, label="Calculated 50 micrometer")
    plt.plot(xs500, rhs500, "--", label="Calculated 500 micrometer")
    plt.ylim(0, max(1, plt.ylim()[1]))
    plt.xlabel("Distance, m")
    plt.ylabel("Relative humidity (fraction)")
    plt.legend()
    plt.savefig("iads1dmp_rh.png")

    plt.figure()
    plt.suptitle("TASK REPORT 97-03, Reference Case 2")
    plt.plot(xs, lwcs, label="Calculated 50 micrometer")
    plt.plot(xs500, lwcs500, "--", label="Calculated 500 micrometer")
    plt.ylim(0, 1.1 * plt.ylim()[1])
    plt.xlabel("Distance, m")
    plt.ylabel("LWC, liquid water content, g/m^3")
    plt.legend()
    plt.savefig("iads1dmp_lwc.png")

    plt.figure()
    v_rel = [(u_ - v_) for u_, v_ in zip(us, vs)]
    v_rel500 = [(u_ - v_) for u_, v_ in zip(us500, vs500)]
    plt.plot(xs, v_rel, label="50 micrometer")
    plt.plot(xs500, v_rel500, "--", label="500 micrometer")
    plt.ylim(0)
    plt.xlabel("Distance, m")
    plt.ylabel("Relative velocity, m/s")
    plt.legend()

    plt.show()
