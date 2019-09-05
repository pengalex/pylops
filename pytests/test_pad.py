import pytest

import numpy as np
from numpy.testing import assert_array_equal

from pylops.utils import dottest
from pylops.basicoperators import Pad

par1 = {'ny': 11, 'nx': 11, 'pad':((0, 2), (4, 5)),
        'dtype':'float32'}  # square
par2 = {'ny': 21, 'nx': 11, 'pad':((3, 1), (0, 3)),
        'dtype':'float32'}  # rectangular

np.random.seed(10)

@pytest.mark.parametrize("par", [(par1)])
def test_Pad_1d_negative(par):
    """Check error is raised when pad has negative number
    """
    with pytest.raises(ValueError):
        _ = Pad(dims=par['ny'], pad=(-10, 0))

@pytest.mark.parametrize("par", [(par1)])
def test_Pad_2d_negative(par):
    """Check error is raised when pad has negative number for 2d
    """
    with pytest.raises(ValueError):
        _ = Pad(dims=(par['ny'], par['nx']), pad=((-10, 0), (3, -5)))


@pytest.mark.parametrize("par", [(par1)])
def test_Pad1d(par):
    """Dot-test and adjoint for Pad operator on 1d signal
    """
    Pop = Pad(dims=par['ny'], pad=par['pad'][0], dtype=par['dtype'])
    assert dottest(Pop, Pop.shape[0], Pop.shape[1])

    x = np.arange(par['ny'], dtype=par['dtype']) + 1.
    y = Pop * x
    xinv = Pop.H * y
    assert_array_equal(x, xinv)


@pytest.mark.parametrize("par", [(par1), (par2)])
def test_Pad2d(par):
    """Dot-test and adjoint for Pad operator on 2d signal
    """
    Pop = Pad(dims=(par['ny'], par['nx']), pad=par['pad'], dtype=par['dtype'])
    assert dottest(Pop, Pop.shape[0], Pop.shape[1])

    x = (np.arange(par['ny']*par['nx'],
                   dtype=par['dtype']) + 1.).reshape(par['ny'], par['nx'])
    y = Pop * x.ravel()
    xadj = Pop.H * y
    assert_array_equal(x.ravel(), xadj)
