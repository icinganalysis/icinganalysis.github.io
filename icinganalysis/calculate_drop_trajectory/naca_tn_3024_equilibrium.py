from math import pi
from icinganalysis.air_properties import calc_pressure, CP_AIR, GAMMA_AIR, R_AIR, calc_air_thermal_conductivity, calc_air_density, calc_air_viscosity
from icinganalysis.iads1dmp import calc_mach, calc_mach_from_t_total
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis.units_helpers import FT_PER_M, INCH_PER_M, MICROMETERS_PER_METER, tc_to_k, G_PER_KG
from icinganalysis.water_properties import RATIO_MOLECULAR_WEIGHTS, find_tk_for_pv, WATER_DENSITY, calc_vapor_p, L_EVAPORATION, WATER_SPECIFIC_HEAT
gamma = GAMMA_AIR
gp1d2gm1 = (gamma + 1) / (2 * (gamma - 1))  # 3.0
gdgm1 = gamma / (gamma - 1)  # 3.5
inv_gm1 = 1 / (gamma - 1)  # 2.5
gm1d2 = (gamma - 1) / 2  # 0.2
gp1d2 = (gamma + 1) / 2  # 0.7

# fmt: off
d_figure9 = (
    0.001, 0.00235,
    0.007, 0.0023,
    0.02, 0.0022,
    0.05, 0.002,
    0.1, 0.0018,
    0.2, 0.00135,
    0.3, 0.00105,
    0.4, 0.00085,
    0.5, 0.00065,
    0.75, 0.00037,
    1, 0.00022,
    1.5, 0.00011,
)
# fmt: on
radii_figure9 = d_figure9[::2]
fraction_evap_figure9 = d_figure9[1::2]

# fmt: off
d_figure8 = (
    0.001, 0.31, 0.0015,
    0.007, 0.31, 0.01,
    0.02, 0.31, 0.028,
    0.05, 0.3, 0.067,
    0.1, 0.28, 0.125,
    0.2, 0.245, 0.22,
    0.3, 0.21, 0.295,
    0.4, 0.185, 0.35,
    0.5, 0.165, 0.4,
    0.75, 0.125, 0.495,
    1, 0.095, 0.55,
    1.25, 0.075, 0.59,
    1.5, 0.06, 0.62,
    2, 0.04, 0.655,
    2.5, 0.028, 0.68,
    3, 0.021, 0.7,
    4, 0.012, 0.715,
    5, 0.0075, 0.73,
    6, 0.005, 0.735,
    7, 0.003, 0.74,
    8, 0.0015, 0.75,
)
# fmt: on
radii_figure8 = d_figure8[::3]
drop_mach_relative8 = d_figure8[1::3]
air_mach8 = d_figure8[2::3]


def make_u_function_of_x(u, diameter):
    """equation (23) rearranged to use distance, d = (x-1)"""

    def f(d):
        d = abs(d / diameter)
        if d < 1e-15:
            return u * 2 * d
        return u * (d ** 2 + 2 * d) / (d ** 2 + 2 * d + 1)

    return f


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


