from scipy.interpolate import interp2d, interp1d
import numpy as np
import matplotlib.pyplot as plt
from math import log10
from icinganalysis import langmuir_cylinder


def trim_extra_x_y_zeros(x, y):
    xs = []
    ys = []
    last_zero = False
    for x, y, in zip(x, y):
        if y > 0:
            xs.append(x)
            ys.append(y)
        elif not last_zero:
            xs.append(x)
            ys.append(y)
            last_zero = True
        else:
            break
    return xs, ys


d_1000 = {
    128: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.57, 1.6),
        'beta': (
            1, 0.99, 0.975, 0.955, 0.92, 0.88, 0.825, 0.765, 0.7, 0.625, 0.545, 0.455, 0.37, 0.27, 0.175, 0.075, 0,
            -.025
        # extrapolated negative values at the end are needed to accurately interpolate theta impingement limit
        ),
    },
    16: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.445, 1.57),
        'beta': (
        0.9, 0.895, 0.88, 0.855, 0.82, 0.775, 0.72, 0.66, 0.585, 0.51, 0.42, 0.33, 0.24, 0.145, 0.045, 0, -0.14),
    },
    4: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.445),
        'beta': (0.805, 0.8, 0.78, 0.745, 0.7, 0.645, 0.57, 0.495, 0.41, 0.31, 0.21, 0.105, 0, -0.29),
    },
    2: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.995, 1.2),
        'beta': (0.675, 0.665, 0.645, 0.6, 0.55, 0.475, 0.395, 0.305, 0.205, 0.1, 0, -.22),
    },
    1: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.76, .995),
        'beta': (0.52, 0.51, 0.475, 0.42, 0.35, 0.265, 0.17, 0.065, 0, -.26),
    },
    0.5: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, .76),
        'beta': (0.355, 0.34, 0.285, 0.21, 0.115, 0, -.29),
    },
    0.25: {
        'theta': (0, 0.05, 0.1, 0.15, 0.2, 0.225, .5),
        'beta': (0.185, 0.175, 0.145, 0.09, 0.03, 0, -.32),
    },
}
k_1000_interps = {k: interp1d(d_1000[k]['theta'], d_1000[k]['beta'], kind='cubic') for k in d_1000}

d_10000 = {
    128: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.57),
        'beta': (
        1, 0.99, 0.975, 0.955, 0.92, 0.88, 0.825, 0.765, 0.7, 0.625, 0.545, 0.455, 0.37, 0.27, 0.175, 0.075, 0),
    },
    16: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.345, 1.57,),
        'beta': (0.88, 0.875, 0.86, 0.83, 0.785, 0.73, 0.675, 0.6, 0.52, 0.435, 0.34, 0.25, 0.15, 0.045, 0, -0.25,),
    },
    4: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.055, 1.345,),
        'beta': (0.71, 0.7, 0.68, 0.64, 0.585, 0.52, 0.445, 0.36, 0.26, 0.16, 0.06, 0, -0.3,),
    },
    2: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.835, 1.055,),
        'beta': (0.565, 0.555, 0.52, 0.48, 0.41, 0.33, 0.24, 0.14, 0.035, 0, -0.25,),
    },
    1: {
        'theta': (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.59, 0.835,),
        'beta': (0.41, 0.4, 0.36, 0.29, 0.21, 0.1, 0, -0.30,),
    },
    0.5: {
        'theta': (0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.39, 0.59,),
        'beta': (0.28, 0.275, 0.26, 0.235, 0.195, 0.15, 0.1, 0.045, 0, -0.25,),
    },
    0.25: {
        'theta': (0, 0.05, 0.1, 0.15, 0.165, 0.39,),
        'beta': (0.14, 0.125, 0.085, 0.02, 0, -0.30,),
    },
}
k_10000_interps = {k: interp1d(d_10000[k]['theta'], d_10000[k]['beta'], kind='cubic') for k in d_10000}


def interp_beta(theta, k):
    xs = []
    ys = []
    for k_ in d_1000.keys():
        k_interp = interp1d(d_1000[k_]['theta'], d_1000[k_]['beta']
                            , kind='cubic'
                            )
        xs.append(k_)
        theta_to_use = max(min(d_1000[k_]['theta']), theta)
        theta_to_use = min(max(d_1000[k_]['theta']), theta_to_use)
        ys.append(k_interp(theta_to_use))
    beta = interp1d(xs, ys)(k)
    return beta


def interp_beta_phi_1000(theta, k):
    xs = []
    ys = []
    for k_, k_interp in k_1000_interps.items():
        xs.append(log10(k_))
        theta_to_use = max(min(d_1000[k_]['theta']), theta)
        theta_to_use = min(max(d_1000[k_]['theta']), theta_to_use)
        ys.append(k_interp(theta_to_use))
    beta = interp1d(xs, ys, fill_value='extrapolate')(log10(k))
    return max(0, beta)


