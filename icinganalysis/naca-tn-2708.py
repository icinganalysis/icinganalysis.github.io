import matplotlib.pyplot as plt
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator, FuncFormatter
from scipy.optimize import curve_fit
from scipy.stats import norm
import numpy as np
from icinganalysis import langmuir_cylinder_values
from icinganalysis.markdown_table_helper import make_markdown_table


class NormProbScale(mscale.ScaleBase):
    """
    derived from example at https://matplotlib.org/stable/gallery/scales/custom_scale.html
    """

    name = "normprob"

    def __init__(self, axis, *, xmin=0.0001, xmax=0.9999, **kwargs):
        super().__init__(axis)
        self.xmin = xmin
        self.xmax = xmax

    def get_transform(self):
        return self.NormProbTransform(self.xmin, self.xmax)

    def set_default_locators_and_formatters(self, axis):
        fmt = FuncFormatter(lambda x, pos=None: f"{x * 100}")
        axis.set(
            major_locator=FixedLocator(
                (0.0001, 0.001, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999, 0.9999),
                # (.05, .15, .35, .65, .85, .95),
                # (.025, .1, .25, .5, .75, .9, .975),
                # (.025,.05, .1,.15, .25,.35, .5,.65, .75,.85, .9, .95, .975),
            ),
            major_formatter=fmt,
            minor_formatter=fmt,
        )

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(vmin, -self.xmin), min(vmax, self.xmax)

    class NormProbTransform(mtransforms.Transform):
        input_dims = output_dims = 1

        def __init__(self, xmin, xmax):
            mtransforms.Transform.__init__(self)
            self.xmin = xmin
            self.xmax = xmax

        def transform_non_affine(self, a):
            return norm.ppf(a)

        def inverted(self):
            return NormProbScale.InvertedNormProbTransform(self.xmin, self.xmax)

    class InvertedNormProbTransform(mtransforms.Transform):
        input_dims = output_dims = 1

        def __init__(self, xmin, xmax):
            mtransforms.Transform.__init__(self)
            self.xmin = xmin
            self.xmax = xmax

        def transform_non_affine(self, a):
            return norm.cdf(a)

        def inverted(self):
            return NormProbScale.NormProbTransform(self.xmin, self.xmax)


mscale.register_scale(NormProbScale)


def to_stairs_x(vs, insert_initial=True):
    ws = []
    if insert_initial:
        ws = [vs[0]]
    for v in vs[1:]:
        ws.append(v)
        ws.append(v)
    ws.insert(0, vs[0])
    ws.append(vs[-1])
    return ws


def to_stairs_y(vs, insert_initial=True):
    ws = []
    if insert_initial:
        ws = [0]
    for v in vs:
        ws.append(v)
        ws.append(v)
    return ws


