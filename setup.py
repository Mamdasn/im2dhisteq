from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


setup(
    name='im2dhisteq',
    version='0.0.6',
    author="mamdasn s",
    author_email="<mamdassn@gmail.com>",
    url="https://github.com/Mamdasn/im2dhisteq",
    description='This module attempts to enhance contrast of a given image by equalizing its two dimensional histogram.',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    include_package_data=True,
    package_dir={'': 'src'},
    py_modules=["im2dhisteq"],
    install_requires=[
        "numpy", 
        "im2dhist",
        ],
    keywords=['python', 'histogram', 'imhist', '2dhist', 'hist2d', 'im2dhisteq', 'histogram equalization', 'two dimensional histogram'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
)
