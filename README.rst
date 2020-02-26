============
ColorMatcher
============

Description
-----------

*ColorMatcher* is a Python package to enable color transfer across images.
It can be used for automatic color-grading of photographs or film sequences.

Results
-------

.. list-table::
   :widths: 8 8 8

   * - |src|
     - |ref|
     - |res|
   * - Source image
     - Target image
     - Result

Installation
------------

* via pip:
    1. install with ``pip3 install color_matcher``
    2. type ``color_matcher -h`` to the command line once installation finished

|

* from source:
    1. install Python from https://www.python.org/
    2. download the source_ using ``git clone https://github.com/hahnec/color_matcher.git``
    3. go to the root directory ``cd color_matcher``
    4. install with ``python3 setup.py install``
    5. if installation ran smoothly, enter ``color_matcher -h`` to the command line

Command Line Usage
==================

From the root directory of your downloaded repo, you can type

``color_matcher -s './test/data/scotland_house.png' -r './test/data/scotland_plain.png'``

on a UNIX system. A windows equivalent command may be

``color_matcher --src=".\\test\\data\\scotland_house.png" --ref=".\\test\\data\\scotland_plain.png"``

Alternatively, you can specify the method or select your images manually with

``color_matcher --win --method='hm-mkl-hm'``

More information on optional arguments, can be found using the help parameter

``color_matcher -h``

Credits
-------

`Francois Pitie <http://francois.pitie.net/>`__

`Christopher Hahne <http://www.christopherhahne.de/>`__

.. Hyperlink aliases

.. _source: https://github.com/hahnec/color_matcher/archive/master.zip

.. |src| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color_matcher/master/test/data/scotland_house.png" height="187px" max-width:"100%">

.. |ref| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color_matcher/master/test/data/scotland_plain.png" height="187px" max-width:"100%">

.. |res| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color_matcher/master/test/data/scotland_pitie.png" height="187px" max-width:"100%">
