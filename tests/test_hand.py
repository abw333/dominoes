import collections.abc
import dominoes
import unittest

class TestHand(unittest.TestCase):
    def test_init(self):
        h1 = dominoes.Hand([])

        self.assertIsNotNone(h1)

        d = dominoes.Domino(1, 2)
        h2 = dominoes.Hand([d])

        self.assertIsNotNone(h2)

    def test_contains(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)

        h = dominoes.Hand([d1])

        self.assertTrue(d1 in h)
        self.assertFalse(d2 in h)

    def test_getitem(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)

        h = dominoes.Hand([d1, d2])

        self.assertEqual(h[0], d1)
        self.assertEqual(h[1], d2)

    def test_iter(self):
        h = dominoes.Hand([])

        self.assertIsInstance(h, collections.abc.Iterable)
        self.assertIsNotNone(iter(h))

    def test_eq(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)

        h1 = dominoes.Hand([])
        h2 = dominoes.Hand([])
        h3 = dominoes.Hand([d1])
        h4 = dominoes.Hand([d1])
        h5 = dominoes.Hand([d2])
        h6 = dominoes.Hand([d1, d2])
        h7 = dominoes.Hand([d1, d2])
        h8 = dominoes.Hand([d2, d1])

        self.assertEqual(h1, h2)
        self.assertEqual(h3, h4)
        self.assertEqual(h6, h7)

        self.assertNotEqual(h1, h3)
        self.assertNotEqual(h3, h5)
        self.assertNotEqual(h5, h6)
        self.assertNotEqual(h6, h8)

        class PseudoHand:
            def __init__(self, _dominoes):
                self._dominoes = _dominoes

        ph1 = PseudoHand([])
        ph2 = PseudoHand([d1])
        ph3 = PseudoHand([d1, d2])

        self.assertNotEqual(h1, ph1)
        self.assertNotEqual(h3, ph2)
        self.assertNotEqual(h6, ph3)

    def test_len(self):
        h1 = dominoes.Hand([])

        self.assertEqual(len(h1), 0)

        d = dominoes.Domino(1, 2)
        h2 = dominoes.Hand([d])

        self.assertEqual(len(h2), 1)

    def test_str(self):
        h1 = dominoes.Hand([])

        self.assertEqual(str(h1), '')

        d1 = dominoes.Domino(1, 2)
        h2 = dominoes.Hand([d1])

        self.assertEqual(str(h2), '[1|2]')

        d2 = dominoes.Domino(1, 3)
        h3 = dominoes.Hand([d1, d2])

        self.assertEqual(str(h3), '[1|2][1|3]')

    def	test_repr(self):
        h1 = dominoes.Hand([])

        self.assertEqual(repr(h1), '')

        d1 = dominoes.Domino(1, 2)
        h2 = dominoes.Hand([d1])

        self.assertEqual(repr(h2), '[1|2]')

        d2 = dominoes.Domino(1, 3)
        h3 = dominoes.Hand([d1, d2])

        self.assertEqual(repr(h3), '[1|2][1|3]')

    def test_play(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)
        d3 = dominoes.Domino(1, 4)

        h = dominoes.Hand([d1, d2, d3])

        self.assertEqual(len(h), 3)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)
        self.assertTrue(d3 in h)

        self.assertEqual(h.play(d3), 2)

        self.assertEqual(len(h), 2)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)
        self.assertFalse(d3 in h)

        self.assertRaises(dominoes.NoSuchDominoException, h.play, d3)

        self.assertEqual(len(h), 2)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)
        self.assertFalse(d3 in h)

        self.assertEqual(h.play(d1), 0)

        self.assertEqual(len(h), 1)
        self.assertFalse(d1 in h)
        self.assertTrue(d2 in h)
        self.assertFalse(d3 in h)

        self.assertEqual(h.play(d2), 0)

        self.assertEqual(len(h), 0)
        self.assertFalse(d1 in h)
        self.assertFalse(d2 in h)
        self.assertFalse(d3 in h)

    def test_draw(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)
        d3 = dominoes.Domino(1, 4)
        d4 = dominoes.Domino(1, 5)

        h = dominoes.Hand([])

        self.assertEqual(len(h), 0)
        self.assertFalse(d1 in h)
        self.assertFalse(d2 in h)
        self.assertFalse(d3 in h)
        self.assertFalse(d4 in h)

        self.assertIsNone(h.draw(d1))

        self.assertEqual(len(h), 1)
        self.assertEqual(h[0], d1)
        self.assertTrue(d1 in h)
        self.assertFalse(d2 in h)
        self.assertFalse(d3 in h)
        self.assertFalse(d4 in h)

        self.assertIsNone(h.draw(d2, 0))

        self.assertEqual(len(h), 2)
        self.assertEqual(h[0], d2)
        self.assertEqual(h[1], d1)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)
        self.assertFalse(d3 in h)
        self.assertFalse(d4 in h)

        self.assertIsNone(h.draw(d3, 1))

        self.assertEqual(len(h), 3)
        self.assertEqual(h[0], d2)
        self.assertEqual(h[1], d3)
        self.assertEqual(h[2], d1)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)
        self.assertTrue(d3 in h)
        self.assertFalse(d4 in h)

        self.assertIsNone(h.draw(d4))

        self.assertEqual(len(h), 4)
        self.assertEqual(h[0], d2)
        self.assertEqual(h[1], d3)
        self.assertEqual(h[2], d1)
        self.assertEqual(h[3], d4)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)
        self.assertTrue(d3 in h)
        self.assertTrue(d4 in h)

    def test_contains_value(self):
        self.assertFalse(dominoes.hand.contains_value(dominoes.Hand([]), 0))

        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(3, 3)

        h = dominoes.Hand([d1, d2])

        self.assertFalse(dominoes.hand.contains_value(h, 0))
        self.assertTrue(dominoes.hand.contains_value(h, 1))
        self.assertTrue(dominoes.hand.contains_value(h, 2))
        self.assertTrue(dominoes.hand.contains_value(h, 3))

if __name__ == '__main__':
    unittest.main()
