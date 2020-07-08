# -*- coding: utf-8 -*-
from typing import Iterable, Tuple, cast

import numpy as np
from rpy2 import robjects
from rpy2.robjects import IntVector, numpy2ri
from rpy2.robjects.packages import PackageNotInstalledError, importr


def set_seed(seed: int) -> None:
    robjects.r("set.seed")(seed)


numpy2ri.activate()

try:
    devtools = importr("devtools")
    numbers = importr("numbers")
    rgnlhd = importr("GNLHD")
except PackageNotInstalledError:
    utils = importr("utils")

    utils.install_packages("devtools")
    utils.install_packages("numbers")

    devtools = importr("devtools")
    numbers = importr("numbers")
    devtools.install_github("DavidDJChen/GNLHD")

    rgnlhd = importr("GNLHD")


class RMeta(type):
    def __new__(mcs, name, bases, attrs, rclass=None, is_abstract=False):
        cls = super().__new__(mcs, name, bases, attrs)
        cls.__slots__ = ("_robj",)
        if not is_abstract:
            cls._RCLASS_NEW = rclass["new"]
        return cls

    def _robj_init(self, *args, **kwargs):
        return self._RCLASS_NEW(*args, **kwargs)


class RClass(metaclass=RMeta, is_abstract=True):
    def __init__(self, *args, **kwargs):
        self._robj = type(self)._robj_init(*args, **kwargs)

    def _call(self, name: str, *args, **kwargs):
        return self._robj[name](*args, **kwargs)

    def _get(self, name: str):
        return self._robj[name]

    def _set(self, name: str, value):
        self._robj[name] = value


class GGNLHD(RClass, rclass=rgnlhd.GGNLHD):
    def __init__(self, s: Tuple[int], q: int):
        try:
            iter(s)
        except TypeError:
            s = (s,)
        super().__init__(s=IntVector(s), q=q)

    @property
    def s(self) -> Tuple[int]:
        return cast(Tuple[int], tuple(self._get("s")))

    @property
    def q(self) -> int:
        return int(self._get("q")[0])

    @property
    def lcm(self) -> int:
        return int(self._get("Lcm")[0])

    @property
    def t(self) -> Tuple[int]:
        # wth mypy???
        return cast(Tuple[int], tuple(int(i) for i in self._get("t")))

    def normalize(
        self,
        lhd: np.ndarray,
        rng: np.random.Generator = None,
        lims: Tuple[float, float] = None,
    ) -> np.ndarray:
        if rng is None:
            rng = np.random.default_rng()

        lhd = np.asarray(lhd)
        samples = (lhd - rng.uniform(low=0, high=1, size=lhd.shape)) / self.lcm
        if lims is not None:
            samples = lims[0] + samples * (lims[1] - lims[0])

        return samples


class LHD(GGNLHD, rclass=rgnlhd.LHD):
    def __init__(self, s: int, q: int):
        super().__init__((s,), q)

    @property
    def s(self) -> int:
        return super().s[0]

    @property
    def t(self) -> int:
        return super().t[0]

    def swap(self, lhd: np.ndarray, column: int):
        return np.asarray(
            self._call("Swap", LH=np.assarray(lhd), column=column), dtype=np.int
        )

    def __call__(self):
        return np.asarray(self._call("LH"), dtype=np.int)

    def standard(self):
        return np.asarray(self._call("StandLHD"), dtype=np.double)


class NLHD(GGNLHD, rclass=rgnlhd.NLHD):
    def permutation(self):
        return np.asarray(self._call("NLH_permutation"), dtype=np.int)

    def __call__(self):
        return np.asarray(self._call("NLH"), dtype=np.int)

    def swap(
        self,
        nlhd: np.ndarray,
        column: int,
        swap_type: str,
        swap_layer: int,
        structure: Tuple[int] = None,
    ):
        if structure is None:
            structure = self.s
        return np.asarray(
            self._call(
                "Swap",
                NLH=np.asarray(nlhd),
                structure=IntVector(structure),
                column=column,
                Swap_type=swap_type,
                Swap_layer=swap_layer,
            )
        )

    def standard(self):
        return np.asarray(self._call("StandNLHD"), dtype=np.double)


class GNLHD(GGNLHD, rclass=rgnlhd.GNLHD):
    def illegal_set(self):
        return np.asarray(self._call("GNLH_illegal_set"), dtype=np.int)

    def permutation(self):
        return np.asarray(self._call("GNLH_permutation"), dtype=np.int)

    def full(self):
        return np.asarray(self._call("GNLH_Full"), dtype=np.int)

    def __call__(self):
        # this is somewhat special in 1D compared to other samplers...
        a = np.asarray(self._call("GNLH"), dtype=np.int)
        return a.reshape([len(a), self.q])

    def swap(
        self,
        column: int,
        swap_layer: int,
        full: np.ndarray = None,
        swap_type: str = "in",
        structure: Tuple[int] = None,
        lcm: int = None,
    ):
        if structure is None:
            structure = self.s
        if lcm is None:
            lcm = self.lcm
        if full is None:
            full = self.full()

        return np.asarray(
            self._call(
                "GNLH_Swap",
                GNLH_Full=np.asarray(full),
                structure=IntVector(structure),
                column=column,
                Swap_type=swap_type,
                Swap_layer=swap_layer,
                lcm=lcm,
            ),
            dtype=np.int,
        )

    def standard(self):
        return np.asarray(self._call("StandGNLHD"), dtype=np.double)

    # --BROKEN-----------
    # def optimize(
    #     self,
    #     iterations: int,
    #     w: np.ndarray,
    #     full: np.ndarray = None,
    #     th_initial: float = 0.1,
    #     m: int = 100,
    #     j: int = 6,
    #     t: int = 2,
    #     p: int = 50,
    #     tolerance: float = 0.1,
    #     alpha: Iterable[float] = (0.8, 0.9, 0.7),
    # ):
    #     if full is None:
    #         full = self.full()
    #     else:
    #         full = np.asarray(full)

    #     w = np.asarray(w)
    #     if len(w) != len(self.s):
    #         raise ValueError("w must be the same length as sample sequence")

    #     # the R function seems to be buggy, fails with
    #     # rpy2.rinterface_lib.embedded.RRuntimeError:
    #     # Error in rep(0, n * n) : invalid 'times' argument
    #     # doesn't even work from R console...
    #     return np.asarray(
    #         rgnlhd.Optimal_GNLHD_SequentialAlg(
    #             GNLHD_in=self._robj,
    #             GNLH_Full=full,
    #             iteration=iterations,
    #             w=w,
    #             T_h_initial=th_initial,
    #             M=m,
    #             J=j,
    #             t=t,
    #             p=p,
    #             tolerance=tolerance,
    #             alpha=np.asarray(alpha),
    #         )
    #     )


def phi_p(design: np.ndarray, t: int, p: int) -> float:
    return rgnlhd.Phi_p(Design=np.asarray(design), t=t, p=p)[0]
