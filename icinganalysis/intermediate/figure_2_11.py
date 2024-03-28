from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

f = r"figure_2_11_ko_em.csv"

import csv

with open(f, "r") as fd:
    lines = [[float(_) for _ in line] for line in list(csv.reader(fd))]
kos, ems = list(zip(*lines))
__ke_interpolate = interp1d(
    np.log(kos), ems, "linear", fill_value=float("nan"), bounds_error=False
)
__ke_extrapolate = interp1d(
    np.log(kos), ems, "linear", fill_value="extrapolate", bounds_error=False
)


def interp_em(ko):
    v = __ke_interpolate(np.log(ko))
    return v


def interp_em_with_linear_extrapolation(ko):
    v = __ke_extrapolate(np.log(ko))
    return v


def calc_e_and_make_plot(ko):
    plt.figure()
    em = interp_em_with_linear_extrapolation(ko)
    # print(f"For ko={ko:.5f}, Em={em:0.3f}")

    xs = np.geomspace(0.001, 10, 200)
    ys = interp_em_with_linear_extrapolation(xs)
    ys2 = interp_em(xs)

    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-2")
    # plt.plot(kos, ems, "+", label="Figure 2-11 Digitized points")
    plt.plot(xs, ys, "--", label="Figure 2-11 extrapolated")
    plt.plot(xs, ys2, label="Figure 2-11 data range")
    plt.plot(
        ko,
        em,
        "o",
        fillstyle="none",
        label=f"Interpolated for Ko={ko:.4f}, Em={em:.3f}",
    )
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.xlabel("Ko")
    plt.ylabel("Em")
    plt.legend()


if __name__ == "__main__":

    ko = 0.05
    em = interp_em_with_linear_extrapolation(ko)
    print(f"For ko={ko:.5f}, Em={em:0.3f}")

    xs = np.geomspace(0.001, 10, 200)
    ys = interp_em_with_linear_extrapolation(xs)
    ys2 = interp_em(xs)

    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-2")
    plt.plot(kos, ems, "+", label="Figure 2-11 Digitized points")
    plt.plot(xs, ys, "--", label="Figure 2-11 extrapolated")
    plt.plot(xs, ys2, label="Figure 2-11 data range")
    plt.plot(
        ko, em, "o", fillstyle="none", label=f"Interpolated for Ko={ko}, Em={em:.3f}"
    )
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.xlabel("Ko")
    plt.ylabel("Em")
    plt.legend()
    plt.savefig("Example 2-2.png")

    plt.show()