def interp_beta_phi_10000(theta, k):
    xs = []
    ys = []
    for k_, k_interp in k_10000_interps.items():
        xs.append(log10(k_))
        theta_to_use = max(min(d_10000[k_]['theta']), theta)
        theta_to_use = min(max(d_10000[k_]['theta']), theta_to_use)
        ys.append(k_interp(theta_to_use))
    beta = interp1d(xs, ys, fill_value='extrapolate')(log10(k))
    return max(0, beta)


def interp_beta_phi(phi, theta, k):
    xs = []
    ys = []
    for phi_, interp_beta_phi_ in zip((1000, 10000), (interp_beta_phi_1000, interp_beta_phi_10000)):
        xs.append(log10(phi_))
        # xs.append(phi_)
        ys.append(interp_beta_phi_(theta, k))
    beta = interp1d(xs, ys,
                    fill_value='extrapolate'
                    )(log10(phi))
    return max(0, beta)


mvd = 20
u = 90
p = 101325
tk = -10 + 273.15

mvd = 10  # from the appendix
lwc = 0.5  # from the appendix
time = 60  # from the appendix
tk = 273.15 - 20  # assumed to be cold enough to freeze all water
p = 101325  # assumed
mph = 2.5 * 100 / 1.5  # inferred from table in appendix, "2.5 mph" and "1.5%", results in 166 mph, which is "reasonable"
assumed_distribution = 'Langmuir C'  # inferred from table in appendix "Error due to using "C" distribution curves for unknown distribution"
ice_density = 800  # kg/m^3, inferred from "0.08 g/cm^3", assuming a 10% variation
u = mph * 0.44704

d_cylinder = 0.0254 * 6

k = langmuir_cylinder.calc_k(tk, u, mvd, d_cylinder)
phi = langmuir_cylinder.calc_phi(tk, p, u, d_cylinder)
print(k, phi)

print()
print(np.degrees(0.1))

plt.figure()
for k_ in d_1000:
    # plt.plot(d[k]['theta'][:-1], d[k]['beta'][:-1], 'o--', label=k)
    plt.plot(d_1000[k_]['theta'], d_1000[k_]['beta'], 'o--', label=k_)

thetas = np.linspace(0, 1.6, 100)
betas = [interp_beta_phi_1000(theta, k) for theta in thetas]
thetas, betas = trim_extra_x_y_zeros(thetas, betas)
plt.plot(thetas, betas, label=f'interpolated at k={k:.2f}')

thetas = np.linspace(0, 1.6, 1000)
# print('thetas')
# print(thetas)
betas_tree_rings = []
betas = [0] * len(thetas)
weighted_betas = []
for d_ratio, w in zip(langmuir_cylinder.langmuir_e_mids, langmuir_cylinder.langmuir_lwc_fractions):
    d_drop = mvd * d_ratio
    k_drop = langmuir_cylinder.calc_k(tk, u, d_drop, d_cylinder)
    # print(d_drop, k_drop)
    betas_k = [w * interp_beta_phi_10000(theta, k_drop) for theta in thetas]
    # print(betas_k)
    weighted_betas.append(betas_k)
    betas_tree_rings.append([b0 + b for b0, b in zip(betas, betas_k)])
    betas = [b0 + b for b0, b in zip(betas, betas_k)]

# print(betas)
# print(thetas)

thetas, betas = trim_extra_x_y_zeros(thetas, betas)
plt.plot(thetas, betas, label=f'interpolated Langmuir E at k={k:.2f}')

thetas = np.linspace(0, 1.6, 1000)
# print('thetas')
# print(thetas)
betas_tree_rings = []
betas = [0] * len(thetas)
weighted_betas = []
for d_ratio, w in zip(langmuir_cylinder.langmuir_e_mids, langmuir_cylinder.langmuir_lwc_fractions):
    d_drop = mvd * d_ratio
    k_drop = langmuir_cylinder.calc_k(tk, u, d_drop, d_cylinder)
    # print(d_drop, k_drop)
    betas_k = [w * interp_beta_phi(phi, theta, k_drop) for theta in thetas]
    # print(betas_k)
    weighted_betas.append(betas_k)
    betas_tree_rings.append([b0 + b for b0, b in zip(betas, betas_k)])
    betas = [b0 + b for b0, b in zip(betas, betas_k)]

# print(betas)
# print(thetas)

thetas, betas = trim_extra_x_y_zeros(thetas, betas)
plt.plot(thetas, betas, label=f'interpolated phi Langmuir E at k={k:.2f}')
#
#
#
# # print(betas)
# # print(thetas)
#
#
# for betas in betas_tree_rings:
#     thetas = np.linspace(0, 1.6, 1000)
#     thetas, betas = trim_extra_x_y_zeros(thetas, betas)
#     plt.plot(thetas, betas, '--',
#              # label='component'
#              )


# plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.show()
