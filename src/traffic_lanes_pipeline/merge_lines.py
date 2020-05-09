import math
import numpy as np
from src.traffic_lanes_pipeline.lane import TrafficLane, extend_line


def merge_lines(lines, height, width, y_cut=0.65):
    angles = map_lines(lines, height, width)
    res_list = {}
    for key, value in angles.items():
        if not value in res_list:
            res_list[value] = []
        res_list[value].append(key)

    res = {}
    for key, value in res_list.items():
        lane = TrafficLane(height, width, y_cut)
        for i in value:
            lane.add_line(lines[i])
        res[key] = lane
    return list(res.values())


def map_lines(lines, height, width):
    """Makes a dictionary of lists mapping lines with close angles"""
    res = []
    angles_map = dict()

    # Getting sorted index taken here:
    # https://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
    sorted_lines_index = sorted(((e, i) for i, e in enumerate(lines)), key=lambda x: line_angle(x[0]))
    sorted_lines_index = [x[1] for x in sorted_lines_index]
    # print("Sorted Lines Index: {sorted_lines_index}".format(sorted_lines_index = sorted_lines_index))
    lines = sort_lines(lines)

    current_line = 0
    angle_difference = 0
    x_difference = 0
    angle_threshold = 5
    x_bottom_distance_threshold = width // 30
    for i in range(len(lines)):
        if i > 0:
            angle_difference = diff_angle(lines[i], lines[i - 1])
            x_bottom_distance = diff_lane_bottom_x(lines[i], lines[i - 1], height)
            # print("Lines are different angle {angle} and away from each other by {x}".format(
            #   angle = angle_difference,
            #   x = x_bottom_distance
            # ))
            if angle_difference > angle_threshold or x_bottom_distance > x_bottom_distance_threshold:
                current_line = i

        angles_map[sorted_lines_index[i]] = sorted_lines_index[current_line]

    return angles_map


def line_angle(line):
    x1, y1, x2, y2 = line[0]
    angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    return angle


def sort_lines(lines):
    return sorted(lines, key=line_angle)


def diff_angle(line1, line2):
    angle1 = line_angle(line1)
    angle2 = line_angle(line2)
    return abs(angle2 - angle1)


def diff_lane_bottom_x(line1, line2, height):
    x1 = line_bottom_x(line1, height)
    x2 = line_bottom_x(line2, height)
    return abs(x2 - x1)


def line_bottom_x(line, height):
    lane = extend_line(line, height)
    x1, y1, x2, y2 = lane[0]
    if y1 > y2:
        return x1
    else:
        return x2
