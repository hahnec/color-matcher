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

        # extract method from kwargs (if available)
        self._fun_dict = {'mvgd': self.analytical_solver, 'mkl': self.mkl_solver}
        try:
            self._fun_name = [kw for kw in list(self._fun_dict.keys()) if kwargs['method'].__contains__(kw)][0]
        except (BaseException, IndexError):
            # use MKL as default
            self._fun_name = 'mkl'
        self._fun_call = self._fun_dict[self._fun_name] if self._fun_name in self._fun_dict else self.mkl_solver

        # initialize variables
        self.r = np.reshape(self._src, [-1, self._src.shape[2]])
        self.z = np.reshape(self._ref, [-1, self._ref.shape[2]])
        self.cov_r, self.cov_z = np.cov(self.r.T), np.cov(self.z.T)
        self.mu_r, self.mu_z = np.mean(self.r, axis=0), np.mean(self.z, axis=0)

    def _init_vars(self):

        self.r = np.reshape(self._src, [-1, self._src.shape[2]])
        self.z = np.reshape(self._ref, [-1, self._ref.shape[2]])

        self.cov_r = np.cov(self.r.T)
        self.cov_z = np.cov(self.z.T)

        self.mu_r = np.mean(self.r, axis=0)
        self.mu_z = np.mean(self.z, axis=0)

    def transfer(self, src: np.ndarray = None, ref: np.ndarray = None, fun: FunctionType = None) -> np.ndarray:
        """

        Transfer function to map colors based on for Multi-Variate Gaussian Distributions (MVGDs).

        :param src: Source image that requires transfer
        :param ref: Palette image which serves as reference
        :param fun: optional argument to pass a transfer function to solve for covariance matrices
        :param res: Resulting image after the mapping

        :type src: :class:`~numpy:numpy.ndarray`
        :type ref: :class:`~numpy:numpy.ndarray`
        :type res: :class:`~numpy:numpy.ndarray`

        :return: **res**
        :rtype: np.ndarray

        """

        # override source and reference image with arguments (if provided)
        self._src = src if src is not None else self._src
        self._ref = ref if ref is not None else self._ref

        # check if three color channels are provided
        self.validate_color_chs()

        # re-initialize variables to account for change in src and ref when passed to self.transfer()
        self._init_vars()

        # set solver function for transfer matrix
        self._fun_call = fun if fun is FunctionType else self._fun_call

        # compute transfer matrix
        transfer_mat = self._fun_call()

        # transfer the intensity distributions
        res = np.dot((self.r - self.mu_r), transfer_mat) + self.mu_z
        res = np.reshape(res, self._src.shape)

        return res

    def mkl_solver(self):
        """
        This function computes the transfer matrix based on the Monge-Kantorovich Linearization (MKL).

        :return: **transfer_mat**: Transfer matrix
        :type transfer_mat: :class:`~numpy:numpy.ndarray`
        :rtype: np.ndarray

        """

        [Da2, Ua] = np.linalg.eig(self.cov_r)
        Ua = np.array([Ua[:, 2] * -1, Ua[:, 1], Ua[:, 0] * -1]).T
        Da2[Da2 < 0] = 0
        Da = np.diag(np.sqrt(Da2[::-1]))
        C = np.dot(Da, np.dot(Ua.T, np.dot(self.cov_z, np.dot(Ua, Da))))
        [Dc2, Uc] = np.linalg.eig(C)
        Dc2[Dc2 < 0] = 0
        Dc = np.diag(np.sqrt(Dc2))
        Da_inv = np.diag(1. / (np.diag(Da + np.spacing(1))))

        return np.dot(Ua, np.dot(Da_inv, np.dot(Uc, np.dot(Dc, np.dot(Uc.T, np.dot(Da_inv, Ua.T))))))

    def analytical_solver(self) -> np.ndarray:
        """
        An analytical solution to the linear equation system of Multi-Variate Gaussian Distributions (MVGDs).

        :return: **transfer_mat**: Transfer matrix
        :type transfer_mat: :class:`~numpy:numpy.ndarray`
        :rtype: np.ndarray

        """

        cov_r_inv = np.linalg.inv(self.cov_r)
        cov_z_inv = np.linalg.inv(self.cov_z)

        return np.dot(np.dot(np.linalg.pinv(np.dot(self.z-self.mu_z, cov_z_inv)), self.r-self.mu_r), cov_r_inv).T

    @staticmethod
    def w2_dist(mu_a: np.ndarray, mu_b: np.ndarray, cov_a: np.ndarray, cov_b: np.ndarray) -> float:
        """
        Wasserstein-2 distance metric is a similarity measure for Gaussian distributions

        :param mu_a: Gaussian mean of distribution *a*
        :param mu_b: Gaussian mean of distribution *b*
        :param cov_a: Covariance matrix of distribution *a*
        :param cov_b: Covariance matrix of distribution *b*

        :type mu_a: :class:`~numpy:numpy.ndarray`
        :type mu_b: :class:`~numpy:numpy.ndarray`
        :type cov_a: :class:`~numpy:numpy.ndarray`
        :type cov_b: :class:`~numpy:numpy.ndarray`

        :return: **scalar**: Wasserstein-2 metric as a scalar
        :rtype: float
        """

        return sum((mu_a-mu_b)**2)+np.trace(cov_a+cov_b-2*(np.dot(cov_b**.5, np.dot(cov_a, cov_b**.5))**.5))
