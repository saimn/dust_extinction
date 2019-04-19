import numpy as np
import pytest

import astropy.units as u

from ..parameter_averages import VCG04
from .helpers import _invalid_x_range


x_bad = [-1.0, 0.1, 8.1, 100.]


@pytest.mark.parametrize("x_invalid", x_bad)
def test_invalid_wavenumbers(x_invalid):
    _invalid_x_range(x_invalid, VCG04(), 'VCG04')


@pytest.mark.parametrize("x_invalid_wavenumber", x_bad/u.micron)
def test_invalid_wavenumbers_imicron(x_invalid_wavenumber):
    _invalid_x_range(x_invalid_wavenumber, VCG04(), 'VCG04')


@pytest.mark.parametrize("x_invalid_micron", u.micron/x_bad)
def test_invalid_micron(x_invalid_micron):
    _invalid_x_range(x_invalid_micron, VCG04(), 'VCG04')


@pytest.mark.parametrize("x_invalid_angstrom", u.angstrom*1e4/x_bad)
def test_invalid_angstrom(x_invalid_angstrom):
    _invalid_x_range(x_invalid_angstrom, VCG04(), 'VCG04')


def get_axav_cor_vals(Rv):
    # testing wavenumbers
    x = np.array([8., 7., 6., 5., 4.6, 4., 3.4])

    # add units
    x = x/u.micron

    # correct values
    # from IDL version
    if Rv == 3.1:
        cor_vals = np.array([3.36528, 2.84166, 2.58283, 2.88248,
                             3.25880, 2.43315, 2.00025])
    elif Rv == 2.0:
        cor_vals = np.array([5.20767, 4.25652, 3.74640, 4.16150,
                             4.73050, 3.33399, 2.54668])
    elif Rv == 3.0:
        cor_vals = np.array([3.47694, 2.92741, 2.65335, 2.96000,
                             3.34799, 2.48775, 2.03337])
    elif Rv == 4.0:
        cor_vals = np.array([2.61157, 2.26285, 2.10683, 2.35925,
                             2.65674, 2.06463, 1.77671])
    elif Rv == 5.0:
        cor_vals = np.array([2.09235, 1.86411, 1.77892, 1.99880,
                             2.24199, 1.81076, 1.622711])
    elif Rv == 6.0:
        cor_vals = np.array([1.74620, 1.59829, 1.56031, 1.75850,
                             1.96549, 1.64151, 1.52005])
    else:
        cor_vals = np.array([0.0])

    return (x, cor_vals)


@pytest.mark.parametrize("Rv", [2.0, 3.0, 3.1, 4.0, 5.0, 6.0])
def test_extinction_VCG04_values(Rv):
    # get the correct values
    x, cor_vals = get_axav_cor_vals(Rv)

    # initialize extinction model
    tmodel = VCG04(Rv=Rv)

    # test
    np.testing.assert_allclose(tmodel(x), cor_vals, rtol=1e-5)
