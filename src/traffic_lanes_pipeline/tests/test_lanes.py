import unittest
from src.traffic_lanes_pipeline.lanes import filter_line_angle


class TestLanesMethods(unittest.TestCase):

    def test_filter_lanes(self):

        line = [[136, 540, 414, 351]]
        self.assertTrue(filter_line_angle(line))

        lane = [[553, 351, 860, 540]]
        self.assertTrue(filter_line_angle(lane))

        # Near horizontal line 1 (negative angle)
        lane = [[553, 351, 860, 340]]
        self.assertFalse(filter_line_angle(lane))

        # Near horizontal line 2 (positive angle)
        lane = [[553, 340, 860, 300]]
        self.assertFalse(filter_line_angle(lane))

        # 45 degrees line
        lane = [[100, 100, 300, 300]]
        self.assertTrue(filter_line_angle(lane))

        # a near vertical line
        lane = [[550, 340, 551, 300]]
        self.assertTrue(filter_line_angle(lane))

        # vertical line
        lane = [[550, 340, 550, 300]]
        self.assertTrue(filter_line_angle(lane))
