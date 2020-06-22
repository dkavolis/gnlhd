#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:               Daumantas Kavolis <dkavolis>
@Date:                 21-Jun-2020
@Filename:             __init__.py
@Last Modified By:     Daumantas Kavolis
@Last Modified Time:   22-Jun-2020
"""

from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

from gnlhd.wrap import LHD, NLHD, GNLHD, phi_p, set_seed
