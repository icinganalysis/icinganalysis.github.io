import matplotlib.pyplot as plt
from icinganalysis import (
    langmuir_blodgett_multicylinder_k_phi_unique_mvd as multicylinder,
)
from icinganalysis.markdown_table_helper import make_markdown_table


def calc_percent_difference(reference, value):
    return (value - reference) / reference * 100


if __name__ == "__main__":
    diameters = [_ * 0.0254 for _ in (0.125, 1)]  # from the appendix
    lengths = [6 * 0.0254, 6 * 0.0254]  # apparent lengths from Figure 2
    mvd = 10  # from the appendix
    lwc = 0.5  # from the appendix
    time = 60  # from the appendix
    tk = 273.15 - 20  # assumed to be cold enough to freeze all water
    p = 101325  # assumed
    mph = (
        2.5 * 100 / 1.5
    )  # inferred from table in appendix, "2.5 mph" and "1.5%", results in 166 mph, which is "reasonable"
    assumed_distribution = "Langmuir C"  # inferred from table in appendix "Error due to using "C" distribution curves for unknown distribution"
    ice_density = 800  # kg/m^3, inferred from "0.08 g/cm^3", assuming a 10% variation
    u = mph * 0.44704
    print(mph, u)
    mc = multicylinder.Multicylinder(diameters, lengths)
    (
        reference_calculated_masses,
        reference_average_ems,
        reference_average_dias,
    ) = mc.calc_masses_average_ems_diameters(
        tk, p, u, lwc, mvd, time, assumed_distribution, ice_density
    )
    print(reference_average_ems)
    print("reference_calculated_masses", reference_calculated_masses)
    apparent_mass_1 = 0.02 / 1000 * 100 / 2.6
    appearent_mass_2 = 0.03 / 1000 * 100 / 1.0
    print(apparent_mass_1, appearent_mass_2)
    print(0.02 / 1000, 0.03 / 1000)
    lwc_percent_errors = []
    mvd_percent_errors = []
    header = [
        "Source of error",
        "Estimated amount of error",
        "Resultant percent error (E) Water content",
        "Resultant percent error (E) Drop diameter",
    ]
    rows = []
    case = "Weighing sample 1/8-in. cylinder"
    delta_weight_grams = 0.02
    delta_text = f"+/-{delta_weight_grams:.2f} gram"
    lwc_percents = []
    mvd_percents = []
    masses_with_error_1 = (
        reference_calculated_masses[0] + delta_weight_grams / 1000,
        reference_calculated_masses[1],
    )
    lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
        tk, u, p, masses_with_error_1, time, assumed_distribution, ice_density
    )
    print("lwc1, mvd1, rss1", lwc1, mvd1, rss1, lwc, mvd)
    lwc_percents.append(calc_percent_difference(lwc, lwc1))
    mvd_percents.append(calc_percent_difference(mvd, mvd1))
    masses_with_error_1 = (
        reference_calculated_masses[0] - delta_weight_grams / 1000,
        reference_calculated_masses[1],
    )
    lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
        tk, u, p, masses_with_error_1, time, assumed_distribution, ice_density
    )
    print("lwc1, mvd1, rss1", lwc1, mvd1, rss1, lwc, mvd)
    lwc_percents.append(calc_percent_difference(lwc, lwc1))
    mvd_percents.append(calc_percent_difference(mvd, mvd1))
    lwc_percent = max([abs(_) for _ in lwc_percents])
    mvd_percent = max([abs(_) for _ in mvd_percents])
    lwc_percent_errors.append(lwc_percent)
    mvd_percent_errors.append(mvd_percent)
    rows.append(
        [f"{case}", f"{delta_text}", f"{lwc_percent:.1f}", f"{mvd_percent:.1f}"]
    )

    case = "Weighing sample 1-in. cylinder"
    delta_weight_grams = 0.03
    delta_text = f"+/-{delta_weight_grams:.2f} gram"
    lwc_percents = []
    mvd_percents = []
    masses_with_error_2 = (
        reference_calculated_masses[0],
        reference_calculated_masses[1] + delta_weight_grams / 1000,
    )
    lwc2, mvd2, rss2 = mc.find_lwc_mvd_from_dist(
        tk, u, p, masses_with_error_2, time, assumed_distribution, ice_density
    )
    lwc_percents.append(calc_percent_difference(lwc, lwc2))
    mvd_percents.append(calc_percent_difference(mvd, mvd2))
    masses_with_error_2 = (
        reference_calculated_masses[0],
        reference_calculated_masses[1] - delta_weight_grams / 1000,
    )
    lwc2, mvd2, rss2 = mc.find_lwc_mvd_from_dist(
        tk, u, p, masses_with_error_2, time, assumed_distribution, ice_density
    )
    lwc_percents.append(calc_percent_difference(lwc, lwc2))
    mvd_percents.append(calc_percent_difference(mvd, mvd2))
    lwc_percent = max([abs(_) for _ in lwc_percents])
    mvd_percent = max([abs(_) for _ in mvd_percents])
    lwc_percent_errors.append(lwc_percent)
    mvd_percent_errors.append(mvd_percent)
    rows.append(
        [f"{case}", f"{delta_text}", f"{lwc_percent:.1f}", f"{mvd_percent:.1f}"]
    )

    case = "Assumed density of ice"
    delta_value = 0.08  # g/cm^3
    delta_text = f"-{delta_value:.2f} g/cm^3"
    ice_density_adjusted = ice_density - delta_value * 1000
    lwc2, mvd2, rss2 = mc.find_lwc_mvd_from_dist(
        tk,
        u,
        p,
        reference_calculated_masses,
        time,
        assumed_distribution,
        ice_density_adjusted,
    )
    lwc_percent = abs(calc_percent_difference(lwc, lwc2))
    mvd_percent = abs(calc_percent_difference(mvd, mvd2))
    lwc_percent_errors.append(lwc_percent)
    mvd_percent_errors.append(mvd_percent)
    rows.append(
        [f"{case}", f"{delta_text}", f"{lwc_percent:.1f}", f"{mvd_percent:.1f}"]
    )

    case = "Timing exposure"
    delta_value = 1.5
    delta_text = f"+/-{delta_value:.1f} seconds"
    lwc_percents = []
    mvd_percents = []
    masses = [(time + delta_value) / time * _ for _ in reference_calculated_masses]
    lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
        tk,
        u,
        p,
        reference_calculated_masses,
        time + delta_value,
        assumed_distribution,
        ice_density,
    )
    lwc_percents.append(calc_percent_difference(lwc, lwc1))
    mvd_percents.append(calc_percent_difference(mvd, mvd1))
    lwc2, mvd2, rss2 = mc.find_lwc_mvd_from_dist(
        tk,
        u,
        p,
        reference_calculated_masses,
        time - delta_value,
        assumed_distribution,
        ice_density,
    )
    lwc_percents.append(calc_percent_difference(lwc, lwc2))
    mvd_percents.append(calc_percent_difference(mvd, mvd2))
    lwc_percent = max([abs(_) for _ in lwc_percents])
    mvd_percent = max([abs(_) for _ in mvd_percents])
    lwc_percent_errors.append(lwc_percent)
    mvd_percent_errors.append(mvd_percent)
    rows.append(
        [f"{case}", f"{delta_text}", f"{lwc_percent:.1f}", f"{mvd_percent:.1f}"]
    )

    case = "True airspeed"
    delta_value = 2.5
    delta_text = f"+/-{delta_value:.1f} mph"
    lwc_percents = []
    mvd_percents = []
    lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
        tk,
        u + 0.44704 * delta_value,
        p,
        reference_calculated_masses,
        time,
        assumed_distribution,
        ice_density,
    )
    lwc_percents.append(calc_percent_difference(lwc, lwc1))
    mvd_percents.append(calc_percent_difference(mvd, mvd1))
    lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
        tk,
        u - 0.44704 * delta_value,
        p,
        reference_calculated_masses,
        time,
        assumed_distribution,
        ice_density,
    )
    lwc_percents.append(calc_percent_difference(lwc, lwc1))
    mvd_percents.append(calc_percent_difference(mvd, mvd1))
    lwc_percent = max([abs(_) for _ in lwc_percents])
    mvd_percent = max([abs(_) for _ in mvd_percents])
    lwc_percent_errors.append(lwc_percent)
    mvd_percent_errors.append(mvd_percent)
    rows.append(
        [f"{case}", f"{delta_text}", f"{lwc_percent:.1f}", f"{mvd_percent:.1f}"]
    )

    case = "Miscellaneous other errors"
    lwc_percent_errors.append(1)
    mvd_percent_errors.append(1)
    rows.append(["Miscellaneous other errors", "----", "1.0", "1"])

    case = 'Error due to using "C" distribution curves for unknown distribution'
    delta_value = 2.5
    delta_text = "----"
    lwc_percents = []
    mvd_percents = []
    for dist in ("Langmuir A", "Langmuir B", "Langmuir C", "Langmuir D", "Langmuir E"):
        dist_calculated_masses, ems, dias = mc.calc_masses_average_ems_diameters(
            tk, p, u, lwc, mvd, time, dist, ice_density
        )
        lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
            tk, u, p, dist_calculated_masses, time, assumed_distribution, ice_density
        )
        lwc_percents.append(calc_percent_difference(lwc, lwc1))
        mvd_percents.append(calc_percent_difference(mvd, mvd1))
    print("lwc_percents", lwc_percents)
    print("mvd_percents", mvd_percents)
    lwc_percent = max([abs(_) for _ in lwc_percents])
    mvd_percent = max([abs(_) for _ in mvd_percents])
    lwc_percent_errors.append(lwc_percent)
    mvd_percent_errors.append(mvd_percent)
    rows.append(
        [f"{case}", f"{delta_text}", f"{lwc_percent:.1f}", f"{mvd_percent:.1f}"]
    )

    print(lwc_percent_errors)
    print(mvd_percent_errors)

    lwc_rss = sum([_ ** 2 for _ in lwc_percent_errors]) ** 0.5
    mvd_rss = sum([_ ** 2 for _ in mvd_percent_errors]) ** 0.5
    lwc_total_error = sum([abs(_) for _ in lwc_percent_errors])
    mvd_total_error = sum([abs(_) for _ in mvd_percent_errors])
    print(lwc_rss, mvd_rss)
    print(lwc_total_error, mvd_total_error)

    make_markdown_table(header, rows)

    header = ["Total error", "Water content (percent)", "Drop diameter (percent)"]
    rows = [
        [
            "Maximum total error (sum(E))",
            f"{lwc_total_error:.1f}",
            f"{mvd_total_error:.1F}",
        ],
        ["Maximum resultant error (sum(E^2)^0.5)", f"{lwc_rss:.1f}", f"{mvd_rss:.1F}"],
    ]
    make_markdown_table(header, rows)

    plt.figure()
    for dist in ("Langmuir A", "Langmuir B", "Langmuir C", "Langmuir D", "Langmuir E"):
        lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
            tk, u, p, masses_with_error_1, time, dist, ice_density
        )
        plt.plot(dist, rss1, "+")
    plt.yscale("log")

    vs = []
    for dist in ("Langmuir A", "Langmuir B", "Langmuir C", "Langmuir D", "Langmuir E"):
        lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
            tk, u, p, reference_calculated_masses, time, dist, ice_density
        )
        print(
            dist,
            lwc1,
            mvd1,
            rss1,
            calc_percent_difference(lwc, lwc1),
            calc_percent_difference(mvd, mvd1),
        )
        vs.append((mvd1, lwc1, dist))
    plt.figure()
    plt.suptitle("Langmuir C compared to distribution noted")
    for mvd1, lwc1, dist in vs:
        plt.plot(mvd1, lwc1, "o", label=dist)
    plt.xlabel("Calculated Mean Effective Drop Diameter, micrometer")
    plt.ylabel("Calculated Liquid Water Content, g/m^3")
    plt.legend()
    plt.savefig("naca_tn_1393_error_assuming_c.png")

    vs = []
    for dist in ("Langmuir A", "Langmuir B", "Langmuir C", "Langmuir D", "Langmuir E"):
        dist_calculated_masses, ems, dias = mc.calc_masses_average_ems_diameters(
            tk, p, u, lwc, mvd, time, dist, ice_density
        )
        lwc1, mvd1, rss1 = mc.find_lwc_mvd_from_dist(
            tk, u, p, dist_calculated_masses, time, assumed_distribution, ice_density
        )
        vs.append((mvd1, lwc1, dist))
    plt.figure()
    plt.suptitle("Distribution noted compared to Langmuir C")
    for mvd1, lwc1, dist in vs:
        plt.plot(mvd1, lwc1, "o", label=dist)
    plt.xlabel("Calculated Mean Effective Drop Diameter, micrometer")
    plt.ylabel("Calculated Liquid Water Content, g/m^3")
    plt.legend()

    plt.figure()
    # NACA-TN-1393 Figure 5 values
    altitude_ft = 10000
    airspeed_mph = 200
    t_deg_f = -15
    tk = (469.59 + t_deg_f) / 1.8
    p = multicylinder.langmuir_cylinder_values.calc_pressure(altitude_ft * 12 * 0.025)
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
        em = multicylinder.langmuir_cylinder_values.calc_em(
            tk, p, u, d_drop, d_cylinder
        )
        lwcs_trace.append(rate_upper_trace_icing * 100 ** 2 / 3600 / (em * u))
        lwcs_light.append(rate_upper_light_icing * 100 ** 2 / 3600 / (em * u))
        lwcs_moderate.append(rate_upper_moderate_icing * 100 ** 2 / 3600 / (em * u))

    plt.plot(d_drops, lwcs_trace, label="Trace (1 g/cm^2-hr")
    plt.plot(d_drops, lwcs_light, label="Light (6 g/cm^2-hr")
    plt.plot(d_drops, lwcs_moderate, label="Moderate (12 g/cm^2-hr")

    plt.xlim(0, 60)
    plt.xlabel("Mean Effective Drop Diameter, micrometer")
    plt.ylim(0, 2.2)
    plt.yticks((0, 0.5, 1.0, 1.5, 2))
    plt.ylabel("Liquid Water Content, g/m^3")

    plt.legend(loc="upper left")
    plt.savefig("naca-tn-1393_figure_5_comparison_k_phi_unique.png", transparent=True)

    plt.show()
