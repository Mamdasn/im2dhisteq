from setuptools import setup, find_packages
import os

parent_dir = os.path.abspath(os.path.dirname(__file__))

def get_version():
    with open(os.path.join(parent_dir, "src", "im2dhisteq", "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split("=")[1].strip(" '\"")

def get_readme():
    with open(os.path.join(parent_dir, "README.md"), encoding="utf-8") as readme:
        readme_description = "\n" + readme.read()
        return readme_description


setup(
    name="im2dhisteq",
    version=get_version(),
    author="Mamdasan Sabrian",
    author_email="<reach.s.farhad@gmail.com>",
    url="https://github.com/Mamdasn/im2dhisteq",
    description="This module attempts to enhance contrast of a given image by equalizing its two dimensional histogram.",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    py_modules=["im2dhisteq"],
    install_requires=[
        "numpy",
        "numba",
        "im2dhist",
        "opencv-python",
        "tqdm",
    ],
    keywords=[
        "python",
        "histogram",
        "image-processing",
        "contrast-enhancement",
        "histogram-equalization",
        "image-contrast-enhancement",
        "imhist",
        "2dhist",
        "hist2d",
        "im2dhisteq",
        "two-dimensional-histogram",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/im2dhisteq", "bin/vid2dhisteq"],
)
