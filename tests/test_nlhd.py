# -*- coding: utf-8 -*-

import pytest
from gnlhd import NLHD

__author__ = "dkavolis"
__copyright__ = "dkavolis"
__license__ = "mit"


@pytest.mark.parametrize("structure,dims,lcm,t", [((3, 5), 1, 15, (5, 3))])
def test_nlhd_properties(structure, dims, lcm, t):
    lhd = NLHD(structure, dims)
    assert lhd.s == structure
    assert lhd.q == dims
    assert lhd.lcm == lcm
    assert lhd.t == t


@pytest.mark.parametrize(
    "count,dims",
    [
        pytest.param((3, 5), 1, id="1D"),
        pytest.param((6, 9), 2, id="2D"),
        pytest.param((9, 12), 3, id="3D"),
    ],
)
def test_nlhd(count, dims):
    lhd = NLHD(count, dims)
    a = lhd()
    assert a.shape[0] == max(count)
    assert a.shape[1] == dims


@pytest.mark.parametrize(
    "count,dims",
    [
        pytest.param((3, 5), 1, id="1D"),
        pytest.param((6, 9), 2, id="2D"),
        pytest.param((9, 12), 3, id="3D"),
    ],
)
def test_nlhd_normalized(count, dims):
    lhd = NLHD(count, dims)
    a = lhd.standard()
    assert a.shape[0] == max(count)
    assert a.shape[1] == dims


# TODO: NLHD.permutation()
# TODO: NLHD.swap()
