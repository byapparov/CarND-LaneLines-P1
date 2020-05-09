import unittest
from src.traffic_lanes_pipeline.merge_lines import merge_lines, map_lines, diff_lane_bottom_x, line_bottom_x
from src.traffic_lanes_pipeline.lane import extend_line

class TestLineMergeMethods(unittest.TestCase):

    def test_pass(self):
        return True

    def test_merge_lines(self):
        lines = [
            [[661, 424, 767, 493]],
            [[473, 301, 610, 386]],
            [[138, 539, 329, 410]],
            [[376, 377, 483, 300]],
            [[172, 529, 450, 327]]
        ]

        w = 540
        y_cut = 0.5

        res = merge_lines(lines, 540, 960, y_cut)
        for lane in res:
            x1, y1, x2, y2 = lane.coordinates[0]
            print(lane)
        res_list = [res[i].coordinates for i in range(len(res))]
        expected = [
            [[148, w, 529, w * y_cut]],
            [[423, w * y_cut, 849, w]]
        ]
        self.assertEqual(res_list, expected)

    def test_map_lines(self):
        lines = [
            [[661, 424, 767, 493]],
            [[473, 301, 610, 386]],
            [[138, 539, 329, 410]],
            [[376, 377, 483, 300]],
            [[172, 529, 450, 327]]
        ]

        res = map_lines(lines, 540, 960)

        expected = {4: 4, 3: 4, 2: 4, 1: 1, 0: 1}
        self.assertEqual(res, expected)


    def test_lane_bottom_x(self):

        # line that crosses [0,0]
        line = [[25, 25, 50, 50]]
        lane = extend_line(line, 100)
        res = line_bottom_x(lane, 100)

        self.assertEqual(res, 100)

        line = [[50, 50, 62, 75]]
        lane = extend_line(line, 100)
        print(lane)
        res = line_bottom_x(lane, 100)

        self.assertLessEqual(abs(res - 75), 1)

    def test_difference_lane_bottom_x(self):

        height: int = 100
        line1 = [[25, 25, 50, 50]]
        line2 = [[50, 50, 62, 75]]
        res = diff_lane_bottom_x(line1, line2, height)

        self.assertLessEqual(abs(res - 25), 1)

if __name__ == '__main__':
    unittest.main()
