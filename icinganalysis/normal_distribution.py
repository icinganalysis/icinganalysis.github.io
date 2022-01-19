import numpy as np
from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator, FuncFormatter
from scipy.stats import norm


class NormProbScale(mscale.ScaleBase):
    """
    derived from example at https://matplotlib.org/stable/gallery/scales/custom_scale.html
    """
    name = 'normprob'

    def __init__(self, axis, *, xmin=.0001, xmax=.9999, **kwargs):
        super().__init__(axis)
        self.xmin = xmin
        self.xmax = xmax

    def get_transform(self):
        return self.NormProbTransform(self.xmin, self.xmax)

    def set_default_locators_and_formatters(self, axis):
        fmt = FuncFormatter(
            lambda x, pos=None: f"{x * 100}")
        axis.set(major_locator=FixedLocator(
            (.0001, .001, .01, .1, .25, .5, .75, .9, .99, .999, .9999),
            # (.05, .15, .35, .65, .85, .95),
            # (.025, .1, .25, .5, .75, .9, .975),
            # (.025,.05, .1,.15, .25,.35, .5,.65, .75,.85, .9, .95, .975),
        ),
            major_formatter=fmt, minor_formatter=fmt)

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
            return NormProbScale.InvertedNormProbTransform(
                self.xmin, self.xmax)

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


def to_stairs(vs):
    ws = []
    for v in vs[1:]:
        ws.append(v)
        ws.append(v)
    ws.insert(0, vs[0])
    ws.append(vs[-1])
    return ws


def to_risers(vs):
    ws = []
    for v in vs[:]:
        ws.append(v)
        ws.append(v)
    return ws


