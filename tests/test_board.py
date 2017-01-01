import collections
import dominoes
import unittest

class TestBoard(unittest.TestCase):
    def test_init(self):
        b = dominoes.Board()

        self.assertIsNotNone(b.board)
        self.assertEqual(len(b), 0)
        self.assertRaises(dominoes.EmptyBoardException, b.left_end)
        self.assertRaises(dominoes.EmptyBoardException, b.right_end)
        self.assertEqual(str(b), '')
        self.assertEqual(repr(b), '')

    def test_eq(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)
        d3 = dominoes.Domino(2, 3)

        b1 = dominoes.Board()
        b2 = dominoes.Board()

        PseudoBoard = collections.namedtuple('PseudoBoard', ['board'])

        pb = PseudoBoard(collections.deque())

        self.assertEqual(b1, b2)
        self.assertNotEqual(b1, pb)

        b1.add(d1, True)

        self.assertNotEqual(b1, b2)

        b2.add(d1, True)

        self.assertEqual(b1, b2)

        b1.add(d2, True)

        self.assertNotEqual(b1, b2)

        b2.add(d2, True)

        self.assertEqual(b1, b2)

        b1.add(d3, False)

        self.assertNotEqual(b1, b2)

        b2.add(d3, False)

        self.assertEqual(b1, b2)

    def test_add_left(self):
        b = dominoes.Board()

        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(1, 3)
        d3 = dominoes.Domino(2, 3)
        d4 = dominoes.Domino(4, 4)

        b.add(d1, True)

        self.assertEqual(len(b), 1)
        self.assertEqual(b.left_end(), 1)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[1|2]')
        self.assertEqual(repr(b), '[1|2]')

        b.add(d2, True)

        self.assertEqual(len(b), 2)
        self.assertEqual(b.left_end(), 3)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[3|1][1|2]')
        self.assertEqual(repr(b), '[3|1][1|2]')

        b.add(d3, True)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|3][3|1][1|2]')
        self.assertEqual(repr(b), '[2|3][3|1][1|2]')

        self.assertRaises(dominoes.EndsMismatchException, b.add, d4, True)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|3][3|1][1|2]')
        self.assertEqual(repr(b), '[2|3][3|1][1|2]')

    def test_add_right(self):
        b = dominoes.Board()

        d1 = dominoes.Domino(2, 1)
        d2 = dominoes.Domino(3, 1)
        d3 = dominoes.Domino(3, 2)
        d4 = dominoes.Domino(4, 4)

        b.add(d1, False)

        self.assertEqual(len(b), 1)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 1)
        self.assertEqual(str(b), '[2|1]')
        self.assertEqual(repr(b), '[2|1]')

        b.add(d2, False)

        self.assertEqual(len(b), 2)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 3)
        self.assertEqual(str(b), '[2|1][1|3]')
        self.assertEqual(repr(b), '[2|1][1|3]')

        b.add(d3, False)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|1][1|3][3|2]')
        self.assertEqual(repr(b), '[2|1][1|3][3|2]')

        self.assertRaises(dominoes.EndsMismatchException, b.add, d4, False)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|1][1|3][3|2]')
        self.assertEqual(repr(b), '[2|1][1|3][3|2]')

if __name__ == '__main__':
    unittest.main()
