from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file
from color_matcher.normalizer import Normalizer

import os
import numpy as np
import imageio
try:
    from PIL import Image, ImageSequence
except:
    raise Exception('Please install pillow')

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
fn_img1 = "wave.gif"
if fn_img1.endswith('gif'):
    im = Image.open(os.path.join(dir_path, fn_img1))
duration = 40  #im.info['duration'] if 'duration' in im.info else
img2 = load_img_file(os.path.join(dir_path, 'sunrise_mvgd.png'))

sequence = []
method = 'mvgd'
#size = 200, 200
for frame in ImageSequence.Iterator(im):

    #img1 = np.asarray(frame.convert('RGB').resize(size, Image.ANTIALIAS), np.uint8)
    img1 = np.asarray(frame.convert('RGB'), np.uint8)

    # create color match object
    match = ColorMatcher(img1, img2, method=method).main()

    sequence.append(Image.fromarray(Normalizer(match).uint8_norm()))

output_fn = os.path.join(dir_path, os.path.splitext(fn_img1)[0] + '_' + method + '.gif')
imageio.mimwrite(output_fn, sequence, duration=1/duration, palettesize=2**8)
