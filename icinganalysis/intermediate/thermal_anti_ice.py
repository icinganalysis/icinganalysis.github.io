from icinganalysis import water_properties
from icinganalysis.intermediate.standard_computational_model import (
    T_MP,
    calc_m_evap,
    calc_q_conv,
    calc_q_drop_ke,
    calc_q_drop_warm,
    calc_q_aero_heat,
    calc_q_evap,
)
from icinganalysis.iteration_helpers import solve_minimize_f


def find_t_surface(
    t,
    p,
    u,
    hc,
    m_imp,
    m_run_in=0,
    po=None,
    to=None,
    rc=0.85,
    q_heating=0,
    fraction_wetted=1.0,
):
    t_surf = T_MP
    (
        n,
        q_aero_heat,
        q_freeze,
        q_drop_ke,
        q_conv,
        q_evap,
        q_drop_warm,
        q_balance,
        m_run_out,
    ) = calc_energy_and_mass_balance_with_heating_fixed_surface_t(
        t, p, u, hc, m_imp, m_run_in, t_surf, po, to, rc, q_heating, fraction_wetted
    )
    if abs(q_balance) < 0.001:
        return t_surf

    def f(t_surf):
        (
            n,
            q_aero_heat,
            q_freeze,
            q_drop_ke,
            q_conv,
            q_evap,
            q_drop_warm,
            q_balance,
            m_run_out,
        ) = calc_energy_and_mass_balance_with_heating_fixed_surface_t(
            t, p, u, hc, m_imp, m_run_in, t_surf, po, to, rc, q_heating, fraction_wetted
        )
        return abs(q_balance)

    t_surf = solve_minimize_f(f, (233.15, 473.15))

    return t_surf


def calc_energy_and_mass_balance_with_heating_fixed_surface_t(
    t,
    p,
    u,
    hc,
    m_imp,
    m_run_in=0,
    t_surf=T_MP,
    po=None,
    to=None,
    rc=0.85,
    q_heating=0,
    fraction_wetted=1.0,
):
    if po is None:
        po = p
    if to is None:
        to = t
    m_incoming = m_imp + m_run_in
    q_aero_heat = calc_q_aero_heat(u, hc, rc)
    q_drop_ke = calc_q_drop_ke(m_imp, u)
    q_conv = calc_q_conv(hc, t, t_surf)
    q_drop_warm = calc_q_drop_warm(m_imp, t, t_surf)
    m_evap = fraction_wetted * calc_m_evap(t, p, hc, t_surf, po, to)
    m_evap = min(m_incoming, m_evap)
    q_evap = calc_q_evap(m_evap)
    q_sink = q_conv + q_drop_warm + q_evap
    q_freeze = 0
    if t_surf <= T_MP:
        q_freeze = max(0, -(q_aero_heat + q_drop_ke + q_heating - q_sink))
    m_freeze = q_freeze / water_properties.L_FREEZING
    m_freeze = min(m_freeze, m_incoming - m_evap)
    q_freeze = m_freeze * water_properties.L_FREEZING
    q_balance = -(q_aero_heat + q_drop_ke + q_heating + q_freeze - q_sink)
    m_run_out = m_incoming - m_evap - m_freeze

    if m_incoming == 0:
        n = 0
        if m_freeze > 0:
            n = 1
    else:
        n = m_freeze / m_incoming
    return (
        n,
        q_aero_heat,
        q_freeze,
        q_drop_ke,
        q_conv,
        q_evap,
        q_drop_warm,
        q_balance,
        m_run_out,
    )


def find_t_surface_for_complete_evaporation(
    t, p, hc, m_imp, m_run_in=0, po=None, to=None, fraction_wetted=1.0
):
    def f(t_surface):
        m_evap = fraction_wetted * calc_m_evap(t, p, hc, t_surface, po, to)
        return abs(m_evap - (m_imp + m_run_in))

    t_surface = solve_minimize_f(f, [233.15, 473.15])
    return t_surface


def calc_q_heating_for_complete_evaporation(
    t, p, u, hc, m_imp, m_run_in=0, po=None, to=None, rc=0.85, fraction_wetted=1.0
):
    if m_imp <= 0:
        return 0
    t_surface = find_t_surface_for_complete_evaporation(
        t, p, hc, m_imp, m_run_in, po, to, fraction_wetted
    )
    (
        n,
        q_aero_heat,
        q_freeze,
        q_drop_ke,
        q_conv,
        q_evap,
        q_drop_warm,
        q_balance,
        m_run_out,
    ) = calc_energy_and_mass_balance_with_heating_fixed_surface_t(
        t,
        p,
        u,
        hc,
        m_imp,
        m_run_in,
        t_surface,
        po,
        to,
        rc,
        fraction_wetted=fraction_wetted,
    )
    q_heating = q_balance
    return q_heating


def calc_ts_q_for_complete_evap(tk, p, u, hc, m_imp, m_run_in=0, po=None, to=None, rc=0.85, q_heating=0,
                                fraction_wetted=1.0):
    ts = find_t_surface_for_complete_evaporation(
        tk, p, hc, m_imp, m_run_in, po, to, fraction_wetted=fraction_wetted
    )
    (
        n,
        q_aero_heat,
        q_freeze,
        q_drop_ke,
        q_conv,
        q_evap,
        q_drop_warm,
        q_balance,
        m_run_out,
    ) = calc_energy_and_mass_balance_with_heating_fixed_surface_t(
        tk, p, u, hc, m_imp, m_run_in, t_surf=ts,
        po=po,
        to=to,
        rc=rc,
        q_heating=q_heating,
        fraction_wetted=fraction_wetted
    )
    return ts, q_balance
