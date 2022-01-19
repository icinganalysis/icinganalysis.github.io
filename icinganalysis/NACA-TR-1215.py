from math import pi
from icinganalysis.ludlam import calc_vapor_p, L_EVAPORATION, L_FREEZING, calc_air_thermal_conductivity
from icinganalysis.langmuir_cylinder import calc_re, calc_pressure, calc_em
import matplotlib.pyplot as plt

cp_air = 1000
cp_water = 4220
r = 0.75


def calc_lwc_em_from(tk, p, u, h, ts=273.15, r=0.75, u1=None):
    return (pi * h) * (
        (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r))) +
        .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    ) / (cp_water * (ts - tk) + u ** 2 / 2) / u * 1000


def calc_water_freeze_rate(tk, p, u, h, ts=273.15, r=0.75, u1=None):
    if u1 is None:
        u1 = u
    # q_conv = pi * h * (ts - tk - r * u ** 2 / 2 / cp_air)
    # # q_conv = pi * h * (ts - tk)
    # q_evap = pi * h * .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    # q_sensible = em * lwc / 1000 * u * cp_water * (ts - tk)
    # q_kinetic = em * lwc / 1000 * u * u ** 2 / 2
    # qf = q_conv + q_evap + q_sensible - q_kinetic
    # wf = qf / L_FREEZING
    # we = q_evap / L_EVAPORATION
    # wc = wf + we
    # lwc_f = (wf + we) / (em * u) * 1000
    # lwc_f = (
    #             (q_conv + q_evap + q_sensible - q_kinetic) / L_FREEZING
    #             + (pi * h * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)
    #         ) / (em * u) * 1000
    # lwc_f = (
    #             (
    #                 pi * h * (ts - tk - r * u ** 2 / 2 / cp_air)
    #                 + pi * h * .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    #                 + em * lwc / 1000 * u * cp_water * (ts - tk)
    #                 - em * lwc / 1000 * u * u ** 2 / 2
    #             ) / L_FREEZING
    #             + (pi * h * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)
    #         ) / (em * u) * 1000
    # lwc_f = (
    #             (
    #                 pi * h * (ts - tk - r * u ** 2 / 2 / cp_air)
    #                 + pi * h * .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    #                 + em * lwc / 1000 * u * cp_water * (ts - tk)
    #                 - em * lwc / 1000 * u * u ** 2 / 2
    #             ) / L_FREEZING
    #             + (pi * h * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)
    #         ) / (em * u) * 1000
    # lwc * em * u / 1000 = (
    #     em * u * lwc / 1000 / L_FREEZING *(cp_water * (ts - tk) - u * u ** 2 / 2)
    #     + pi * h / L_FREEZING * (
    #         ts - tk - r * u ** 2 / 2 / cp_air
    #         +(L_EVAPORATION+L_FREEZING) * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    #     )
    # lwc_ em  = (
    #     lwc_em_  / L_FREEZING *(cp_water * (ts - tk) - u * u ** 2 / 2)
    #     + pi * h / L_FREEZING / u *1000 * (
    #         ts - tk - r * u ** 2 / 2 / cp_air
    #         +(L_EVAPORATION+L_FREEZING) * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    #     )
    #
    # )
    lwc_em = (
        pi * h / L_FREEZING / u * (
        ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r))
        + (L_EVAPORATION + L_FREEZING) * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    ) / (
            1 - (cp_water * (ts - tk) - u * u ** 2 / 2) / L_FREEZING
        )
    )
    return lwc_em * 1000


def calc_qf(tk, p, u, lwc, em, h, ts=273.15, r=0.75, u1=None):
    if u1 is None:
        u1 = u
    q_conv = pi * h * (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r)))
    q_evap = pi * h * .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
    q_sensible = em * lwc / 1000 * u * cp_water * (ts - tk)
    q_kinetic = em * lwc / 1000 * u * u ** 2 / 2
    qf = q_conv + q_evap + q_sensible - q_kinetic
    print()
    print('    ', q_conv)
    print('    ', q_evap)
    print('    ', q_sensible)
    print('    ', q_kinetic)
    print('    ', qf)
    print('    mf', qf/L_FREEZING)
    print('    me', q_evap/L_EVAPORATION)
    print('   em_lwcf', qf/L_FREEZING*1000/u)
    print('    ', em * lwc / 1000 * u)
    print('    ', em * lwc / 1000 * u*L_FREEZING)
    print('    ', em * lwc)
    print()

    return qf


