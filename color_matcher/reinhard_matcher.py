import numpy as np

from .baseclass import MatcherBaseclass

LMS_MAT = np.array([[0.3811, 0.5783, 0.0402], [0.1967, 0.7244, 0.0782], [0.0241, 0.1288, 0.8444]])
LMS_MAT_INV = np.array([[4.4679, -3.5873, 0.1193], [-1.2186, 2.3809, -0.1624], [0.0497, -0.2439, 1.2045]])


class ReinhardMatcher(MatcherBaseclass):

    def __init__(self, *args, **kwargs):
        super(ReinhardMatcher, self).__init__(*args, **kwargs)

    def reinhard(self, src: np.ndarray = None, ref: np.ndarray = None) -> np.ndarray:
        """

        This function conducts color matching based on the principles proposed by Reinhard et al.
        The paper of the original work can be found at https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf

        :param src: Source image that requires transfer
        :param ref: Palette image which serves as reference
        :param ref: Resulting image after the mapping

        :type src: :class:`~numpy:numpy.ndarray`
        :type ref: :class:`~numpy:numpy.ndarray`
        :type res: :class:`~numpy:numpy.ndarray`

        :return: **result**
        :rtype: np.ndarray

        """

        # override source and reference image with arguments (if provided)
        self._src = src if src is not None else self._src
        self._ref = ref if ref is not None else self._ref

        # get image dimensions after validating that 3 color channels are present
        m, n, p = self._src.shape if self.validate_color_chs() else self._src.shape + (1,)

        # flatten images along spatial dimensions
        src = self._src.reshape((-1, p)).transpose()
        ref = self._ref.reshape((-1, p)).transpose()

        # replace zeros with small value for numerical stability
        src[src == 0] = 1/(2**8-1)
        ref[ref == 0] = 1/(2**8-1)

        # convert to LMS color space
        lms_src = np.dot(LMS_MAT, src)
        lms_ref = np.dot(LMS_MAT, ref)

        # convert data to logarithmic LMS color space to eliminate skew
        lms_src = np.log10(lms_src)
        lms_ref = np.log10(lms_ref)

        # PCA transform matrices according to Rudermann et al.
        b = np.array([[1/np.sqrt(3), 0, 0], [0, 1/np.sqrt(6), 0], [0, 0, 1/np.sqrt(2)]])
        c = np.array([[1, 1, 1], [1, 1, -2], [1, -1, 0]])

        # convert to Lab space
        lab_src = np.dot(np.dot(b, c), lms_src)
        lab_ref = np.dot(np.dot(b, c), lms_ref)

        # compute statistical measures
        mean_src, std_src = np.mean(lab_src, axis=1), np.std(lab_src, axis=1)
        mean_ref, std_ref = np.mean(lab_ref, axis=1), np.std(lab_ref, axis=1)

        # compute ratios of standard deviations channel-wise
        std_ratios = std_ref / std_src

        # apply statistical alignment channel-wise
        res_lab = ((lab_src.T - mean_src) * std_ratios + mean_ref).T

        # convert back to LMS
        lms_res = np.dot(np.dot(c.T, b), res_lab)
        lms_res = 10**lms_res

        # convert back to RGB
        res_img = np.dot(LMS_MAT_INV, lms_res).transpose()

        # reshape to 2-D image
        res_img = res_img.reshape((m, n, p))

        return res_img