def make_markdown_table(header, rows):
    text = '|'.join(header)+'\n'
    text += '|'.join(['---']*len(header)) + '\n'
    for row in rows:
        text += '|'.join([str(_) for _ in row]) + '\n'
    return text


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit

    from scipy.stats import norm

    import numpy as np
    from icinganalysis import langmuir_cylinder


    # Fit NACA-TN-2708 Figure 6 data
    p = 0.01, 0.0175, 0.0175, 0.085, 0.085, 0.16, 0.16, 0.30, 0.30, 0.475, 0.475, 1.00, 1.00, 1.85, 1.85, 3.30, 3.30, 5.80, 5.80, 9.40, 9.40, 15.10, 15.10, 22.55, 22.55, 32.00, 32.00, 41.50, 41.50, 51.50, 51.50, 61.40, 61.40, 72.40, 72.40, 80.00, 80.00, 86.90, 86.90, 91.40, 91.40, 94.20, 94.20, 96.40, 96.40, 97.40, 97.40, 99.25, 99.25, 99.75, 99.75, 99.99, 99.99, 99.99
    r = 2.5, 2.5, 3.7, 3.7, 4.8, 4.8, 6.3, 6.3, 7.2, 7.2, 8.2, 8.2, 9.7, 9.7, 10.6, 10.6, 11.8, 11.8, 13.1, 13.1, 14.1, 14.1, 15.5, 15.5, 16.8, 16.8, 18.0, 18.0, 18.8, 18.8, 20.3, 20.3, 21.7, 21.7, 22.6, 22.6, 24.1, 24.1, 25.0, 25.0, 26.8, 26.8, 27.5, 27.5, 28.7, 28.7, 30.0, 30.0, 31.2, 31.2, 32.7, 32.7, 32.7, 32.7
    pp = [_ / 100 for _ in p]
    mvr, dev = curve_fit(norm.cdf, r, pp, p0=[1, 1])[0]
    print(mvr, dev, dev / mvr)
    q = norm(mvr, dev)
    plt.figure(figsize=(7, 5))
    plt.plot(to_stairs(pp), to_risers(r), 'o-', fillstyle='none', lw=0.5, ms=3,
             label='Data from Houghton and Radford')
    ps = np.linspace(.0001, .9999, 1000)
    zs = q.ppf(ps)
    plt.plot(ps, zs, label=f'Normal CDF best fit (scipy), MVR={mvr:.2f}, stdev={dev:.2f}')

    # work with an ideal normal curve with stdev=0.25
    normal_distribution = norm(1, 0.237)
    naca_tn_2708_bin_points = (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47)
    cumulative_volumes_for_naca_tn_2708_bin_mids = normal_distribution.cdf(naca_tn_2708_bin_points)
    cumulative_volumes_for_langmuir_b = normal_distribution.cdf(langmuir_cylinder.langmuir_b_mids)
    expected_midpoint_cumulative_volumes = 0.025, .1, .25, .5, .75, .9, .975
    size_ratios_for_expected_midpoint_cumulative_volumes = normal_distribution.ppf(expected_midpoint_cumulative_volumes)

    header = [
        'Percentile divisions of total liquid volume in clouds',
        'Expected midpoint cumulative %',
        'Drop size ratios to match midpoint cumulative % (normal distribution)',
        'Drop size ratios (Langmuir B)',
        'Calculate cumulative volume (Langmuir B), %',
        'Drop size ratios (Clark)',
        'Calculate cumulative volume (Clark), %',
    ]
    columns = [
        ['0-5', '5-15', '15-35', '35-65', '65-85', '85-95', '95-100'],
        (2.5, 10, 25, 50, 75, 90, 97.5),
        [round(_, 2) for _ in size_ratios_for_expected_midpoint_cumulative_volumes],
        langmuir_cylinder.langmuir_b_mids,
        [round(_*100, 1) for _ in cumulative_volumes_for_langmuir_b],
        (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47),
        [round(_*100, 1) for _ in cumulative_volumes_for_naca_tn_2708_bin_mids],
    ]
    print()
    print('With normal distribution stdev=0.237 (fit to Houghton and Radford)')
    print()
    print(make_markdown_table(header, zip(*columns)))
    print()

    # work with an ideal normal curve with stdev=0.25
    normal_distribution = norm(1, 0.25)
    naca_tn_2708_bin_points = (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47)
    cumulative_volumes_for_naca_tn_2708_bin_mids = normal_distribution.cdf(naca_tn_2708_bin_points)
    cumulative_volumes_for_langmuir_b = normal_distribution.cdf(langmuir_cylinder.langmuir_b_mids)
    expected_midpoint_cumulative_volumes = 0.025, .1, .25, .5, .75, .9, .975
    size_ratios_for_expected_midpoint_cumulative_volumes = normal_distribution.ppf(expected_midpoint_cumulative_volumes)

    header = [
        'Percentile divisions of total liquid volume in clouds',
        'Expected midpoint cumulative %',
        'Drop size ratios to match midpoint cumulative % (normal distribution)',
        'Drop size ratios (Langmuir B)',
        'Calculate cumulative volume (Langmuir B), %',
        'Drop size ratios (Clark)',
        'Calculate cumulative volume (Clark), %',
    ]
    columns = [
        ['0-5', '5-15', '15-35', '35-65', '65-85', '85-95', '95-100'],
        (2.5, 10, 25, 50, 75, 90, 97.5),
        [round(_, 2) for _ in size_ratios_for_expected_midpoint_cumulative_volumes],
        langmuir_cylinder.langmuir_b_mids,
        [round(_*100, 1) for _ in cumulative_volumes_for_langmuir_b],
        (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47),
        [round(_*100, 1) for _ in cumulative_volumes_for_naca_tn_2708_bin_mids],
    ]
    print()
    print('With normal distribution stdev=0.25')
    print()
    print(make_markdown_table(header, zip(*columns)))
    print()


    print(langmuir_cylinder.langmuir_b_mids)

    print(naca_tn_2708_bin_points)



    bin_volumes = 0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05
    # cumulative_volumes = [0]
    # for v in bin_volumes:
    #     cumulative_volumes.append(cumulative_volumes[-1] + v)
    # print(cumulative_volumes)
    cumulative_volumes = 0.05, 0.15, 0.35, 0.65, 0.85, 0.95, 1  # assumed 0 starting point
    assumed_bin_mid_point_cumulative_volumes = (.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975)
    ds_for_assumed_bin_mid_point_cumulative_volumes = q.ppf(assumed_bin_mid_point_cumulative_volumes)
    size_ratios_for_assumed_bin_mid_point_cumulative_volumes = [_ / mvr for _ in ds_for_assumed_bin_mid_point_cumulative_volumes]
    print('size ratios for assumed_bin_mid_point_cumulative_volumes =', ', '.join([f"{_:.2f}" for _ in size_ratios_for_assumed_bin_mid_point_cumulative_volumes]))
    normal_cumulative_volumes = 0.01, 0.05, 0.15, 0.35, 0.65, 0.85, 0.95, .99  # assumed 0 starting point
    ds_for_normal_cumulative_volumes = q.ppf(normal_cumulative_volumes)
    size_ratios_for_normal_cumulative_volumes = [_ / mvr for _ in ds_for_normal_cumulative_volumes]
    print('size ratios for normal_cumulative_volumes =', ', '.join([f"{_:.2f}" for _ in size_ratios_for_normal_cumulative_volumes]))
    arithmetic_mids_for_normal_cumulative_volumes = [(v1+v2) / 2 / mvr for v1, v2 in zip(ds_for_normal_cumulative_volumes[:-1], ds_for_normal_cumulative_volumes[1:])]
    print('mids of size ratios for normal_cumulative_volumes =', ', '.join([f"{_:.2f}" for _ in arithmetic_mids_for_normal_cumulative_volumes]))
    # print([_/mvd for _ in q.ppf(normal_cumulative_volumes)])

    ds = [mvr * _ for _ in naca_tn_2708_bin_points]
    print(ds)
    print(q.cdf(ds))
    q_cdfs = q.cdf(ds)

    # plt.plot(q_cdfs, ds, 'o', label='NACA-TN-2708 ')

    plt.xscale('normprob')
    plt.xlabel('Cumulative Probability, %')
    plt.xlim(.0001, .9999)
    plt.ylabel("Drop Radius, micrometer")
    plt.ylim(0, 45)
    plt.legend(loc='upper left')
    plt.savefig('NACA-TN-2708_Figure_6.png', transparent=True)

    plt.figure()
    plt.plot(ps, zs, label=f'Houghton and Radford data best fit, MVD={mvr:.2f}, stdev={dev:.2f}')

    ds = [mvr * _ for _ in naca_tn_2708_bin_points]
    print(ds)
    print(q.cdf(ds))
    q_cdfs = q.cdf(ds)
    plt.plot(q_cdfs, ds, 'o', label='NACA-TN-2708 ')

    ds = [mvr * _ for _ in langmuir_cylinder.langmuir_b_mids]
    print(ds)
    print(q.cdf(ds))
    q_cdfs = q.cdf(ds)
    plt.plot(q_cdfs, ds, 's', fillstyle='none', label='Langmuir B')

    pxs = (0.05, .15, .35, .65, .85, .95)
    dxs = q.ppf(pxs)
    plt.plot(pxs, dxs, 'x', label='mids')

    dls = q.ppf(assumed_bin_mid_point_cumulative_volumes)
    print('dls', dls)
    print('dls', [f"{float(_ / mvr):.3f}" for _ in dls])
    plt.plot(assumed_bin_mid_point_cumulative_volumes, dls, '+', ms=14)

    cpms = (.025, .1, .25, .5, .75, .9, .975)
    dxs = q.ppf(cpms)
    # plt.plot(cpms, dxs, 'x')

    plt.xscale('normprob')
    plt.xlabel('Cumulative Probability, %')
    plt.xlim(.0001, .9999)
    plt.ylabel("Drop Radius, micrometer")
    plt.ylim(0, 45)
    plt.legend(loc='upper left')

    plt.figure(figsize=(8, 5))
    plt.plot(zs, ps, label=f'Houghton and Radford data best fit\nMVR={mvr:.2f}, stdev={dev:.2f}')

    naca_tn_2708_bin_points = (0.53, 0.69, 0.91, 1.0, 1.09, 1.31, 1.47)
    ds = [mvr * _ for _ in naca_tn_2708_bin_points]
    print(ds)
    print(q.cdf(ds))
    q_cdfs = q.cdf(ds)
    plt.plot(ds, q_cdfs, 'o', label='NACA-TN-2708 ')

    ds = [mvr * _ for _ in langmuir_cylinder.langmuir_b_mids]
    print(ds)
    print(q.cdf(ds))
    q_cdfs = q.cdf(ds)
    plt.plot(ds, q_cdfs, 's', fillstyle='none', label='Langmuir B')

    pxs = (.01, 0.05, .15, .35, .65, .85, .95, .99)
    dxs = q.ppf(pxs)
    plt.plot(dxs, pxs, 'x', c='r', label='proposed boundaries')
    for dl, cm in zip(dxs, pxs):
        plt.text(dl, cm, f"({dl / mvr:.3f}, {cm:.3f})", color='r', verticalalignment='bottom',
                 horizontalalignment='right')

    print('bds', ','.join([f"{_ / mvr:.3f}" for _ in dxs]))

    dls = q.ppf(assumed_bin_mid_point_cumulative_volumes)
    plt.plot(dls, assumed_bin_mid_point_cumulative_volumes, '+', c='g', ms=14, label='centroids')
    for dl, cm in zip(dls, assumed_bin_mid_point_cumulative_volumes):
        plt.text(dl, cm, f"({dl / mvr:.3f}, {cm:.3f})", color='g', verticalalignment='top')

    cpms = (.025, .1, .25, .5, .75, .9, .975)
    dxs = q.ppf(cpms)
    # plt.plot(cpms, dxs, 'x')

    risers = 0.536, 0.536, 0.696, 0.696, 0.840, 0.840, 1.000, 1.000, 1.160, 1.160, 1.304, 1.304, 1.464, 1.464
    stairs = 0, .05, .05, .15, .15, .35, .35, .65, .65, .85, .85, .95, .95, 1
    ds = [_ * mvr for _ in risers]
    plt.plot(ds, stairs)

    stairs = 0, 0.05, 0.05, .15, .15, .35, .35, .65, .65, .85, .85, .95, .95, 1
    print(len(risers))
    print(len(stairs))

    risers = 0.449, 0.449, 0.610, 0.610, 0.754, 0.754, 0.909, 0.909, 1.091, 1.091, 1.246, 1.246, 1.390, 1.390, 1.551
    stairs = (0, 0.05, 0.05, .15, .15, .35, .35, .65, .65, .85, .85, .95, .95, 1, 1)
    ds = [_ * mvr for _ in risers]
    plt.plot(ds, stairs, '--')
    print(ds)
    print(stairs)

    print(len(risers))
    print(len(stairs))

    bds = 0.449, 0.610, 0.754, 0.909, 1.091, 1.246, 1.390, 1.551
    mid_bds = [(v1 + v2) / 2 for v1, v2 in zip(bds[:-1], bds[1:])]
    print(mid_bds)

    from itertools import zip_longest

    # for vs in zip_longest(risers, stairs):
    #     print(vs)

    plt.ylabel('Cumulative Probability, %')
    plt.xlabel("Drop Radius, micrometer")
    plt.xlim(0, 45)
    plt.legend(loc='lower right')

    plt.figure()
    ds = np.arange(1, 61)
    ps = q.pdf(ds)
    plt.plot(ds, ps)

    plt.show()
