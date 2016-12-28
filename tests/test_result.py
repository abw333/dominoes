import dominoes
import unittest

class TestResult(unittest.TestCase):
    def test_result(self):
        p = 0
        w = True
        pts = 100
        r = dominoes.Result(p, w, pts)

        self.assertEqual(r.player, p)
        self.assertEqual(r.won, True)
        self.assertEqual(r.points, pts)

if __name__ == '__main__':
    unittest.main()
