# -*- coding: utf-8 -*-

import pytest
from gnlhd import LHD

__author__ = "dkavolis"
__copyright__ = "dkavolis"
__license__ = "mit"


import utilities


@pytest.mark.parametrize("count,dims,lcm,t", [(3, 1, 3, 1)])
def test_lhd_properties(count, dims, lcm, t):
    lhd = LHD(count, dims)
    assert lhd.s == count
    assert lhd.q == dims
    assert lhd.lcm == lcm
    assert lhd.t == t


@pytest.mark.parametrize(
    "count,dims",
    [
        pytest.param(3, 1, id="1D"),
        pytest.param(6, 2, id="2D"),
        pytest.param(9, 3, id="3D"),
    ],
)
def test_lhd(count, dims):
    lhd = LHD(count, dims)
    a = lhd()
    assert a.shape[0] == count
    assert a.shape[1] == dims
    assert a.size == count * dims
    utilities.test_lhd(a)


@pytest.mark.parametrize(
    "count,dims",
    [
        pytest.param(3, 1, id="1D"),
        pytest.param(6, 2, id="2D"),
        pytest.param(9, 3, id="3D"),
    ],
)
def test_lhd_normalized(count, dims):
    lhd = LHD(count, dims)
    a = lhd.standard()
    assert a.shape[0] == count
    assert a.shape[1] == dims
    assert a.size == count * dims
    utilities.test_lhd(a)


# TODO: LHD.swap()
