from icinganalysis.air_properties import calc_pressure

conditions_data = {
    'NACA-TR-1215 Figure 24a, NACA-TN-1424 Run 20': dict(
        tf=23,  # 20 1/29/47
        tk=((23 + 459.59) / 1.8),
        mph=168,
        u=168 * 0.44704,
        alt_ft=8270,
        p=calc_pressure(8270 * 12 * .0254),
        lwc=0.2,
        mvd=12,
        distribution="Langmuir A",
        d_cyls=[.185, .53, 1.3, 3],
        em_lwcs=[.17, .125, .078, .035],
        d_cyls_m=[_ * 0.0254 for _ in [.185, .53, 1.3, 3]],
    ),
    'NACA-TR-1215 Figure 24b, NACA-TN-2306 Flight 10, run 2': dict(
        mph=192,
        u=192 * 0.44704,
        alt_ft=5000,
        p=calc_pressure(5000 * 12 * .0254),
        tf=25,
        tk=((25 + 459.59) / 1.8),
        lwc=0.44,
        mvd=15,
        distribution="Langmuir A",
        d_cyls=[.23, .58, 1.3, 3],
        em_lwcs=[.35, .28, .199, .09],
        d_cyls_m=[_ * 0.0254 for _ in [.23, .58, 1.3, 3]],
    ),
    'NACA-TR-1215 Figure 24c, NACA-TN-2306 Flight 19, run 2': dict(
        mph=200,
        u=200 * 0.44704,
        alt_ft=2700,
        p=calc_pressure(2700 * 12 * .0254),
        tf=26,
        tk=((26 + 459.59) / 1.8),
        lwc=0.45,
        mvd=8,
        distribution="Langmuir D",
        d_cyls=[.19, .535, 1.3, 3, 4.6],
        em_lwcs=[.235, .175, .13, .05, .025],
        d_cyls_m=[_ * 0.0254 for _ in [.19, .535, 1.3, 3, 4.6]],
    ),
    'NACA-TR-1215 Figure 24d, NACA-TN-1904 Flight 179, run 17': dict(
        mph=180,
        u=180 * 0.44704,
        alt_ft=11800,
        p=calc_pressure(11800 * 12 * .0254),
        tf=15,
        tk=((15 + 459.59) / 1.8),
        lwc=1.1,
        mvd=25,
        distribution="Langmuir E",
        d_cyls=[.27, .6, 1.32, 3],
        # em_lwcs = [.11, .088, .072, .06]  # Figure 24d Y axis appears to be mislabeled by a factor of 10
        em_lwcs=[1.1, .88, .725, .6],  # Figure 24a Y values corrected
        d_cyls_m=[_ * 0.0254 for _ in [.27, .6, 1.32, 3]],
    )
}
