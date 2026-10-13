import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.optimize import minimize
from scipy.stats import weibull_min

# AR-07/04 Figure 23 Layer Clouds MVD=15, T>=-10C
ds_23 = 3, 7, 10, 14, 20, 30, 50, 70, 100, 150, 200, 300, 340
lws_p999_23 = 1.23, 1.125, 1.07, 0.995, 0.91, 0.81, 0.69, 0.615, 0.52, 0.39, 0.32, 0.23, 0.2
lws_p99_23 = .835, 0.8, 0.77, 0.73, 0.68, 0.615, 0.525, 0.46, 0.39, 0.3, 0.245, 0.17, 0.15
lws_p95_23 = 0.55, 0.555, 0.55, 0.53, 0.5, 0.46, 0.39, 0.335, 0.28, 0.215, 0.175, 0.125, 0.11
lws_p9_23 = 0.43, 0.445, 0.445, 0.435, 0.415, 0.385, 0.325, 0.275, 0.225, 0.17, 0.14, 0.1, 0.09
lws_p5_23 = 0.135, 0.16, 0.17, 0.175, 0.175, 0.17, 0.14, 0.11, 0.085, 0.07, 0.06, 0.045, 0.04
lw_ps = 0.999, 0.99, 0.95, 0.9, 0.5


def calc_p_from_fig23(distance, lwc):
    lws_d = []
    xps = lw_ps[:]

    for p, lws in zip(lw_ps, (lws_p999_23, lws_p99_23, lws_p95_23, lws_p9_23, lws_p5_23)):
        lw = make_interp_spline(np.log(ds_23), lws)(np.log(distance))
        lws_d.append(lw)

    def objective(params):
        c, loc, scale = params
        if scale <= 0:
            return np.inf  # Scale must be positive
        p_model = weibull_min.cdf(lws_d, c, loc=loc, scale=scale)
        return np.sum((p_model - np.array(xps)) ** 2)

    result = minimize(objective, x0=[1.0, -0.5, 0.5])
    fitted_c, fitted_loc, fitted_scale = result.x
    fit = weibull_min(fitted_c, loc=fitted_loc, scale=fitted_scale)
    p = fit.cdf(lwc)
    return p


def calc_p_from_fig23_report_values(distance, lwc):
    lws_d = []
    xps = lw_ps[:]

    for p, lws in zip(lw_ps, (lws_p999_23, lws_p99_23, lws_p95_23, lws_p9_23, lws_p5_23)):
        lw = make_interp_spline(np.log(ds_23), lws)(np.log(distance))
        lws_d.append(lw)

    def objective(params):
        c, loc, scale = params
        if scale <= 0:
            return np.inf  # Scale must be positive
        p_model = weibull_min.cdf(lws_d, c, loc=loc, scale=scale)
        return np.sum((p_model - np.array(xps)) ** 2)

    result = minimize(objective, x0=[1.0, -0.5, 0.5])
    fitted_c, fitted_loc, fitted_scale = result.x
    fit = weibull_min(fitted_c, loc=fitted_loc, scale=fitted_scale)
    p = fit.cdf(lwc)
    return p, xps, lws_d, fit


def calc_lwc_from_fig23(distance, p):
    lws_d = []
    xps = lw_ps[:]

    for lws in (lws_p999_23, lws_p99_23, lws_p95_23, lws_p9_23, lws_p5_23):
        lw = make_interp_spline(np.log(ds_23), lws)(np.log(distance))
        lws_d.append(lw)

    def objective(params):
        c, loc, scale = params
        if scale <= 0:
            return np.inf  # Scale must be positive
        p_model = weibull_min.cdf(lws_d, c, loc=loc, scale=scale)
        return np.sum((p_model - np.array(xps)) ** 2)

    result = minimize(objective, x0=[1.0, -0.5, 0.5])
    fitted_c, fitted_loc, fitted_scale = result.x
    fit = weibull_min(fitted_c, loc=fitted_loc, scale=fitted_scale)
    lwc = fit.ppf(p)
    return lwc


def make_smooth_plot_lines(data_ds, data_lwcs, plot_ds=None):
    if not plot_ds:
        plot_ds = np.geomspace(data_ds[0], data_ds[-1], 100)
    plot_lws = make_interp_spline(np.log(data_ds), data_lwcs)(np.log(plot_ds))
    return plot_ds, plot_lws


if __name__ == '__main__':

    plt.figure(figsize=(6.4, 6.4))
    plt.suptitle('Natural Probabilities from AR-00/30 Figure 23')
    for p, lws in zip(lw_ps, (lws_p999_23, lws_p99_23, lws_p95_23, lws_p9_23, lws_p5_23)):
        line, = plt.plot(*make_smooth_plot_lines(ds_23, lws), '-', label=f"P={p}")
    plt.legend()
    plt.xscale('log')
    plt.ylim(0, 1.6)
    plt.xlabel('Distance, nmi')
    plt.ylabel('LWC, g/m^3')
    plt.tight_layout()
    plt.savefig('Natural Probabilities from Figure 23.png')

    d = 9.6
    lwc = 1.12  # row 1611 NorthSea: 1984
    p = calc_p_from_fig23(d, lwc)  # the simpler version of the function
    plt.plot(d, lwc, '+', ms=12, mew=2, label=f"P={p:.4f}\nDistance={d:.1f} nmi \nLWC={lwc:.2f}")
    plt.legend()
    plt.tight_layout()
    plt.savefig('Natural Probabilities from Figure 23 with example.png')

    p, xps, lws_d, fit = calc_p_from_fig23_report_values(d, lwc)
    plt.figure(figsize=(6.4, 6.4))
    plt.suptitle('Weibull Fit Details and Analysis of an Example Point')
    plt.plot(1 - np.array(xps), lws_d, 'x', label=f"Probability line data at {d} nmi")
    pes = np.geomspace(1 - .9999, 1)
    lws = fit.ppf(1 - pes)
    plt.plot(pes, lws, '--', label='Weibull fit of data')
    plt.plot(1 - np.array(p), lwc, '+', ms=12, mew=2, label=f"P={p:.5f}\nDistance={d:.1f} nmi\nLWC={lwc:.2f}")
    plt.legend()
    plt.xscale('log')
    plt.ylim(0, 1.6)
    plt.xlabel('PE = P-1')
    plt.ylabel('LWC, g/m^3')
    plt.tight_layout()
    plt.savefig('Weibull Fit Details and Analysis of an Example Point.png')

    plt.figure(figsize=(6.4, 6.4))
    plt.suptitle('Natural Probabilities from AR-00/30 Figure 23')
    for p, lws in zip(lw_ps, (lws_p999_23, lws_p99_23, lws_p95_23, lws_p9_23, lws_p5_23)):
        line, = plt.plot(*make_smooth_plot_lines(ds_23, lws), '-', label=f"P={p}")
    plt.legend()
    plt.xscale('log')
    plt.ylim(0, 1.6)
    plt.xlabel('Distance, nmi')
    plt.ylabel('LWC, g/m^3')

    plot_ds = np.geomspace(3, 310, 100)

    lws9999 = [calc_lwc_from_fig23(_, .9999) for _ in plot_ds]
    plt.plot(plot_ds, lws9999, ':r', lw=2, label=f"P=0.9999")
    plt.ylim(0)

    plt.legend()
    plt.tight_layout()
    plt.savefig('Figure 23 add 9999.png')

    plt.show()
