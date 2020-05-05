import math
from src.traffic_lanes_pipeline.merge_lines import merge_lines

def detect_traffic_lanes(lines, height, width):
    lines = merge_lines(lines)
    lanes = []
    for line in lines:
        lanes.append(extend_line(line, height, width))

    lanes = filter(filter_lanes, lanes)
    return lanes


def extend_line(line, h, w, y_cut = 0.65):
    x1, y1, x2, y2 = line[0]

    y_out = h
    y_top_out = int(h * y_cut)

    if (x1 == x2):
        return [[x1, y_out, x2, y_top_out]]

    # get line parameters to calculate end points
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # TODO define what this sensitivity should be
    if (abs(m) < 0.0001):
        return [[x1, y_out, x2, y_top_out]]

    x_out = int((y_out - b) / m)
    x_top_out = int((y_top_out - b) / m)

    if y1 > y2:
        return [[x_out, y_out, x_top_out, y_top_out]]
    else:
        return [[x_top_out, y_top_out, x_out, y_out]]

def filter_lanes(lane, threshold = 25):
    x1, y1, x2, y2 = lane[0]
    angle_raw = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    if angle_raw < 0:
        angle = angle_raw + 180
    else:
        angle = angle_raw

    if angle > 90:
        angle = 180 - angle

    filter = angle > threshold
    # TODO this probably can be useful as a log message
    # print("Angle is updated from {angle_raw} to {angle}, pass threshold: {filter}".format(angle_raw = angle_raw, angle = angle, filter = filter))
    return angle > threshold