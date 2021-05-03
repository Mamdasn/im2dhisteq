from im2dhisteq import im2dhisteq
import numpy as np 
import cv2
import os

filename = 'assets/cloudy-day.jpg'
filename = 'assets/Plane.jpg'

name, ext = os.path.splitext(filename)
image = cv2.imread(filename)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image_v = image_hsv[:, :, 2].copy()

image_v_2dheq = im2dhisteq(image_v)
image_v_heq = im2dhisteq(image_v, w_neighboring=0)

image_hsv[:, :, 2] = image_v_2dheq.copy()
image_2dheq = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

image_hsv[:, :, 2] = image_v_heq.copy()
image_heq = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

cv2.imwrite(f'{name}-im2dhisteq{ext}', image_2dheq)
cv2.imwrite(f'{name}-imhisteq{ext}', image_heq)

