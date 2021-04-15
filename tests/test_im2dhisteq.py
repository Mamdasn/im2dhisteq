from im2dhisteq import im2dhisteq
from im2dhist import im2dhist
import cv2
import numpy as np

def test_im2dhisteq_with_param():
    image_name = '../assets/Plane.jpg'
    image = cv2.imread(image_name)
    # convert rgb image to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    gray_image_2DHisteq = im2dhisteq(gray_image, w_neighboring=6)
    

    #np.save(f'{image_name}-2D-Histogram-Equalized', gray_image_2DHisteq)
    gray_image_2DHisteq_cmpr = np.load(f'{image_name}-2D-Histogram-Equalized.npy')
    assert np.all(gray_image_2DHisteq == gray_image_2DHisteq_cmpr)
#test_im2dhisteq_with_param()
