#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:               Daumantas Kavolis <dkavolis>
@Date:                 22-Jun-2020
@Filename:             utilities.py
@Last Modified By:     Daumantas Kavolis
@Last Modified Time:   22-Jun-2020
"""

import numpy as np


def test_lhd(lhd):
    lhd = np.asarray(lhd)
    if len(lhd.shape) == 1:
        assert lhd.shape[0] == len(np.unique(lhd))
    else:
        lhd = lhd.reshape([lhd.shape[0], np.prod(lhd.shape[1:])])
        for i in range(lhd.shape[1]):
            assert lhd.shape[0] == len(np.unique(lhd[:, i]))
