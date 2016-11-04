import domino
import unittest

class TestGame(unittest.TestCase):
    def test_init(self):
        g = domino.Game()

        self.assertEqual(len(g.board), 0)

        self.assertEqual(len(g.hands), 4)
        for hand in g.hands:
            self.assertEqual(len(hand), 7)

        self.assertEqual(g.turn, 0)

        self.assertIsNone(g.result)

if __name__ == '__main__':
    unittest.main()
