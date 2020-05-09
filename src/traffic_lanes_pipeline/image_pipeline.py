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
    canvas = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lanes_grey = image_traffic_lanes(image)
    lanes_saturation = image_traffic_lanes(image, use_saturation = True)

    # Add lanes to the output image
    img_lanes_grey = np.copy(canvas) * 0  # creating a blank to draw lines on

    for lane in lanes_grey:
        if lane.confidence >= 0.25:
            x1, y1, x2, y2 = lane.coordinates[0]
            cv2.line(img_lanes_grey, (x1, y1), (x2, y2), 255, 10)

    img_lanes_grey = cv2.merge((img_lanes_grey, np.copy(canvas) * 0, np.copy(canvas) * 0))

    img_lanes_saturation = np.copy(canvas) * 0  # creating a blank to draw lines on

    for lane in lanes_saturation:
        if lane.confidence >= 0.40:
            x1, y1, x2, y2 = lane.coordinates[0]
            cv2.line(img_lanes_saturation, (x1, y1), (x2, y2), 255, 10)
    img_lanes_saturation = cv2.merge((np.copy(canvas) * 0, np.copy(canvas) * 0, img_lanes_saturation * 100))

    image_tagged = image.copy()
    image_tagged = cv2.addWeighted(image_tagged, 0.8, img_lanes_grey, 1, 0)
    image_tagged = cv2.addWeighted(image_tagged, 0.8, img_lanes_saturation, 1, 0)
    # image_tagged = cv2.cvtColor(image_tagged, cv2.COLOR_BGR2RGB)
    return image_tagged


def image_traffic_lanes(image, use_saturation = False):
    img_gradient_grey = gradient_filter(image)
    if use_saturation:
        img_gradient_saturation = gradient_filter(image, color_filter=color_filter_saturation)
        img_gradient = cv2.add(
            img_gradient_grey,
            img_gradient_saturation
        )
    else:
        img_gradient = img_gradient_grey

    img_limited_view = limit_view(img_gradient, ratio = 0.45)
    # return img_limited_view

    lines = detect_edges(img_limited_view)

    height, width = img_gradient.shape

    lanes = detect_traffic_lanes(lines, height, width)
    return lanes


def color_filter_grey(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return result


def gradient_filter(image, color_filter = color_filter_grey):
    img_grey = color_filter(image)

    # Define a kernel size for Gaussian smoothing / blurring
    kernel_size = 5
    img_blur = cv2.GaussianBlur(img_grey, (kernel_size, kernel_size), 0)

    # Edge detection with Canny filter

    high_threshold = threshold_otsu(img_blur)

    low_threshold = int(high_threshold / 2)

    img_gradient = cv2.Canny(img_blur, low_threshold, high_threshold)
    return img_gradient


def detect_edges(image):
    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    height, width = image.shape
    rho = 1
    theta = np.pi / 180
    threshold = int(height * 0.10)
    min_line_length = int(height * 0.10)
    max_line_gap = min_line_length

    # Run Hough on edge detected image
    # OpenCV contains explanation of theory and parameters for HoughLinesP
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    lines = cv2.HoughLinesP(
        image, rho, theta, threshold, np.array([]),
        min_line_length, max_line_gap)

    return lines


def color_filter_saturation(image):
    # this function improves detection
    # of the yellow line specifically
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # set hue and value channels to 0
    image_hsv[:, :, 0] = 0
    image_hsv[:, :, 2] = 0

    result = cv2.cvtColor(image_hsv, cv2.COLOR_BGR2GRAY)
    return result
