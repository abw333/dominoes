import domino
import unittest

class TestDomino(unittest.TestCase):
    def test_init(self):
        d = domino.Domino(1, 2)

        self.assertEqual(d.first, 1)
        self.assertEqual(d.second, 2)

    def test_inverted(self):
        d = domino.Domino(1, 2)
        d_inv = d.inverted()

        self.assertEqual(d.first, d_inv.second)
        self.assertEqual(d.second, d_inv.first)

    def test_str(self):
        d = domino.Domino(1, 2)

        self.assertEqual(str(d), '[1|2]')

    def	test_repr(self):
        d = domino.Domino(1, 2)

        self.assertEqual(repr(d), '[1|2]')

if __name__ == '__main__':
    unittest.main()
