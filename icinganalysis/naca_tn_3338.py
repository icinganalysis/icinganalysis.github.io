M_PER_INCH = 0.0254
MS_PER_MPH = 0.44704
PA_PER_INCH_HG = 3386.389
KG_PER_LBM = 0.4535924
SECONDS_PER_HOUR = 3600
INCHES_PER_FT = 12
SQ_FT_PER_SQ_M = (INCHES_PER_FT * M_PER_INCH) ** -2
M_PER_FT = M_PER_INCH * INCHES_PER_FT
G_PER_KG = 1000

from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement
from icinganalysis.langmuir_cylinder_values import calc_k, calc_phi, calc_d_drop_from_k
from scipy.optimize import minimize_scalar
from scipy.interpolate import interp1d
from math import degrees, radians
import matplotlib.pyplot as plt


def find_d_drop_for_theta(theta, tk, p, u, d_cyl):
    phi = calc_phi(tk, p, u, d_cyl)

    def f(d_drop):
        k = calc_k(tk, u, d_drop, d_cyl)
        theta_calc = NACA_TN_2904_impingement.calc_theta_from_figure_9_data(k, phi)
        return abs(theta - degrees(theta_calc))

    solution = minimize_scalar(f, bounds=[1, 100], method="bounded")
    d_drop = float("nan")
    if solution.success:
        d_drop = minimize_scalar(f, bounds=[1, 100], method="bounded").x
    return d_drop


def calc_area_theta(wbs, thetas):
    area = sum(
        [
            (s2 - s1) * (w1 + w2) / 2
            for s1, s2, w1, w2 in zip(thetas[:-1], thetas[1:], wbs[:-1], wbs[1:])
        ]
    )
    return area


def calc_distribution(wbs, thetas, tk, p, u, d_cyl, thetas_intervals=None):
    wb_interpolator = interp1d(thetas, wbs)
    total_area_theta = calc_area_theta(wbs, thetas)
    if thetas_intervals is None:
        thetas_intervals = plt.np.linspace(0, max(thetas), 10)

    plt.figure()
    plt.plot(thetas, wbs, c="k", label="Measured data")
    plt.plot([], [], " ", label="MVD  Fraction Cumulative")

    dr_data = []
    fractions = []
    ems = []
    ems_weighted = []
    lwcs = []

    phi = calc_phi(tk, p, u, d_cyl)
    cf = 0
    for theta_left, theta_right in reversed(
        tuple(zip(thetas_intervals[:-1], thetas_intervals[1:]))
    ):
        d_drop = find_d_drop_for_theta(theta_right, tk, p, u, d_cyl)
        k = calc_k(tk, u, d_drop, d_cyl)
        beta_1_2 = NACA_TN_2904_impingement.calc_beta_from_figure_9(
            k, phi, radians(theta_left)
        )
        wb_1_2 = wb_interpolator(theta_left)

        wbs_accounted_so_far = 0
        for d, ratio in dr_data:
            wbs_accounted_so_far += (
                ratio
                * NACA_TN_2904_impingement.calc_beta_from_figure_9(
                    calc_k(tk, u, d, d_cyl), phi, radians(theta_left)
                )
            )
        delta_wb = max(0, wb_1_2 - wbs_accounted_so_far)
        ratio = delta_wb / beta_1_2 if beta_1_2 else 0
        dr_data.append((d_drop, ratio))
        thetas_local = plt.np.linspace(
            0, max(thetas)
        )  # get several (default 50) for accurate area
        wbs_local = [
            ratio
            * NACA_TN_2904_impingement.calc_beta_from_figure_9(k, phi, radians(tl))
            for tl in thetas_local
        ]
        area_local = calc_area_theta(wbs_local, thetas_local)

        wb_local = beta_1_2 * ratio
        wcr_per_unit_area = wb_local * KG_PER_LBM / SECONDS_PER_HOUR * SQ_FT_PER_SQ_M
        lwc = wcr_per_unit_area / (1 / G_PER_KG * u * beta_1_2) if u * beta_1_2 else 0
        lwcs.append(lwc)

        fraction = area_local / total_area_theta
        fractions.append(fraction)
        cf += fraction
        em = NACA_TN_2904_impingement.calc_em_from(k, phi)
        ems.append(em)
        ems_weighted.append(em * fraction)

        wbs_so_far = []
        for t in thetas:
            wb_local = 0
            for d, ratio in dr_data:
                wb_local += ratio * NACA_TN_2904_impingement.calc_beta_from_figure_9(
                    calc_k(tk, u, d, d_cyl), phi, radians(t)
                )
            wbs_so_far.append(wb_local)
        plt.plot(
            thetas,
            wbs_so_far,
            "--",
            label=f"{d_drop:>4.1f}  {fraction:5.3f}  {cf:5.3f}",
        )

    em_weighted = sum(ems_weighted)
    plt.xlim(0, 90)
    plt.xlabel("Cylinder angle, Theta, degrees")
    plt.ylim(0)
    plt.ylabel("Local catch rate, lbm/hr/ft^2")
    plt.legend()
    ds, ratios = list(zip(*dr_data))
    total_area_ft = total_area_theta * radians(1) * d_cyl / 2 / M_PER_FT
    wcr_per_unit_length = total_area_ft / M_PER_FT * KG_PER_LBM / SECONDS_PER_HOUR
    lwc = wcr_per_unit_length / (1 / G_PER_KG * em_weighted * u * d_cyl / 2)

    return fractions, ds, em_weighted, lwcs


