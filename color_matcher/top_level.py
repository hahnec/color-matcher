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

from color_matcher.hist_matcher import HistogramMatcher
from color_matcher.mvgd_matcher import TransferMVGD
from color_matcher.reinhard_matcher import ReinhardMatcher
import numpy as np

METHODS = ('default', 'hm', 'reinhard', 'mvgd', 'mkl', 'hm-mvgd-hm', 'hm-mkl-hm')


class ColorMatcher(HistogramMatcher, ReinhardMatcher, TransferMVGD):

    def __init__(self, *args, **kwargs):
        super(ColorMatcher, self).__init__(*args, **kwargs)

        self._method = kwargs['method'] if 'method' in kwargs else 'default'
        self._funs = []

    def main(self) -> np.ndarray:
        """
        The main function is the high-level entry point performing the mapping based on instantiation arguments.

        :return: Resulting image after color mapping
        :rtype: np.ndarray
        """

        self.transfer()

        return self._src

    def transfer(self, src: np.ndarray = None, ref: np.ndarray = None, method: str = None) -> np.ndarray:
        """

        Transfer function to map colors based on provided transfer method.

        :param src: Source image that requires transfer
        :param ref: Palette image which serves as reference
        :param method: ('default', 'hm', 'reinhard', 'mvgd', 'mkl', 'hm-mvgd-hm', 'hm-mkl-hm') determining color mapping

        :type src: :class:`~numpy:numpy.ndarray`
        :type ref: :class:`~numpy:numpy.ndarray`
        :type method: :class:`str`

        :return: Resulting image after color mapping
        :rtype: np.ndarray

        """

        # assign input arguments to variables (if provided)
        self._method = self._method.lower() if method is None else method.lower()
        self._src = src if src is not None else self._src
        self._ref = ref if ref is not None else self._ref

        # color transfer methods (to be iterated through)
        if self._method == METHODS[0]:
            self._funs = [self.multivar_transfer]
        elif self._method == METHODS[1]:
            self._funs = [self.hist_match]
        elif self._method == METHODS[2]:
            self._funs = [self.reinhard]
        elif self._method in METHODS[3:5]:
            self._funs = [self.multivar_transfer]
        elif self._method in METHODS[5:]:
            self._funs = [self.hist_match, self.multivar_transfer, self.hist_match]
        else:
            raise BaseException('Method type \'%s\' not recognized' % method)

        # check if three color channels are provided
        self.validate_img_dims()

        # check provided color channels
        self.validate_color_chs()

        # proceed with the color match
        for fun in self._funs:
            self._src = fun(self._src, self._ref)

        return self._src
