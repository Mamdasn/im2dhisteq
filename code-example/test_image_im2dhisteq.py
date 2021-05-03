import numpy as np 
from im2dhisteq import im2dhisteq
import cv2


image = cv2.imread('assets/Plane.jpg')
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image_v = image_hsv[:, :, 2].copy()

image_v_2dheq = im2dhisteq(image_v)
image_v_heq = im2dhisteq(image_v, w_neighboring=0)

image_hsv[:, :, 2] = image_v_2dheq.copy()
image_2dheq = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

image_hsv[:, :, 2] = image_v_heq.copy()
image_heq = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

cv2.imwrite('assets/Plane-im2dhisteq.jpg', image_2dheq)
cv2.imwrite('assets/Plane-imhisteq.jpg', image_heq)

