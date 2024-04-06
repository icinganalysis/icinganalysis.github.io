from icinganalysis import air_properties, simple_csv_reader
from icinganalysis import compressible_flow
from icinganalysis import units_helpers
from icinganalysis.intermediate import standard_computational_model
from icinganalysis.langmuir_cylinder_values import (
    langmuir_lwc_fractions,
    get_mids,
)

hc_calc_method = standard_computational_model.calc_hc_o_cylinder_from


def calc_cylinder_beta_max_standard_computational_model_with_distribution(
    t,
    p,
    u,
    mvd,
    diameter,
    distribution="Langmuir A",
):
    d_mids = get_mids(distribution)
    beta = 0
    for r, w in zip(d_mids, langmuir_lwc_fractions):
        ko = standard_computational_model.calc_ko_d2(t, p, u, r * mvd, diameter)
        if ko == ko and ko > 0:  # Filter out 'nan' and unrealistic Ko values
            beta += w * max(
                0,
                standard_computational_model.cylinder_beta_max_from_figure_2_43.get_beta(
                    ko
                ),
            )
    return beta


def calc_cylinder_standard_computational_model_with_distribution(
    t,
    p,
    u,
    lwc,
    mvd,
    diameter,
    distribution="Langmuir A",
):
    beta = calc_cylinder_beta_max_standard_computational_model_with_distribution(
        t, p, u, mvd, diameter, distribution
    )
    hc = standard_computational_model.calc_hc_o_cylinder_from(u, t, diameter, p)
    cp = 1
    mach = compressible_flow.calc_mach(u, t)
    po = p * (0.7 * cp * mach**2 + 1)
    to = t * (p / po) ** (1 / 3.5)
    (
        n_calc,
        q_aero_heat,
        q_freeze,
        q_drop_ke,
        q_conv,
        q_evap,
        q_drop_warm,
    ) = standard_computational_model.calc_energy_and_mass_balance(
        t, p, u, lwc, hc, beta, po=po, to=to
    )
    return (n_calc, q_aero_heat, q_freeze, q_drop_ke, q_conv, q_evap, q_drop_warm, beta)


