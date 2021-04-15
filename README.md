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

```python
import numpy as np
import cv2
from im2dhisteq import im2dhisteq

def imresize(img, wr=500, hr=None): # This is just for imshow-ing images with titles
    [ h, w] = img.shape
    hr = (h*wr)//w if not hr else hr
    img_resized = cv2.resize(img, dsize=(wr, hr))
    return img_resized

def main():
    fullname = 'Plane.jpg'
    image = cv2.imread(fullname)
    # convert rgb image to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # w_neighboring=6 is generally an adequate value, drived by a lot of experimenting.
    # w_neighboring=6 corresponds to a 13*13 square
    gray_image_2DHisteq = im2dhisteq(gray_image, w_neighboring=6)
    
    # This is just for imshow-ing images with titles
    gray_Image_resized = imresize(gray_image)
    gray_Image_2DHisteq_resized = imresize(gray_image_2DHisteq)

    cv2.imshow('Original Image', gray_Image_resized)
    cv2.imshow('2DHeq Image', gray_Image_2DHisteq_resized)
    cv2.waitKey(0)

if __name__ == '__main__': main()
```

## Showcase
This is a sample image and its corresponding 2D-Histogram Equalized image.
![Plane.jpg Image](https://raw.githubusercontent.com/Mamdasn/im2dhisteq/main/assets/Original-Image.jpg "Plane.jpg Image")  
![corresponding 2D-Histogram Equalized image](https://raw.githubusercontent.com/Mamdasn/im2dhisteq/main/assets/2DHeq-Image.jpg "corresponding 2D-Histogram Equalized image")  
