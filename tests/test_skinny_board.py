import dominoes
import unittest

class TestSkinnyBoard(unittest.TestCase):
    def test_init(self):
        b = dominoes.SkinnyBoard()

        self.assertEqual(len(b), 0)
        self.assertRaises(dominoes.EmptyBoardException, b.left_end)
        self.assertRaises(dominoes.EmptyBoardException, b.right_end)
        self.assertEqual(str(b), '')
        self.assertEqual(repr(b), '')

    def test_from_board(self):
        b = dominoes.Board()

        sb1 = dominoes.SkinnyBoard.from_board(b)

        d = dominoes.Domino(1, 2)

        b.add(d, True)

        sb2 = dominoes.SkinnyBoard.from_board(b)

        self.assertEqual(len(sb1), 0)
        self.assertRaises(dominoes.EmptyBoardException, sb1.left_end)
        self.assertRaises(dominoes.EmptyBoardException, sb1.right_end)
        self.assertEqual(str(sb1), '')
        self.assertEqual(repr(sb1), '')

        self.assertEqual(len(sb2), 1)
        self.assertEqual(sb2.left_end(), 1)
        self.assertEqual(sb2.right_end(), 2)
        self.assertEqual(str(sb2), '[1|2]')
        self.assertEqual(repr(sb2), '[1|2]')

    def test_eq(self):
        b1 = dominoes.SkinnyBoard(1, 2, 3)
        b2 = dominoes.SkinnyBoard(1, 2, 3)
        b3 = dominoes.SkinnyBoard(4, 2, 3)
        b4 = dominoes.SkinnyBoard(1, 4, 3)
        b5 = dominoes.SkinnyBoard(1, 2, 4)

        class PseudoSkinnyBoard:
            def __init__(self, _left, _right, _length):
                self._left = _left
                self._right = _right
                self._length = _length

        pb = PseudoSkinnyBoard(1, 2, 3)

        self.assertEqual(b1, b2)
        self.assertNotEqual(b1, b3)
        self.assertNotEqual(b1, b4)
        self.assertNotEqual(b1, b5)
        self.assertNotEqual(b1, pb)

    def test_add_left(self):
        b = dominoes.SkinnyBoard()

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
        self.assertEqual(str(b), '[3|?][?|2]')
        self.assertEqual(repr(b), '[3|?][?|2]')

        b.add(d3, True)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

        self.assertRaises(dominoes.EndsMismatchException, b.add, d4, True)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

    def test_add_right(self):
        b = dominoes.SkinnyBoard()

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
        self.assertEqual(str(b), '[2|?][?|3]')
        self.assertEqual(repr(b), '[2|?][?|3]')

        b.add(d3, False)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

        self.assertRaises(dominoes.EndsMismatchException, b.add, d4, False)

        self.assertEqual(len(b), 3)
        self.assertEqual(b.left_end(), 2)
        self.assertEqual(b.right_end(), 2)
        self.assertEqual(str(b), '[2|?][?|?][?|2]')
        self.assertEqual(repr(b), '[2|?][?|?][?|2]')

if __name__ == '__main__':
    unittest.main()
