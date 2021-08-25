#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>
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
import warnings


class MatcherBaseclass(object):

    def __init__(self, *args, **kwargs):

        self._src = None
        self._ref = None
        self._funs = []

        if len(args) == 2:
            self._src = args[0]
            self._ref = args[1]

        if bool(kwargs):
            self._src = kwargs['src'] if 'src' in kwargs else self._src
            self._ref = kwargs['ref'] if 'ref' in kwargs else self._ref

    def validate_img_dims(self):
        """
        This function validates the image dimensions. It throws an exception if the dimension are unequal to 2 or 3.
        """

        # add third image dimension for monochromatic images
        self._src = self._src[..., np.newaxis] if len(self._src.shape) == 2 else self._src
        self._ref = self._ref[..., np.newaxis] if len(self._ref.shape) == 2 else self._ref

        if len(self._src.shape) not in (2, 3) or len(self._ref.shape) not in (2, 3):
            raise BaseException('Each image must have 2 or 3 dimensions')

        return True

    def validate_color_chs(self):
        """
        This function checks whether provided images consist of a valid number of color channels.
        """

        if len(self._src.shape) == 3 or len(self._ref.shape) == 3:
            if self._src.shape[2] > 4 or self._ref.shape[2] > 4:
                raise BaseException('Each image cannot have more than 4 color channels')
            elif self._src.shape[2] == 3 and self._ref.shape[2] == 4:
                self._ref = self._ref[..., :3]
            elif self._src.shape[2] == 4 and self._ref.shape[2] == 3:
                self._src = self._src[..., :3]
            elif self._src.shape[2] == 1 and self._ref.shape[2] == 3:
                self._ref = self.rgb2gray(self._ref)
            elif self._src.shape[2] == 3 and self._ref.shape[2] == 1:
                self._src = self.rgb2gray(self._src)

            if self._src.shape[2] == 1 and self._ref.shape[2] == 1:
                # restrict monochromatic transfer to histogram matching
                self._funs = [self.hist_match]
                warnings.warn('Transfer restricted to histogram matching due to monochromatic input')

        return True

    @staticmethod
    def rgb2gray(rgb: np.ndarray = None, standard: str = 'HDTV') -> np.ndarray:
        """ Convert RGB color space to monochromatic color space

        :param rgb: input array in red, green and blue (RGB) space
        :type rgb: :class:`~numpy:numpy.ndarray`
        :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
        :type standard: :class:`string`
        :return: array in monochromatic space
        :rtype: ~numpy:np.ndarray

        """

        # store shape
        shape = rgb.shape

        # reshape image to channel vectors
        rgb = rgb.reshape(-1, 3).T

        # choose standard
        mat = np.array([0.2126, 0.7152, 0.0722]) if standard == 'HDTV' else np.array([0.299, 0.587, 0.114])

        # convert to gray
        arr = np.dot(mat, rgb)

        # reshape to 2-D image
        arr = arr.reshape(shape[:2] + (1,))

        return arr
