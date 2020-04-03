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

import unittest
import os
import numpy as np


class MatchMethodTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MatchMethodTester, self).__init__(*args, **kwargs)

    def setUp(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')

        self.test_run()

    def test_run(self):

        # test command line interface
        #self.test_cli()

        # validate match methods based on Pities images
        methods = ['default', 'mvgd', 'hm', 'hm-mkl-hm', 'reinhard']
        for method in methods:
            print('Use method "'+method+'":')
            self.test_match_method(method)
            print('')

    @staticmethod
    def avg_hist_dist(img1, img2, bins=2**8-1):

        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]

        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    def test_match_method(self, method=None):

        # skip
        if method is None:
            self.skipTest('')

        # load images
        plain = load_img_file(os.path.join(self.dat_path, 'scotland_house.png'))
        house = load_img_file(os.path.join(self.dat_path, 'scotland_plain.png'))
        refer = load_img_file(os.path.join(self.dat_path, 'scotland_pitie.png'))

        # create color match object
        match = ColorMatcher(plain, house, method=method).main()

        # assess quality
        refer_val = self.avg_hist_dist(refer, house)
        match_val = self.avg_hist_dist(match, house)
        print('Avg. histogram distances from original %s vs. method %s' % (round(refer_val, 3), round(match_val, 3)))

        # assertion
        self.assertEqual(True, refer_val > match_val)

    @unittest.skipUnless(False, "n.a.")
    def test_cli(self):

        from color_matcher.bin.cli import main
        import sys

        sys.args = ''
        ret = main()

        # assertion
        self.assertEqual(True, ret)

    @unittest.skipUnless(False, "n.a.")
    def test_match_method_imageio(self, method=None):

        # get test data from imageio lib
        import imageio
        fn_img1 = 'chelsea'
        fn_img2 = 'coffee'
        img1 = imageio.imread('imageio:'+fn_img1+'.png')
        img2 = imageio.imread('imageio:'+fn_img2+'.png')

        # create color match object
        match = ColorMatcher(img1, img2, method=method).main()

        # assess quality
        match_val = self.avg_hist_dist(match, img2)
        print('Avg. histogram distances %s vs %s' % (float('inf'), match_val))

        # save result
        loc_path = './test/data'
        output_filename = os.path.join(loc_path, fn_img1.split('.')[0] + '_from_' + fn_img2)
        save_img_file(img1, file_path=os.path.join(loc_path, fn_img1))
        save_img_file(img2, file_path=os.path.join(loc_path, fn_img2))
        save_img_file(match, file_path=output_filename)

        # assertion
        self.assertEqual(True, float('inf') > match_val)

if __name__ == '__main__':
    unittest.main()
