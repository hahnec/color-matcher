from setuptools import setup, find_packages
from color_matcher import __version__
from sys import platform
from docutils import core
import os

APP = ['color_matcher/bin/cli.py']

FILES = [
    ('tests/data', ['tests/data/scotland_house.png']),
    ('tests/data', ['tests/data/scotland_plain.png']),
    ('tests/data', ['tests/data/scotland_pitie.png']),
]

OPTIONS = {
    "argv_emulation": True,
    "compressed": True,
    "optimize": 2,
    "excludes": ['matplotlib'],
    "plist": dict(NSHumanReadableCopyright='2020 Christopher Hahne'),
    "packages": ['numpy', 'docutils'],
}

if platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=APP,
        data_files=FILES,
        options=dict(py2app=OPTIONS),
    )
elif platform == 'win32':
    extra_options = dict(
        setup_requires=[],
        data_files=FILES,
    )
else:
    extra_options = dict(
        setup_requires=[],
        data_files=FILES,
    )

path = os.path.dirname(os.path.realpath(__file__))
# parse description section text
readme_path = os.path.join(path, 'README.rst')
with open(readme_path, "r") as f:
    data = f.read()
    readme_nodes = list(core.publish_doctree(data))
    for node in readme_nodes:
        if node.astext().startswith('Description'):
            long_description = node.astext().rsplit('\n\n')[1]

# parse package requirements from text file
reqtxt_path = os.path.join(path, 'requirements.txt')
with open(reqtxt_path, 'r') as f:
    req_list = f.read().split('\n')

setup(
    name='color-matcher',
    version=__version__,
    description='Package enabling color transfer across images',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='http://github.com/hahnec/color-matcher',
    author='Christopher Hahne',
    author_email='inbox@christopherhahne.de',
    license='GNU GPL v3',
    keywords='color match histogram matching image colour transfer',
    scripts=['color_matcher/bin/cli.py'],
    entry_points={'console_scripts': ['color-matcher=color_matcher.bin.cli:main'], },
    packages=find_packages(
        include=['color_matcher', 'color_matcher.bin', 'tests', 'tests.data']
    ),
    install_requires=req_list,
    include_package_data=True,
    python_requires='>=3',
    zip_safe=False,
    **extra_options
)
