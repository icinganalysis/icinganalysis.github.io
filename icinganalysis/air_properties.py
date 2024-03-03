"""
reference:
Langmuir, Irving, and Blodgett, Katherine B.: A Mathematical Investigation of Water Droplet Trajectories.
Tech. Rep. No. 5418, Air Materiel Command, AAF, Feb. 19, 1946. (Contract No. W-33-038-ac-9151 with General Electric Co.)

Units:
tk: free-stream static temperature, K
p: air static pressure, Pa (N/m^2)
u: free-stream air speed, m/s
d_cylinder: cylinder diameter, m
d_drop: water drop diameter, micrometer (1e-6 m)
altitude: pressure altitude, m
"""
CP_AIR = 1000  # J/kg-K
SPECIFIC_HEAT_AIR = 1000  # J/kg-K
GAMMA_AIR = 1.401
R_AIR = 287.05  # J/kg-K
MOLECULAR_MASS = 0.0289647  # kg/mol
P_std = 101325  # Pa
TK_std = 288.15  # K


def calc_air_thermal_conductivity(tk):
    return -0.0147486 + 0.00235815 * tk ** 0.5  # A.3, translated to SI W/m-K (J/s-m-K)


def calc_prandtl(tk):
    return CP_AIR * calc_air_viscosity(tk) / calc_air_thermal_conductivity(tk)


def calc_air_viscosity(tk):
    """
    Calculate the dynamic viscosity of air
    :param tk: temperature, K
    :return: dynamic viscosity of air, Pa-s (N-s/m^2)
    """
    return 2.48e-7 * tk ** 0.7542  # equ. (13)


def calc_air_density(tk, p):
    return 0.3484 / 100 * p / tk  # equ. (15)


def calc_pressure(altitude):
    p = P_std * (1 - 2.25577e-5 * altitude) ** 5.25588
    return p


def calc_altitude(pressure):
    return (1 - (pressure / P_std) ** (1 / 5.25588)) / 2.25577e-5
