from scipy.interpolate import interp1d
from icinganalysis.iteration_helpers import solve_minimize_f


locations_s_23012m = 0, 0.03677, 0.08293, 0.12490, 0.22569
locations_23012m = 0, 0.02, 0.06, 0.1, 0.2
h_cl_max_data_23012m = {  # h/c, cl
    0: (1.5, 1.5, 1.5, 1.5, 1.5),
    0.0056: (1, 0.82, 0.62, 0.6, 0.99),
    0.0083: (0.99, 0.7, 0.5, 0.46, 0.75),
    0.0139: (0.98, 0.56, 0.31, 0.26, 0.41),
}


# NACA-TR-446

locations_s_NACA0012 = -0.06, 0, 0.06475, 0.16649, 0.31670, 0.66731
locations_NACA0012 = -0.05, 0, 0.05, 0.15, 0.3, 0.65
h_cl_max_data_NACA0012 = {  # h/c, cl
    0: (1.52, 1.52, 1.52, 1.52, 1.52, 1.52),
    0.001: (1.52, 1.12, 1.305, 1.495, 1.5, 1.51),
    0.002: (1.52, 1.09, 1.1, 1.43, 1.48, 1.5),
    0.005: (1.52, 0.9, 0.82, 1.32, 1.42, 1.45),
    0.0125: (1.52, 0.87, 0.5, 1.01, 1.16, 1.4),
}


def get_cl_max_NACA0012_x(x, h):
    hs = list(h_cl_max_data_NACA0012.keys())
    vs = [
        interp1d(locations_NACA0012, v, bounds_error=False, fill_value="extrapolate")(x)
        for k, v in h_cl_max_data_NACA0012.items()
    ]
    cl = interp1d(hs, vs, bounds_error=False, fill_value="extrapolate")(h)
    return cl


def get_cl_max_NACA0012(s, h):
    hs = list(h_cl_max_data_NACA0012.keys())
    vs = [
        interp1d(locations_s_NACA0012, v, bounds_error=False, fill_value="extrapolate")(
            s
        )
        for k, v in h_cl_max_data_NACA0012.items()
    ]
    cl = interp1d(hs, vs, bounds_error=False, fill_value="extrapolate")(h)
    return cl


def find_h_for_cl_max_NACA0012_x(cl_max, x, h_max_allowed=0.5):
    def f(h):
        cl_ = get_cl_max_NACA0012(x, h)
        return abs(cl_ - cl_max)

    h = solve_minimize_f(f, (0, h_max_allowed))
    return h


def find_h_for_cl_max_NACA0012(cl_max, s, h_max_allowed=0.5):
    def f(h):
        cl_ = get_cl_max_NACA0012(s, h)
        return abs(cl_ - cl_max)

    h = solve_minimize_f(f, (0, h_max_allowed))
    return h


def get_cl_max_23012m_x(x, h):
    hs = list(h_cl_max_data_23012m.keys())
    vs = [
        interp1d(locations_23012m, v, bounds_error=False, fill_value="extrapolate")(x)
        for k, v in h_cl_max_data_23012m.items()
    ]
    cl = interp1d(hs, vs, bounds_error=False, fill_value="extrapolate")(h)
    return cl


def get_cl_max_23012m(s, h):
    hs = list(h_cl_max_data_23012m.keys())
    vs = [
        interp1d(locations_s_23012m, v, bounds_error=False, fill_value="extrapolate")(s)
        for k, v in h_cl_max_data_23012m.items()
    ]
    cl = interp1d(hs, vs, bounds_error=False, fill_value="extrapolate")(h)
    return cl


def find_h_for_cl_max_23012m_x(cl_max, x, h_max_allowed=0.5):
    def f(h):
        cl_ = get_cl_max_23012m(x, h)
        return abs(cl_ - cl_max)

    h = solve_minimize_f(f, (0, h_max_allowed))
    return h


def find_h_for_cl_max_23012m(cl_max, s, h_max_allowed=0.5):
    def f(h):
        cl_ = get_cl_max_23012m(s, h)
        return abs(cl_ - cl_max)

    h = solve_minimize_f(f, (0, h_max_allowed))
    return h
