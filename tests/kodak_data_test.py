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
from .img_downloader import download_stack

import unittest
import os


class MatchKodakTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MatchKodakTester, self).__init__(*args, **kwargs)

    def setUp(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')


    def test_kodak_images(self):
        # prepare data
        url = 'https://www.math.purdue.edu/~lucier/PHOTO_CD/BMP_IMAGES/'
        self.fnames = ['IMG' + str(i + 1).zfill(4) + '.bmp' for i in range(24)]
        loc_path = os.path.join(self.dat_path, 'kodak')

        try:
            os.makedirs(loc_path, 0o755)
            os.makedirs(os.path.join(loc_path, 'results'), 0o755)
        except:
            pass

        if not os.path.exists(loc_path):
            download_stack(url, loc_path)

        for fn_img1 in self.fnames:
            for fn_img2 in self.fnames:
                # load images
                img1 = load_img_file(os.path.join(loc_path, fn_img1))
                img2 = load_img_file(os.path.join(loc_path, fn_img2))

                # create color match object
                res = ColorMatcher(img1, img2, method='hm-mkl-hm').main()

                # assess quality
                val = self.avg_hist_dist(res, img2)
                print('Avg. histogram distance %s' % val)

                # save result
                output_filename = os.path.join(loc_path, 'results', fn_img1.split('.')[0] + '_from_' + fn_img2)
                save_img_file(res, file_path=output_filename)

                # assertion
                self.assertEqual(True, val != 0)
