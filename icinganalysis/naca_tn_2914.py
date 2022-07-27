from icinganalysis.units_helpers import FT_PER_M
from icinganalysis.water_properties import (
    calc_vapor_p,
    L_EVAPORATION,
    RATIO_MOLECULAR_WEIGHTS,
)
from icinganalysis.air_properties import CP_AIR, calc_altitude, calc_pressure
from icinganalysis.iteration_helpers import solve_minimize_f
from icinganalysis.markdown_table_helper import make_nice_width_markdown_table

INCH_HG_PER_PA = 0.00029529980164712

mach = 1.36

# fmt: off
_d_front = (  # NACA-TN-2861, page 9
    9.13, 404, 403,
    9.76, 406, 401,
)
# fmt: on
ps_front = [_ / INCH_HG_PER_PA for _ in _d_front[::3]]
ts_expirement_front_r = _d_front[1::3]
ts_analytical_front_r = _d_front[2::3]

# fmt: off
_d_back = (  # NACA-TN-2861, page 9
    9.41, 422, 422,
    9.91, 418, 422,
    3.91, float('nan'), 447,
)
# fmt: on
ps_back = [_ / INCH_HG_PER_PA for _ in _d_back[::3]]
ts_expirement_back_r = _d_back[1::3]
ts_analytical_back_r = _d_back[2::3]


def calc_pressure_coefficient(mach, pl_p):
    return (pl_p - 1) / (0.7 * mach ** 2)


def calc_pressure_coefficient_from(mach, vl_vo):
    pl_po = (-((vl_vo * mach / 2.236) ** 2 - 1 - 0.2 * mach ** 2)) ** (1 / 0.286)
    cp = calc_pressure_coefficient(mach, pl_po)
    return cp


def calc_t(p, mach, pressure_coefficient, r=0.85, rh=1):
    t_freeze = 273.15
    pl = p * (1 + 0.7 * mach ** 2 * pressure_coefficient)
    es = calc_vapor_p(t_freeze)
    if pl <= es:
        return float("nan")
    tl_toc_mach = (1 + 0.2 * mach ** 2) * r + (1 - r) * (pl / p) ** 0.286

    def calc_t_diff(tk):
        eo = rh*calc_vapor_p(tk)
        if p <= eo:
            return float("nan")
        dt = (
            tk * tl_toc_mach
            - t_freeze
            - 1
            * RATIO_MOLECULAR_WEIGHTS
            / CP_AIR
            * L_EVAPORATION
            * (es / (pl - es) - eo / (p - eo))
        )
        return abs(dt)

    tk = solve_minimize_f(calc_t_diff, [213.15, 293.15])

    return tk


def calc_min_cp(mach):
    """cp value where pl = 0"""
    return -1 / (0.7 * mach ** 2)


def calc_cp_for_t_ambient_0c(p, mach, r=0.85, rh=1):
    def calc_diff(cp):
        return abs(273.15 - calc_t(p, mach, cp, r, rh=rh))

    cp_min = calc_min_cp(mach)  # cp_min: cp value where pl = 0
    cp = solve_minimize_f(
        calc_diff, [cp_min + 0.1, 1]  # need a little tolerance above cp_min
    )
    return cp


# fmt: off
d_p10_table_1 = (  # mach, pl/p, tl_toc_mach term, toc_rankine, NACA-TN-2914
    0.4, 0.97, 1.028, 486.6,
    0.5, 0.95, 1.041, 483.8,
    0.6, 0.929, 1.059, 480,
    0.7, 0.902, 1.079, 475.6,
)
# fmt: on
machs_table_1 = d_p10_table_1[::4]
pl_ps_table_1 = d_p10_table_1[1::4]
tl_terms_table_1 = d_p10_table_1[2::4]
toc_rankines_table_1 = d_p10_table_1[3::4]

# fmt: off
d_p10_table_2 = (  # mach, pl/p, tl_toc_mach term, toc_rankine, NACA-TN-2914
    0.848, -0.355, 0.820, 460, 472.5, 484,
    0.935, -0.330, 0.789, 452, 466.5, 481.5,
    1.11, -0.045, 0.961, 423.5, 440, 464,
)
# fmt: on

if __name__ == "__main__":

    mach = 1.36
    print()
    for p, ts, cp in zip(ps_front, ts_analytical_front_r, (0.205, 0.225)):
        tk = calc_t(p, mach, cp)
        print(p, calc_altitude(p) * FT_PER_M, ts, tk * 1.8)

    print()
    for p, ts, cp in zip(ps_back, ts_analytical_back_r, (-0.096, -0.125, 0.15)):
        tk = calc_t(p, mach, cp)
        print(p, calc_altitude(p) * FT_PER_M, ts, tk * 1.8)
    print()

    p = calc_pressure(15000 / FT_PER_M)
    vl_vo = 1.139
    d = []
    for mach, pl_p, tl_term, t_rankine in zip(
        machs_table_1, pl_ps_table_1, tl_terms_table_1, toc_rankines_table_1
    ):
        cp = calc_pressure_coefficient_from(mach, vl_vo)
        pl_p_calc = 1 + 0.7 * mach ** 2 * cp
        tk = calc_t(p, mach, cp, r=0.85)
        print(mach, cp, (1 + 0.7 * mach ** 2 * cp), pl_p, tk * 1.8, t_rankine)
        d.append((mach, pl_p, f"{pl_p_calc:.3f}", t_rankine, f"{tk * 1.8:.1f}"))

    print("Table on Page 10")
    print()
    text = make_nice_width_markdown_table(
        (
            "Mach",
            "Reported pl/po",
            "Calculated pl/po",
            "Reported Toc, R",
            "Calculated Toc, R",
        ),
        d,
    )
    print(text)
    print()
    print()
    d = []
    for mach, cp, pl_po, tr_10000, tr_25000, tr_40000 in zip(
        *(iter(d_p10_table_2),) * 6
    ):
        tk_10000 = calc_t(calc_pressure(10000 / FT_PER_M), mach, cp, r=0.90)
        tk_25000 = calc_t(calc_pressure(25000 / FT_PER_M), mach, cp, r=0.90)
        tk_40000 = calc_t(calc_pressure(40000 / FT_PER_M), mach, cp, r=0.90)
        d.append(
            (
                mach,
                cp,
                tr_10000,
                f"{tk_10000 * 1.8:.1f}",
                tr_25000,
                f"{tk_25000 * 1.8:.1f}",
                tr_40000,
                f"{tk_40000 * 1.8:.1f}",
            )
        )
    text = make_nice_width_markdown_table(
        (
            "Mach",
            "Coefficient of pressure",
            "10000 ft. Toc, R",
            "Calculated Toc, R",
            "25000 ft. Toc, R",
            "Calculated Toc, R",
            "40000 ft. Toc, R",
            "Calculated Toc, R",
        ),
        d,
    )
    print(text)

    import matplotlib.pyplot as plt

    p = calc_pressure(15000 / FT_PER_M)
    machs = plt.np.linspace(0.1, 0.9)
    cps = [calc_cp_for_t_ambient_0c(p, _) for _ in machs]
    plt.figure()
    plt.suptitle("T_ambient = 0C, Altitude = 15000 ft.")
    plt.plot(machs, cps)
    plt.xlabel("Mach")
    plt.xlim(0, 1)
    plt.ylabel("Coefficient of pressure for wet t_surface=0C")
    plt.ylim(1, -3)
    plt.savefig('naca-tn-2914_cp_for_0c.png')

    plt.show()
