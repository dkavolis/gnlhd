# -*- coding: utf-8 -*-

import pytest
from gnlhd import GNLHD, phi_p
import numpy as np

__author__ = "dkavolis"
__copyright__ = "dkavolis"
__license__ = "mit"


@pytest.mark.parametrize("structure,dims,lcm,t", [((3, 5), 1, 15, (5, 3))])
def test_gnlhd_properties(structure, dims, lcm, t):
    lhd = GNLHD(structure, dims)
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
def test_gnlhd(count, dims):
    lhd = GNLHD(count, dims)
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
def test_gnlhd_normalized(count, dims):
    lhd = GNLHD(count, dims)
    a = lhd.standard()
    assert a.shape[0] == max(count)
    assert a.shape[1] == dims


def test_phi_p():
    a = np.array(
        [
            [12, 12],
            [2, 3],
            [9, 9],
            [14, 6],
            [6, 14],
            [1, 1],
            [10, 7],
            [15, 11],
            [7, 4],
            [5, 15],
            [8, 5],
            [4, 8],
            [3, 13],
            [13, 2],
            [11, 10],
        ],
        dtype=np.int,
    )
    assert phi_p(design=a, t=2, p=50) == pytest.approx(0.7169776)


# TODO: GNLHD.permutation()
# TODO: GNLHD.swap()
# TODO: GNLHD.optimize()
# TODO: GNLHD.full()
# TODO: GNLHD.illegal_set()