tables_2_5_to_8 = """Case, U, D, LWC, TC, N, PQV, PQF, PQK, PQC, PQE, PQW
2-5-a, 70, 20, 0.7, -26, 0.9, 5, 94, 1, 48, 16, 36
2-5-a, 70, 20, 0.7, -20, 0.7, 6, 93, 1, 47, 18, 35
2-5-a, 70, 20, 0.7, -14, 0.49, 8, 91, 1, 46, 21, 33
2-5-a, 70, 20, 0.7, -8, 0.27, 14, 84, 2, 44, 24, 32
2-5-a, 70, 20, 0.7, -2, 0.03, 53, 38, 9, 44, 25, 31
2-5-b, 70, 20, 0.1, -6, 0.93, 24, 75, 1, 60, 34, 6
2-5-b, 70, 20, 0.1, -4, 0.53, 36, 63, 1, 59, 35, 6
2-5-b, 70, 20, 0.1, -2, 0.10, 73, 25, 2, 60, 34, 6
2-6-a, 70, 20, 0.7, -26, .90, 5, 95, 1, 48, 15, 36
2-6-a, 70, 20, 0.8, -26, .83, 4, 95, 1, 46, 14, 40
2-6-a, 70, 20, 0.9, -26, .78, 4, 95, 1, 44, 14, 42
2-6-a, 70, 20, 1.0, -26, .73, 4, 95, 1, 42, 13, 45
2-6-a, 70, 20, 2.0, -26, .54, 3, 96, 1, 29,  9, 62
2-6-a, 70, 20, 3.0, -26, .47, 2, 96, 2, 22,  7, 71
2-6-a, 70, 20, 4.0, -26, .44, 2, 97, 2, 18,  6, 77
2-6-a, 70, 20, 5.0, -26, .42, 1, 97, 2, 15,  5, 80
2-6-b, 70, 20, 0.1, -6, .93, 24, 75,  1, 60, 34, 6
2-6-b, 70, 20, 0.4, -6, .28, 21, 77,  2, 51, 29, 21
2-6-b, 70, 20, 0.7, -6, .19, 18, 79,  3, 44, 25, 32
2-6-b, 70, 20, 1.0, -6, .15, 16, 80,  4, 39, 22, 40
2-6-b, 70, 20, 1.3, -6, .14, 14, 82,  4, 34, 19, 46
2-6-b, 70, 20, 1.6, -6, .12, 13, 82,  5, 31, 18, 51
2-6-b, 70, 20, 1.9, -6, .11, 12, 83,  5, 28, 16, 56
2-6-b, 70, 20, 2.2, -6, .11, 11, 84,  6, 26, 15, 59
2-6-b, 70, 20, 2.5, -6, .10, 10, 84,  6, 24, 14, 62
2-6-b, 70, 20, 2.8, -6, .10, 9 , 85,  6, 23, 13, 65
2-7-a, 70, 20, 0.7, -26, 0.90, 5, 95, 1, 48, 15, 36
2-7-a, 70, 40, 0.7, -26, 0.68, 4, 95, 1, 39, 12, 48
2-7-a, 70, 60, 0.7, -26, 0.64, 3, 95, 1, 37, 11, 52
2-7-a, 70, 80, 0.7, -26, 0.62, 3, 96, 1, 35, 11, 54
2-7-b, 70, 20, 0.1, -6, .93, 24, 75, 1, 60, 34, 6
2-7-b, 70, 40, 0.1, -6, .60, 24, 76, 1, 58, 33, 10
2-7-b, 70, 60, 0.1, -6, .52, 23, 76, 1, 57, 32, 11
2-7-b, 70, 80, 0.1, -6, .49, 23, 76, 1, 56, 32, 12
2-8-a, 70, 20, 0.7, -26, .90, 5 , 95, 1, 48, 15, 36
2-8-a, 80, 20, 0.7, -26, .82, 6 , 93, 1, 46, 14, 39
2-8-a, 90, 20, 0.7, -26, .76, 7 , 92, 1, 45, 14, 42
2-8-a, 100, 20, 0.7, -26, .71, 8 , 90, 2, 43, 13, 44
2-8-a, 110, 20, 0.7, -26, .67, 10, 88, 2, 42, 13, 46
2-8-a, 120, 20, 0.7, -26, .62, 11, 86, 3, 40, 12, 48
2-8-a, 130, 20, 0.7, -26, .59, 13, 84, 4, 39, 11, 49
2-8-b, 70 ,20, 0.1, -6, .93, 24, 75, 1, 60, 34, 6
2-8-b, 80 ,20, 0.1, -6, .74, 32, 67, 1, 60, 33, 7
2-8-b, 90 ,20, 0.1, -6, .58, 40, 58, 1, 60, 32, 8
2-8-b, 100,20, 0.1, -6, .44, 50, 48, 2, 60, 32, 8
2-8-b, 110,20, 0.1, -6, .31, 61, 37, 2, 60, 30, 9
2-8-b, 120,20, 0.1, -6, .19, 72, 25, 3, 60, 30, 10
2-8-b, 130,20, 0.1, -6, .08, 85, 11, 3, 61, 29, 10
"""


