import unittest
from src.traffic_lanes_pipeline.merge_lines import merge_lines, combine_lines, map_lines

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

        res = merge_lines(lines)
        expected = [
            [[138, 539, 483, 300]],
            [[473, 301, 767, 493]]
        ]
        self.assertEqual(res, expected)

    def test_map_lines(self):

        lines = [
            [[661, 424, 767, 493]],
            [[473, 301, 610, 386]],
            [[138, 539, 329, 410]],
            [[376, 377, 483, 300]],
            [[172, 529, 450, 327]]
        ]

        res = map_lines(lines)

        expected = {4: 4, 3: 4, 2: 4, 1: 1, 0: 1}
        self.assertEqual(res, expected)

    def test_combine_lines(self):
        line1 = [[66, 42, 76, 49]]
        line2 = [[47, 30, 60, 40]]

        res = combine_lines([line1, line2])
        self.assertEqual(res, [[47, 30, 76, 49]])

        # case required for extended line going outside of
        # image



if __name__ == '__main__':
    unittest.main()