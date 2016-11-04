import collections
import domino
import unittest

class TestHand(unittest.TestCase):
    def test_init(self):
        h1 = domino.Hand([])

        self.assertIsNotNone(h1)

        d = domino.Domino(1, 2)
        h2 = domino.Hand([d])

        self.assertIsNotNone(h2)

    def test_contains(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(1, 3)

        h = domino.Hand([d1])

        self.assertTrue(d1 in h)
        self.assertFalse(d2 in h)

    def test_getitem(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(1, 3)

        h = domino.Hand([d1, d2])

        self.assertEqual(h[0], d1)
        self.assertEqual(h[1], d2)

    def test_iter(self):
        h = domino.Hand([])

        self.assertIsInstance(h, collections.Iterable)
        self.assertIsNotNone(iter(h))

    def test_len(self):
        h1 = domino.Hand([])

        self.assertEqual(len(h1), 0)

        d = domino.Domino(1, 2)
        h2 = domino.Hand([d])

        self.assertEqual(len(h2), 1)

    def test_str(self):
        h1 = domino.Hand([])

        self.assertEqual(str(h1), '')

        d1 = domino.Domino(1, 2)
        h2 = domino.Hand([d1])

        self.assertEqual(str(h2), '[1|2]')

        d2 = domino.Domino(1, 3)
        h3 = domino.Hand([d1, d2])

        self.assertEqual(str(h3), '[1|2][1|3]')

    def	test_repr(self):
        h1 = domino.Hand([])

        self.assertEqual(repr(h1), '')

        d1 = domino.Domino(1, 2)
        h2 = domino.Hand([d1])

        self.assertEqual(repr(h2), '[1|2]')

        d2 = domino.Domino(1, 3)
        h3 = domino.Hand([d1, d2])

        self.assertEqual(repr(h3), '[1|2][1|3]')

    def test_play(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(1, 3)

        h = domino.Hand([d1, d2])

        self.assertEqual(len(h), 2)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)

        h.play(d1)

        self.assertEqual(len(h), 1)
        self.assertFalse(d1 in h)
        self.assertTrue(d2 in h)

        self.assertRaises(domino.NoSuchDominoException, h.play, d1)

        self.assertEqual(len(h), 1)
        self.assertFalse(d1 in h)
        self.assertTrue(d2 in h)

        h.play(d2)

        self.assertEqual(len(h), 0)
        self.assertFalse(d1 in h)
        self.assertFalse(d2 in h)

    def test_draw(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(1, 3)

        h = domino.Hand([])

        self.assertEqual(len(h), 0)
        self.assertFalse(d1 in h)
        self.assertFalse(d2 in h)

        h.draw(d2)

        self.assertEqual(len(h), 1)
        self.assertFalse(d1 in h)
        self.assertTrue(d2 in h)

        h.draw(d1)

        self.assertEqual(len(h), 2)
        self.assertTrue(d1 in h)
        self.assertTrue(d2 in h)

if __name__ == '__main__':
    unittest.main()
