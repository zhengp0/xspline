from functools import partial
from math import factorial
from operator import attrgetter
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from xspline.typing import (BoundaryPoint, Callable, RawDFunction,
                            RawIFunction, RawVFunction)


class XFunction:

    def __init__(self, fun: Optional[Callable] = None) -> None:
        if not hasattr(self, "fun"):
            self.fun = fun

    def _check_args(self, x: NDArray, order: int) -> tuple[NDArray, int, bool]:
        x, order = np.asarray(x, dtype=float), int(order)
        if (x.ndim not in [0, 1, 2]) or (x.ndim == 2 and len(x) != 2):
            raise ValueError("please provide a scalar, an 1d array, or a 2d "
                             "array with two rows")

        # reshape array
        isscalar = x.ndim == 0
        if isscalar:
            x = x.ravel()
        if order >= 0 and x.ndim == 2:
            x = x[1] - x[0]
        if order < 0 and x.ndim == 1:
            x = np.vstack([np.repeat(x.min(), x.size), x])

        # check interval bounds
        if order < 0 and (x[0] > x[1]).any():
            raise ValueError("to integrate, `x` must satisfy `x[0] <= x[1]`")

        return x, order, isscalar

    def __call__(self, x: NDArray, order: int = 0) -> NDArray:
        """Function returns function values, derivatives and definite integrals.

        Parameters
        ----------
        x
            Data points where the function is evaluated. If `order >= 0` and
            `x` is a 2d array with two rows, the difference between the rows
            will be used for function evaluation. If `order < 0` and `x` is a
            2d array with two rows, the rows will be treated as the starting and
            ending points for definite interval. If `order < 0` and `x` is a
            1d array, function will use the smallest number in `x` as the
            starting point of the definite interval.
        order
            Order of differentiation or integration. When `order = 0`, function
            value will be returned. When `order > 0` function derviative will
            be returned. When `order < 0`, function integral will be returned.
            Default is `0`.

        Returns
        -------
        describe
            Return function values, derivatives or definite integrals.

        Raises
        ------
        AttributeError
            Raised when the function implementation is not provided.
        ValueError
            Raised when `x` is not a scalar, 1d array or 2d array with two rows.
        ValueError
            Raised when `order < 0` and `any(x[0] > x[1])`.

        """
        if getattr(self, "fun", None) is None:
            raise AttributeError("please provide the function implementation")

        x, order, isscalar = self._check_args(x, order)

        if x.size == 0:
            return np.empty(shape=x.shape, dtype=x.dtype)
        result = self.fun(x, order)

        if isscalar:
            result = result[0]
        return result

    def append(self, other: "XFunction", sep: BoundaryPoint) -> "XFunction":

        def fun(x: NDArray, order: int = 0) -> NDArray:
            left = x <= sep[0] if sep[1] else x < sep[0]

            if order >= 0:
                return np.where(left, self.fun(x, order), other.fun(x, order))

            lboth, rboth = left.all(axis=0), (~left).all(axis=0)
            landr = (~lboth) & (~rboth)

            result = np.zeros(x.shape[1], dtype=x.dtype)
            result[lboth] = self.fun(x[:, lboth], order)
            result[rboth] = other.fun(x[:, rboth], order)

            if landr.any():
                lx = np.insert(x[np.ix_([0], landr)], 1, sep[0], axis=0)
                rx = np.insert(x[np.ix_([1], landr)], 0, sep[0], axis=0)
                dx = x[1][landr] - sep[0]

                for i in range(1, -order):
                    result[landr] += self.fun(lx, order + i) * (dx**i / factorial(i))
                result[landr] += self.fun(lx, order) + other.fun(rx, order)
            return result

        return XFunction(fun)


class BundleXFunction(XFunction):

    def __init__(self,
                 params: tuple,
                 val_fun: RawVFunction,
                 der_fun: RawDFunction,
                 int_fun: RawIFunction) -> None:
        self.params = params
        self.val_fun = partial(val_fun, params)
        self.der_fun = partial(der_fun, params)
        self.int_fun = partial(int_fun, params)

    def fun(self, x: NDArray, order: int = 0) -> NDArray:
        if order == 0:
            return self.val_fun(x)
        if order > 0:
            return self.der_fun(x, order)
        dx = np.diff(x, axis=0)[0]
        val = self.int_fun(x[1], order)
        for i in range(-order):
            val -= self.int_fun(x[0], order + i) * (dx**i / factorial(i))
        return val


class BasisXFunction(XFunction):

    coefs = property(attrgetter("_coefs"))

    def __init__(self,
                 basis_funs: tuple[XFunction],
                 coefs: Optional[NDArray] = None) -> None:
        if not all(isinstance(fun, XFunction) for fun in basis_funs):
            raise TypeError("basis functions must all be instances of "
                            "`XFunction`")
        self.basis_funs = tuple(basis_funs)
        self.coefs = coefs

    @coefs.setter
    def coefs(self, coefs: Optional[NDArray]) -> None:
        if coefs is not None:
            coefs = np.asarray(coefs, dtype=float).ravel()
            if coefs.size != len(self):
                raise ValueError("number of coeffcients does not match number "
                                 "of basis functions")
        self._coefs = coefs

    def get_design_mat(self, x: NDArray,
                       order: int = 0,
                       check_args: bool = True) -> NDArray:
        if check_args:
            x, order, _ = self._check_args(x, order)
        return np.vstack([fun.fun(x, order) for fun in self.basis_funs]).T

    def fun(self, x: NDArray, order: int = 0) -> NDArray:
        if self.coefs is None:
            raise ValueError("please provide the coefficients for the basis "
                             "functions")
        design_mat = self.get_design_mat(x, order=order, check_args=False)
        return design_mat.dot(self.coefs)

    def __len__(self) -> int:
        return len(self.basis_funs)
