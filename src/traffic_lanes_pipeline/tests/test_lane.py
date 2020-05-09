import unittest
from src.traffic_lanes_pipeline.lane import TrafficLane, extend_line


class TestLaneMethods(unittest.TestCase):

    def test_combine_lines(self):
        lane = TrafficLane(100, 100, 0.65)

        line1 = [[66, 42, 76, 49]]
        line2 = [[47, 30, 60, 40]]

        lane.add_line(line1)
        lane.add_line(line2)

        res = lane.coordinates
        self.assertEqual(res, [[94, 65, 142, 100]])

        # case required for extended line going outside of
        # image

    def test_extend_line(self):
        line = [[2, 6, 4, 8]]
        res = extend_line(line, 10, 0.65)
        expected = [[2, 6, 6, 10]]
        self.assertEqual(res, expected)

        line = [[25, 25, 50, 50]]
        res = extend_line(line, 100, 0.5)
        expected = [[50, 50, 100, 100]]
        self.assertEqual(res, expected)

    def test_confidence_calculation(self):

        # test no overlap
        line1 = [[2, 6, 4, 8]] # covers two y points
        line2 = [[2, 2, 3, 4]] # covers two y points
        lane = TrafficLane(10, 10, 0)
        lane.add_line(line1)
        lane.add_line(line2)
        res = lane.confidence

        self.assertEqual(res, 4 / 10)

        # test overlap
        line2 = [[2, 2, 3, 8]]  # covers two y points
        line1 = [[2, 6, 4, 8]]  # covers no y points after overlap
        lane = TrafficLane(10, 10, 0)
        lane.add_line(line1)
        lane.add_line(line2)
        res = lane.confidence

        self.assertEqual(res, 6 / 10)