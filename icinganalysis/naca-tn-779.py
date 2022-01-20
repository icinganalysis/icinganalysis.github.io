"""
reference:
Kantrowitz, Arthur,
“Aerodynamic Heating and Deflection of Drops by an Obstacle in an Airstream in Relation to Aircraft Icing”,
NACA-TN-779, 1940.

Units:
tk: temperature, K
p: air static pressure, Pa (N/m^2)
u: air speed, m/s
d_cylinder: cylinder diameter, m
d_drop: water drop diameter, micrometer (1e-6 m)
altitude: pressure altitude, m
"""
from math import log10
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from icinganalysis import langmuir_cylinder
from icinganalysis.air_properties import calc_altitude

# NACA-TN-779
d_cylinder = 12 * 0.0254
u = 200 * 0.44704
tk = -10 + 273.15

d_inch = 0.0007, .001, .002, .004, 0.006, .01, 0.04
d_micrometer = [_ * 0.0254 * 1000000 for _ in d_inch]
em_points = 0.075, 0.2, .52, .78, .86, .92, .99  # fig. 4
ems_table_iv = 0.25, 0.445, 0.76, 0.928, 0.966, 0.987, 0.999

ks_points = []
for dm in d_micrometer:
    k = langmuir_cylinder.calc_k(tk, u, dm, d_cylinder)
    ks_points.append(k)

plt.figure(figsize=(7, 6))
line0, = plt.plot(ks_points, em_points, 'o', c='g', label='NACA-TN-779 Figure 4 points')

d_drops_micrometer = [10 ** _ for _ in plt.np.arange(log10(8), log10(4000), (log10(4000) - log10(8)) / 100)]

phi_target = 0.1  # use as an approximation for phi=0
p = minimize_scalar(
    lambda _: abs(langmuir_cylinder.calc_phi(tk, _, u, d_cylinder) - phi_target)
).x
altitude = calc_altitude(p)
phi = langmuir_cylinder.calc_phi(tk, p, u, d_cylinder)
print(f"For φ={phi:.0f}, p={p:.0f}, altitude={altitude:.0f}")
ems = [langmuir_cylinder.calc_em(tk, p, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
ks = [langmuir_cylinder.calc_k(tk, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
line, = plt.plot(ks, ems, label=f'Calculated φ={phi:.0f}')
plt.plot(ks_points, ems_table_iv, 's', c=line.get_color(), label='Table IV(a) D.A. points')

phi_target = 6000
p = minimize_scalar(
    lambda _: abs(langmuir_cylinder.calc_phi(tk, _, u, d_cylinder) - phi_target)
).x
altitude = calc_altitude(p)
phi = langmuir_cylinder.calc_phi(tk, p, u, d_cylinder)
print(f"For φ={phi:.0f}, p={p:.0f}, altitude={altitude:.0f}")
ems = [langmuir_cylinder.calc_em(tk, p, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
ks = [langmuir_cylinder.calc_k(tk, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
line, = plt.plot(ks, ems, c=line0.get_color(), label=f'Calculated φ={phi:.0f}, altitude={altitude:.0f} m')
ems = [langmuir_cylinder.calc_em(tk, p, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
plt.plot(ks_points, ems, 's', fillstyle='none', c=line.get_color(), ms=12, label=f'Revised points at φ={phi:.0f}')
# for x, y, s in zip(ks_points, ems, [f"{_:.3f}" for _ in ems]):
#     plt.text(x, y, s, verticalalignment='top')

phi_target = 16000
p = minimize_scalar(
    lambda _: abs(langmuir_cylinder.calc_phi(tk, _, u, d_cylinder) - phi_target)
).x
altitude = calc_altitude(p)
phi = langmuir_cylinder.calc_phi(tk, p, u, d_cylinder)
print(f"For φ={phi:.0f}, p={p:.0f}, altitude={altitude:.0f}")
ems = [langmuir_cylinder.calc_em(tk, p, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
ks = [langmuir_cylinder.calc_k(tk, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
line, = plt.plot(ks, ems, c='r', label=f'Calculated φ={phi:.0f}, altitude={altitude:.0f} m')
plt.plot(ks_points, ems, 's', fillstyle='none', c=line.get_color(), label=f'Revised points at φ={phi:.0f}')
ems = [langmuir_cylinder.calc_em(tk, p, u, d_drop_m, d_cylinder) for d_drop_m in d_micrometer]
for x, y, s in zip(ks_points, ems, [f"{_:.3f}" for _ in ems]):
    plt.text(x, y, s, verticalalignment='top')

plt.legend()
plt.xscale('log')
plt.xlim(.1)
plt.ylim(0, 1)
plt.xlabel('K')
plt.ylabel('Em')
plt.savefig('comparison_to_NACA-TN-779.png')
plt.show()
