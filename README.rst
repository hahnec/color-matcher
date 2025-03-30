=============
color-matcher
=============

Description
-----------

*color-matcher* enables color transfer across images which comes in handy for automatic color-grading
of photographs, paintings and film sequences as well as light-field and stopmotion corrections. The methods behind
the mappings are based on the approach from Reinhard *et al.*, the Monge-Kantorovich Linearization (MKL) as proposed by
Pitie *et al.* and our analytical solution to a Multi-Variate Gaussian Distribution (MVGD) transfer in conjunction with
classical histogram matching. As shown below our HM-MVGD-HM compound outperforms existing methods.

|release| |license| |build_github| |coverage| |pypi_total| |pypi|

|binder|

|hf_spaces|

Results
-------

|vspace|

.. list-table::
   :widths: 1 2 2 2
   :header-rows: 1
   :stub-columns: 1

   * -
     - Source
     - Target
     - Result
   * - Photograph
     - |src_photo|
     - |ref_photo|
     - |res_photo|
   * - Film sequence
     - |src_seq|
     - |ref_seq|
     - |res_seq|
   * - Light-field correction
     - |src_lfp|
     - |ref_lfp|
     - |res_lfp|
   * - Paintings
     - |src_paint|
     - |ref_paint|
     - |res_paint|

|

Installation
------------

* via pip:
    1. install with ``pip3 install color-matcher``
    2. type ``color-matcher -h`` to the command line once installation finished

* from source:
    1. install Python from https://www.python.org/
    2. download the source_ using ``git clone https://github.com/hahnec/color-matcher.git``
    3. go to the root directory ``cd color-matcher``
    4. load dependencies ``$ pip3 install -r requirements.txt``
    5. install with ``python3 setup.py install``
    6. if installation ran smoothly, enter ``color-matcher -h`` to the command line

CLI Usage
---------

From the root directory of your downloaded repo, you can run the tool on the provided test data by

``color-matcher -s './tests/data/scotland_house.png' -r './tests/data/scotland_plain.png'``

on a UNIX system where the result is found at ``./tests/data/``. A windows equivalent of the above command is

``color-matcher --src=".\\tests\\data\\scotland_house.png" --ref=".\\tests\\data\\scotland_plain.png"``

Alternatively, you can specify the method or select your images manually with

``color-matcher --win --method='hm-mkl-hm'``

Note that batch processing is possible by passing a source directory, e.g., via

``color-matcher -s './tests/data/' -r './tests/data/scotland_plain.png'``

More information on optional arguments, can be found using the help parameter

``color-matcher -h``

API Usage
---------

.. code-block:: python

    from color_matcher import ColorMatcher
    from color_matcher.io_handler import load_img_file, save_img_file, FILE_EXTS
    from color_matcher.normalizer import Normalizer
    import os

    img_ref = load_img_file('./tests/data/scotland_plain.png')

    src_path = '.'
    filenames = [os.path.join(src_path, f) for f in os.listdir(src_path)
                         if f.lower().endswith(FILE_EXTS)]

    cm = ColorMatcher()
    for i, fname in enumerate(filenames):
        img_src = load_img_file(fname)
        img_res = cm.transfer(src=img_src, ref=img_ref, method='mkl')
        img_res = Normalizer(img_res).uint8_norm()
        save_img_file(img_res, os.path.join(os.path.dirname(fname), str(i)+'.png'))


.. Hyperlink aliases

.. _source: https://github.com/hahnec/color-matcher/archive/master.zip

.. |src_photo| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/scotland_house.png" max-width="100%">

.. |ref_photo| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/scotland_plain.png" max-width="100%">

.. |res_photo| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/scotland_pitie.png" max-width="100%">

.. |src_paint| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/parismusees/cezanne_paul_trois_baigneuses.png" max-width="100%">

.. |ref_paint| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/parismusees/cezanne_paul_portrait_dambroise_vollard.png" max-width="100%">

.. |res_paint| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/parismusees/cezanne_paul_trois_baigneuses_mvgd.png" max-width="100%">

