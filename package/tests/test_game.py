import domino
import unittest

class TestGame(unittest.TestCase):
    def test_randomized_hands(self):
        hands = domino.game._randomized_hands()

        self.assertEqual(len(hands), 4)

        all_dominoes = set()
        for h in hands:
            self.assertEqual(len(h), 7)

            for d in h:
                self.assertTrue(0 <= d.first)
                self.assertTrue(d.first <= 6)
                self.assertTrue(0 <= d.second)
                self.assertTrue(d.second <= 6)

                all_dominoes.add(d)

        self.assertEqual(len(all_dominoes), 28)

    def test_validate_player(self):
        for i in range(4):
            self.assertIsNone(domino.game._validate_player(i))

        self.assertRaises(domino.NoSuchPlayerException,
                          domino.game._validate_player, -1)
        self.assertRaises(domino.NoSuchPlayerException,
                          domino.game._validate_player, 4)

    def test_domino_hand(self):
        d1 = domino.Domino(1, 1)
        d2 = domino.Domino(1, 2)
        d3 = domino.Domino(1, 3)
        d4 = domino.Domino(1, 4)
        d5 = domino.Domino(1, 5)

        h1 = domino.Hand([d1, d2])
        h2 = domino.Hand([d3, d4])
        hands = [h1, h2]

        self.assertEqual(domino.game._domino_hand(d1, hands), 0)
        self.assertEqual(domino.game._domino_hand(d4, hands), 1)

        self.assertRaises(domino.NoSuchDominoException,
                          domino.game._domino_hand, d5, hands)

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
