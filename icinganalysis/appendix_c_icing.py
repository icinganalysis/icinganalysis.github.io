import numpy as np
from scipy.interpolate import interp1d

continuous_maximum_figure_1_points = {  # tf: (mvd), (lwc)
    32: ((15, 20, 25, 30, 35, 40), (0.8, 0.635, 0.5, 0.375, 0.26, 0.155)),
    14: (
        (15, 20, 25, 30, 35, 40),
        (0.59, 0.415, 0.30, 0.22, 0.15, 0.10),
    ),
    -4: (
        (15, 20, 25, 30, 35, 40),
        (0.30, 0.21, 0.15, 0.11, 0.08, 0.06),
    ),
    -22: (
        (15, 20, 25, 30, 35, 40),
        (0.20, 0.14, 0.10, 0.07, 0.05, 0.04),
    ),
}

continuous_maximum_figure_2_points = (  # alt_ft, tc
    (0, 12000, 22000, 22000, 0, 0),
    (32, 32, -4, -22, -22, 32),
)

continuous_maximum_figure_3_points = (  # nmi, factor
    (5, 10, 17.4, 50, 170, 310),
    (1.34, 1.16, 1, 0.67, 0.32, 0.2),
)


def get_continuous_maximum_lwc(tf, mvd):
    ts = list(continuous_maximum_figure_1_points.keys())
    lwcs = []
    for tc_ in ts:
        ds, lwcs_ = continuous_maximum_figure_1_points[tc_]
        lwc_ = interp1d(
            ds, lwcs_, kind="quadratic", bounds_error=False, fill_value=float("nan")
        )(mvd)
        lwcs.append(lwc_)
    lwc = interp1d(
        ts, lwcs, kind="quadratic", bounds_error=False, fill_value=float("nan")
    )(tf)
    return lwc


def get_continuous_maximum_lwc_factor(nmi):
    nmis, fs = continuous_maximum_figure_3_points
    lms = np.log(nmis)
    f = interp1d(
        lms, fs, kind="quadratic", bounds_error=False, fill_value=float("nan")
    )(np.log(nmi))
    return f


def get_continuous_maximum_t_min_t_max(altitude_ft):
    t_min, t_max = float("nan"), float("nan")
    if 0 <= altitude_ft <= 22000:
        t_max = interp1d((0, 12000, 22000), (32, 32, -4))(altitude_ft)
        t_min = -22
    return t_min, t_max


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    t = 17
    mvd = 18
    lwc = get_continuous_maximum_lwc(t, mvd)

    plt.figure()
    plt.plot(mvd, lwc, "+", ms=10, mew=2, label="interpolated point")
    plt.text(mvd, lwc, f"{lwc:.3f} g/m^3\n{t:.0f}F\n{mvd:.0f} MVD")
    ds = plt.np.linspace(15, 40, 26)
    for t in continuous_maximum_figure_1_points:
        lwcs = [get_continuous_maximum_lwc(t, _) for _ in ds]
        plt.plot(ds, lwcs, label=f"Figure 1 {t:.0f}F")
    plt.ylim(0)
    plt.legend()
    plt.xlabel("Mean effective drop diameter, micrometer")
    plt.ylabel("Liquid water content, g/m^3")

    plt.figure()
    nms = plt.np.geomspace(5, 310)
    fs = [get_continuous_maximum_lwc_factor(_) for _ in nms]
    plt.plot(nms, fs, label="Figure 2")
    plt.xscale("log")
    plt.ylim(0)
    plt.xlabel("Could Horizontal Extent, nmi")
    plt.ylabel("Liquid Water Content Factor F")
    plt.axvline(17.4, linestyle="--", lw=0.5, c="green", label="17.4 nmi")
    plt.grid()
    plt.legend()

    plt.figure()
    plt.plot(*continuous_maximum_figure_2_points, lw=3, label="Figure 2 envelope")
    alt = 16000
    tn, tx = get_continuous_maximum_t_min_t_max(alt)
    print(tn, tx)
    plt.plot((alt, alt), (tn, tx), "+", ms=10, label="Interpolated Tmin, Tmax")
    plt.plot()
    plt.xlim(0)
    plt.ylim(-30)
    plt.xlabel("Pressure altitude, ft")
    plt.ylabel("Temperature, F")
    plt.legend()

    plt.show()