if __name__ == "__main__":
    # Fit NACA-TN-2708 Figure 6 data
    p = (
        0.01,
        0.0175,
        0.0175,
        0.085,
        0.085,
        0.16,
        0.16,
        0.30,
        0.30,
        0.475,
        0.475,
        1.00,
        1.00,
        1.85,
        1.85,
        3.30,
        3.30,
        5.80,
        5.80,
        9.40,
        9.40,
        15.10,
        15.10,
        22.55,
        22.55,
        32.00,
        32.00,
        41.50,
        41.50,
        51.50,
        51.50,
        61.40,
        61.40,
        72.40,
        72.40,
        80.00,
        80.00,
        86.90,
        86.90,
        91.40,
        91.40,
        94.20,
        94.20,
        96.40,
        96.40,
        97.40,
        97.40,
        99.25,
        99.25,
        99.75,
        99.75,
        99.99,
        99.99,
        99.99,
    )
    r = (
        2.5,
        2.5,
        3.7,
        3.7,
        4.8,
        4.8,
        6.3,
        6.3,
        7.2,
        7.2,
        8.2,
        8.2,
        9.7,
        9.7,
        10.6,
        10.6,
        11.8,
        11.8,
        13.1,
        13.1,
        14.1,
        14.1,
        15.5,
        15.5,
        16.8,
        16.8,
        18.0,
        18.0,
        18.8,
        18.8,
        20.3,
        20.3,
        21.7,
        21.7,
        22.6,
        22.6,
        24.1,
        24.1,
        25.0,
        25.0,
        26.8,
        26.8,
        27.5,
        27.5,
        28.7,
        28.7,
        30.0,
        30.0,
        31.2,
        31.2,
        32.7,
        32.7,
        32.7,
        32.7,
    )
    pp = [_ / 100 for _ in p]
    mvr, dev = curve_fit(norm.cdf, r, pp, p0=[1, 1])[0]
    print(mvr, dev, dev / mvr)
    q = norm(mvr, dev)
    plt.figure(figsize=(7, 5))
    plt.plot(
        pp,
        r,
        "o-",
        fillstyle="none",
        lw=0.5,
        ms=3,
        label="Data from Houghton and Radford",
    )
    ps = np.linspace(0.0001, 0.9999, 1000)
    zs = q.ppf(ps)
    plt.plot(
        ps, zs, label=f"Normal CDF best fit (scipy), MVR={mvr:.2f}, stdev={dev:.2f}"
    )
    plt.xscale("normprob")
    plt.xlabel("Cumulative Probability, %")
    plt.xlim(0.0001, 0.9999)
    plt.ylabel("Drop Radius, micrometer")
    plt.ylim(0, 45)
    plt.legend(loc="upper left")

    # work with an ideal normal curve with stdev=0.25
    normal_distribution = norm(1, 0.237)
    naca_tn_2708_bin_points = (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47)
    cumulative_volumes_for_naca_tn_2708_bin_mids = normal_distribution.cdf(
        naca_tn_2708_bin_points
    )
    cumulative_volumes_for_langmuir_b = normal_distribution.cdf(
        langmuir_cylinder_values.langmuir_b_mids
    )
    expected_midpoint_cumulative_volumes = 0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975
    size_ratios_for_expected_midpoint_cumulative_volumes = normal_distribution.ppf(
        expected_midpoint_cumulative_volumes
    )

    header = [
        "Percentile divisions of total liquid volume in clouds",
        "Expected midpoint cumulative %",
        "Drop size ratios to match midpoint cumulative % (normal distribution)",
        "Drop size ratios (Langmuir B)",
        "Calculate cumulative volume (Langmuir B), %",
        "Drop size ratios (Clark)",
        "Calculate cumulative volume (Clark), %",
    ]
    columns = [
        ["0-5", "5-15", "15-35", "35-65", "65-85", "85-95", "95-100"],
        (2.5, 10, 25, 50, 75, 90, 97.5),
        [round(_, 2) for _ in size_ratios_for_expected_midpoint_cumulative_volumes],
        langmuir_cylinder_values.langmuir_b_mids,
        [round(_ * 100, 1) for _ in cumulative_volumes_for_langmuir_b],
        (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47),
        [round(_ * 100, 1) for _ in cumulative_volumes_for_naca_tn_2708_bin_mids],
    ]
    print()
    print("With normal distribution stdev=0.237 (fit to Houghton and Radford)")
    print()
    print(make_markdown_table(header, zip(*columns)))
    print()

    # work with an ideal normal curve with stdev=0.25
    normal_distribution = norm(1, 0.25)
    naca_tn_2708_bin_points = (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47)
    cumulative_volumes_for_naca_tn_2708_bin_mids = normal_distribution.cdf(
        naca_tn_2708_bin_points
    )
    cumulative_volumes_for_langmuir_b = normal_distribution.cdf(
        langmuir_cylinder_values.langmuir_b_mids
    )
    expected_midpoint_cumulative_volumes = 0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975
    size_ratios_for_expected_midpoint_cumulative_volumes = normal_distribution.ppf(
        expected_midpoint_cumulative_volumes
    )

    header = [
        "Percentile divisions of total liquid volume in clouds",
        "Expected midpoint cumulative %",
        "Drop size ratios to match midpoint cumulative % (normal distribution)",
        "Drop size ratios (Langmuir B)",
        "Calculate cumulative volume (Langmuir B), %",
        "Drop size ratios (Clark)",
        "Calculate cumulative volume (Clark), %",
    ]
    columns = [
        ["0-5", "5-15", "15-35", "35-65", "65-85", "85-95", "95-100"],
        (2.5, 10, 25, 50, 75, 90, 97.5),
        [round(_, 2) for _ in size_ratios_for_expected_midpoint_cumulative_volumes],
        langmuir_cylinder_values.langmuir_b_mids,
        [round(_ * 100, 1) for _ in cumulative_volumes_for_langmuir_b],
        (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47),
        [round(_ * 100, 1) for _ in cumulative_volumes_for_naca_tn_2708_bin_mids],
    ]
    print()
    print("With normal distribution stdev=0.25")
    print()
    print(make_markdown_table(header, zip(*columns)))
    print()

    plt.figure()
    plt.plot(
        r,
        pp,
        "o-",
        fillstyle="none",
        lw=0.5,
        ms=3,
        label="Data from \nHoughton & Radford",
    )
    ps = np.linspace(0.0001, 0.9999, 1000)
    zs = q.ppf(ps)
    plt.plot(
        zs, ps, label=f"Normal CDF best fit (scipy)\nMVR={mvr:.2f}, stdev={dev:.2f}"
    )

    # expected_midpoint_cumulative_volumes = 0.025, .1, .25, .5, .75, .9, .975
    ds = [mvr * _ for _ in langmuir_cylinder_values.langmuir_b_mids]
    (line,) = plt.plot(
        ds,
        expected_midpoint_cumulative_volumes,
        "+-",
        ms=10,
        mew=2,
        label="Langmuir B (as lines)",
    )
    cumulative_volumes_at_upper_ends = 0.05, 0.15, 0.35, 0.65, 0.85, 0.95, 1
    plt.plot(
        to_stairs_x(ds),
        to_stairs_y(cumulative_volumes_at_upper_ends),
        ":",
        c=line.get_color(),
        label="Langmuir B (as steps)",
    )

    plt.ylabel("Cumulative Fraction LWC")
    plt.xlabel("Drop Radius, micrometer")
    plt.xlim(0, 40)
    plt.ylim(0, 1)
    plt.legend(loc="lower right")
    plt.savefig("Langmuir B and normal.png")

    plt.figure()
    normal_distribution = norm(1, 0.75)
    ps = np.linspace(0.0001, 0.9999, 1000)
    zs = normal_distribution.ppf(ps)
    plt.plot(zs, ps, label=f"Normal distribution stdev=0.75")
    mvr, dev = curve_fit(
        norm.cdf,
        langmuir_cylinder_values.langmuir_e_mids,
        expected_midpoint_cumulative_volumes,
        p0=[1, 1],
    )[0]
    normal_distribution = norm(mvr, dev)
    ps = np.linspace(0.0001, 0.9999, 1000)
    zs = normal_distribution.ppf(ps)
    plt.plot(zs, ps, "--", label=f"Langmuir E normal best fit stdev={dev:.2f}")
    # normal_distribution = norm(1, 1)
    # ps = np.linspace(.0001, .9999, 1000)
    # zs = normal_distribution.ppf(ps)
    # plt.plot(zs, ps, label=f'Normal distribution stdev=1')
    (line,) = plt.plot(
        langmuir_cylinder_values.langmuir_e_mids,
        expected_midpoint_cumulative_volumes,
        "+-",
        ms=8,
        mew=2,
        label="Langmuir E (as lines)",
    )
    plt.plot(
        to_stairs_x(langmuir_cylinder_values.langmuir_e_mids),
        to_stairs_y(cumulative_volumes_at_upper_ends),
        ":",
        c=line.get_color(),
        label="Langmuir E (as steps)",
    )
    plt.ylabel("Cumulative Fraction LWC")
    plt.xlabel("Drop size ratio, r/MVR or d/MVD")
    # plt.xlim(0, 40)
    plt.ylim(0, 1)
    plt.xlim(-1)
    plt.legend(loc="lower right")
    plt.savefig("Langmuir E and normal.png")

    plt.show()
