#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "info@christopherhahne.de"
__license__ = """
    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import numpy as np

from .baseclass import MatcherBaseclass
from types import FunctionType


class TransferMVGD(MatcherBaseclass):

    def __init__(self, *args, **kwargs):
        super(TransferMVGD, self).__init__(*args, **kwargs)

        self._fun = kwargs['fun'] if 'fun' in kwargs else self.mkl_solver

    def transfer(self, src: np.ndarray=None, ref: np.ndarray=None, fun: FunctionType=None) -> np.ndarray:
        """

        Transfer function to map colors based on for Multi-Variate Gaussian Distributions (MVGDs).

        :param src: Source image that requires transfer
        :param ref: Palette image which serves as reference
        :param fun: optional argument to pass a transfer function to solve for covariance matrices
        :param t_r: Resulting image after the mapping

        :type src: :class:`~numpy:numpy.ndarray`
        :type ref: :class:`~numpy:numpy.ndarray`
        :type t_r: :class:`~numpy:numpy.ndarray`

        :return: **t_r**
        :rtype: np.ndarray

        """

        # override source and reference image with arguments (if provided)
        self._src = src if src is not None else self._src
        self._ref = ref if ref is not None else self._ref

        # check if three color channels are provided
        self.validate_color_chs()

        # set solver function for transfer matrix (default is MKL)
        self._fun = fun if fun is not None else self._fun

        r = np.reshape(src, [-1, src.shape[2]])
        z = np.reshape(ref, [-1, ref.shape[2]])

        cov_r = np.cov(r.T)
        cov_z = np.cov(z.T)

        transfer_mat = self._fun(cov_r, cov_z)

        mu_r = np.mean(r, axis=0)
        mu_z = np.mean(z, axis=0)

        t_r = np.dot((r - mu_r), transfer_mat) + mu_z
        t_r = np.reshape(t_r, src.shape)

        return t_r

    @staticmethod
    def mkl_solver(cov_r: np.ndarray, cov_z: np.ndarray):
        """

        This function computes the transfer matrix based on the Monge-Kantorovich linearization.

        :param cov_r: Covariance matrix of source image
        :param cov_z: Covariance matrix of reference image
        :param T: Transfer matrix

        :type cov_r: :class:`~numpy:numpy.ndarray`
        :type cov_z: :class:`~numpy:numpy.ndarray`
        :type T: :class:`~numpy:numpy.ndarray`

        :return: **T**
        :rtype: np.ndarray

        """

        [Da2, Ua] = np.linalg.eig(cov_r)
        Ua = np.array([Ua[:, 2] * -1, Ua[:, 1], Ua[:, 0] * -1]).T
        Da2[Da2 < 0] = 0
        Da = np.diag(np.sqrt(Da2[::-1]))
        C = np.dot(Da, np.dot(Ua.T, np.dot(cov_z, np.dot(Ua, Da))))
        [Dc2, Uc] = np.linalg.eig(C)
        Dc2[Dc2 < 0] = 0
        Dc = np.diag(np.sqrt(Dc2))
        Da_inv = np.diag(1. / (np.diag(Da + np.spacing(1))))

        T = np.dot(Ua, np.dot(Da_inv, np.dot(Uc, np.dot(Dc, np.dot(Uc.T, np.dot(Da_inv, Ua.T))))))

        return T
