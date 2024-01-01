[![PyPI Latest Release](https://img.shields.io/pypi/v/im2dhisteq.svg)](https://pypi.org/project/im2dhisteq/) [![Package Status](https://img.shields.io/pypi/status/im2dhisteq.svg)](https://pypi.org/project/im2dhisteq/) [![Downloads](https://pepy.tech/badge/im2dhisteq)](https://pepy.tech/project/im2dhisteq) [![License](https://img.shields.io/pypi/l/im2dhisteq.svg)](https://github.com/Mamdasn/im2dhisteq/blob/main/LICENSE) ![Repository Size](https://img.shields.io/github/repo-size/mamdasn/im2dhisteq)

# im2dhisteq
This module attempts to enhance contrast of a given image by equalizing its two dimensional histogram. An easy way to enhance quality of a given image is to just equalize its histogram, but despite using minimum resources and a very short process time, there are a lot of drawbacks to it.
One of the ways to tackle drawbacks of `histogram equalization method` is to instead equalize the image's `two dimensional histogram`, as one dimensional histogram of a given image does not contain the image's contextual information. Tests on a multitude of images has shown, by taking contextual information of an image in addition to the image's histogram into account when attempting to enhance contrast, output images are significantly better in quality in compare to histogram equalizaion and a handful of other known methods.

You can access the article that came up with this method [here](https://www.researchgate.net/publication/256822485_Two-dimensional_histogram_equalization_and_contrast_enhancement).

## Two Dimensional Histogram
[Here](https://github.com/Mamdasn/im2dhist) is the source code for the im2dhist python library with a short description on how it's done.

## Installation

Run the following to install:

```python
pip install im2dhisteq
```

## Usage

For images
```Bash
im2dhisteq --input 'cloudy-day.jpg' --output 'assets/cloudy-day-2dhisteq.jpg' --w 6
```
For videos
```Bash
vid2dhisteq --input 'video-input.mp4' --output 'video-output-enhanced.mp4' --w 6
```
### Speed up
The speed of the program can be significantly increased if the go library `lib-im2dhist.go` in src/go_libs in the package is compiled and moved to a dir in the system path. To compile, simply install `go`. Then run
```Bash
go mod init lib-im2dhist.go
go mod tidy
```
followed by running the script `make-library`.

## Showcase
* A one minute comparative video: https://youtu.be/7LrzX2ZpLAQ
* This is a sample image and its corresponding 2d-histogram equalized image.
![cloudy-day-original-im2dhisteq.jpg Image](https://raw.githubusercontent.com/Mamdasn/im2dhisteq/main/assets/cloudy-day-original-im2dhisteq.jpg "cloudy-day-original-im2dhisteq.jpg Image")
