"""
Interpolation functions and figure making routines for 14 CFR Part 25 Appendix C.
Interpolations that are out of range return nan.
Units are domain specific:
    Altitude: ft.
    Temperature: F
    Distance: nmi
    MVD: micrometer μm
    LWC: g/m^3
"""

import csv
import numpy as np
from scipy.interpolate import make_interp_spline
from numpy import interp
import matplotlib.pyplot as plt

continuous_maximum_figure_1_points = {  # tf: (mvds), (lwcs)
    32: ((15, 20, 25, 30, 35, 40), (0.8, 0.635, 0.5, 0.375, 0.26, 0.155)),
    14: (
        (15, 20, 25, 30, 35, 40),
        (0.6, 0.425, 0.30, 0.22, 0.15, 0.10),
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

continuous_maximum_figure_2_points = (  # alt_ft, tf
    (0, 12000, 22000, 22000, 0, 0),
    (32, 32, -4, -22, -22, 32),
)

continuous_maximum_figure_3_points = (  # nmi, factor
    (5, 10, 17.4, 50, 170, 310),
    (1.34, 1.16, 1., 0.665, 0.325, 0.2),
)

intermittent_maximum_figure_4_points = {
    32: ((15, 17.5, 20, 22.5, 25, 30, 35, 40, 50), (2.9, 2.81, 2.5, 2.1, 1.75, 1.325, 1, 0.75, 0.413)),
    14: ((15, 17.5, 20, 22.5, 25, 30, 35, 40, 50), (2.5, 2.44, 2.2, 1.78, 1.45, 1.025, 0.713, 0.513, 0.3),),
    -4: ((15, 20, 25, 30, 35, 40, 50), (1.925, 1.7, 1.15, 0.8, 0.575, 0.4, 0.188),),
    -22: ((15, 20, 25, 30, 35, 40, 50), (1.1, 0.988, 0.713, 0.5, 0.35, 0.25, 0.1),),
    -40: ((15, 20, 25, 30, 35, 40, 50), (0.25, 0.21, 0.15, 0.1, 0.075, 0.06, 0.05),),
}

intermittent_maximum_figure_5_points = (  # alt_ft, tf
    (4000, 12000, 30500, 19000, 4000, 4000),
    (26, 26, -40, -40, 14, 26)
)

intermittent_maximum_figure_6_points = (  # nmi, factor
    (0.26,0.5, 1, 2.61, 5.21),
    (1.35, 1.297, 1.19, 1, 0.85)
)

def get_continuous_maximum_lwc(tf, mvd):
    '''
    Interpolate the standard distance LWC from Figure 1.
    :param tf: ambient temperature, F
    :param mvd: drop size, μm
    :return: LWC, g/m^3 (returns float('nan') if input was out of range)
    '''
    ts = sorted(continuous_maximum_figure_1_points.keys())
    lwcs = []
    for ts_ in ts:
        ds, lwcs_ = continuous_maximum_figure_1_points[ts_]
        if not (min(ds) <= mvd <= max(ds)):
            return np.nan
        fx = make_interp_spline(ds, lwcs_, k=2)
        lwc_ = np.nan
        if min(ds) <= mvd <= max(ds):
            lwc_ = fx(mvd)
        lwcs.append(lwc_)
    fx = make_interp_spline(ts, lwcs, k=2)
    try:
        lwc = [fx(_) if min(ts) <= _ <= max(ts) else np.nan for _ in tf]
    except Exception:
        lwc = fx(tf) if min(ts) <= tf <= max(ts) else np.nan
    return lwc


def get_intermittent_maximum_lwc(tf, mvd):
    '''
    Interpolate the standard distance LWC from Figure 4.
    :param tf: ambient temperature, F
    :param mvd: drop size, μm
    :return: LWC, g/m^3 (returns float('nan') if input was out of range)
    '''
    ts = sorted(intermittent_maximum_figure_4_points.keys())
    lwcs = []
    for ts_ in ts:
        ds, lwcs_ = intermittent_maximum_figure_4_points[ts_]
        print(ds)
        print(lwcs_)
        if not (min(ds) <= mvd <= max(ds)):
            return np.nan
        fx = make_interp_spline(ds, lwcs_, k=2)
        lwc_ = np.nan
        if min(ds) <= mvd <= max(ds):
            lwc_ = fx(mvd)
        lwcs.append(lwc_)
    fx = make_interp_spline(ts, lwcs, k=2)
    try:
        lwc = [fx(_) if min(ts) <= _ <= max(ts) else np.nan for _ in tf]
    except Exception:
        lwc = fx(tf) if min(ts) <= tf <= max(ts) else np.nan
    return lwc


def get_continuous_maximum_lwc_factor(nmi):
    '''
    Interpolate the Liquid Water Content Factor-F from Figure 3.
    :param nmi: distance in nmi
    :return: F (dimensionless)
    '''
    nmis, fs = continuous_maximum_figure_3_points
    fx = make_interp_spline(np.log(nmis), fs, k=2)
    try:
        f = [fx(np.log(_)) if min(nmis) <= _ <= max(nmis) else np.nan for _ in nmi]
    except TypeError:
        f = fx(np.log(nmi)) if min(nmis) <= nmi <= max(nmis) else np.nan
    return f


def get_intermittent_maximum_lwc_factor(nmi):
    '''
    Interpolate the Liquid Water Content Factor-F from Figure 3.
    :param nmi: distance in nmi
    :return: F (dimensionless)
    '''
    nmis, fs = intermittent_maximum_figure_6_points
    fx = make_interp_spline(np.log(nmis), fs, k=2)
    try:
        f = [fx(np.log(_)) if min(nmis) <= _ <= max(nmis) else np.nan for _ in nmi]
    except TypeError:
        f = fx(np.log(nmi)) if min(nmis) <= nmi <= max(nmis) else np.nan
    return f


def get_continuous_maximum_t_min_t_max(altitude_ft):
    t_min, t_max = float("nan"), float("nan")
    if 0 <= altitude_ft <= 22000:
        t_max = interp(altitude_ft, (0, 12000, 22000), (32, 32, -4))
        t_min = -22
    return t_min, t_max


def get_intermittent_maximum_t_min_t_max(altitude_ft):
    t_min, t_max = float("nan"), float("nan")
    if 0 <= altitude_ft <= 30500:
        t_max = interp(altitude_ft, (4000, 12000, 30500), (26, 26, -40))
        t_min = interp(altitude_ft, (30500, 19000, 4000), (-40, -10, 16))
    return t_min, t_max


def make_figure_1(figure=None):
    '''
    Make a matplotlib.figure.Figure object
    You may need a subsequent call to plt.show() to display it,
    or plt.savefig('fig1.png') to save it as a png file.
    :param figure: matplotlib.figure.Figure, if None then a new figure is made
    :return: matplotlib.figure.Figure
    '''
    if figure is None:
        figure = plt.figure(figsize=(7.4, 6.4))
    plt.suptitle(
        "Figure 1. Continuous Maximum (Stratiform Clouds) (Redrawn)"
        "\nAtmospheric Icing Conditions"
        "\nLiquid Water Content vs. Median-Volume Drop Diameter"
    )
    ds = plt.np.linspace(15, 40, 26)
    for t in continuous_maximum_figure_1_points:
        lwcs = [get_continuous_maximum_lwc(t, _) for _ in ds]
        (line,) = plt.plot(ds, lwcs)
        plt.text(ds[0], lwcs[0], f"{t:.0f}F", ha="right", c=line.get_color())
    plt.text(
        0.95,
        0.87,
        s=(
            "1. Pressure altitude range, S.L.-22,000 ft."
            "\n2. Maximum vertical extent, 6,500 ft."
            "\n3. Horizontal Extent, standard distance of 17.4 Nautical Miles"
        ),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(facecolor="white", edgecolor="black", alpha=0.8),
    )
    plt.text(
        0.95,
        0.73,
        s=("SOURCE OF DATA" "\nNACA-TN-1855" "\nCLASS III-M CONTINUOUS MAXIMUM"),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(facecolor="white", edgecolor="black", alpha=0.8),
    )
    plt.ylim(0)
    plt.xlim(13)
    plt.grid()
    plt.xlabel("MEDIAN-VOLUME DROP DIAMETER, μm")
    plt.ylabel("LIQUID WATER CONTENT, g/m^3")
    plt.tight_layout()
    return figure


def make_figure_4(figure=None):
    '''
    Make a matplotlib.figure.Figure object
    You may need a subsequent call to plt.show() to display it,
    or plt.savefig('fig1.png') to save it as a png file.
    :param figure: matplotlib.figure.Figure, if None then a new figure is made
    :return: matplotlib.figure.Figure
    '''
    if figure is None:
        figure = plt.figure(figsize=(7.4, 6.4))
    plt.suptitle(
        "Figure 4. Intermittent Maximum (Cumuliform Clouds) (Redrawn)"
        "\nAtmospheric Icing Conditions"
        "\nLiquid Water Content vs. Median-Volume Drop Diameter"
    )
    ds = plt.np.linspace(15, 50, 36)
    for t in intermittent_maximum_figure_4_points:
        lwcs = [get_intermittent_maximum_lwc(t, _) for _ in ds]
        if t==-40:
            (line,) = plt.plot(ds, lwcs, '--')
        else:
            (line,) = plt.plot(ds, lwcs, '-')
        plt.text(ds[0], lwcs[0], f"{t:.0f}F", ha="right", c=line.get_color())
    plt.text(
        0.95,
        0.87,
        s=(
            "1. Pressure altitude range, 4,000-22,000 ft."
            "\n2. Horizontal Extent, standard distance of 2.6 Nautical Miles"
            "\nNote: dashed line indicate possible extent of limits"
        ),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(facecolor="white", edgecolor="black", alpha=0.8),
    )
    plt.text(
        0.95,
        0.73,
        s=("SOURCE OF DATA" "\nNACA-TN-1855" "\nCLASS II-M INTERMITTENT MAXIMUM"),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(facecolor="white", edgecolor="black", alpha=0.8),
    )
    plt.ylim(0)
    plt.xlim(13)
    plt.grid()
    plt.xlabel("MEDIAN-VOLUME DROP DIAMETER, μm")
    plt.ylabel("LIQUID WATER CONTENT, g/m^3")
    plt.tight_layout()
    return figure


def make_figure_2(figure=None):
    if figure is None:
        figure = plt.figure(figsize=(6.4, 6.4))
    plt.suptitle(
        "Figure 2. Continuous Maximum (Stratiform Clouds) (Redrawn)"
        "\nAtmospheric Icing Conditions"
        "\nAmbient Temperature vs. Pressure Altitude"
    )
    plt.plot(*continuous_maximum_figure_2_points)
    plt.text(
        0.95,
        0.87,
        s=("SOURCE OF DATA" "\nNACA-TN-2569"),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(facecolor="white", edgecolor="black", alpha=0.8),
    )
    plt.xlim(-100)
    plt.ylim(-30)
    plt.xlabel("Pressure Altitude, ft")
    plt.ylabel("Ambient Temperature, F")
    plt.tight_layout()
    return figure


def make_figure_3(figure=None):
    if figure is None:
        figure = plt.figure(figsize=(6.4, 6.4))
    plt.suptitle(
        "Figure 3. Continuous Maximum (Stratiform Clouds) (Redrawn)"
        "\nAtmospheric Icing Conditions"
        "\nLiquid Water Content Factor vs. Cloud Horizontal Distance"
    )
    nms = np.geomspace(5, 310, 306)  # 1 nmi intervals
    fs = get_continuous_maximum_lwc_factor(
        nms
    )  # this function can accept a numpy array as input
    plt.plot(nms, fs)
    plt.text(
        0.95,
        0.87,
        s=("SOURCE OF DATA" "\nNACA-TN-2738"),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(
            facecolor="white",  # Background color
            edgecolor="black",  # Border color
            alpha=0.8,  # Transparency
        ),
    )
    plt.xscale("log")
    plt.ylim(0)
    plt.xlabel("Cloud Horizontal Extent, nmi")
    plt.ylabel("Liquid Water Content Factor, F-Dimensionless")
    plt.grid()
    plt.tight_layout()
    return figure


def make_jeck_continuous_maximum_distance_based_figure(mvd=15):
    plt.figure(figsize=(6.4, 6.4))
    plt.suptitle(
        "Continuous Maximum (Stratiform Clouds) Distance-Based Format"
        f"\nAtmospheric Icing Conditions for MVD={mvd}"
        "\nLiquid Water Content Factor vs. Distance"
    )
    nms = np.geomspace(5, 310, 306)
    fs = get_continuous_maximum_lwc_factor(nms)
    for t in continuous_maximum_figure_1_points:
        lwcs = get_continuous_maximum_lwc(t, mvd)*fs
        plt.plot(nms, lwcs, label=f"T={t}F")
    plt.legend()
    plt.xscale("log")
    plt.xlim(1, 350)
    plt.ylim(0, 1.2)
    plt.xlabel("Cloud Horizontal Extent, nmi")
    plt.ylabel("Liquid Water Content Factor, g/m^3")
    plt.tight_layout()


def make_jeck_appendix_c_distance_based_figure(mvd=15):
    plt.figure(figsize=(6.4, 6.4))
    plt.suptitle(
        "Appendix C Distance-Based Format"
        f"\nAtmospheric Icing Conditions for MVD={mvd}"
        "\nLiquid Water Content Factor vs. Cloud Horizontal Distance"
    )
    nms = np.geomspace(5., 310, 306)
    fs = get_continuous_maximum_lwc_factor(nms)
    cs = []
    for t in continuous_maximum_figure_1_points:
        lwcs = get_continuous_maximum_lwc(t, mvd)*fs
        line, = plt.plot(nms, lwcs, label=f"T={t}F")
        cs.append(line.get_color())
    nms = np.geomspace(.61, 5.21)
    fs = get_intermittent_maximum_lwc_factor(nms)
    for t, c in zip(continuous_maximum_figure_1_points, cs):
        lwcs = get_intermittent_maximum_lwc(t, mvd)*fs
        plt.plot(nms, lwcs, c=c)
    lwcs = get_intermittent_maximum_lwc(-40, mvd)*fs
    plt.plot(nms, lwcs, '--', label="T=-40F")
    plt.text(0.6, 0.02, 'Intermittent Maximum', va="bottom", ha="left")
    plt.text(5.21, 0.02, 'Continuous Maximum', va="bottom", ha="left")

    plt.legend()
    plt.xscale("log")
    plt.xlim(.5, 350)
    plt.ylim(0)
    plt.xlabel("Cloud Horizontal Extent, nmi")
    plt.ylabel("Liquid Water Content Factor, g/m^3")
    plt.tight_layout()

def make_figure_5(figure=None):
    if figure is None:
        figure = plt.figure(figsize=(6.4, 6.4))
    plt.suptitle(
        "Figure 5. Intermittent Maximum (Stratiform Clouds) (Redrawn)"
        "\nAtmospheric Icing Conditions"
        "\nAmbient Temperature vs. Pressure Altitude"
    )
    plt.plot(*intermittent_maximum_figure_5_points)
    plt.text(
        0.95,
        0.87,
        s=("SOURCE OF DATA" "\nNACA-TN-2569"),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(facecolor="white", edgecolor="black", alpha=0.8),
    )
    plt.xlim(-100)
    plt.ylim(-41, 31)
    plt.xlabel("Pressure Altitude, ft")
    plt.ylabel("Ambient Temperature, F")
    plt.tight_layout()
    return figure


def make_figure_6(figure=None):
    if figure is None:
        figure = plt.figure(figsize=(6.4, 5.4))
    plt.suptitle(
        "Figure 6. Intermittent Maximum (Cumuliform Clouds) (Redrawn)"
        "\nAtmospheric Icing Conditions"
        "\nLiquid Water Content Factor vs. Cloud Horizontal Distance"
    )
    nms = np.geomspace(.26, 5.21)  # 1 nmi intervals
    fs = get_intermittent_maximum_lwc_factor(
        nms
    )  # this function can accept a numpy array as input
    plt.plot(nms, fs)
    plt.text(
        0.95,
        0.87,
        s=("SOURCE OF DATA" "\nNACA-TN-2738"),
        transform=plt.gca().transAxes,
        ha="right",
        multialignment="left",
        c="k",
        bbox=dict(
            facecolor="white",  # Background color
            edgecolor="black",  # Border color
            alpha=0.8,  # Transparency
        ),
    )
    plt.xscale("log")
    plt.xlim(0.2, 6)
    plt.xticks((0.26, 0.5, 1, 2.61, 5.21), labels=[0.26, 0.5, 1, 2.61, 5.21])
    plt.ylim(0.8, 1.4)
    plt.xlabel("Cloud Horizontal Extent, nmi")
    plt.ylabel("Liquid Water Content Factor, F-Dimensionless")
    plt.grid()
    plt.tight_layout()
    return figure




def make_figure_1_csv(filename=None):
    if filename is None:
        filename = "appendix_c_figure_1.csv"
    ds = plt.np.linspace(15, 40, 26)
    all_lwcs = []
    ts = list(continuous_maximum_figure_1_points.keys())
    for t in continuous_maximum_figure_1_points:
        lwcs = [round(float(get_continuous_maximum_lwc(t, _)), 4) for _ in ds]
        all_lwcs.append(lwcs)
    cols = [ds] + all_lwcs
    rows = [["mvd"] + ts] + list(zip(*cols))
    with open(filename, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    return filename


def make_figure_2_csv(filename=None):
    if filename is None:
        filename = "appendix_c_figure_2.csv"
    cols = continuous_maximum_figure_2_points
    with open(filename, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list(zip(*cols)))
    return filename


def make_figure_3_csv(filename=None):
    if filename is None:
        filename = "appendix_c_figure_3.csv"
    nms = np.linspace(5, 310, 306)  # 1 nmi intervals
    fs = [round(float(get_continuous_maximum_lwc_factor(nm)), 4) for nm in nms]
    cols = nms, fs
    with open(filename, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list(zip(*cols)))
    return filename


if __name__ == "__main__":
    """
    Illustrate interpolations
    """
    alt = 16000
    tn, tm = get_continuous_maximum_t_min_t_max(alt)
    t_i = tm  # 17.6 F
    mvd_i = 18
    lwc_i = get_continuous_maximum_lwc(t_i, mvd_i)

    make_figure_1()
    plt.savefig("appc_fig1_redrawn.png")
    plt.plot(
        mvd_i, lwc_i, "+", ms=10, mew=2, label="interpolated point"
    )  # illustrate interpolation
    plt.text(mvd_i, lwc_i, f"{lwc_i:.3f} g/m^3\n{t_i:.1f}F\n{mvd_i:.0f} MVD")
    plt.legend()
    plt.savefig("appc_fig1_redrawn_interp.png")

    make_figure_2()
    plt.savefig("appc_fig2_redrawn.png")
    plt.plot(
        (alt, alt), (tn, tm), ":+", ms=10, label="Interpolated Tmin, Tmax"
    )  # illustrate interpolation
    plt.text(alt, tn, f"{tn:.1f}F")
    plt.text(alt, tm, f"{tm:.1f}F")
    plt.legend(loc="center left")
    plt.tight_layout()
    plt.savefig("appc_fig2_redrawn_interp.png")

    make_figure_3()
    plt.savefig("appc_fig3_redrawn.png")
    d1 = 17.4
    f1 = get_continuous_maximum_lwc_factor(d1)
    d2 = 120
    f2 = get_continuous_maximum_lwc_factor(d2)
    plt.plot(
        d1, f1, "+", ms=12, label=f"Interpolated distance={d1:.1f} nmi, F={f1:.3f}"
    )  # illustrate interpolation
    plt.plot(
        d2, f2, "+", ms=12, label=f"Interpolated distance={d2:.1f} nmi, F={f2:.3f}"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig("appc_fig3_redrawn_interpolate.png")

    plt.figure()
    plt.suptitle("Appendix C, Figure 1 (rearranged)")
    tz = np.linspace(-22, 32, 55)
    mvds = (15, 20, 25, 30, 35, 40)
    for mvd in mvds:
        lwcs = get_continuous_maximum_lwc(tz, mvd)
        plt.plot(tz, lwcs, label=f"MVD={mvd:.0f}")
    plt.ylim(0)
    plt.xlabel("Temperature, F")
    plt.ylabel("Liquid water content, g/m^3")
    plt.legend()
    plt.tight_layout()
    plt.savefig("appc_fig1_rearranged.png")

    make_figure_1()
    dz = np.linspace(15, 40, 26)
    for t in np.linspace(-22, 32, 55):
        if (t + 22) % 18 == 0:
            continue
        lwcs = [get_continuous_maximum_lwc(t, d_) for d_ in dz]
        plt.plot(dz, lwcs, ":o", ms=1, lw=0.5)
    plt.savefig("appc_fig1_redrawn_stripes.png")

    # Make csv files for spreadsheets
    make_figure_1_csv()
    make_figure_2_csv()
    make_figure_3_csv()

    # show in bounds and out of bounds examples
    print(get_continuous_maximum_lwc_factor(4))
    print(get_continuous_maximum_lwc_factor(5))
    print(get_continuous_maximum_lwc(32, 15))
    print(get_continuous_maximum_lwc(32, 14))
    print(get_continuous_maximum_lwc(33, 15))


    print(get_intermittent_maximum_lwc(-14, 20))

    make_figure_4()
    plt.savefig("appc_fig4_redrawn.png", transparent=True)

    make_figure_6()
    plt.savefig("appc_fig6_redrawn.png", transparent=True)

    make_figure_5()
    plt.savefig("appc_fig5_redrawn.png", transparent=True)

    make_jeck_continuous_maximum_distance_based_figure()
    plt.savefig("continuous_max_distance_based.png", transparent=True)

    make_jeck_appendix_c_distance_based_figure()
    plt.savefig("appc_distance_based.png", transparent=True)

    plt.show()
