import unittest
from src.traffic_lanes_pipeline.lanes import extend_line, filter_lanes

class TestLanesMethods(unittest.TestCase):

    def test_extend_line(self):
        line = [[2, 6, 4, 8]]
        res = extend_line(line, 10, 10)
        expected = [[2, 6, 6, 10]]
        self.assertEqual(res, expected)

    def test_filter_lanes(self):
        lane = [[136, 540, 414, 351]]

        self.assertTrue(filter_lanes(lane))
        lane = [[553, 351, 860, 540]]

        self.assertTrue(filter_lanes(lane))

        # Near horisontal line 1 (negative angle)
        lane = [[553, 351, 860, 340]]
        self.assertFalse(filter_lanes(lane))

        # Near horisontal line 2 (positive angle)
        lane = [[553, 340, 860, 300]]
        self.assertFalse(filter_lanes(lane))

        # 45 degrees line
        lane = [[100, 100, 300, 300]]
        self.assertTrue(filter_lanes(lane))

        # a near verticle line
        lane = [[550, 340, 551, 300]]
        self.assertTrue(filter_lanes(lane))

        # verticle line
        lane = [[550, 340, 550, 300]]
        self.assertTrue(filter_lanes(lane))
