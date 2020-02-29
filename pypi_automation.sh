#!/usr/bin/env bash

# upgrade twine
python3 -m pip install --user --upgrade twine

# remove build and dist folder
sudo rm -rf build dist

# bundle pypi package
sudo python3 setup.py sdist bdist_wheel

# test upload and download
python3 -m twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ color-matcher

# production upload and download
python3 -m twine upload dist/*
python3 -m pip install color-matcher

# auto-update colour-matcher (cos of similar name)
sed -i '' 's/color-matcher/colour-matcher/' setup.py
sudo python3 setup.py sdist bdist_wheel
sed -i '' 's/colour-matcher/color-matcher/' setup.py
#for file in dist/color_matcher-*; do sudo cp -a $file "dist/colour_matcher-"$(echo $file | sed 's/.*matcher-//'); done
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*
