from icinganalysis.NACA_TN_2904 import NACA_TN_2904_impingement
import matplotlib.pyplot as plt
from icinganalysis.air_properties import calc_pressure


plt.figure()
# NACA-TN-1393 Figure 5 values
altitude_ft = 10000
airspeed_mph = 200
t_deg_f = -15
tk = (469.59 + t_deg_f) / 1.8
p = calc_pressure(altitude_ft * 12 * 0.025)
u = airspeed_mph * 0.44704
d_cylinder = 3 * 0.0254

rate_upper_trace_icing = 1  # g/cm^2-hr
rate_upper_light_icing = 6  # g/cm^2-hr
rate_upper_moderate_icing = 12  # g/cm^2-hr
lwcs_trace = []
lwcs_light = []
lwcs_moderate = []
d_drops = list(range(5, 60 + 1))
for d_drop in d_drops:
    em = NACA_TN_2904_impingement.calc_em(
        tk, p, u, d_drop, d_cylinder
    )
    lwcs_trace.append(rate_upper_trace_icing * 100 ** 2 / 3600 / (em * u))
    lwcs_light.append(rate_upper_light_icing * 100 ** 2 / 3600 / (em * u))
    lwcs_moderate.append(rate_upper_moderate_icing * 100 ** 2 / 3600 / (em * u))

plt.plot(d_drops, lwcs_trace, label="Trace (1 g/cm^2-hr)")
plt.plot(d_drops, lwcs_light, label="Light (6 g/cm^2-hr)")
plt.plot(d_drops, lwcs_moderate, label="Moderate (12 g/cm^2-hr)")

plt.xlim(0, 60)
plt.xlabel("Mean Effective Drop Diameter, micrometer")
plt.ylim(0, 2.2)
plt.yticks((0, 0.5, 1.0, 1.5, 2))
plt.ylabel("Liquid Water Content, g/m^3")

plt.legend(loc="upper left")
plt.savefig("naca-tn-1393_figure_5_comparison.png", transparent=True)

plt.show()
