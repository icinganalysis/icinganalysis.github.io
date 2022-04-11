"""
Units conversion helpers

Preferred units (primary SI units):
mass: kg
force: N
length: m
tk: temperature, K
time: seconds, s
p: air static pressure, Pa (N/m^2)
u: free-stream air speed, m/s
altitude: pressure altitude, m

Icing specific, entrenched exceptions:
d_drop: water drop diameter, micrometer (1e-6 m)
lwc: liquid water content, g/m^3

"Domain specific" units are units other than the preferred units.
For example, in the NACA reports air speeds are typically in mph (miles per hour).

It is recommended to convert from domain specific units (such as mph) as soon as input:
    u = 180 / MPH_PER_M_S  # for 180 mph

If values are to be reported out in domain specific units, convert as late as possible:
    print(f"Speed = {u * MPH_PER_M_S} mph")

Constant naming convention: domain specific unit per preferred unit.
A few common units will break the convention, such as S_PER_HOUR = 3600.
Constants names are terse, so there may be some ambiguity, for example,
MPH_PER_M_S is mile per hour per m/s, not mile per hour per m-s.

Special purpose conversions, such as one non-standard unit to another, are not included here.
One may define them in the file where they are used, such as:
    FT_S_PER_MPH = 1.466667

Note: there is more than one definition for "BTU", the IT definition is used herein
https://en.wikipedia.org/wiki/British_thermal_unit

A note about mass and force:

    To keep unit consistency in Newton's second law, a unit constant "gc" is introduced.

    Force = mass * acceleration / gc

    In SI units gc = 1 kg-m/(N-s^2)

    N = kg * m/s^2  / (kg-m/N-s^2) = N

    As the value is 1, gc might not be explicitly be included in calculations in SI units,
    but it is always implicitly there.

    In "US customary" units, gc = 32.174 lbm-ft/(lbf-s^2).
    It must be explicitly included in any calculation involving force, mass and acceleration.
    The archaic mass unit "slug" was sometimes used (1 slug = 32.174 lbm) to help "alleviate" this.
         gc = 1 slug-ft/lbf-s^2
    However, I have seen many errors of a factor of 32.174, when either slugs or lbm were used.

    (see an excellent discussion about gc in "Fundamentals of Classical Thermodynamics",
    Van Wylen and Sonntag, Second Edition, John Wiley and Sons, 1973.)

"""


BTU_PER_J = 1055.0558526  # IT BTU
BTU_H_PER_W = 3.412141633  # IT BTU
BTU_H_FT2_F_PER_W_M2_K = 0.17611018367570236  # IT BTU
F_PER_K = 1.8
FT_PER_M = 3.280839895013124
FT2_PER_M2 = 10.763910416709725
G_PER_KG = 1000
HOUR_PER_S = 0.0002777777777777778
INCH_PER_M = 39.37007874
LBM_PER_KG = 2.2046226218
M_PER_FT = 0.3048
MICROMETERS_PER_METER = 1000000
MM_HG_PER_PA = 0.00750063755  # pressure in mm of mercury per Pa
MPH_PER_M_S = 2.236936292054403
S_PER_HOUR = 3600
T_0C_K = 273.15  # 0C in K, also the melting point of ice at standard pressure
T_0F_R = 459.67  # 0F in R


def tf_to_k(tf):
    return (tf + T_0F_R) / F_PER_K


def tk_to_f(tk):
    return tk * F_PER_K - T_0F_R

