from icinganalysis import langmuir_cylinder_values
from icinganalysis import langmuir_blodgett_table_ii
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt


def calc_mvd_for_theta_degree(theta_degree, tk, p, u, d_cylinder):
    def f(mvd_):
        theta_calc = max(
            0,
            langmuir_blodgett_table_ii.value_interpolator(
                langmuir_cylinder_values.calc_k(tk, u, mvd_, d_cylinder),
                langmuir_cylinder_values.calc_phi(tk, p, u, d_cylinder),
                "theta_degree",
            ),
        )
        return abs(theta_calc - theta_degree)

    solution = minimize_scalar(f, bounds=[1, 1000], method="bounded")
    mvd = float("nan")
    if solution.success:
        mvd = solution.x
    return mvd


d_cylinder = 5 * 0.0254

# borrow values from NACA-TN-1393
mvd = 10  # from the appendix
lwc = 0.5  # from the appendix
time = 60  # from the appendix
tk = 273.15 - 20  # assumed to be cold enough to freeze all water
p = 101325  # assumed
mph = (
    2.5 * 100 / 1.5
)  # inferred from table in appendix, "2.5 mph" and "1.5%", results in 166 mph, which is "reasonable"
u = mph * 0.44704

mvds = list(plt.np.arange(5, 47.5 + 2.5, 2.5))
plt.figure()
diff_max_diameters = []
for mvd in mvds:
    theta_degree = max(
        0,
        langmuir_blodgett_table_ii.value_interpolator(
            langmuir_cylinder_values.calc_k(tk, u, mvd, d_cylinder),
            langmuir_cylinder_values.calc_phi(tk, p, u, d_cylinder),
            "theta_degree",
        ),
    )
    mvd_m_5 = float("nan")
    mvd_p_5 = float("nan")
    if theta_degree > 0:
        mvd_p_5 = calc_mvd_for_theta_degree(theta_degree + 5, tk, p, u, d_cylinder)
        if theta_degree - 5 > 0:
            mvd_m_5 = calc_mvd_for_theta_degree(theta_degree - 5, tk, p, u, d_cylinder)
    print(
        mvd,
        mvd_p_5,
        mvd_m_5,
        theta_degree,
        langmuir_blodgett_table_ii.value_interpolator(
            langmuir_cylinder_values.calc_k(tk, u, mvd_p_5, d_cylinder),
            langmuir_cylinder_values.calc_phi(tk, p, u, d_cylinder),
            "theta_degree",
        ),
        langmuir_blodgett_table_ii.value_interpolator(
            langmuir_cylinder_values.calc_k(tk, u, mvd_m_5, d_cylinder),
            langmuir_cylinder_values.calc_phi(tk, p, u, d_cylinder),
            "theta_degree",
        ),
    )
    diff_max_diameters.append(max(abs(mvd_p_5 - mvd) / mvd, abs(mvd_m_5 - mvd) / mvd))

plt.plot(mvds, diff_max_diameters, "+-", label="5 inch cylinder maximum drop diameter")

plt.xlim(5, 50)
plt.ylim(0)
plt.xlabel("Maximum drop diameter, micrometer")
plt.ylabel("Maximum measurement error fraction, (dia_calc-dia)/dia")
plt.legend()

plt.show()
