from scipy.interpolate import interp1d
import numpy as np
import csv
import matplotlib.pyplot as plt

f = r"figure_2_12_ko_beta.csv"

with open(f, "r") as fd:
    lines = [[float(_) for _ in line] for line in list(csv.reader(fd))]
kos, betas = list(zip(*lines))
__kb_interpolate = interp1d(
    np.log(kos), betas, "linear", fill_value=float("nan"), bounds_error=False
)
__kb_extrapolate = interp1d(
    np.log(kos), betas, "linear", fill_value="extrapolate", bounds_error=False
)


def interp_beta_max(ko):
    v = __kb_interpolate(np.log(ko))
    return v


def interp_beta_max_with_linear_extrapolation(ko):
    v = __kb_extrapolate(np.log(ko))
    return v


def calc_beta_and_make_plot(ko):
    plt.figure()
    beta = interp_beta_max_with_linear_extrapolation(ko)
    # print(f"For ko={ko:.5f}, Beta_max={beta:0.3f}")

    xs = np.geomspace(0.001, 10, 200)
    ys = interp_beta_max_with_linear_extrapolation(xs)
    ys2 = interp_beta_max(xs)

    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-2")
    # plt.plot(kos, betas, "+", label="Figure 2-12 Digitized points")
    plt.plot(xs, ys, "--", label="Figure 2-12 extrapolated")
    plt.plot(xs, ys2, label="Figure 2-12 data range")
    plt.plot(
        ko,
        beta,
        "o",
        fillstyle="none",
        label=f"Interpolated for Ko={ko:.4f}, Beta_max={beta:.3f}",
    )
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.xlabel("Ko")
    plt.ylabel("Beta_max")
    plt.legend()
    return beta


if __name__ == "__main__":

    ko = 0.05
    beta = interp_beta_max_with_linear_extrapolation(ko)
    print(f"For ko={ko:.5f}, Beta_max={beta:0.3f}")

    xs = np.geomspace(0.001, 10, 200)
    ys = interp_beta_max_with_linear_extrapolation(xs)
    ys2 = interp_beta_max(xs)

    plt.suptitle("DOT/FAA/CT-88/8-1 Example 2-2")
    plt.plot(kos, betas, "+", label="Figure 2-12 Digitized points")
    plt.plot(xs, ys, "--", label="Figure 2-12 extrapolated")
    plt.plot(xs, ys2, label="Figure 2-12 data range")
    plt.plot(
        ko,
        beta,
        "o",
        fillstyle="none",
        label=f"Interpolated for Ko={ko}, Beta_max={beta:.3f}",
    )
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.xlabel("Ko")
    plt.ylabel("Beta_max")
    plt.legend()
    plt.savefig("Example 2-2 beta.png")

    plt.show()
