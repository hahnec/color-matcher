#!/usr/bin/env bash

# upgrade twine
python3 -m pip install --user --upgrade twine

# remove build and dist folder
sudo rm -rf build dist

# bundle pypi package
#python3 ../setup.py sdist
python3 setup.py sdist bdist_wheel

# occupy colour-matcher (cos of similar name)
for file in dist/color_matcher-*; do sudo cp -a $file "dist/colour_matcher-"$(echo $file | sed 's/.*matcher-//'); done

# test upload and download
python3 -m twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ color_matcher

# production upload and download
python3 -m twine upload dist/*
python3 -m pip install color_matcher
