import unittest
from src.lines_processing.merge_lines import merge_lines, combine_lines, map_lines, extend_line

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
            [[473, 301, 767, 493]],
            [[138, 539, 483, 300]]
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
        expected = {0: 0, 1: 0, 2: 2, 3: 2, 4: 2}
        self.assertEqual(res, expected)

    def test_combine_lines(self):
        line1 = [[66, 42, 76, 49]]
        line2 = [[47, 30, 60, 40]]

        res = combine_lines([line1, line2])
        self.assertEqual(res, [[47, 30, 76, 49]])

    def test_extend_line(self):
        line = [[2, 6, 4, 8]]
        res = extend_line(line, 10)
        expected = [[2, 6, 6,10]]
        self.assertEqual(res, expected)

        # case required for extended line going outside of
        # image 


if __name__ == '__main__':
    unittest.main()