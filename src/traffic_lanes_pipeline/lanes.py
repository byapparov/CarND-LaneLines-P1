import math
from src.traffic_lanes_pipeline.merge_lines import merge_lines
from src.traffic_lanes_pipeline.lane import line_angle

def detect_traffic_lanes(lines, height, width):
    lanes = merge_lines(lines, height, width)
    lanes = filter(lambda x: filter_line_angle(x.coordinates), lanes)
    return lanes


def filter_line_angle(line, threshold=25):
    angle = line_angle(line)

    # TODO this probably can be useful as a log message
    # print("Angle is updated from {angle_raw} to {angle}, pass threshold: {filter}".format(angle_raw = angle_raw, angle = angle, filter = filter))
    return angle > threshold
