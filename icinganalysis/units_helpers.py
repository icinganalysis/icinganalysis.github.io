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


BTU_PER_J = 1/1055.0558526  # IT BTU
BTU_H_PER_W = 3.412141633  # IT BTU
BTU_H_FT2_F_PER_W_M2_K = 0.17611018367570236  # IT BTU
F_PER_K = 1.8
FT_PER_M = 3.280839895013124
FT2_PER_M2 = 10.763910416709725
G_PER_KG = 1000
HOUR_PER_S = 0.0002777777777777778
INCH_PER_M = 39.37007874
KNOTS_PER_MS = 1.9438444924406
LBM_PER_KG = 2.2046226218
M_PER_FT = 0.3048
MICROMETERS_PER_METER = 1000000
MM_HG_PER_PA = 0.00750063755  # pressure in mm of mercury per Pa
MPH_PER_M_S = 2.236936292054403
S_PER_HOUR = 3600
S_PER_MINUTE = 60
T_0C_K = 273.15  # 0C in K, also the melting point of ice at standard pressure
T_0F_R = 459.67  # 0F in R
PSI_PER_PA = 1.450377319e-4
LBF_PER_N = 4.4482216153


def tf_to_k(tf):
    return (tf + T_0F_R) / F_PER_K


def tk_to_f(tk):
    return tk * F_PER_K - T_0F_R


def tc_to_k(tc):
    return tc + T_0C_K


def tc_to_f(tc):
    return F_PER_K * tc + 32


def tk_to_c(tk):
    return tk - T_0C_K


def ms_to_mph(ms):
    return ms * MPH_PER_M_S


def mph_to_ms(mph):
    return mph / MPH_PER_M_S


def m_to_cm(m):
    return m * 100


def cm_to_m(cm):
    return cm / 100


def m_to_inch(m):
    return m * INCH_PER_M


def inch_to_m(inch):
    return inch / INCH_PER_M


def r_to_k(r):
    return r / 1.8


def k_to_r(k):
    return k * 1.8


def percent_to_fraction(percent):
    return percent / 100


def fraction_to_percent(fraction):
    return fraction * 100


def dyne_cm_to_n_m(dyne_cm):
    return dyne_cm * 1e-5 * 100


def n_m_to_dyne_cm(n_m):
    return n_m / 1e-5 / 100


def n_m_to_lbf_ft(n_m):
    return n_m * LBF_PER_N / FT_PER_M


def lbf_ft_to_n_m(lbf_ft):
    return lbf_ft / LBF_PER_N * FT_PER_M


def psi_to_pa(psi):
    return psi / PSI_PER_PA


def pa_to_psi(pa):
    return pa * PSI_PER_PA


def no_conversion(v):
    return v


conversions_to_domain_units = {
    "cm": m_to_cm,
    "inch": m_to_inch,
    "C": tk_to_c,
    "°C": tk_to_c,
    "F": tk_to_f,
    "°F": tk_to_f,
    "mph": ms_to_mph,
    "MPH": ms_to_mph,
    "R": k_to_r,
    "°R": k_to_r,
    "dyne/cm": n_m_to_dyne_cm,
    "lbf/ft": n_m_to_lbf_ft,
    "psi": pa_to_psi,
    "": no_conversion
}


def convert_to_domain_unit(v, domain_unit):
    return conversions_to_domain_units.get(domain_unit, no_conversion)(v)


