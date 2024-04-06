from io import StringIO
import numpy as np
from scipy.interpolate import interp1d

from icinganalysis import simple_csv_reader

figure_2_43_data = """ko, cyl_beta
0.075, 0.0
0.105, 0.12
0.2, 0.295
0.5, 0.54
1, 0.695
2, 0.815
4, 0.895
10, 0.945
100, 0.99
"""


header, rows = simple_csv_reader.simple_csv_reader_file_descriptor(
    StringIO(figure_2_43_data)
)
columns = list(zip(*rows))
d = {k: v for k, v in zip(header, columns)}

lkos = np.log(d["ko"])
_beta_interp_extrapolate = interp1d(
    lkos, d["cyl_beta"], bounds_error=False, fill_value="extrapolate"
)
_beta_interp = interp1d(
    lkos, d["cyl_beta"], bounds_error=False, fill_value=float("nan")
)


def get_beta_extrapolate(ko):
    b = max(0, min(1, _beta_interp_extrapolate(np.log(ko))))
    return b


def get_beta(ko):
    b = _beta_interp(np.log(ko))
    b = max(0, b)
    return b