.. |src_seq| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/wave.gif" max-width="100%">

.. |ref_seq| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/sunrise.png" max-width="100%">

.. |res_seq| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/wave_mvgd.gif" max-width="100%">

.. |src_lfp| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/view_animation_7px.gif" max-width="100%">

.. |ref_lfp| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/bee_2.png" max-width="100%">

.. |res_lfp| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/tests/data/view_animation_7px_hm-mkl-hm.gif" max-width="100%">

.. |vspace| raw:: latex

   \vspace{1mm}

.. |metric_chart| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/develop/docs/img/hist+wasser_dist.svg" max-width="100%" align="center">

.. |metric_latex| raw:: latex

    W_1 = \int_{0}^{\infty} \left| F\left(\mathbf{r}^{(g)}\right) - F\left(\mathbf{z}^{(g)}\right) \right|_1 \, \mathrm{d}k

    D_2 = \left\| f(\mathbf{r}) - f(\mathbf{z}) \right\|_2

.. |metric_eqs| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/develop/docs/img/distance_metrics.svg" max-width="100%" align="center">


.. Image substitutions

.. |release| image:: https://img.shields.io/github/v/release/hahnec/color-matcher?style=square
    :target: https://github.com/hahnec/color-matcher/releases/
    :alt: release

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3.0-orange.svg?style=square
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License

.. |build_travis| image:: https://img.shields.io/travis/com/hahnec/color-matcher?style=square
    :target: https://travis-ci.com/github/hahnec/color-matcher

.. |build_github| image:: https://img.shields.io/github/actions/workflow/status/hahnec/color-matcher/gh_actions.yml?branch=master&style=square
    :target: https://github.com/hahnec/color-matcher/actions
    :alt: GitHub Workflow Status

.. |coverage| image:: https://img.shields.io/coveralls/github/hahnec/color-matcher?style=square
    :target: https://coveralls.io/github/hahnec/color-matcher

.. |pypi| image:: https://img.shields.io/pypi/dm/color-matcher?label=PyPI%20downloads&style=square
    :target: https://pypi.org/project/color-matcher/
    :alt: PyPI Downloads

.. |pypi_total| image:: https://pepy.tech/badge/color-matcher?style=flat-square
    :target: https://pepy.tech/project/color-matcher
    :alt: PyPi Dl2

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/hahnec/color-matcher/master?labpath=01_api_demo.ipynb

.. |paper| image:: http://img.shields.io/badge/paper-arxiv.2010.11687-red.svg?style=flat-square
    :target: https://arxiv.org/pdf/2010.11687.pdf
    :alt: arXiv link

.. |hf_spaces| image:: https://huggingface.co/datasets/huggingface/badges/resolve/main/deploy-on-spaces-md-dark.svg
   :target: http://www.hahne.website/color_matcher.html
   :alt: Deploy on Spaces

Experimental results
--------------------

|metric_chart|

The above diagram illustrates light-field color consistency from Wasserstein metric :math:`W_1` and histogram distance
:math:`D_2` where low values indicate higher similarity between source :math:`\mathbf{r}` and target :math:`\mathbf{z}`.
These distance metrics are computed as follows

|metric_eqs|

where :math:`f(k,\cdot)` and :math:`F(k,\cdot)` represent the Probability Density Function (PDF) and Cumulative Density Function (CDF) at intensity level :math:`k`, respectively.
More detailed information can be found in `our IEEE paper <https://arxiv.org/pdf/2010.11687.pdf>`__.

|vspace|

Citation
--------

.. code-block:: BibTeX

    @ARTICLE{plenopticam,
        author={Hahne, Christopher and Aggoun, Amar},
        journal={IEEE Transactions on Image Processing},
        title={PlenoptiCam v1.0: A Light-Field Imaging Framework},
        year={2021},
        volume={30},
        number={},
        pages={6757-6771},
        doi={10.1109/TIP.2021.3095671}
    }

Author
------

`Christopher Hahne <http://www.christopherhahne.de/>`__
