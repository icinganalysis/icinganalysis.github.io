import numpy as np
from scipy.interpolate import interp1d

from icinganalysis import simple_csv_reader

header, rows = simple_csv_reader.simple_csv_reader(r'cyl_beta2-43.csv')
columns = list(zip(*rows))
d = {k: v for k, v in zip(header, columns)}

lkos = np.log(d['ko'])
_beta_interp_extrapolate = interp1d(lkos, d['cyl_beta'],
                                    bounds_error=False, fill_value='extrapolate')
_beta_interp = interp1d(lkos, d['cyl_beta'],
                        bounds_error=False, fill_value=float('nan'))


def get_beta_extrapolate(ko):
    b = max(0, min(1, _beta_interp_extrapolate(np.log(ko))))
    return b


def get_beta(ko):
    b = _beta_interp(np.log(ko))
    b = max(0, b)
    return b

