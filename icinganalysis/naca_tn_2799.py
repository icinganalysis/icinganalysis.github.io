from icinganalysis.air_properties import CP_AIR, R_AIR
from icinganalysis.markdown_table_helper import make_nice_width_markdown_table
from icinganalysis.units_helpers import (
    FT_PER_M,
    tf_to_k,
    BTU_H_FT2_F_PER_W_M2_K,
    LBM_PER_KG,
    S_PER_HOUR,
    FT2_PER_M2,
    BTU_H_PER_W,
)
from icinganalysis.water_properties import (
    WATER_SPECIFIC_HEAT,
    L_EVAPORATION,
    calc_vapor_p,
    RATIO_MOLECULAR_WEIGHTS,
)

INCH_HG_PER_PA = 0.00029529980164712


def calc_q_mev_taus(tk, p, u, hc, wcr, f_wet=1, r=0.85):
    t_nominal_rankine = 464
    tk_nominal = t_nominal_rankine / 1.8
    tau1 = (t_surface - tk) * (1 + wcr * WATER_SPECIFIC_HEAT / hc)
    tau2 = u ** 2 / 2 * (r / CP_AIR + wcr / hc)
    tau3 = RATIO_MOLECULAR_WEIGHTS * L_EVAPORATION / CP_AIR * calc_vapor_p(t_surface) / pl
    tau4 = RATIO_MOLECULAR_WEIGHTS * L_EVAPORATION / CP_AIR * calc_vapor_p(tk) / p
    tau5 = (1 - r) * R_AIR * tk_nominal / CP_AIR * (1 - pl / p)
    q = hc * (tau1 - tau2 + f_wet * (tau3 - tau4) + tau5)
    mev = hc / L_EVAPORATION * f_wet * (tau3 - tau4)
    return q, mev, tau1, tau2, tau3, tau4, tau5


tau1_f_example = 102  # F
tau2_f_example = 41.4
tau3_f_example = 179.5
tau4_f_example = 23.5
tau5_f_example = -6.8
q_example = 10490  # BTU/h-ft^2
mev_example = 7.32  # lbm/h-ft^2


if __name__ == "__main__":
    t_nominal_rankine = 464
    tk_nominal = t_nominal_rankine / 1.8
    u = 700 / FT_PER_M
    p = 12 / INCH_HG_PER_PA
    pl = 16 / INCH_HG_PER_PA
    tk = tf_to_k(20)
    t_surface = tf_to_k(80)
    hc = 50 / BTU_H_FT2_F_PER_W_M2_K
    wcr = 35 / LBM_PER_KG / S_PER_HOUR * FT2_PER_M2
    r = 0.85

    q, mev, tau1, tau2, tau3, tau4, tau5 = calc_q_mev_taus(tk, p, u, hc, wcr, r=r)

    rows = (
        ("τ1", f"{tau1*1.8:.1f}", tau1_f_example),
        ("τ2", f"{tau2*1.8:.1f}", tau2_f_example),
        ("τ3", f"{tau3*1.8:.1f}", tau3_f_example),
        ("τ4", f"{tau4*1.8:.1f}", tau4_f_example),
        ("τ5", f"{tau5*1.8:.1f}", tau5_f_example),
    )
    text = make_nice_width_markdown_table(
        ("Value", "Calculated, F", "Example value, F"), rows
    )
    print()
    print(text)
    print()
    text = make_nice_width_markdown_table(
        ("Value", "Calculated", "Example"),
        (
            ("q, BTU/h-ft^2", f"{q * BTU_H_PER_W / FT2_PER_M2:.0f}", q_example),
            (
                "Mev, lbm/h-ft^2",
                f"{mev * LBM_PER_KG * S_PER_HOUR / FT2_PER_M2:.2f}",
                mev_example,
            ),
        ),
    )
    print()
    print(text)
