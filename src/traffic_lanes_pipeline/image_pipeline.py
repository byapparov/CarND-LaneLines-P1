import cv2
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from skimage.filters import threshold_otsu

from src.traffic_lanes_pipeline.lanes import detect_traffic_lanes
from src.traffic_lanes_pipeline.view_filter import limit_view

def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # you should return the final output (image where lines are drawn on lanes)

    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = img_grey.shape

    img_gradient = gradient_filter(img_grey)
    img_limited_view = limit_view(img_gradient)
    # return img_limited_view

    lines =  detect_edges(img_limited_view)

    lanes = detect_traffic_lanes(lines, height, width)

    # Add lanes to the output image
    img_lanes = np.copy(img_grey) * 0  # creating a blank to draw lines on

    for lane in lanes:
        for x1, y1, x2, y2 in lane:
            cv2.line(img_lanes, (x1, y1), (x2, y2), 255, 10)

    img_lanes = cv2.merge((img_lanes, np.copy(img_limited_view) * 0, np.copy(img_limited_view) * 0))

    image_tagged = image.copy()
    image_tagged = cv2.addWeighted(image_tagged, 0.8, img_lanes, 1, 0)
    # image_tagged = cv2.cvtColor(image_tagged, cv2.COLOR_BGR2RGB)
    return image_tagged


def gradient_filter(image):

    # Define a kernel size for Gaussian smoothing / blurring
    kernel_size = 5
    img_blur = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    # Edge detection with Canny filter

    high_threshold = threshold_otsu(img_blur)

    low_threshold = int(high_threshold / 2)

    img_gradient = cv2.Canny(img_blur, low_threshold, high_threshold)
    return img_gradient

def detect_edges(image):
    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 2
    theta = 2 * np.pi / 180
    threshold = 80
    min_line_length = 100
    max_line_gap = 50

    # Run Hough on edge detected image
    # OpenCV contains explanation of theory and parameters for HoughLinesP
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    lines = cv2.HoughLinesP(
        image, rho, theta, threshold, np.array([]),
        min_line_length, max_line_gap)

    return lines
