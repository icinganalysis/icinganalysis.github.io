from scipy.optimize import minimize_scalar
from typing import Any, Callable, Iterator, Optional, Sequence, Union


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
