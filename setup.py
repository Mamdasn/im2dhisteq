from setuptools import setup, find_packages
import codecs
import os

parent_dir = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(parent_dir, "README.md"), encoding="utf-8") as readme:
    readme_description = "\n" + readme.read()


setup(
    name='im2dhisteq',
    version='0.0.13',
    author="mamdasn s",
    author_email="<mamdassn@gmail.com>",
    url="https://github.com/Mamdasn/im2dhisteq",
    description='This module attempts to enhance contrast of a given image by equalizing its two dimensional histogram.',
    long_description=readme_description,
    long_description_content_type = "text/markdown",
    include_package_data=True,
    package_dir={'': 'src'},
    py_modules=["im2dhisteq"],
    install_requires=[
        "numpy",
        "numba",
        "im2dhist",
        ],
    keywords=['python', 'histogram', 'image-processing', 'contrast-enhancement', 'histogram-equalization', 'image-contrast-enhancement', 'imhist', '2dhist', 'hist2d', 'im2dhisteq', 'two-dimensional-histogram'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/im2dhisteq'],
)
