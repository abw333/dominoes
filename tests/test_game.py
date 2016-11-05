import collections
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

    def test_remaining_points(self):
        h1 = []

        self.assertEqual(domino.game._remaining_points(h1), [])

        d1 = domino.Domino(0, 1)
        d2 = domino.Domino(1, 3)
        d3 = domino.Domino(3, 6)
        h2 = [domino.Hand([]), domino.Hand([d1]), domino.Hand([d2, d3])]

        self.assertEqual(domino.game._remaining_points(h2), [0, 1, 13])

    def test_has_valid_move(self):
        h1 = domino.Hand([])
        b1 = domino.Board()

        # empty hand, empty board
        self.assertFalse(domino.game._has_valid_move(h1, b1))

        d1 = domino.Domino(1, 2)
        h2 = domino.Hand([d1])

        # non-empty hand, empty board
        self.assertTrue(domino.game._has_valid_move(h2, b1))

        b1.add_left(d1)

        # empty hand, non-empty board
        self.assertFalse(domino.game._has_valid_move(h1, b1))

        # non-empty hand, non-empty board
        self.assertTrue(domino.game._has_valid_move(h2, b1))

        d2 = domino.Domino(1, 3)
        h3 = domino.Hand([d2])

        # valid move on the left end of the board
        self.assertTrue(domino.game._has_valid_move(h3, b1))

        d3 = domino.Domino(2, 3)
        h4 = domino.Hand([d3])

        # valid move on the right end of the board
        self.assertTrue(domino.game._has_valid_move(h4, b1))

        d4 = domino.Domino(3, 3)
        h5 = domino.Hand([d4])

        # no valid moves
        self.assertFalse(domino.game._has_valid_move(h5, b1))

    def test_init(self):
        g1 = domino.Game()

        self.assertEqual(len(g1.board), 0)
        self.assertEqual(len(g1.hands), 4)
        self.assertEqual(g1.turn, 0)
        self.assertIsNone(g1.result)

        p1 = 3
        g2 = domino.Game(starting_player=p1)

        self.assertEqual(len(g2.board), 0)
        self.assertEqual(len(g2.hands), 4)
        self.assertEqual(g2.turn, 3)
        self.assertIsNone(g2.result)

        d1 = domino.Domino(6, 6)
        g3 = domino.Game(starting_domino=d1)

        self.assertEqual(len(g3.board), 1)
        self.assertEqual(len(g3.hands), 4)
        hand_lengths1 = collections.Counter(len(h) for h in g3.hands)
        self.assertEqual(hand_lengths1[6], 1)
        self.assertEqual(hand_lengths1[7], 3)
        self.assertTrue(g3.turn in range(4))
        self.assertIsNone(g3.result)

        g4 = domino.Game(starting_domino=d1, starting_player=p1)

        self.assertEqual(len(g4.board), 1)
        self.assertEqual(len(g4.hands), 4)
        hand_lengths2 = collections.Counter(len(h) for h in g4.hands)
        self.assertEqual(hand_lengths2[6], 1)
        self.assertEqual(hand_lengths2[7], 3)
        self.assertTrue(g4.turn in range(4))
        self.assertIsNone(g4.result)

        p2 = 4
        self.assertRaises(domino.NoSuchPlayerException,
                          domino.Game, starting_player=p2)

        d2 = domino.Domino(7, 7)
        self.assertRaises(domino.NoSuchDominoException,
                          domino.Game, starting_domino=d2)

if __name__ == '__main__':
    unittest.main()
