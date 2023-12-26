import numpy as np
import cv2
from im2dhisteq import vid2dhisteq

cap = cv2.VideoCapture("assets/Arctic-Convoy-With-Giant-Mack-Trucks.mp4")

# video without sound
video_out_name = "assets/Arctic-Convoy-With-Giant-Mack-Trucks-im2dhisteq.mp4"

i = 0
j = 0
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
Wout_list = np.zeros((10))
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    print("\r", 100 * i // length, "%", end="")

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_v = frame_hsv[:, :, 2].copy()
    image_heq, Wout = vid2dhisteq(frame_v, Wout_list=Wout_list)
    Wout_list[j] = Wout
    j += 1
    if j == 10:
        j = 0
    frame_hsv[:, :, 2] = image_heq
    frame_eq = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame = cv2.putText(
        frame,
        "Original",
        (10, 20),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    frame_eq = cv2.putText(
        frame_eq,
        "Enhanced",
        (10, 20),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    frame_frame_eq = np.concatenate((frame, frame_eq), axis=1)
    if i == 0:
        h, w, d = frame_frame_eq.shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_out = cv2.VideoWriter(video_out_name, fourcc, fps, (w, h))
    video_out.write(frame_frame_eq)

    i += 1
cv2.destroyAllWindows()