u = 90
c = 0.05
d_cyl = 2 * c
p = 101325

tk = -10 + 273.15
u1 = 1
ts = 273.15

h = 200
r = .75

q1 = 2 * pi * c * h * (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r)))  # F3
print(q1)

# q2 =

we = 2 * pi * c * h / cp_air * 0.622 * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
print(we)

wf_e = (pi * h / u1
        * (
            (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r)))
            + (.622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p) * (L_EVAPORATION - u ** 2 / 2)
        )
        / (L_FREEZING + u ** 2 / 2)
        )  # F10

we_e = (h * pi / u1 * .622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)  # F11

lambda_freeze = (cp_water * (ts - tk) - u ** 2 / 2) / L_FREEZING

for dt in range(0, -10, -1):
    tk = 273.15 + dt
    print(dt, (cp_water * (ts - tk) - u ** 2 / 2) / L_FREEZING, dt / 80)

# NACA-TR-1215 Figure 24a, NACA-TN-1424 Run 20
tf = 23  # 20 1/29/47
mph = 168
alt_ft = 8270
p = calc_pressure(alt_ft * 12 * .0254)
print('p', p)
u = mph * .44704
u1 = u
tk = (tf + 459.67) / 1.8
lwc = 0.2
mvd = 12
d_cyl = 1 * 0.0254
re = calc_re(tk, p, u, d_cyl)
nu = 0.082 * re ** .747
h = nu * calc_air_thermal_conductivity(tk) / d_cyl
print(tk)
print('h', h)

em = calc_em(tk, p, u, mvd, d_cyl)
print('em', em)

lwc_em = calc_water_freeze_rate(tk, p, u, h)
print('calc_water_freeze_rate', lwc_em)
print(lwc_em*u/1000*L_FREEZING)
qf = calc_qf(tk, p, u, lwc_em, 1, h)
print(qf)
print(qf/L_FREEZING)

print()
lwc_em = 9
print(lwc_em)
print(lwc_em*u/1000*L_FREEZING)
qf = calc_qf(tk, p, u, lwc_em, 1, h)
print(qf)
print(qf/L_FREEZING)



raise ValueError


# tf = 10  # 34 1/29/47
# mph = 215
# alt_ft = 7400
# p=calc_pressure(alt_ft*12*.0254)


d_cyl = 1 * 0.0254
re = calc_re(tk, p, u, d_cyl)
nu = 0.082 * re ** .747
h = nu * calc_air_thermal_conductivity(tk) / d_cyl
print('h', h)
lambda_freeze = (cp_water * (ts - tk) - u ** 2 / 2) / L_FREEZING
print(lambda_freeze)

wf_e = (pi * h / u1
        * (
            (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r)))
            + (.622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p) * (cp_water * (ts - tk) - u ** 2 / 2)
        )
        / (L_FREEZING + u ** 2 / 2)
        )  # F10
print(wf_e * 1000)

wf_e = (pi * h / u1
        * (
            (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r)))
            + (.622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p) * (L_EVAPORATION - u ** 2 / 2)
        )
        / (L_FREEZING + u ** 2 / 2)
        )  # F10
print()
print(wf_e * 1000)
print()
print((ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r))))
print((ts - tk))
print((.622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p))
print((.622 / cp_air * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p) * L_EVAPORATION)
print(pi * h / u1)
print(L_FREEZING + u ** 2 / 2)

wf_e = (pi * h / u1
        * (
            (ts - tk - u ** 2 / 2 / cp_air * (1 - u1 ** 2 / u ** 2 * (1 - r)))
        )
        / (L_FREEZING + u ** 2 / 2)
        )  # F10
print()
print(wf_e * 1000)

em = 1

