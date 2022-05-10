from scipy.interpolate import interp1d
from icinganalysis.iteration_helpers import take_by
from icinganalysis.units_helpers import tc_to_k, tf_to_k, MPH_PER_M_S

# fmt: off
d = (
    -30, 6, 4.15, 3.22, 2.65, 2.15, 1.75, 1.4, 1.07,
    -25, 4.7, 3.22, 2.5, 2.05, 1.63, 1.32, 1.02, 0.75,
    -20, 3.55, 2.42, 1.85, 1.5, 1.18, 0.9, 0.65, 0.45,
    -15, 2.55, 1.72, 1.3, 1, 0.75, 0.55, 0.34, 0.17,
    -10, 1.65, 1.07, 0.77, 0.56, 0.39, 0.22, 0.05, -0.11,
    -5, 0.77, 0.45, 0.29, 0.16, 0.05, -0.1, -0.24, -0.39,
    0, 0, -0.1, -0.15, -0.22, -0.3, -0.42, -0.53, -0.67,
)
# fmt: on
tcs_, lwcs25, lwcs50, lwcs75, lwcs100, lwcs125, lwcs150, lwcs175, lwcs200 = zip(
    *take_by(d, 9)
)
us = 25, 50, 75, 100, 125, 150, 175, 200


def interp_lwc_critical(tk, u):
    tks = [tc_to_k(_) for _ in tcs_]
    l1 = interp1d(tks, lwcs25)(tk)
    l2 = interp1d(tks, lwcs50)(tk)
    l3 = interp1d(tks, lwcs75)(tk)
    l4 = interp1d(tks, lwcs100)(tk)
    l5 = interp1d(tks, lwcs125)(tk)
    l6 = interp1d(tks, lwcs150)(tk)
    l7 = interp1d(tks, lwcs175)(tk)
    l8 = interp1d(tks, lwcs200)(tk)
    lwc = interp1d(us, (l1, l2, l3, l4, l5, l6, l7, l8), fill_value="extrapolate")(u)
    return max(0, lwc)


# fmt: off
d_table4 = (  # Case, u, tc, lwc, time, g, d_cyl, density, thick, width, lwc, Lwc_2
    30, 100, -15, 0.6, 60, 0.6295, 0.00497, 890, 0.003945, 0.005, 0.61, 0.59,
    31, 100, -15, 0.6, 60, 0.6425, 0.00492, 890, 0.003905, 0.005, 0.6, 0.58,
    35, 100, -15, 0.6, 60, 0.6695, 0.00505, 870, 0.00405, 0.00476, 0.62, 0.6,
    36, 100, -15, 0.6, 30, 0.274, 0.003725, 890, 0.002035, 0.00384, 0.61, 0.59,
    32, 100, -10, 0.6, 60, 0.663, 0.00512, 830, 0.003265, 0.00787, 0.62, 0.6,
    33, 100, -10, 0.6, 60, 0.6435, 0.0051, 810, 0.003275, 0.0078, 0.6, 0.58,
    34, 100, -10, 0.6, 30, 0.2834, 0.00346, 890, 0.001855, 0.00545, 0.62, 0.6,
    37, 100, -7.5, 0.6, 30, 0.217, 0.00354, 850, 0.001585, 0.00503, 0.5, 0.48,
    41, 100, -7.5, 0.6, 30, 0.248, 0.00366, 860, 0.001585, 0.00505, 0.56, 0.56,
    38, 100, -8.5, 0.6, 30, 0.266, 0.00372, 870, 0.001635, 0.00541, 0.59, 0.57,
    39, 100, -6, 0.6, 30, 0.2245, 0.0037, 750, 0.001255, 0.00502, 0.51, 0.49,
    40, 100, -6, 0.6, 30, 0.2155, 0.00366, 750, 0.001265, 0.00496, 0.49, 0.47,
)
# fmt: on
case, u, tc, lwc_nominal, time, g, d_cyl, density, thick, width, lwc, lwc_2 = zip(
    *take_by(d_table4, 12)
)

# fmt: off
df = (  # Figure 3 450 fps data points
    -1, 0.17,
    -1.4, 0.03,
    -1.5, 0.21,
    -1.6, 0.28,
    -1.9, 0.08,
    -2.2, 0.11,
    -2.3, 0.19,
    -2.7, 0.14,
    -3.5, 0.15,
    -3.8, 0.1,
    -3.8, 0.24,
    -4.3, 0.21,
    -4.3, 0.3,
    -4.7, 0.29,
    -4.8, 0.28,
    -5, 0.32,
    -5.1, 0.31,
    -5.3, 0.44,
    -5.6, 0.42,
    -6, 0.44,
    -6.7, 0.44,
    -7, 0.44,
    -7.8, 0.51,
    -7.8, 0.56,
    -9.7, 0.44,
    -9.7, 0.5,
    -10.7, 0.44,
    -11.7, 0.44,
    -11.8, 0.5,
    -13.5, 0.44,
    -13.7, 0.44,
    -14.6, 0.43,
    -14.9, 0.44,
    -16.3, 0.51,
    -16.4, 0.43,
    -17.6, 0.51,
    -17.7, 0.43,
    -18.7, 0.43,
    -19.1, 0.43,
)
# fmt: on
fig3_450fps_tcs = df[::2]
fig3_450fps_lwcs = df[1::2]

if __name__ == "__main__":
    case = "NACA-TR-1215 Figure 24a, NACA-TN-1424 Run 20"
    tf = 23  # 20 1/29/47
    mph = 168
    print(
        case, tf_to_k(tf) - 273.15, interp_lwc_critical(tf_to_k(tf), mph / MPH_PER_M_S)
    )
    case = "NACA-TR-1215 Figure 24b, NACA-TN-2306 Flight 10, run 2"
    mph = 192
    tf = 25
    print(
        case, tf_to_k(tf) - 273.15, interp_lwc_critical(tf_to_k(tf), mph / MPH_PER_M_S)
    )
    case = "NACA-TR-1215 Figure 24c, NACA-TN-2306 Flight 19, run 2"
    mph = 200
    tf = 26
    print(
        case, tf_to_k(tf) - 273.15, interp_lwc_critical(tf_to_k(tf), mph / MPH_PER_M_S)
    )
    case = "NACA-TR-1215 Figure 24d, NACA-TN-1904 Flight 179, run 17"
    mph = 180
    tf = 15
    print(
        case, tf_to_k(tf) - 273.15, interp_lwc_critical(tf_to_k(tf), mph / MPH_PER_M_S)
    )

    import matplotlib.pyplot as plt

    tcs = plt.np.linspace(-12, -5)

    u = 100
    p = 101325
    mvd = 20
    distribution = "Langmuir D"
    lwcs = [interp_lwc_critical(tc_to_k(_), u) for _ in tcs]
    plt.plot(tcs, lwcs, "--", label="LWC critical from Figure 7")

    plt.plot(tc, lwc, "o", label="LTR-LT-92 Table IV Calculated LWC")

    plt.plot(
        (-20, -9, -4),
        (0.6, 0.6, 0.43),
        label="LTR-LT-92 Figure 3 Rotating Cylinder line",
    )

    plt.xlim(-20, 0)
    plt.ylim(0, 1)
    plt.xlabel("Air Temperature, C")
    plt.ylabel("Measured LWC, g/^3")
    plt.legend()
    plt.savefig("ltr-lt-92_figure3_comparison.png")

    plt.show()
