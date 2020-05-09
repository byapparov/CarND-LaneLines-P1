import math
import numpy as np

def line_angle(line):
    x1, y1, x2, y2 = line[0]
    angle_raw = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    if angle_raw < 0:
        angle = angle_raw + 180
    else:
        angle = angle_raw

    if angle > 90:
        angle = 180 - angle
    return angle


def line_length(line):
    x1, y1, x2, y2 = line
    return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))


def extend_line(line: list, height: int, y_cut=0) -> list:
    x1, y1, x2, y2 = line[0]

    y_out = height
    y_top_out = int(height * y_cut)

    if x1 == x2:
        return [[x1, y_out, x2, y_top_out]]

    # get line parameters to calculate end points
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # TODO define what this sensitivity should be
    if abs(m) < 0.0001:
        return [[x1, y_out, x2, y_top_out]]

    x_out = int((y_out - b) / m)
    x_top_out = int((y_top_out - b) / m)

    if y1 > y2:
        return [[x_out, y_out, x_top_out, y_top_out]]
    else:
        return [[x_top_out, y_top_out, x_out, y_out]]


class TrafficLane:
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0

    h: int = 0
    w: int = 0
    y_cut = 0
    y_hits = np.zeros(0)

    def __init__(self, height: int, width: int, y_cut=0):
        self.h = height
        self.w = width
        self.y_cut = y_cut
        self._lines = []
        self.y_hits = np.zeros(height)

    def __str__(self):
        return "Number of lines {lines}, coordinates: {x1}, {y1}, {x2}, {y2}".format(
            lines=len(self._lines),
            x1=self.x1,
            y1=self.y1,
            x2=self.x2,
            y2=self.y2
        )

    def __len__(self):
        return len(self._lines)

    @property
    def confidence(self):
        hits = np.sum(self.y_hits)
        res = hits / (self.h * (1-self.y_cut))
        return res

    @property
    def lines(self):
        return self._lines

    def add_line(self, line):
        x1, y1, x2, y2 = line[0]
        i1, i2 = y1, y2
        if i1 > i2:
            i1, i2 = i2, i1

        self.y_hits[i1:i2] = 1
        self._lines.append(line[0])

    @property
    def coordinates(self):
        self.combine_lines()
        return [[self.x1, self.y1, self.x2, self.y2]]

    def combine_lines(self):
        count = 0
        x1_total = 0
        x2_total = 0
        y1_total = 0
        y2_total = 0

        total_length: int = 0

        for line in self._lines:
            count += 1
            length = line_length(line)
            total_length += length
            lane = self.extend_line([line])
            x1, y1, x2, y2 = lane[0]
            x1_total += x1 * length
            x2_total += x2 * length
            y1_total += y1 * length
            y2_total += y2 * length

        self.x1 = x1_total // total_length
        self.y1 = y1_total // total_length
        self.x2 = x2_total // total_length
        self.y2 = y2_total // total_length

        # print("Total total_length : {x1_mean}".format(x1_mean=total_length))
        # print("Total lines : {n}".format(n=count))

        # print("Total x1_total : {x1_mean}".format(x1_mean=x1_total))
        # print("Total x1 mean: {x1_mean}".format(x1_mean=self.x1))

        # print("Total x2 mean: {x2_mean}".format(x2_mean=self.x2))
        # print("Total y1 mean: {y1_mean}".format(y1_mean=self.y1))
        # print("Total y2 mean: {y2_mean}".format(y2_mean=self.y2))

    def extend_line(self, line: list) -> list:
        return extend_line(line, self.h, self.y_cut)