q_conv = pi * h * (ts - tk - u ** 2 / 2 / cp_air)
q_evap = pi * h * .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
q_sensible = em * lwc * u * cp_water * (ts - tk)
q_kinetic = em * lwc * u * u ** 2 / 2

em_lwc = (pi * h) * (
    (ts - tk - u ** 2 / 2 / cp_air) +
    .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p
) / (cp_water * (ts - tk) + u ** 2 / 2) / u * 1000

qf = q_conv + q_evap + q_sensible - q_kinetic
qf = pi * h * (ts - tk - u ** 2 / 2 / cp_air) + (pi * h) * .622 / cp_air * L_EVAPORATION * (
        calc_vapor_p(ts) - calc_vapor_p(tk)) / p + em * lwc * cp_water * (ts - tk) - em * lwc * u ** 2 / 2

a = 1

qf = ((pi * h) * (
        ts - tk - r * u ** 2 / 2 / cp_air + .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)
      + em * lwc / 1000 * u * (cp_water * (ts - tk) - u ** 2 / 2)
      )
wf = qf / L_FREEZING
lwc_em_wf = wf / u * 1000
print('lwc_em_wf', lwc_em_wf)
lwc_em_wf = 1000 / u / L_FREEZING * ((pi * h) * (
        ts - tk - u ** 2 / 2 / cp_air + .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)
                                     + em * lwc * (cp_water * (ts - tk) - u ** 2 / 2)
                                     )
print('lwc_em_wf', lwc_em_wf)
lwc_em_wf = (1000 / u / L_FREEZING * ((pi * h) * (
        ts - tk - u ** 2 / 2 / cp_air + .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)) /
             (1 - 1000 / u / L_FREEZING * (cp_water * (ts - tk) - u ** 2 / 2)))
print('lwc_em_wf', lwc_em_wf)
lwc_em_wf = (1000 / u / L_FREEZING * ((pi * h) * (
        ts - tk - u ** 2 / 2 / cp_air + .622 / cp_air * L_EVAPORATION * (calc_vapor_p(ts) - calc_vapor_p(tk)) / p)) /
             (1 / u * L_FREEZING * (cp_water * (ts - tk) - u ** 2 / 2)))
print('lwc_em_wf', lwc_em_wf)
print()
print(q_conv)
print(q_evap)
print(q_sensible)
print(q_kinetic)
print()
qf = q_conv + q_evap + q_sensible - q_kinetic
print(qf)
wf = qf / L_FREEZING
print(wf)
lwc = wf / u * 1000
print(lwc)
print(em_lwc)
print('calc_lwc_em_from', calc_lwc_em_from(tk, p, u, h))

"""

wf + we = wc
lwc*em*u = qf/Lf + qe/Le
qf = (wc-qe/Le)/Lf


"""

# NACA-TN-2306 Flight 19, run 2
mph = 200
alt_ft = 2700
tf = 26
p = calc_pressure(alt_ft * 12 * .0254)
print('p', p)
u = mph * .44704
u1 = u
tk = (tf + 459.67) / 1.8
d_cyl = 1 * 0.0254
re = calc_re(tk, p, u, d_cyl)
nu = 0.082 * re ** .747
h = nu * calc_air_thermal_conductivity(tk) / d_cyl
print('h', h)
print(calc_lwc_em_from(tk, p, u, h))
print(calc_water_freeze_rate(tk, p, u, 1, 1, h))
print()

import numpy as np

print(tk, p, u, h)
em = 1
lwc = 0.5
for tk in np.linspace(271.15, 272.15, 21):
    qf = calc_qf(tk, p, u, lwc, em, h)
    lwc_ = qf / L_FREEZING / u * 1000
    print(f"{tk:.2f}, {lwc:3f}, {lwc_:3f}, {qf}")
print()
tk = 271.15
tk = (tf + 459.67) / 1.8
em = 0.25
for lwc in np.linspace(2., 3., 20):
    qf = calc_qf(tk, p, u, lwc, em, h)
    lwc_ = qf / L_FREEZING / u * 1000
    print(f"{tk:.2f}, {lwc:3f}, {lwc_:3f}, {qf}")
