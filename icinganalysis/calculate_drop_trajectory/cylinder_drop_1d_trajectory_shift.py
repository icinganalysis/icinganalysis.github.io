from icinganalysis import air_properties
from icinganalysis import langmuir_cylinder_values
from icinganalysis.units_helpers import MICROMETERS_PER_METER
from icinganalysis.water_properties import WATER_DENSITY


def calc_ux_from_distance(d):
    """equation (23) rearranged to use distance, d = (x-1)"""
    if d < 1e-15:
        return 2 * d
    return (d ** 2 + 2 * d) / (d ** 2 + 2 * d + 1)


def calc_cd_r_24_approx(re_relative):
    """equation (22)"""
    return 1 + 0.197 * re_relative ** 0.63 + 2.6e-4 * re_relative ** 1.38


def calc_d_vx_d_tau(ux, vx, cd_r_24, k):
    """equation (4) rearranged"""
    return cd_r_24 * (vx - ux) / k


def calc_ru(tk, p, u, drop_radius):
    """equation (9)"""
    return (
        2
        * (drop_radius / MICROMETERS_PER_METER)
        * air_properties.calc_air_density(tk, p)
        * u
        / air_properties.calc_air_viscosity(tk)
    )


def calc_k(tk, u, drop_radius, cylinder_radius):
    """equation (12)"""
    k = (
        2
        / 9
        * WATER_DENSITY
        * (drop_radius / MICROMETERS_PER_METER) ** 2
        * u
        / air_properties.calc_air_viscosity(tk)
        / cylinder_radius
    )  # equ. (12)
    return k


def is_outside_from_distance(d, diameters_ratio=0.0):
    if (d - diameters_ratio) > 0:
        return True
    return False


def interpolate_impingement_x_xv_from_distance(
    d_outside, d_inside, vx_outside, vx_inside, diameters_ratio=0.0
):
    d_impingement = 0 + diameters_ratio
    vx_impingement = vx_outside + (d_impingement - d_outside) / (
        d_inside - d_outside
    ) * (vx_inside - vx_outside)
    return d_impingement, vx_impingement


def calculate_drop_motion(
    tk,
    p,
    u,
    drop_radius,
    cylinder_radius,
    x0=4,
    tau=0.001,
    vxmin=1e-25,
    diameters_ratio=0.0,
):
    """
    Calculate water drop impingement on a cylinder along the stagnation line Y=0
    :param tk: ambient static temperature, K
    :param p:  ambient static pressure, Pa
    :param u: free stream airspeed, m/s
    :param drop_radius: micrometer
    :param cylinder_radius: meter
    :param x0: drop initial dimensionless position, x = x_dimensional / cylinder_radius
    :param tau: dimensionless time step, tau = time * (u0 / cylinder_radius)
    :return: xs, vxs; dimensionless drop positions, drop speeds
    """
    x = x0  # drop initial position condition
    vx = 1  # drop initial velocity condition
    ru = calc_ru(tk, p, u, drop_radius)
    k = calc_k(tk, u, drop_radius, cylinder_radius)
    ds, vxs, cds, re_rels, d_vx_d_taus = calc_one_trajectory(
        x, k, ru, tau, vx, vxmin=vxmin, diameters_ratio=diameters_ratio
    )

    return ds, vxs, cds, re_rels, d_vx_d_taus