if __name__ == "__main__":
    # example data
    # fmt: off
    d = (  # Figure 20a, 2 inch, repeat; theta, wb (lbm/hr/ft^2)
        0, 17.55,
        5, 17.3,
        10, 16.81,
        15, 16,
        20, 15.16,
        25, 13.9,
        30, 12.69,
        35, 11.2,
        40, 9.78,
        45, 8.2,
        50, 6.5,
        55, 4.7,
        60, 2.99,
        65, 1.7,
        70, 0.62,
        75, 0.35,
        80, 0.2,
        83.1, 0,
    )
    # fmt: on

    theta_degrees, wb = d[::2], d[1::2]

    thetas_intervals = 0, 10, 20, 30, 40, 50, 60, 70, 83.1
    d_cyl = 2 * M_PER_INCH
    mph = 175  # page 12
    u = mph * MS_PER_MPH
    tk = (459.67 + 45) / 1.8  # page 12
    p = 28.2 * PA_PER_INCH_HG  # page 12

    fs, ds, em_weighted, lwcs = calc_distribution(
        wb, theta_degrees, tk, p, u, d_cyl, thetas_intervals
    )
    cumulative_lwcs = [sum(lwcs[:i]) if i else 0 for i, _ in enumerate(lwcs)]
    cumulative_fractions = [sum(fs[:i]) if i else 0 for i, _ in enumerate(fs)]

    mvd = interp1d(cumulative_fractions, ds)(0.5)

    total_area_theta = calc_area_theta(wb, theta_degrees)
    total_area_ft = total_area_theta * radians(1) * d_cyl / 2 / M_PER_FT
    wcr_per_unit_length = total_area_ft / M_PER_FT * KG_PER_LBM / SECONDS_PER_HOUR
    lwc = wcr_per_unit_length / (1 / G_PER_KG * em_weighted * u * d_cyl / 2)
    print(f"MVD = {mvd:.1f}, LWC = {lwc:.3f}")

    plt.figure(42, figsize=(8, 5))
    plt.plot(
        [_ / 2 for _ in ds],
        cumulative_lwcs,
        lw=2,
        label="2 inch, Using NACA example intervals",
    )
    plt.xlim(0)
    plt.xlabel("Drop radius, micrometer")
    plt.ylim(0, 1.2)
    plt.ylabel("Cumulative LWC, g/m^3")

    thetas_intervals = plt.np.linspace(0, max(theta_degrees), 50)
    fs, ds, em_weighted, lwcs = calc_distribution(
        wb, theta_degrees, tk, p, u, d_cyl, thetas_intervals
    )
    cumulative_lwcs = [sum(lwcs[:i]) if i else 0 for i, _ in enumerate(lwcs)]
    cumulative_fractions = [sum(fs[:i]) if i else 0 for i, _ in enumerate(fs)]

    mvd = interp1d(cumulative_fractions, ds)(0.5)

    total_area_theta = calc_area_theta(wb, theta_degrees)
    total_area_ft = total_area_theta * radians(1) * d_cyl / 2 / M_PER_FT
    wcr_per_unit_length = total_area_ft / M_PER_FT * KG_PER_LBM / SECONDS_PER_HOUR
    lwc = wcr_per_unit_length / (1 / G_PER_KG * em_weighted * u * d_cyl / 2)
    print(f"MVD = {mvd:.1f}, LWC = {lwc:.3f}")

    plt.figure(42)
    plt.plot(
        [_ / 2 for _ in ds], cumulative_lwcs, "--", lw=2, label="using 50 intervals"
    )
    plt.xlim(0, 40)
    plt.xlabel("Drop radius, micrometer")
    plt.ylim(0, 0.5)
    plt.ylabel("Cumulative LWC, g/m^3")
    plt.legend()

    plt.savefig("naca_tn_3338_example.png", transparent=True)


    k = 0.125
    for d_cyl in [_*.0254 for _ in (2, 4, 6)]:
        print(d_cyl, calc_d_drop_from_k(k, tk, u, d_cyl))


    plt.show()
