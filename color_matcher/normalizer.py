#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "info@christopherhahne.de"
__license__ = """
    Copyright (c) 2019 Christopher Hahne <info@christopherhahne.de>

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


class Normalizer(object):

    def __init__(self, data=None, min=None, max=None):

        self._data, self._min, self._max = None, None, None
        self._var_init(data, min, max)

    def _var_init(self, data=None, min=None, max=None):

        self._data = self._data if data is None else np.asarray(data, dtype='float64')
        self._dtype = str(self._data.dtype) if isinstance(self._data, np.ndarray) else 'float64'

        self._min = self._min if min is None else min
        self._max = self._max if max is None else max
        self._min = self._data.min() if not any([self._min, min]) and isinstance(self._data, np.ndarray) else self._min
        self._max = self._data.max() if not any([self._max, max]) and isinstance(self._data, np.ndarray) else self._max

    def uint16_norm(self):
        """ normalize image array to 16-bit unsigned integer """

        return np.asarray(np.round(self.norm_fun()*(2**16-1)), dtype=np.uint16)

    def uint8_norm(self):
        """ normalize image array to 8-bit unsigned integer """

        return np.asarray(np.round(self.norm_fun()*(2**8-1)), dtype=np.uint8)

    def type_norm(self, data=None, min=None, max=None, new_min=None, new_max=None):
        """ normalize numpy image array for provided data type """

        self._var_init(data, min, max)

        if self._dtype.startswith(('int', 'uint')):
            new_max = np.iinfo(np.dtype(self._dtype)).max if new_max is None else new_max
            new_min = np.iinfo(np.dtype(self._dtype)).min if new_min is None else new_min
            img_norm = np.round(self.norm_fun() * (new_max - new_min) + new_min)
        else:
            new_max = 1.0 if new_max is None else new_max
            new_min = 0.0 if new_min is None else new_min
            img_norm = self.norm_fun() * (new_max - new_min) + new_min

        return np.asarray(img_norm, dtype=self._dtype)

    def norm_fun(self):
        """ normalize image to values between 1 and 0 """

        norm = (self._data - self._min) / (self._max - self._min) if self._max != (self._min and 0) else self._data

        # prevent wrap-around
        norm[norm < 0] = 0
        norm[norm > 1] = 1

        return norm
