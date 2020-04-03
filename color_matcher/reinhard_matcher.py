import numpy as np

from .baseclass import MatcherBaseclass
from color_matcher.normalizer import Normalizer

# Observer. = 2°, Illuminant = D65
REF_X = 95.047
REF_Y = 100.000
REF_Z = 108.883


class ReinhardMatcher(MatcherBaseclass):

    def __init__(self, *args, **kwargs):
        super(ReinhardMatcher, self).__init__(*args, **kwargs)

    def reinhard(self, src: np.ndarray=None, ref: np.ndarray=None) -> np.ndarray:
        '''

        This function conducts color matching in Lab color space based on the principles proposed by Reinhard et al.
        The paper of the original work can be found at https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf

        :param src: Source image that requires transfer
        :param ref: Palette image which serves as reference
        :param ref: Resulting image after the mapping

        :type src: :class:`~numpy:numpy.ndarray`
        :type ref: :class:`~numpy:numpy.ndarray`
        :type res: :class:`~numpy:numpy.ndarray`

        :return: **result**
        :rtype: np.ndarray

        '''

        # convert to Lab color space
        src_lab = self.rgb2lab(src)
        ref_lab = self.rgb2lab(ref)

        # compute color statistics for the source and reference images
        src_means, src_stds = self.gauss_analysis(src_lab)
        ref_means, ref_stds = self.gauss_analysis(ref_lab)
        res = (src_stds/ref_stds) * (src_lab-src_means) + ref_means

        # convert to RGB space
        res = self.lab2rgb(res)
        res = Normalizer(res).uint8_norm()

        # return the color transferred image
        return res

    def gauss_analysis(self, img):

        # compute the mean and standard deviation of each channel
        l, a, b = np.dsplit(img, 3)
        l_mean, l_std = l.mean(), l.std()
        a_mean, a_std = a.mean(), a.std()
        b_mean, b_std = b.mean(), b.std()

        # return the color statistics
        return np.array([l_mean, a_mean, b_mean]), np.array([l_std, a_std, b_std])

    def rgb2xyz(self, rgb):
        '''
        https://web.archive.org/web/20120502065620/http://cookbooks.adobe.com/post_Useful_color_equations__RGB_to_LAB_converter-14227.html
        '''

        rgb = rgb / np.max(rgb)

        for ch in range(rgb.shape[2]):
            mask = rgb[..., ch] > 0.04045
            rgb[..., ch][mask] = np.power((rgb[..., ch] + 0.055) / 1.055, 2.4)[mask]
            rgb[..., ch][~mask] /= 12.92

        rgb *= 100

        # Observer. = 2°, Illuminant = D65 (from Adobe)
        mat_adb = np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]])

        # from Reinhard et al. paper (2001)
        mat_itu = np.array([[0.4306, 0.2220, 0.0202], [0.3415, 0.7067, 0.1295], [0.1784, 0.0713, 0.9394]])

        xyz = np.dot(rgb, mat_adb)

        return xyz

    def xyz2lab(self, xyz):

        xyz[..., 0] /= REF_X
        xyz[..., 1] /= REF_Y
        xyz[..., 2] /= REF_Z

        for ch in range(xyz.shape[2]):
            mask = xyz[..., ch]>0.008856
            xyz[..., ch][mask] = np.power(xyz[..., ch], 1/3.)[mask]
            xyz[..., ch][~mask] = (7.787*xyz[..., ch] + 16/116.)[~mask]

        lab = np.zeros(xyz.shape)
        lab[..., 0] = (116 * xyz[..., 1]) - 16
        lab[..., 1] = 500 * (xyz[..., 0]-xyz[..., 1])
        lab[..., 2] = 200 * (xyz[..., 1]-xyz[..., 2])

        return lab

    def lab2xyz(self, lab):

        xyz = np.zeros(lab.shape)
        xyz[..., 1] = (lab[..., 0] + 16) / 116.
        xyz[..., 0] = lab[..., 1] / 500. + xyz[..., 1]
        xyz[..., 2] = xyz[..., 1] - lab[..., 2] / 200.

        for ch in range(xyz.shape[2]):
            mask = np.power(xyz[..., ch], 3) > 0.008856
            xyz[..., ch][mask] = np.power(xyz[..., ch], 3)[mask]
            xyz[..., ch][~mask] = (xyz[..., ch] - 16/116.)[~mask] / 7.787

        xyz[..., 0] *= REF_X
        xyz[..., 1] *= REF_Y
        xyz[..., 2] *= REF_Z

        return xyz

    def xyz2rgb(self, xyz):

        xyz /= 100.

        # Observer. = 2°, Illuminant = D65
        mat = np.array([[3.2406, -0.9689, -0.0557], [-1.5372,  1.8758, -0.204], [-0.4986, -0.0415,  1.057]])
        rgb = np.dot(xyz, mat)

        for ch in range(rgb.shape[2]):
            mask = rgb[..., ch] > 0.0031308
            rgb[..., ch][mask] = 1.055 * np.power(rgb[..., ch][mask], 1/2.4) - 0.055
            rgb[..., ch][~mask] *= 12.92

        return rgb

    def rgb2lab(self, rgb):

        xyz = self.rgb2xyz(rgb)
        lab = self.xyz2lab(xyz)

        return lab

    def lab2rgb(self, lab):
        xyz = self.lab2xyz(lab)
        rgb = self.xyz2rgb(xyz)

        return rgb
