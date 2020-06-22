# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for gnlhd.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

# import pytest

from gnlhd import set_seed

# use the same seed for tests
set_seed(1987)
