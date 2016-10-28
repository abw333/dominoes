import domino
import unittest

class TestDomino(unittest.TestCase):
    def test_init(self):
        d = domino.Domino(1, 2)

        self.assertEqual(d.first, 1)
        self.assertEqual(d.second, 2)

if __name__ == '__main__':
    unittest.main()
