from typing import Any, Callable, Iterator, Optional, Sequence, Union
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar


def solve_minimize_f(
    f: Callable, bounds: Optional[Sequence] = None,
) -> float:
    """
    Find the value that minimizes a function

    A simplified interface for scipy.optimize.minimize_scalar
    that includes checking the solution success.

    The return value will be float('nan') if a successful solution cannot be found.
    Note that float('nan') is compatible with matplotlib (skips NAN values when plotting).

    :param f: Function to minimize value for
    :param bounds: defined bounds of function, uses 'bounded' solution method if bounds, otherwise default method
    :return: solution value, or float('nan') if a successful solution cannot be found
    """
    x = float("nan")

    if bounds is None:
        solution = minimize_scalar(f)
    else:
        solution = minimize_scalar(f, bounds=bounds, method="bounded")
    if solution.success:
        x = solution.x
    return x


def generate_staggered_pairs(sequence: Sequence) -> Iterator:
    """
    Generate pairs of (sequence[i], sequence[i+1]) for i=0 to i=len(sequence)-2

    Example of use:
        midpoint_averages = [(v1+v2)/2 for v1, v2 in generate_staggered_pairs(sequence)]

    Note that there will be len(sequence)-1 pairs.
    Note that the return is an iterator, which will be exhausted after one pass through.
    Iterators are relatively low resource to create again, if you need to use it more than once.
    You can also use the method below if you want values in memory:
        values = tuple(generate_staggered_pairs(sequence))

    :param sequence: sequence to generate pair for.
    :return: iterator of values
    """
    return zip(sequence[:-1], sequence[1:])


def generate_even_odd_pairs(sequence):
    return zip(sequence[::2], sequence[1::2])


def get_x_y_split_at_x_value(x, y, x_value=0.0):
    if not any(x):
        return [], [], [], []
    if x_value in x:
        i = x.index(x_value)
        return x[0 : i + 1], y[0 : i + 1], x[i:], y[i:]
    if max(x) < x_value:
        return x, y, [], []
    elif min(x) > x_value:
        return [], [], x, y
    else:
        x = list(x)
        y = list(y)
        i = [i for i, _ in enumerate(x) if _ < x_value][-1]
        yi = interp1d(x[i : i + 1 + 1], y[i : i + 1 + 1])(x_value)
        x_lower = x[:i] + [x_value]
        x_upper = [x_value] + x[i:]
        y_lower = y[:i] + [yi]
        y_upper = [yi] + y[i:]
        return x_lower, y_lower, x_upper, y_upper


def trim_extra_x_y_zeros(x, y, threshold=0):
    i_s = [i for i, _ in enumerate(y) if _ > threshold]
    if not i_s:
        return [], []
    i0 = i_s[0] - 1 if i_s[0] > 0 else 0
    i_end = i_s[-1] + 1 + 1 if i_s[-1] + 1 + 1 <= len(y) else len(y)
    return x[i0:i_end], y[i0:i_end]


def calc_area(x, y):
    area = sum(
        [
            (y1 + y2) / 2 * (x2 - x1)
            for (y1, y2), (x1, x2) in zip(
                generate_staggered_pairs(y), generate_staggered_pairs(x)
            )
        ]
    )
    return area