if __name__ == "__main__":
    from io import StringIO
    import matplotlib.pyplot as plt

    # DOT/FAA/CT-88/8-1
    header, vs = simple_csv_reader.simple_csv_reader_file_descriptor(
        StringIO(tables_2_5_to_8)
    )

    p = air_properties.calc_pressure(0)
    diameter = 0.2
    ns = []
    cases = []
    n_scms = []
    print()
    print("DOT/FAA/CT-88/8-1 Tables 2-5 thru 2-8 cylinder cases")
    print(r"                       Reference\calculated")
    print("                                   Heat Sources         Heat Sinks")
    print("Case   TC  V  LWC  MVD  n          %qv    %qf     %qk   %qc    %qe    %qw")
    for vs_ in vs:
        case, u, mvd, lwc, tc, N, PQV, PQF, PQK, PQC, PQE, PQW = vs_
        cases.append(case)
        ns.append(N)
        tk = units_helpers.tc_to_k(tc)

        (
            n_scm,
            q_aero_heat,
            q_freeze,
            q_drop_ke,
            q_conv,
            q_evap,
            q_drop_warm,
            beta,
        ) = calc_cylinder_standard_computational_model_with_distribution(
            tk, p, u, lwc, mvd, diameter, "Langmuir A"
        )
        heat_sources = q_drop_ke + q_freeze + q_aero_heat
        sinks = q_conv + q_evap + q_drop_warm
        pcts = (
            q_aero_heat / heat_sources,
            q_freeze / heat_sources,
            q_drop_ke / heat_sources,
            q_conv / sinks,
            q_evap / sinks,
            q_drop_warm / sinks,
        )
        try:
            pcts = [
                float(_[0])  # values are np.ndarray type, float for easy printing
                for _ in pcts
            ]
        except Exception:
            pass
        n_scms.append(n_scm)
        print(
            f"{case:5s} {tc:3.0f} {u:3.0f} {lwc:.2f} {mvd:3.0f}  {N:.2f}\\{float(n_scm):.2f} ",
            "".join(
                [
                    f"{_[1]:2.0f}\\{100 * _[0]:2.0f}  "
                    for _ in zip(pcts, (PQV, PQF, PQK, PQC, PQE, PQW))
                ]
            ),
        )

    plt.figure(figsize=(8, 8))
    plt.suptitle("DOT/FAA/CT-88/8-1 Tables 2-5 thru 2-8 Cylinder cases")
    for n_, nc_, t_ in zip(ns, n_scms, cases):
        plt.text(n_, nc_, t_)
    plt.plot((0, 1), (0, 1), "--", label="Perfect agreement")
    plt.plot(
        ns,
        n_scms,
        "o",
        fillstyle="none",
        label="Standard Computational Model calculated points",
    )
    plt.xlabel("Reference freezing fraction n")
    plt.ylabel("Calculated freezing fraction n")
    plt.xlim(0, 1)
    plt.ylim(0, 1.1)
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig("dot_faa_ct_88_8_1_cylinder_n.png")

    """
DOT/FAA/CT-88/8-1 Tables 2-5 thru 2-8 cylinder cases
                       Reference\calculated
                                   Heat Sources         Heat Sinks
Case   TC  V  LWC  MVD  n          %qv    %qf     %qk   %qc    %qe    %qw
2-5-a -26  70 0.70  20  0.90\0.91   5\ 4  94\95   1\ 1  48\49  16\16  36\34  
2-5-a -20  70 0.70  20  0.70\0.71   6\ 5  93\94   1\ 1  47\48  18\18  35\33  
2-5-a -14  70 0.70  20  0.49\0.50   8\ 7  91\92   1\ 1  46\47  21\21  33\32  
2-5-a  -8  70 0.70  20  0.27\0.28  14\12  84\86   2\ 2  44\45  24\24  32\31  
2-5-a  -2  70 0.70  20  0.03\0.03  53\48  38\43   9\ 9  44\46  25\23  31\32  
2-5-b  -6  70 0.10  20  0.93\0.98  24\21  75\78   1\ 1  60\61  34\33   6\ 6  
2-5-b  -4  70 0.10  20  0.53\0.57  36\32  63\68   1\ 1  59\61  35\33   6\ 6  
2-5-b  -2  70 0.10  20  0.10\0.13  73\65  25\33   2\ 2  60\63  34\31   6\ 6  
2-6-a -26  70 0.70  20  0.90\0.91   5\ 4  95\95   1\ 1  48\49  15\16  36\34  
2-6-a -26  70 0.80  20  0.83\0.83   4\ 4  95\95   1\ 1  46\47  14\15  40\37  
2-6-a -26  70 0.90  20  0.78\0.78   4\ 4  95\95   1\ 1  44\45  14\15  42\40  
2-6-a -26  70 1.00  20  0.73\0.73   4\ 3  95\96   1\ 1  42\43  13\14  45\43  
2-6-a -26  70 2.00  20  0.54\0.53   3\ 2  96\96   1\ 1  29\30   9\10  62\60  
2-6-a -26  70 3.00  20  0.47\0.46   2\ 2  96\97   2\ 2  22\23   7\ 8  71\69  
2-6-a -26  70 4.00  20  0.44\0.42   2\ 2  97\97   2\ 2  18\19   6\ 6  77\75  
2-6-a -26  70 5.00  20  0.42\0.40   1\ 1  97\97   2\ 2  15\16   5\ 5  80\79  
2-6-b  -6  70 0.10  20  0.93\0.98  24\21  75\78   1\ 1  60\61  34\33   6\ 6  
2-6-b  -6  70 0.40  20  0.28\0.30  21\18  77\80   2\ 2  51\52  29\28  21\20  
2-6-b  -6  70 0.70  20  0.19\0.20  18\15  79\81   3\ 3  44\45  25\24  32\31  
2-6-b  -6  70 1.00  20  0.15\0.16  16\14  80\83   4\ 4  39\39  22\21  40\39  
2-6-b  -6  70 1.30  20  0.14\0.14  14\12  82\83   4\ 4  34\35  19\19  46\46  
2-6-b  -6  70 1.60  20  0.12\0.13  13\11  82\84   5\ 5  31\32  18\17  51\51  
2-6-b  -6  70 1.90  20  0.11\0.12  12\10  83\85   5\ 5  28\29  16\16  56\55  
2-6-b  -6  70 2.20  20  0.11\0.11  11\ 9  84\85   6\ 6  26\27  15\15  59\59  
2-6-b  -6  70 2.50  20  0.10\0.10  10\ 9  84\85   6\ 6  24\25  14\13  62\62  
2-6-b  -6  70 2.80  20  0.10\0.10   9\ 8  85\86   6\ 6  23\23  13\13  65\64  
2-7-a -26  70 0.70  20  0.90\0.91   5\ 4  95\95   1\ 1  48\49  15\16  36\34  
2-7-a -26  70 0.70  40  0.68\0.68   4\ 3  95\96   1\ 1  39\41  12\13  48\46  
2-7-a -26  70 0.70  60  0.64\0.63   3\ 3  95\96   1\ 1  37\38  11\12  52\50  
2-7-a -26  70 0.70  80  0.62\0.61   3\ 3  96\96   1\ 1  35\36  11\12  54\52  
2-7-b  -6  70 0.10  20  0.93\0.98  24\21  75\78   1\ 1  60\61  34\33   6\ 6  
2-7-b  -6  70 0.10  40  0.60\0.62  24\20  76\79   1\ 1  58\59  33\32  10\10  
2-7-b  -6  70 0.10  60  0.52\0.55  23\20  76\79   1\ 1  57\58  32\31  11\11  
2-7-b  -6  70 0.10  80  0.49\0.51  23\20  76\79   1\ 1  56\57  32\31  12\12  
2-8-a -26  70 0.70  20  0.90\0.91   5\ 4  95\95   1\ 1  48\49  15\16  36\34  
2-8-a -26  80 0.70  20  0.82\0.83   6\ 5  93\94   1\ 1  46\48  14\15  39\37  
2-8-a -26  90 0.70  20  0.76\0.76   7\ 6  92\92   1\ 1  45\46  14\14  42\40  
2-8-a -26 100 0.70  20  0.71\0.71   8\ 7  90\91   2\ 2  43\44  13\14  44\42  
2-8-a -26 110 0.70  20  0.67\0.66  10\ 9  88\89   2\ 2  42\43  13\13  46\44  
2-8-a -26 120 0.70  20  0.62\0.62  11\10  86\87   3\ 3  40\42  12\12  48\46  
2-8-a -26 130 0.70  20  0.59\0.59  13\11  84\85   4\ 4  39\41  11\12  49\48  
2-8-b  -6  70 0.10  20  0.93\0.98  24\21  75\78   1\ 1  60\61  34\33   6\ 6  
2-8-b  -6  80 0.10  20  0.74\0.79  32\28  67\71   1\ 1  60\61  33\32   7\ 7  
2-8-b  -6  90 0.10  20  0.58\0.63  40\35  58\64   1\ 1  60\61  32\31   8\ 8  
2-8-b  -6 100 0.10  20  0.44\0.49  50\44  48\54   2\ 2  60\62  32\30   8\ 8  
2-8-b  -6 110 0.10  20  0.31\0.37  61\54  37\44   2\ 2  60\63  30\28   9\ 9  
2-8-b  -6 120 0.10  20  0.19\0.25  72\64  25\33   3\ 3  60\63  30\27  10\10  
2-8-b  -6 130 0.10  20  0.08\0.14  85\76  11\20   3\ 4  61\64  29\25  10\11  
    """

    plt.show()
