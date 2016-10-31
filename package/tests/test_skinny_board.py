import domino
import unittest

class TestSkinnyBoard(unittest.TestCase):
    def test_init(self):
        b = domino.SkinnyBoard()

        self.assertIsNotNone(b)

    def test_from_board(self):
        b = domino.Board()

        sb1 = domino.SkinnyBoard.from_board(b)

        d = domino.Domino(1, 2)

        b.add_left(d)

        sb2 = domino.SkinnyBoard.from_board(b)

        self.assertEqual(len(sb1), 0)
        self.assertRaises(domino.EmptyBoardException, sb1.left_end)
        self.assertRaises(domino.EmptyBoardException, sb1.right_end)

        self.assertEqual(len(sb2), 1)
        self.assertEqual(sb2.left_end(), 1)
        self.assertEqual(sb2.right_end(), 2)

    def test_add_left(self):
        b = domino.SkinnyBoard()

        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(1, 3)
        d3 = domino.Domino(2, 3)
        d4 = domino.Domino(4, 4)

        b.add_left(d1)

        self.assertEqual(len(b), 1)
        self.assertEqual(b.left_end(), 1)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[1|2]')
        self.assertEqual(repr(b), '[1|2]')

        b.add_left(d2)

        self.assertEqual(len(b), 2)
        self.assertEqual(b.left_end(), 3)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[3|?][?|2]')
        self.assertEqual(repr(b), '[3|?][?|2]')

        b.add_left(d3)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

        self.assertRaises(domino.EndsMismatchException, b.add_left, d4)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

    def test_add_right(self):
        b = domino.SkinnyBoard()

        d1 = domino.Domino(2, 1)
        d2 = domino.Domino(3, 1)
        d3 = domino.Domino(3, 2)
        d4 = domino.Domino(4, 4)

        b.add_right(d1)

        self.assertEqual(len(b), 1)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 1)
        self.assertEqual(str(b), '[2|1]')
        self.assertEqual(repr(b), '[2|1]')

        b.add_right(d2)

        self.assertEqual(len(b), 2)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 3)
        self.assertEqual(str(b), '[2|?][?|3]')
        self.assertEqual(repr(b), '[2|?][?|3]')

        b.add_right(d3)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

        self.assertRaises(domino.EndsMismatchException, b.add_right, d4)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

    def test_empty_board_exception(self):
        b = domino.SkinnyBoard()

        self.assertRaises(domino.EmptyBoardException, b.left_end)
        self.assertRaises(domino.EmptyBoardException, b.right_end)

if __name__ == '__main__':
    unittest.main()