def integrate_drop(
    tk_total,
    p_total,
    d_drop,
    v_drop,
    t_drop,
    initial_position,
    final_position,
    rh,
    lwc,
    u_function_of_x,
    tau=0.0001,
    n_max=1000000,
    include_t_total_change=False,
    include_vapor_ratio_change=False,
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
    mach = calc_mach_from_t_total(u, t_totals[-1])
    p = p_total / (1 + gm1d2 * mach ** 2) ** gdgm1
    rho_air = p / (R_AIR * tk)
    vapor_ratios = [rh * calc_vapor_p(tk) * RATIO_MOLECULAR_WEIGHTS / (p)]
    water_ratio = lwc / G_PER_KG / rho_air
    mass_of_drop = WATER_DENSITY * pi / 6 * (d_drop / MICROMETERS_PER_METER) ** 3
    number_of_drops_per_unit_mass_dry_air = water_ratio / mass_of_drop * rho_air
    t_drop_recs = [float("nan")]
    for i in range(n_max):
        (
            v_drop2,
            d_drop2,
            t_drop2,
            delta_position,
            t_recovery_local_drop_relative,
            qc
        ) = increment_drop_position(tau, t_totals[-1], p_total, us[-1], vs[-1], d_drops[-1], t_drops[-1],
                                    vapor_ratios[-1])
        if (
            d_drop2 != d_drop2
        ):  # float('nan'), drop evaporated, cannot continue the integration
            break
        position2 = xs[-1] + delta_position
        if position2 <= xs[-1]:
            raise ValueError(
                f"Integration error, try a smaller tau value, x2 <= xs[-1], tau={tau}, x2={position2} xs[-1]={xs[-1]}"
            )

        t_total2 = tk_total
        if include_t_total_change:
            t_total2 = t_total - qc * number_of_drops_per_unit_mass_dry_air / CP_AIR
        u2 = u_function_of_x(position2)
        mach2 = calc_mach_from_t_total(u2, t_total2)
        tk2 = t_total2 / (1 + gm1d2 * mach2 ** 2)
        p2 = p_total / (1 + gm1d2 * mach2 ** 2) ** gp1d2gm1

        mass_of_drop = WATER_DENSITY * pi / 6 * (d_drops[-1] / MICROMETERS_PER_METER) ** 3
        mass_of_drop2 = WATER_DENSITY * pi / 6 * (d_drop2 / MICROMETERS_PER_METER) ** 3
        delta_mass_of_drop = mass_of_drop2 - mass_of_drop
        vrx = vapor_ratios[-1] - delta_mass_of_drop * number_of_drops_per_unit_mass_dry_air
        vapor_ratio2 = vrx
        if not include_vapor_ratio_change:
            vapor_ratio2 = vapor_ratios[-1]
        rh2 = p2 * vapor_ratio2 / RATIO_MOLECULAR_WEIGHTS / calc_vapor_p(tk2)
        lwc2 = number_of_drops_per_unit_mass_dry_air * mass_of_drop2 * G_PER_KG

        if position2 > final_position:
            u = u_function_of_x(final_position)
            t_drop2 = t_drops[-1] + (t_drop2 - t_drops[-1]) * (
                final_position - xs[-1]
            ) / (position2 - xs[-1])
            d_drop2 = d_drops[-1] + (d_drop2 - d_drops[-1]) * (
                final_position - xs[-1]
            ) / (position2 - xs[-1])
            t_total2 = t_totals[-1] + (t_total2 - t_totals[-1]) * (
                final_position - xs[-1]
            ) / (position2 - xs[-1])
            tk2 = t_total2 - u ** 2 / 2 / CP_AIR
            rh2 = rhs[-1] + (rh2 - rhs[-1]) * (final_position - xs[-1]) / (
                position2 - xs[-1]
            )
            lwc2 = lwcs[-1] + (lwc2 - lwcs[-1]) * (final_position - xs[-1]) / (
                position2 - xs[-1]
            )
            vapor_ratio2 = vapor_ratios[-1] + (vapor_ratio2 - vapor_ratios[-1]) * (
                final_position - xs[-1]
            ) / (position2 - xs[-1])
        xs.append(position2)
        vs.append(v_drop2)
        t_drops.append(t_drop2)
        d_drops.append(d_drop2)
        us.append(u2)
        tks.append(tk2)
        rhs.append(rh2)
        lwcs.append(lwc2)
        t_drop_recs.append(t_recovery_local_drop_relative)
        t_totals.append(t_total2)
        vapor_ratios.append(vapor_ratio2)
        if position2 > final_position:
            xs[-1] = final_position
            break
    else:
        raise ValueError(
            f"Did not complete integration, try increasing n_max or tau,\nx={xs[-1]}, target final position={final_position}, tau={tau}, n_max={n_max}"
        )
    print("iterations", i)
    return (
        xs,
        vs,
        us,
        t_drops,
        d_drops,
        tks,
        rhs,
        lwcs,
        t_totals,
        vapor_ratios,
        t_drop_recs,
    )


def increment_drop_position(d_tau, t_total, p_total, u, v_drop, d_drop, t_drop, vapor_ratio):
    """

    :param d_tau: time step, seconds
    :param t_total: air total temperature, K
    :param p_total: air total pressure, Pa
    :param u: local air speed, m/s
    :param v_drop: water drop speed, m/s
    :param d_drop: water drop diameter, micrometer
    :param t_drop: water drop temperature, K
    :param vapor_ratio:
    :return:
    """
    r = 0.8  # NACA-TN-3024, "Note that a recovery coefficient of 0.8 is used; this is no more than a representative average figure based on many data reported in the literature."
    mach = calc_mach_from_t_total(u, t_total)
    tk = t_total / (1 + gm1d2 * mach ** 2)
    p = p_total / (1 + gm1d2 * mach ** 2) ** gdgm1
    re_relative = calc_ru(tk, p, abs(u - v_drop), d_drop / 2)
    mach_relative = calc_mach(abs(u - v_drop), tk)
    t_static_local = tk  # after equation 1 in NACA-TN-3024, p. 7
    t_drop_effective_local = t_static_local * (
        1 + r * gm1d2 * mach_relative ** 2
    )  # after equation 1 in NACA-TN-3024, p. 7
    p_effective_local_relative = (
        p_total
        / (1 + gm1d2 * mach ** 2) ** gdgm1
        * (1 + gm1d2 * mach_relative ** 2) ** gdgm1
    )
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
    mass_of_drop = pi / 6 * (d_drop / MICROMETERS_PER_METER) ** 3 * WATER_DENSITY
    if mass_of_drop <= 1e-15:
        (
            t_total2,
            v_drop2,
            d_drop2,
            t_drop2,
            delta_position,
            vapor_ratio2,
            t_drop_effective_local,
        ) = (
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
        )
        return (
            t_total2,
            v_drop2,
            d_drop2,
            t_drop2,
            delta_position,
            vapor_ratio2,
            t_drop_effective_local,
        )
    accel = f / mass_of_drop
    delta_v = 1 * accel * d_tau
    v_drop2 = v_drop + delta_v
    delta_position = v_drop * d_tau + delta_v / 2 * d_tau
    nu = 2 + 0.2464 * (0.71) ** (1 / 3) * re_relative ** 0.6393  # NACA-TN-3024, page 10
    hc = nu * calc_air_thermal_conductivity(tk) / (d_drop / MICROMETERS_PER_METER)
    nue = 2 + 0.33 * re_relative ** 0.56  # NACA-TN-3024, page 11
    hce = nue * calc_air_thermal_conductivity(tk) / (d_drop / MICROMETERS_PER_METER)
    pv = p * vapor_ratio / RATIO_MOLECULAR_WEIGHTS
    t_drop = calc_t_drop_equilibrium(hc, hce, pv, p, p_effective_local_relative, t_drop_effective_local)

    pvs = calc_vapor_p(t_drop)
    me = (
        hce
        * RATIO_MOLECULAR_WEIGHTS
        / CP_AIR
        * (pvs / p_effective_local_relative - pv / p)
    )
    qe = me * L_EVAPORATION
    surface_area = 4 * pi * (d_drop / 2 / MICROMETERS_PER_METER) ** 2
    qc = surface_area * hc * (t_drop_effective_local - t_drop) * d_tau
    delta_mass_of_drop = me * surface_area * d_tau
    mass_of_drop2 = mass_of_drop - delta_mass_of_drop
    if mass_of_drop2 < 0:
        raise ValueError(
            "mass_of_drop, delta_mass_of_drop", mass_of_drop, delta_mass_of_drop
        )

    d_drop2 = (mass_of_drop2 * 6 / pi / WATER_DENSITY) ** (
        1 / 3
    ) * MICROMETERS_PER_METER
    t_drop2 = t_drop

    return (
        v_drop2,
        d_drop2,
        t_drop2,
        delta_position,
        t_drop_effective_local,
        qc
    )


def calc_t_drop_equilibrium(hc, hce, pv, p, p_effective_local_relative, t_drop_effective_local):
    def calc_diff(t_drop):
        pvs = calc_vapor_p(t_drop)
        me = (
            hce
            * RATIO_MOLECULAR_WEIGHTS
            / CP_AIR
            * (pvs / p_effective_local_relative - pv / p)
        )
        qe = me * L_EVAPORATION
        return abs(hc * (t_drop_effective_local - t_drop) - qe)

    t_drop = solve_minimize_f(calc_diff, bounds=[202, 373])
    return t_drop


if __name__ == "__main__":

    d_cyl = 3.95 / INCH_PER_M
    alt = 10000 / FT_PER_M
    mvd = 15
    lwc = 0.5
    p = calc_pressure(alt)
    tk = tc_to_k(-25)
    mach_inf = 0.75
    rh = 0.9
    mach = mach_inf
    t_total = tk * (1 + 0.2 * mach ** 2)
    p_total = p * (1 + 0.2 * mach ** 2) ** 3.5
    u_inf = mach * (GAMMA_AIR * R_AIR * tk) ** 0.5
    f = make_u_function_of_x(u_inf, d_cyl)
    x_start = -20 * d_cyl
    u = f(x_start)
    t_drop = t_total - u**2/2/CP_AIR
    v_drop = f(x_start)
    tk = t_total - u**2 / 2 / CP_AIR

    import matplotlib.pyplot as plt

    taus = (0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001)
    delta_lwcs = []
    print(t_total, p_total, mvd, v_drop, tk, x_start)
    for tau in taus:
        (xs,
        vs,
        us,
        t_drops,
        d_drops,
        tks,
        rhs,
        lwcs,
        t_totals,
        vapor_ratios, t_drop_effective_local) = integrate_drop(t_total, p_total, mvd, v_drop, tk, x_start, 0, rh, 1, f,
                                                               tau=tau)
        delta_lwcs.append([abs(_ - lwcs[0]) for _ in lwcs][-1])
        print(tau, delta_lwcs[-1])

    plt.figure()
    plt.plot(taus, delta_lwcs, "--+")
    plt.xscale("log")
    plt.xlabel("Dimensionless time step, tau")
    plt.ylabel("Delta LWC, g/m^2")
    plt.savefig("naca_tn_3024_tau_sensitivity_equilibrium.png")

    tau = 0.0000001  # a rather small tau value is required

    (xs,
        vs,
        us,
        t_drops,
        d_drops,
        tks,
        rhs,
        lwcs,
        t_totals,
        vapor_ratios,
     t_drop_recs) = integrate_drop(t_total, p_total, mvd, v_drop, t_drop, x_start, -1e-6, rh, lwc, f, tau=tau)

    plt.figure()
    plt.suptitle("Figure 8 Comparison")
    v_rel = [abs(u_ - v_) for u_, v_ in zip(us, vs)]

    mach_rel = [mach_inf * _ / u_inf for _ in v_rel]
    mach_us = [mach_inf * _ / u_inf for _ in us]
    mach_vs = [mach_inf * _ / u_inf for _ in vs]
    radii = [abs(-_ / d_cyl * 2) for _ in xs]
    (line,) = plt.plot(radii, mach_us, ":", label="Air Mach")
    plt.plot(
        radii_figure8, air_mach8, ":+", c=line.get_color(), label="Air Figure 8 values"
    )
    (line,) = plt.plot(radii, mach_rel, label="Drop relative Mach")
    plt.plot(
        radii_figure8,
        drop_mach_relative8,
        "--^",
        c=line.get_color(),
        label="Drop relative Figure 8 values",
    )
    plt.plot(radii, mach_vs, "--", label="Drop (speed) Mach")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim(1e-3, 10)
    plt.ylim(1e-3, 1)
    plt.xlabel("Distance from cylinder surface, radii (distance/r_cylinder)")
    plt.ylabel("Mach, m/s")
    plt.legend()
    plt.savefig("naca_tn_3024_mach_equilibrium.png")

    plt.figure()
    plt.plot(xs, [p_total]*len(xs), '--', label="p_total")
    p_relative_drops = [p_total/(1+0.2*mach_relative**2)**3.5 for mach_relative in mach_rel]
    plt.plot(xs, p_relative_drops, label="p_relative_drop")
    ps = [p_total/(1+0.2*mach_**2)**3.5 for mach_ in mach_us]
    plt.plot(xs, ps, label="P_static")
    plt.xlabel("Distance from cylinder surface, m")
    plt.ylabel("P, Pa")
    plt.legend()

    plt.figure()

    t_sats = []
    for t_, ratio, u_ in zip(tks, vapor_ratios, us):
        mach = calc_mach_from_t_total(u_, t_total)
        p = p_total / (1+0.2*mach**2)**3.5
        pv = p*ratio/RATIO_MOLECULAR_WEIGHTS
        t_sats.append(find_tk_for_pv(pv))

    plt.plot(radii, tks, "--", label="Air static temperature")
    plt.plot(radii, t_totals, ":", label="Air total temperature")
    plt.plot(radii, t_drops, label="Drop temperature")
    plt.plot(radii, t_drop_recs, '-.', label="T drop effective local")
    plt.plot(radii, t_sats, ':', label="Vapor saturation temperature")
    plt.xlim(0)
    plt.ylabel("Temperature, K")
    plt.xlabel("Distance from cylinder surface, radii (distance/r_cylinder)")
    plt.legend()
    plt.savefig("naca_tn_3024_temperature_equilibrium.png")

    plt.figure()
    plt.suptitle("Figure 9 Comparison")
    plt.plot(
        [abs(-_ / d_cyl * 2) for _ in xs],
        [abs(_ - lwcs[0])/lwcs[0] for _ in lwcs],
        label="iads1dmp (loss)",
    )
    plt.plot(radii_figure9, fraction_evap_figure9, ":^", label="Figure 9 values")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim(1e-3, 10)
    plt.ylim(1e-4, 1)
    plt.xlabel("Distance from cylinder surface, radii (distance/r_cylinder)")
    plt.ylabel("fraction LWC change")
    plt.plot()
    plt.legend()
    plt.savefig("naca_tn_3024_lwc_change_equilibrium.png")

    plt.figure()
    plt.plot(radii, d_drops)
    plt.xscale("log")

    from icinganalysis import langmuir_cylinder_values
    print()

    # A case from cylinder_drop_1d_trajectory_shift.py
    tk = 263
    p = 101325
    u = 90
    phi = 1000
    k = 0.125
    d_drop = langmuir_cylinder_values.calc_drop_diameter_micrometer_from_re_drop(
        (k * phi) ** 0.5, tk, p, u
    )
    get_d_drop = langmuir_cylinder_values.calc_drop_diameter_micrometer_from_re_drop
    d_cyl = langmuir_cylinder_values.calc_d_cylinder_from_phi(phi, tk, p, u)
    print(d_drop)
    print(d_cyl)
    print("K*Phi", langmuir_cylinder_values.calc_k_phi(tk, p, u, d_drop))
    print("Phi", langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl))
    print("K", langmuir_cylinder_values.calc_k(tk, u, d_drop, d_cyl))
    mach = calc_mach(u, tk)
    t_total = tk * (1 + 0.2 * mach ** 2)
    p_total = p * (1 + 0.2 * mach ** 2) ** 3.5
    u_inf = mach * (GAMMA_AIR * R_AIR * tk) ** 0.5
    f = make_u_function_of_x(u_inf, d_cyl)
    x_start = -10 * d_cyl
    u = f(x_start)
    v_drop = f(x_start)
    mach_start = calc_mach_from_t_total(u, t_total)
    tk = t_total / (1 + 0.2 * mach_start ** 2)
    t_drop = tk
    tau = 0.0000001
    final_position = -d_drop / MICROMETERS_PER_METER / 2
    # final_position = -1e-30
    print('t_total', t_total)
    (xs,
        vs,
        us,
        t_drops,
        d_drops,
        tks,
        rhs,
        lwcs,
        t_totals,
        vapor_ratios, t_drop_recs) = integrate_drop(t_total, p_total, d_drop, v_drop, t_drop, x_start, final_position,
                                                    1, 1, f, tau=tau)
    plt.figure()
    plt.suptitle(f"Phi=1000, K=0.125")
    plt.plot(xs, d_drops)
    plt.ylim(0, 1.2*d_drop)
    plt.xlabel("Distance from cylinder, m")
    plt.ylabel("Drop diameter, micrometer")
    plt.savefig("naca_tn_3024_d_drop_k0_125_equilibrium.png")
    print((d_drops[-1]-d_drops[0])/d_drops[0])
    t_sats = []
    for t_, ratio, u_ in zip(tks, vapor_ratios, us):
        mach = calc_mach_from_t_total(u_, t_total)
        p = p_total / (1+0.2*mach**2)**3.5
        pv = p*ratio/RATIO_MOLECULAR_WEIGHTS
        t_sats.append(find_tk_for_pv(pv))

    plt.figure()
    plt.suptitle(f"Phi=1000, K=0.125")
    plt.plot(xs, t_drops, label="Drop")
    plt.plot(xs, t_sats, ':', label="Vapor saturation")
    plt.plot(xs, t_drop_recs, "--", label="Local drop effective recovery")
    plt.xlabel("Distance from cylinder, m")
    plt.ylabel("Temperature, K")
    plt.savefig("naca_tn_3024_t_drop_k0_125_equilibrium.png")
    plt.figure()
    plt.suptitle(f"Phi=1000, K=0.125")
    plt.plot(xs, vs, label="Water drop")
    plt.plot(xs, us, '--', label="Air")
    plt.xlabel("Distance from cylinder, m")
    plt.ylabel("Speed, m/s")
    plt.legend()
    plt.savefig("naca_tn_3024_v_drop_k0_125_equilibrium.png")
    ts = [i * tau for i in range(len(xs))]

    plt.figure()
    plt.suptitle(f"Phi=1000, K=0.125")
    plt.plot(xs, ts)
    plt.ylim(0)
    plt.xlabel("Distance from cylinder, m")
    plt.ylabel("Time, s")
    plt.savefig("naca_tn_3024_time_k0_125_equilibrium.png")

    plt.show()
