import collections
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

    def test_eq(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(1, 2)
        d3 = domino.Domino(2, 1)

        # order of values does not matter
        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

        d4 = domino.Domino(1, 1)
        d5 = domino.Domino(1, 1)

        # it's OK if both values are the same
        self.assertEqual(d4, d5)

        # both values must be the same
        self.assertNotEqual(d1, d4)

        PseudoDomino = collections.namedtuple('PseudoDomino',
                                              ['first', 'second'])
        pd = PseudoDomino(1, 2)

        # needs to be a real Domino instance
        self.assertNotEqual(d1, pd)

    def test_hash(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(2, 1)
        d3 = domino.Domino(1, 3)

        d_set = {d1}

        self.assertTrue(d1 in d_set)
        self.assertTrue(d2 in d_set)
        self.assertFalse(d3 in d_set)

    def test_contains(self):
        d = domino.Domino(1, 2)

        self.assertTrue(1 in d)
        self.assertTrue(2 in d)
        self.assertFalse(3 in d)

if __name__ == '__main__':
    unittest.main()
