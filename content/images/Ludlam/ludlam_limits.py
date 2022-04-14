from icinganalysis import try_wet_lift
from icinganalysis import NACA_TR_1215_find_critical_line
from icinganalysis.units_helpers import INCH_PER_M, tc_to_k, tk_to_c, G_PER_KG
from icinganalysis.ludlam import eq6
from icinganalysis.ludlam3 import calc_lwc_critical
from icinganalysis.langmuir_cylinder_values import calc_re
from icinganalysis.water_properties import ICE_BULK_DENSITY

KNOTS_PER_MS = 1.9438444924406
MM_PER_M = 1000
S_PER_MINUTE = 60

# DOT/FAA-00/30 Figure 22b
d = 0.25 / INCH_PER_M
v_knots = 90
u = v_knots / KNOTS_PER_MS
print(u, v_knots)
e = 0.9
p = 80000
vs = []
for tc, mm_m_jeck, lwc_mazin in zip((-5, -10, -15), (0.59, 1.34, 2.08), (.4, .8, 1.25)):
    thick_rate = mm_m_jeck / S_PER_MINUTE / MM_PER_M
    rho_ice = ICE_BULK_DENSITY
    mass_per_m2 = thick_rate * rho_ice
    lwc_jeck = mass_per_m2 / u * G_PER_KG

    print(tc, calc_re(tc + 273.15, p, u, d))
    tk = tc_to_k(tc)
    lwc = try_wet_lift.calc(tk, p, u, d, e)
    h = NACA_TR_1215_find_critical_line.calc_hc_cyl(tk, p, u, d)
    lwctr = NACA_TR_1215_find_critical_line.find_critical_lwc_em_freeze(tk, p, u, h)
    rey = try_wet_lift.calc_reynolds(tk, p, u, d)
    l = eq6(tc, p / 100, d, rey) / u / 1000
    l3 = calc_lwc_critical(tk, p, u, d, e)
    vs.append((tc, lwc, lwc_jeck, lwctr, lwc_mazin, l, l3))
    print(tc, lwc, lwc_jeck, lwctr, lwc_mazin, l, l3)

tc, lwc, lwc_jeck, lwctr, lwc_mazin, l, l3 = zip(*vs)
import matplotlib.pyplot as plt

plt.figure()
plt.suptitle('100 knots (46 m/s), p=80000 Pa, diameter=0.25 inch (0.00635 m')
plt.plot(tc, l3, label='calculated Ludlam (rotating)')
# plt.plot(tc, lwc, label='Ludlam (rotating)')
plt.plot(tc, lwc_jeck, '--', label='Jeck (Ludlam) (non-rotating)')
plt.xlim(-15, 0)
plt.xticks(range(-15, 0 + 5, 5))
plt.xlabel("T_static, C")
plt.ylim(0)
plt.legend()
plt.ylabel('LWC_critical, g/m^3')

plt.figure()
plt.suptitle('100 knots (46 m/s), p=80000 Pa, diameter=0.25 inch (0.00635 m')
plt.plot(tc, lwctr, label='NACA-TR-1215 (rotating)')
plt.plot(tc, l3, label='calculated Ludlam (rotating)')
# plt.plot(tc, lwc, label='Ludlam (rotating)')
plt.plot(tc, lwc_mazin, '--', label='Mazin (non-rotating)')
plt.plot(tc, lwc_jeck, '-.', label='Jeck (Ludlam) (non-rotating)')
plt.xlim(-15, 0)
plt.xticks(range(-15, 0 + 5, 5))
plt.xlabel("T_static, C")
plt.ylim(0)
plt.legend()
plt.ylabel('LWC_critical, g/m^3')

v_knots = 150
u = v_knots / KNOTS_PER_MS
print(u, v_knots)
e = 0.9
p = 80000
vs = []
for tc, mm_m_jeck, lwc_mazin in zip((-5, -10, -15), (0.76, 1.62, 2.59), (.25, .6, 0.9)):
    thick_rate = mm_m_jeck / S_PER_MINUTE / MM_PER_M
    rho_ice = ICE_BULK_DENSITY
    mass_per_m2 = thick_rate * rho_ice
    lwc_jeck = mass_per_m2 / u * G_PER_KG

    print(tc, calc_re(tc + 273.15, p, u, d))
    tk = tc_to_k(tc)
    lwc = try_wet_lift.calc(tk, p, u, d, e)
    h = NACA_TR_1215_find_critical_line.calc_hc_cyl(tk, p, u, d)
    lwctr = NACA_TR_1215_find_critical_line.find_critical_lwc_em_freeze(tk, p, u, h)
    rey = try_wet_lift.calc_reynolds(tk, p, u, d)
    l = eq6(tc, p / 100, d, rey) / u / 1000
    l3 = calc_lwc_critical(tk, p, u, d, e)
    vs.append((tc, lwc, lwc_jeck, lwctr, lwc_mazin, l, l3))
    print(tc, lwc, lwc_jeck, lwctr, lwc_mazin, l, l3)

tc, lwc, lwc_jeck, lwctr, lwc_mazin, l, l3 = zip(*vs)

plt.figure()
plt.suptitle('150 knots (77 m/s), p=80000 Pa, diameter=0.25 inch (0.00635 m')
plt.plot(tc, lwctr, label='calculated (NACA-TR-1215) (rotating)')
plt.plot(tc, l3, label='calculated Ludlam (rotating)')
plt.plot(tc, lwc_mazin, '--', label='Mazin (non-rotating)')
plt.plot(tc, lwc_jeck, '-.', label='Jeck (Ludlam) (non-rotating)')

plt.plot(tc, (.65, 1.3, 1.9), ':', label="Ludlam Figure 1 (90 m/s, 73000 to 60000 Pa, 0.0035 m)")

plt.xlim(-15, 0)
plt.xticks(range(-15, 0 + 5, 5))
plt.xlabel("T_static, C")
plt.ylim(0, 2.5)
plt.ylabel('LWC_critical, g/m^3')
plt.legend()
plt.savefig('ludlam_comparisons_all.png')

plt.figure()
plt.suptitle('150 knots (77 m/s), p=80000 Pa, diameter=0.25 inch (0.00635 m')
plt.plot(tc, l3, label='calculated Ludlam (rotating)')
plt.plot(tc, lwc_jeck, '-.', label='Jeck (Ludlam) (non-rotating)')

plt.plot(tc, (.65, 1.3, 1.9), ':', label="Ludlam Figure 1 (90 m/s, 73000 to 60000 Pa, 0.0035 m)")

plt.xlim(-15, 0)
plt.xticks(range(-15, 0 + 5, 5))
plt.xlabel("T_static, C")
plt.ylim(0, 2.5)
plt.ylabel('LWC_critical, g/m^3')
plt.legend()
plt.savefig('ludlam_comparisons.png')

plt.show()
