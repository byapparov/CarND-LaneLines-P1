import cv2
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math


cap = cv2.VideoCapture('test_videos/solidWhiteRight.mp4')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test_videos_output.avi', fourcc, 20.0, (640, 480))

while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()