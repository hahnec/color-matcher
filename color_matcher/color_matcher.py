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

from .hist_matcher import HistogramMatcher
from .mvgd_matcher import TransferMVGD


class ColorMatcher(HistogramMatcher, TransferMVGD):

    def __init__(self, *args, **kwargs):
        super(ColorMatcher, self).__init__(*args, **kwargs)

        self._src = kwargs['src'] if 'src' in kwargs else None
        self._ref = kwargs['ref'] if 'ref' in kwargs else None
        self._method = kwargs['method'] if 'method' in kwargs else 'default'

    def main(self):

        # color transfer methods (to be iterated through)
        if self._method == 'default':
            funs = [self.transfer]
        elif self._method == 'mvgd':
            funs = [self.transfer]
        elif self._method == 'hist':
            funs = [self.hist_match]
        elif self._method == 'hm-mkl-hm':
            funs = [self.hist_match, self.transfer, self.hist_match]
        else:
            raise BaseException('Method type not recognized')

        # proceed with the color match
        for fun in funs:
            self._src = fun(self._src, self._ref)

        return self._src
