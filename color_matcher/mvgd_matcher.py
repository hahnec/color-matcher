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
            # default function
            self._fun_name = 'mkl'
        self._fun_call = self._fun_dict[self._fun_name] if self._fun_name in self._fun_dict else self.mkl_solver

        # initialize variables
        self.r, self.z, self.cov_r, self.cov_z, self.mu_r, self.mu_z, self.transfer_mat = [None]*7

    def init_vars(self):

        # reshape source and reference images
        self.r, self.z = self._src.reshape([-1, self._src.shape[2]]).T, self._ref.reshape([-1, self._ref.shape[2]]).T

        # compute covariance matrices
        self.cov_r, self.cov_z = np.cov(self.r), np.cov(self.z)

        # compute color channel means
        self.mu_r, self.mu_z = self.r.mean(axis=1)[..., np.newaxis], self.z.mean(axis=1)[..., np.newaxis]

        # validate dimensionality
        self.check_dims()

    def multivar_transfer(self, src: np.ndarray = None, ref: np.ndarray = None, fun: FunctionType = None) -> np.ndarray:
        """

        Transfer function to map colors based on for Multi-Variate Gaussian Distributions (MVGDs).

        :param src: Source image that requires transfer
        :param ref: Palette image which serves as reference
        :param fun: Optional argument to pass a transfer function to solve for covariance matrices
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
        self.init_vars()

        # set solver function for transfer matrix
        self._fun_call = fun if fun is FunctionType else self._fun_call

        # compute transfer matrix
        self.transfer_mat = self._fun_call()

        # transfer the intensity distributions
        res = np.dot(self.transfer_mat, self.r - self.mu_r) + self.mu_z

        # reshape pixel array
        res = res.T.reshape(self._src.shape)

        return res

    def mkl_solver(self):
        """
        This function computes the transfer matrix based on the Monge-Kantorovich Linearization (MKL).

        :return: **transfer_mat**: Transfer matrix
        :type transfer_mat: :class:`~numpy:numpy.ndarray`
        :rtype: np.ndarray

        """

        # validate dimensionality
        self.check_dims()

        eig_val_r, eig_vec_r = np.linalg.eig(self.cov_r)
        eig_val_r[eig_val_r < 0] = 0
        val_r = np.diag(np.sqrt(eig_val_r[::-1]))
        vec_r = np.array(eig_vec_r[:, ::-1])
        inv_r = np.diag(1. / (np.diag(val_r + np.spacing(1))))

        mat_c = val_r @ vec_r.T @ self.cov_z @ vec_r @ val_r
        eig_val_c, eig_vec_c = np.linalg.eig(mat_c)
        eig_val_c[eig_val_c < 0] = 0
        val_c = np.diag(np.sqrt(eig_val_c))

        self.transfer_mat = vec_r @ inv_r @ eig_vec_c @ val_c @ eig_vec_c.T @ inv_r @ vec_r.T

        return self.transfer_mat

    def analytical_solver(self) -> np.ndarray:
        """
        An analytical solution to the linear equation system of Multi-Variate Gaussian Distributions (MVGDs).

        :return: **transfer_mat**: Transfer matrix
        :type transfer_mat: :class:`~numpy:numpy.ndarray`
        :rtype: np.ndarray

        """

        # validate dimensionality
        self.check_dims()
        if self.r.shape[-1] != self.z.shape[-1]:
            raise Exception('Analytical MVGD solution requires spatial dimensions of both images to be equal')

        cov_r_inv = np.linalg.pinv(self.cov_r)
        cov_z_inv = np.linalg.pinv(self.cov_z)

        # compute transfer matrix using analytical method
        self.transfer_mat = np.linalg.pinv((self.z-self.mu_z).T @ cov_z_inv) @ (self.r-self.mu_r).T @ cov_r_inv

        return self.transfer_mat

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

        mean_dist = np.sum((mu_a-mu_b)**2)
        vars_dist = np.trace(cov_a+cov_b - 2*(np.dot(np.abs(cov_b)**.5, np.dot(np.abs(cov_a), np.abs(cov_b)**.5))**.5))

        return float(mean_dist + vars_dist)

    def w2_img_dist(self, img_a: np.ndarray, img_b:np.ndarray):

        """
        Wasserstein-2 image distance metric is a similarity measure for Gaussian distributions

        :param img_a: Image array *a*
        :param img_b: Image array *b*

        :type img_a: :class:`~numpy:numpy.ndarray`
        :type img_b: :class:`~numpy:numpy.ndarray`

        :return: **scalar**: Wasserstein-2 image metric as a scalar
        :rtype: float
        """

        mu_a, mu_b = np.mean(img_a, axis=(0, 1)), np.mean(img_b, axis=(0, 1))
        cov_a, cov_b = np.cov(img_a.reshape(-1, 3).T), np.cov(img_b.reshape(-1, 3).T)
        w2_img_dist = self.w2_dist(mu_a, mu_b, cov_a, cov_b)

        return w2_img_dist

    def check_dims(self):
        """
        Catch error for wrong color channel number (e.g., gray scale image)

        :return: None
        """

        if np.ndim(self.cov_r) == 0 or np.ndim(self.cov_z) == 0:
            raise Exception('Wrong color channel dimensionality for %s method' % self._fun_name)
