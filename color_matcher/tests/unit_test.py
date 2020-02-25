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

from color_matcher.top_level import ColorMatcher
from color_matcher.io_handler import *
from .img_downloader import main

import unittest
import os
import numpy as np


class ColorMatchTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ColorMatchTester, self).__init__(*args, **kwargs)

    def setUp(self):

        self.path = os.path.join(os.getcwd(), 'tests', 'data')
        self.fnames = ['IMG'+str(i+1).zfill(4)+'.bmp' for i in range(24)]

        # url path to dataset
        url = 'https://www.math.purdue.edu/~lucier/PHOTO_CD/BMP_IMAGES/'

        for fn in self.fnames:
            if not os.path.exists(os.path.join(self.path, fn)):
                main(url, os.path.join(os.getcwd(), 'data'))

        self.runTest()

    def runTest(self):

        self.test_color_matcher()

    @staticmethod
    def avg_hist_dist(img1, img2, bins=2**8-1):

        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]

        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    def test_color_matcher(self):

        # create folder (if it doesn't already exist)
        try:
            os.makedirs(os.path.join(self.path, 'results'), 0o755)
        except:
            pass

        for fn_img1 in self.fnames:
            for fn_img2 in self.fnames:

                # load images
                img1 = load_img_file(os.path.join(self.path, fn_img1))
                img2 = load_img_file(os.path.join(self.path, fn_img2))

                # create color match object
                res = ColorMatcher(img1, img2, method='hm-mkl-hm').main()

                # assess quality
                val = self.avg_hist_dist(res, img2)

                # save result
                save_img_file(res, file_path=os.path.join(self.path, 'results', fn_img1.split('.')[0]+'_from_'+fn_img2))

                # assertion
                self.assertEqual(True, val!=0)


if __name__ == '__main__':
    unittest.main()
