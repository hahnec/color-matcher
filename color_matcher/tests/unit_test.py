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

import unittest

import requests
import zipfile
import io
import os
import numpy as np

from color_matcher import ColorMatcher
from color_matcher.io_handler import *


class ColorMatchTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ColorMatchTester, self).__init__(*args, **kwargs)

    def setUp(self):

        self.path = os.path.join(os.getcwd(), 'data')
        self.fnames = ['f197with4m11pxf16Final.bmp', 'f197Inf9pxFinalShift12.7cmf22.bmp']

        # url path to dataset
        url = 'http://r0k.us/graphics/kodak/'

        for fn in self.fnames:
            if not os.path.exists(os.path.join(self.path, fn)):
                self.download_data(url)

        self.runTest()

    def runTest(self):

        self.test_color_matcher()

    def download_data(self, url):
        ''' download image data '''

        print('Downloading data ...')

        # establish internet connection for test data download
        try:
            request = requests.get(url, stream=True)
        except requests.exceptions.ConnectionError:
            raise(Exception('Check your internet connection, which is required for downloading test data.'))

        # tbd: extract content from downloaded data
        print(request.content)

        print('Progress: Finished')

        return True

    @staticmethod
    def avg_hist_dist(img1, img2, bins=2**8-1):

        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]

        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    def test_color_matcher(self):

        # create folder (if it doesn't already exist)
        os.makedirs(os.path.join(self.path, ))

        for fn_img1, fn_img2 in self.fnames:

            # load images
            img1 = load_img_file(fn_img1)
            img2 = load_img_file(fn_img2)

            # create color match object
            res = ColorMatcher(img1, img2).main()

            # assess quality
            val = self.avg_hist_dist(res, img2)

            # assertion
            self.assertEqual(True, val)


if __name__ == '__main__':
    unittest.main()
