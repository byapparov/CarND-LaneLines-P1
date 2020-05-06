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
    """Makes a dictionary of lists mapping lines with close angles"""
    res = []
    angles_map = dict()

    # Getting sorted index taken here:
    # https://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
    sorted_lines_index = sorted(((e,i) for i,e in enumerate(lines)), key= lambda x: line_angle(x[0]))
    sorted_lines_index = [x[1] for x in sorted_lines_index]
    # print("Sorted Lines Index: {sorted_lines_index}".format(sorted_lines_index = sorted_lines_index))
    lines = sort_lines(lines)

    current_line = 0
    difference = 0
    for i in range(len(lines)):
        if i > 0:
            difference = diff_angle(lines[i], lines[i - 1])
            if difference > 3:
                current_line = i

        angles_map[sorted_lines_index[i]] = sorted_lines_index[current_line]

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


