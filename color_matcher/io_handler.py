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

import os
import numpy as np

try:
    from PIL import Image
except ImportError:
    raise ImportError('Please install pillow.')

from color_matcher.normalizer import Normalizer

FILE_EXTS = ('bmp', 'png', 'tiff', 'tif', 'jpeg', 'jpg')


def save_img_file(img, file_path=None, file_type=None):

    file_path = os.getcwd() if file_path is None else file_path
    ext = os.path.splitext(file_path)[-1][1:]

    if not file_type:
        file_type = ext if ext == 'png' or ext == 'tiff' else 'tiff' if img.dtype == 'uint16' else 'png'

    # compose new file path string if extension type changed
    file_path = os.path.splitext(file_path)[-2] if file_path.endswith(FILE_EXTS) else file_path
    file_type = 'png' if file_type is None else file_type
    file_path += '.' + file_type

    # normalization
    img = Normalizer(img).uint16_norm() if file_type.__contains__('tif') else Normalizer(img).uint8_norm()

    try:
        import imageio
        suppress_user_warning(True, category=UserWarning)
        imageio.imwrite(uri=file_path, im=img)
        suppress_user_warning(False, category=UserWarning)
    except ImportError:
        if file_type == 'png' or file_type == 'bmp':
            try:
                Image.fromarray(img).save(file_path, file_type, optimize=True)
                #imageio.imwrite(uri=file_path, im=img)
            except PermissionError as e:
                raise Exception(e)

    return True


def load_img_file(file_path):

    # get file extension
    file_type = file_path.split('.')[-1]

    if any(file_type.lower() in ext for ext in FILE_EXTS):
        try:
            import imageio
            suppress_user_warning(True, category=UserWarning)
            img = imageio.imread(uri=file_path, format=file_type)
            suppress_user_warning(False, category=UserWarning)
        except ImportError:
            try:
                img = Image.open(file_path)
            except OSError or TypeError:
                # support load of truncated images
                from PIL import ImageFile
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                img = Image.open(file_path)

    else:
        raise TypeError('Filetype %s not recognized' % file_type)

    # normalize (convert to numpy array)
    img = Normalizer(np.asarray(img)).type_norm()

    return img


def suppress_user_warning(switch=None, category=None):

    import warnings
    switch = switch if switch is None else True
    if switch:
        warnings.filterwarnings("ignore", category=category)
    else:
        warnings.filterwarnings("default", category=category)


def select_file(init_dir=None, title=''):
    """ get filepath from tkinter dialog """

    # consider initial directory if provided
    init_dir = os.path.expanduser('~/') if not init_dir else init_dir

    # import tkinter while considering Python version
    try:
        import tkinter as tk
        from tkinter.filedialog import askopenfilename
    except ImportError:
        import Tkinter as tk
        from tkFileDialog import askopenfilename

    # open window using tkinter
    root = tk.Tk()
    root.withdraw()
    root.update()
    file_path = askopenfilename(initialdir=[init_dir], title=title)
    root.update()

    return file_path if file_path else None
