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


class HistogramMatcher(MatcherBaseclass):

    def __init__(self, *args, **kwargs):
        super(HistogramMatcher, self).__init__(*args, **kwargs)

    def hist_match(self, src=None, ref=None):
        ''' channel-wise histogram matching '''

        # override source and reference image with arguments (if provided)
        self._src = src if src is not None else self._src
        self._ref = ref if ref is not None else self._ref

        # parameter init
        result = np.zeros_like(self._src)

        for ch in range(self._src.shape[2]):

            # convert to 1D arrays
            src_vec = self._src[..., ch].ravel()
            ref_vec = self._ref[..., ch].ravel()

            # analyze histograms
            _, src_idxs, src_cnts = np.unique(src_vec, return_inverse=True, return_counts=True)
            ref_vals, ref_cnts = np.unique(ref_vec, return_counts=True)

            # compute cumulative distribution functions
            src_cdf = np.cumsum(src_cnts).astype(np.float64) / src_vec.size
            ref_cdf = np.cumsum(ref_cnts).astype(np.float64) / ref_vec.size

            # do the histogram mapping
            interp_vals = np.interp(src_cdf, ref_cdf, ref_vals)
            result[..., ch] = interp_vals[src_idxs].reshape(src[..., ch].shape)

        return result
