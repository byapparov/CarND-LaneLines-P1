import math
import numpy as np

def merge_lines(lines):
    angles = map_lines(lines)
    res_list = {}
    for key, value in angles.items():
        if not value in res_list:
            res_list[value] = []
        res_list[value].append(key)

    res = {}

    for key, value in res_list.items():
        res[key] = combine_lines([lines[i] for i in value])

    return list(res.values())

def map_lines(lines):
    res = []
    angles_map = dict()

    for i in range(len(lines)):
        angles_map[i] = i

    for i in range(len(lines)):
        for j in range(len(lines)):
            if i < j:
                if angles_map[i] == i:
                    angle = diff_angle(lines[i], lines[j])
                    if angle <= 5:
                        angles_map[j] = i

    return angles_map


def combine_lines(lines):
    count = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]

        if count == 0:
            res_x1, res_x2, res_y1, res_y2 = x1, x2, y1, y2

        res_x1 = min(res_x1, x1)
        res_x2 = max(res_x2, x2)

        if y2 - y1 > 0:
            res_y1 = min(y1, res_y1)
            res_y2 = max(y2, res_y2)
        else:
            res_y1 = max(y1, res_y1)
            res_y2 = min(y2, res_y2)

        count += 1
    return ([[res_x1, res_y1, res_x2, res_y2]])


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