def calc_one_trajectory(x, k, ru, tau=0.001, vx=None, vxmin=1e-25, diameters_ratio=0.0):
    """
    Calculate water drop impingement on a cylinder along the stagnation line Y=0
    :param x: dimensionless position, x = x_dimensional / cylinder_radius
    :param k: drop acceleration parameter
    :param ru: drop relative airspeed Reynolds number
    :param tau: dimensionless time, tau = time * (u0 / cylinder_radius)
    :param vx: drop dimensionless speed
    :return: ds, vxs; dimensionless drop positions, drop speeds
    """

    z = x - 1
    if vx is None:
        vx = calc_ux_from_distance(z)
    vxs = [vx]
    n = 10000001  # should be plenty, typically >>1000 cylinder radii at u0
    ds = [z]
    ux = calc_ux_from_distance(z)
    re_rel = ru * abs(ux - vx)
    cd_r_24 = calc_cd_r_24_approx(re_rel)
    d_vx_d_tau = calc_d_vx_d_tau(ux, vx, cd_r_24, k)
    cds = [cd_r_24]
    re_rels = [re_rel]
    d_vx_d_taus = [d_vx_d_tau]
    """using z produces less round-off near x=1, allow more accuracy near the impingement point (x=1)
    example: z = 4.109382787428e-16, x = 1.0000000000000004
    """
    for i in range(n):
        ux = calc_ux_from_distance(z)
        re_rel = ru * abs(ux - vx)
        cd_r_24 = calc_cd_r_24_approx(re_rel)
        d_vx_d_tau = calc_d_vx_d_tau(ux, vx, cd_r_24, k)
        vx_new = vx + tau * -d_vx_d_tau
        dx = -abs(tau) * vx_new
        z_new = z + dx
        if not is_outside_from_distance(z_new, diameters_ratio):
            d_i, vx_i = interpolate_impingement_x_xv_from_distance(
                z, z_new, vx, vx_new, diameters_ratio
            )
            ds.append(d_i)
            vxs.append(vx_i)
            cds.append(cd_r_24)
            re_rels.append(re_rel)
            d_vx_d_taus.append(d_vx_d_tau)
            return ds, vxs, cds, re_rels, d_vx_d_taus
        z = z_new
        vx = vx_new
        ds.append(z)
        vxs.append(vx)
        cds.append(cd_r_24)
        re_rels.append(re_rel)
        d_vx_d_taus.append(d_vx_d_tau)
        if (
            abs(vx_new) < vxmin
        ):  # any slower than this is essentially stopped, or exceeds the available precision
            break

    return ds, vxs, cds, re_rels, d_vx_d_taus


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    tk = 263
    p = 101325
    u = 90

    phi = 1000
    k = 0.126
    d_drop = langmuir_cylinder_values.calc_drop_diameter_micrometer_from_re_drop(
        (k * phi) ** 0.5, tk, p, u
    )
    get_d_drop = langmuir_cylinder_values.calc_drop_diameter_micrometer_from_re_drop
    d_cyl = langmuir_cylinder_values.calc_d_cylinder_from_phi(phi, tk, p, u)
    diameters_ratio = d_drop / MICROMETERS_PER_METER / d_cyl
    print(d_drop)
    print(d_cyl)
    print(diameters_ratio)
    print("K*Phi", langmuir_cylinder_values.calc_k_phi(tk, p, u, d_drop))
    print("Phi", langmuir_cylinder_values.calc_phi(tk, p, u, d_cyl))
    print("K", langmuir_cylinder_values.calc_k(tk, u, d_drop, d_cyl))

    plt.figure()
    plt.suptitle(f"Phi=1000, K={k:.3f}")
    for x0 in (2, 4, 7, 10, 15, 20):
        ds, vxs, cds, re_rels, d_vx_d_taus = calculate_drop_motion(
            tk, p, u, d_drop / 2, d_cyl / 2, x0=x0
        )
        plt.plot([-_ for _ in ds], vxs, "-", label=f"X0={x0}")
    plt.xlabel("distance from surface, x+1")
    plt.ylabel("vx")
    plt.xlim(-20, -0)
    plt.xticks(range(-20, 0 + 2, 2))
    plt.ylim(0, 1.2)
    plt.grid()
    plt.legend()
    plt.savefig(f"1d_cyl_shift_k{k:.3f}_x0_x_vx.png")

    plt.figure()
    plt.suptitle(f"Phi=1000, K={k:.3f}")
    x0 = 4
    for tau in (0.1, 0.01, 0.001, 0.0001, 0.00001):
        ds, vxs, cds, re_rels, d_vx_d_taus = calculate_drop_motion(
            tk, p, u, d_drop / 2, d_cyl / 2, tau=tau
        )
        plt.plot([-_ for _ in ds], vxs, "-", label=f"tau={tau}")
    plt.xlabel("distance from surface, x+1")
    plt.ylabel("vx")
    plt.xlim(-3, -0)
    plt.ylim(0, 1.2)
    plt.grid()
    plt.legend()
    plt.savefig(f"1d_cyl_shift_k{k:.3f}_tau_x_vx.png")

    plt.figure()
    plt.suptitle(f"Phi=1000")
    all_xs = []
    for tau in reversed((0.1, 0.01, 0.001, 0.0001, 0.00001)):
        vs_ = []
        ks_ = (0.122, 0.123, 0.124, 0.125, 0.126, 0.127)
        for k in ks_:
            d_drop = langmuir_cylinder_values.calc_drop_diameter_micrometer_from_re_drop(
                (k * phi) ** 0.5, tk, p, u
            )
            ds, vxs, cds, re_rels, d_vx_d_taus = calculate_drop_motion(
                tk, p, u, d_drop / 2, d_cyl / 2, x0=x0, tau=tau
            )
            vs_.append((ds[-1], vxs[-1]))
        print(tau, len(ds))
        x_, y_ = zip(*vs_)
        all_xs.extend(x_)
        plt.plot(ks_, x_, "-+", label=f"d_tau={tau}")
    plt.xscale("log")
    plt.xlabel("K")
    plt.ylabel("Final distance from cylinder, x-1")
    plt.ylim(0)
    plt.legend()
    print()

    plt.figure()
    plt.suptitle("Conditions in Langmuir and Blodgett Figure 8")
    ks = plt.np.logspace(plt.np.log10(0.125), 2)
    phis = (0.1, 100, 1000, 10000, 1e6)
    vs = []
    for phi in phis:
        d_cyl = langmuir_cylinder_values.calc_d_cylinder_from_phi(phi, tk, p, u)
        vls = [
            calculate_drop_motion(
                tk, p, u, get_d_drop((k * phi) ** 0.5, tk, p, u) / 2, d_cyl / 2, x0=x0
            )[1][-1]
            for k in ks
        ]
        vs.append(vls)
        plt.plot(ks, vls, label=f"Phi={phi}")
    plt.xscale("log")
    plt.xlabel("K")
    plt.xlim(0.1, 100)
    plt.ylim(0, 0.7)
    plt.grid()
    plt.ylabel("Vl")
    plt.legend(loc="lower right")
    plt.savefig(f"1d_cyl_shift_fig8_vls_{x0}.png")

    plt.figure()
    plt.suptitle("Analysis at Phi=1000, Near K=0.125")
    phi = 1000
    d_cyl = langmuir_cylinder_values.calc_d_cylinder_from_phi(phi, tk, p, u)
    ks = 0.126, 0.125, 0.124
    markers = "o^v"
    for k, marker in zip(ks, markers):
        d_drop = get_d_drop((k * phi) ** 0.5, tk, p, u)
        ds, vxs, cds, re_rels, d_vx_d_taus = calculate_drop_motion(
            tk, p, u, d_drop / 2, d_cyl / 2, x0=4, vxmin=1e-25
        )
        plt.plot(-ds[-1], vxs[-1], marker, ms=14, mew=2, label=f"K={k}")

    plt.xlabel("Terminal distance from surface, x+1")
    plt.ylabel("Terminal velocity, vx")
    plt.xlim(-0.3e-25, 0)
    plt.ylim(0)
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig("1d_cyl_shift_near_k_0_125_x_vx.png")

    plt.figure()
    plt.suptitle("Analysis at Phi=1000, drop diameter considered for contact")
    phi = 1000
    d_cyl = langmuir_cylinder_values.calc_d_cylinder_from_phi(phi, tk, p, u)
    ks = 0.125, 0.1, 0.05, 0.01, 0.005, 0.001
    markers = "o^v<>8"
    for k, marker in zip(ks, markers):
        d_drop = get_d_drop((k * phi) ** 0.5, tk, p, u)
        diameters_ratio = d_drop / MICROMETERS_PER_METER / d_cyl
        ds, vxs, cds, re_rels, d_vx_d_taus = calculate_drop_motion(
            tk,
            p,
            u,
            d_drop / 2,
            d_cyl / 2,
            x0=4,
            vxmin=1e-25,
            diameters_ratio=diameters_ratio,
        )
        plt.plot(
            -ds[-1],
            vxs[-1],
            marker,
            ms=14,
            mew=2,
            fillstyle="none",
            label=f"K={k}, diameters_ratio={diameters_ratio:.3e}",
        )

    plt.xlabel("Terminal distance from surface, x+1")
    plt.ylabel("Terminal velocity, vx")
    plt.xlim(None, 0)
    plt.yscale("log")
    plt.grid()
    plt.legend(loc=("lower left"))
    plt.savefig("1d_cyl_shift_low_k_x_vx.png")

    plt.show()
