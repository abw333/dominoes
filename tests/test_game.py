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
        b = domino.Board()

        # empty hand, empty board
        self.assertFalse(domino.game._has_valid_move(h1, b))

        d1 = domino.Domino(1, 2)
        h2 = domino.Hand([d1])

        # non-empty hand, empty board
        self.assertTrue(domino.game._has_valid_move(h2, b))

        b.add_left(d1)

        # empty hand, non-empty board
        self.assertFalse(domino.game._has_valid_move(h1, b))

        # non-empty hand, non-empty board
        self.assertTrue(domino.game._has_valid_move(h2, b))

        d2 = domino.Domino(1, 3)
        h3 = domino.Hand([d2])

        # valid move on the left end of the board
        self.assertTrue(domino.game._has_valid_move(h3, b))

        d3 = domino.Domino(2, 3)
        h4 = domino.Hand([d3])

        # valid move on the right end of the board
        self.assertTrue(domino.game._has_valid_move(h4, b))

        d4 = domino.Domino(3, 3)
        h5 = domino.Hand([d4])

        # no valid moves
        self.assertFalse(domino.game._has_valid_move(h5, b))

    def test_result(self):
        p = 0
        w = True
        pts = 100
        r = domino.game.Result(p, w, pts)

        self.assertEqual(r.player, p)
        self.assertEqual(r.won, True)
        self.assertEqual(r.points, pts)

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

    def test_skinny_board(self):
        d = domino.Domino(1, 2)
        g = domino.Game(starting_domino=d)

        g.skinny_board()

        ends = [g.board.left_end(), g.board.right_end()]
        self.assertTrue(d.first in ends)
        self.assertTrue(d.second in ends)

        self.assertEqual(len(g.board), 1)

    def test_valid_moves(self):
        h1 = domino.Hand([])
        p = 3
        g = domino.Game(starting_player=p)
        g.hands[p] = h1

        # empty hand, empty board
        m1 = g.valid_moves()
        self.assertEqual(m1, [])

        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(2, 3)
        h2 = domino.Hand([d1, d2])
        g.hands[p] = h2

        # non-empty hand, empty board
        m2 = g.valid_moves()
        self.assertEqual(len(m2), 2)
        self.assertTrue((d1, True) in m2)
        self.assertTrue((d2, True) in m2)

        g.board.add_left(d1)
        g.hands[p] = h1

        # empty hand, non-empty board
        m3 = g.valid_moves()
        self.assertEqual(m3, [])

        g.hands[p] = h2

        # non-empty hand, non-empty board
        m4 = g.valid_moves()
        self.assertEqual(len(m4), 3)
        self.assertTrue((d1, True) in m4)
        self.assertTrue((d1, False) in m4)
        self.assertTrue((d2, False) in m4)

        g.board.add_left(d1)

        # left end of board == right end of board
        m5 = g.valid_moves()
        self.assertEqual(len(m5), 2)
        self.assertTrue((d1, True) in m5)
        self.assertTrue((d2, True) in m5)

    def test_make_move(self):
        g = domino.Game()

        d1 = domino.Domino(7, 7)
        g.board.add_left(d1)

        d2 = domino.Domino(7, 6)
        p1 = g.turn
        len_hand1 = len(g.hands[p1])
        g.hands[p1].draw(d2)

        # make a move on the left end of the board
        g.make_move(d2, True)

        self.assertEqual(g.board.left_end(), d2.second)
        self.assertEqual(g.board.right_end(), d1.second)
        self.assertEqual(len(g.board), 2)
        self.assertEqual(len(g.hands[p1]), len_hand1)
        self.assertFalse(d2 in g.hands[p1])
        self.assertTrue(domino.game._has_valid_move(g.hands[g.turn], g.board))
        self.assertIsNone(g.result)

        d3 = domino.Domino(7, 5)
        p2 = g.turn
        len_hand2 = len(g.hands[p2])
        g.hands[p2].draw(d3)

        # make a move on the right end of the board
        g.make_move(d3, False)

        self.assertEqual(g.board.left_end(), d2.second)
        self.assertEqual(g.board.right_end(), d3.second)
        self.assertEqual(len(g.board), 3)
        self.assertEqual(len(g.hands[p2]), len_hand2)
        self.assertFalse(d3 in g.hands[p2])
        self.assertTrue(domino.game._has_valid_move(g.hands[g.turn], g.board))
        self.assertIsNone(g.result)

        d4 = domino.Domino(7, 7)
        p3 = g.turn
        len_hand3 = len(g.hands[p3])

        # try to play a domino that is not in the player's hand
        self.assertRaises(domino.NoSuchDominoException, g.make_move, d4, True)

        self.assertEqual(g.board.left_end(), d2.second)
        self.assertEqual(g.board.right_end(), d3.second)
        self.assertEqual(len(g.board), 3)
        self.assertEqual(len(g.hands[p3]), len_hand3)
        self.assertFalse(d4 in g.hands[p3])
        self.assertEqual(g.turn, p3)
        self.assertTrue(domino.game._has_valid_move(g.hands[g.turn], g.board))
        self.assertIsNone(g.result)

        g.hands[p3].draw(d4)

        # try to play a domino that does not match the board
        self.assertRaises(domino.EndsMismatchException, g.make_move, d4, True)

        self.assertEqual(g.board.left_end(), d2.second)
        self.assertEqual(g.board.right_end(), d3.second)
        self.assertEqual(len(g.board), 3)
        self.assertEqual(len(g.hands[p3]), len_hand3 + 1)
        self.assertTrue(d4 in g.hands[p3])
        self.assertEqual(g.turn, p3)
        self.assertTrue(domino.game._has_valid_move(g.hands[g.turn], g.board))
        self.assertIsNone(g.result)

    def test_make_move_endgame(self):
        d1 = domino.Domino(1, 2)
        d2 = domino.Domino(2, 3)
        d3 = domino.Domino(3, 4)
        d4 = domino.Domino(4, 5)
        h1 = domino.Hand([d1])
        h2 = domino.Hand([d2])
        h3 = domino.Hand([d3])
        h4 = domino.Hand([d4])
        g1 = domino.Game()
        g1.hands = [h1, h2, h3, h4]

        g1.make_move(d1, True)
        str1 = str(g1)
        repr1 = str(g1)

        self.assertEqual(g1.board.left_end(), d1.first)
        self.assertEqual(g1.board.right_end(), d1.second)
        self.assertEqual(len(g1.board), 1)
        self.assertEqual(len(g1.hands[0]), 0)
        self.assertEqual(len(g1.hands[1]), 1)
        self.assertEqual(len(g1.hands[2]), 1)
        self.assertEqual(len(g1.hands[3]), 1)
        self.assertEqual(g1.result, domino.game.Result(0, True, 21))
        self.assertEqual(g1.turn, 0)
        self.assertTrue('Board: {}'.format(g1.board) in str1)
        self.assertTrue("Player 0's hand: {}".format(g1.hands[0]) in str1)
        self.assertTrue("Player 1's hand: {}".format(g1.hands[1]) in str1)
        self.assertTrue("Player 2's hand: {}".format(g1.hands[2]) in str1)
        self.assertTrue("Player 3's hand: {}".format(g1.hands[3]) in str1)
        self.assertFalse("Player 0's turn" in str1)
        self.assertTrue('Player 0 won and scored 21 points!' in str1)
        self.assertEqual(str1, repr1)

        d5 = domino.Domino(7, 7)
        d6 = domino.Domino(1, 1)
        d7 = domino.Domino(2, 2)
        d8 = domino.Domino(3, 3)
        d9 = domino.Domino(4, 4)
        h5 = domino.Hand([d5, d6])
        h6 = domino.Hand([d7])
        h7 = domino.Hand([d8])
        h8 = domino.Hand([d9])
        g2 = domino.Game()
        g2.hands = [h5, h6, h7, h8]

        g2.make_move(d5, True)
        str2 = str(g2)
        repr2 = repr(g2)

        self.assertEqual(g2.board.left_end(), d5.first)
        self.assertEqual(g2.board.right_end(), d5.second)
        self.assertEqual(len(g2.board), 1)
        self.assertEqual(len(g2.hands[0]), 1)
        self.assertEqual(len(g2.hands[1]), 1)
        self.assertEqual(len(g2.hands[2]), 1)
        self.assertEqual(len(g2.hands[3]), 1)
        self.assertEqual(g2.result, domino.game.Result(0, False, 20))
        self.assertEqual(g2.turn, 0)
        self.assertTrue('Board: {}'.format(g2.board) in str2)
        self.assertTrue("Player 0's hand: {}".format(g2.hands[0]) in str2)
        self.assertTrue("Player 1's hand: {}".format(g2.hands[1]) in str2)
        self.assertTrue("Player 2's hand: {}".format(g2.hands[2]) in str2)
        self.assertTrue("Player 3's hand: {}".format(g2.hands[3]) in str2)
        self.assertFalse("Player 0's turn" in str2)
        self.assertTrue('Player 0 stuck the game and won 20 points!' in str2)
        self.assertEqual(str2, repr2)

        h9 = domino.Hand([d5, d6])
        h10 = domino.Hand([d7])
        h11 = domino.Hand([d9])
        h12 = domino.Hand([d8])
        g3 = domino.Game()
        g3.hands = [h9, h10, h11, h12]

        g3.make_move(d5, True)
        str3 = str(g3)
        repr3 = repr(g3)

        self.assertEqual(g3.board.left_end(), d5.first)
        self.assertEqual(g3.board.right_end(), d5.second)
        self.assertEqual(len(g3.board), 1)
        self.assertEqual(len(g3.hands[0]), 1)
        self.assertEqual(len(g3.hands[1]), 1)
        self.assertEqual(len(g3.hands[2]), 1)
        self.assertEqual(len(g3.hands[3]), 1)
        self.assertEqual(g3.result, domino.game.Result(0, False, 0))
        self.assertEqual(g3.turn, 0)
        self.assertTrue('Board: {}'.format(g3.board) in str3)
        self.assertTrue("Player 0's hand: {}".format(g3.hands[0]) in str3)
        self.assertTrue("Player 1's hand: {}".format(g3.hands[1]) in str3)
        self.assertTrue("Player 2's hand: {}".format(g3.hands[2]) in str3)
        self.assertTrue("Player 3's hand: {}".format(g3.hands[3]) in str3)
        self.assertFalse("Player 0's turn" in str3)
        self.assertTrue('Player 0 stuck the game and tied!' in str3)
        self.assertEqual(str3, repr3)

        h13 = domino.Hand([d5, d7])
        h14 = domino.Hand([d6])
        h15 = domino.Hand([d9])
        h16 = domino.Hand([d8])
        g4 = domino.Game()
        g4.hands = [h13, h14, h15, h16]

        g4.make_move(d5, True)
        str4 = str(g4)
        repr4 = repr(g4)

        self.assertEqual(g4.board.left_end(), d5.first)
        self.assertEqual(g4.board.right_end(), d5.second)
        self.assertEqual(len(g4.board), 1)
        self.assertEqual(len(g4.hands[0]), 1)
        self.assertEqual(len(g4.hands[1]), 1)
        self.assertEqual(len(g4.hands[2]), 1)
        self.assertEqual(len(g4.hands[3]), 1)
        self.assertEqual(g4.result, domino.game.Result(0, False, -20))
        self.assertEqual(g4.turn, 0)
        self.assertTrue('Board: {}'.format(g4.board) in str4)
        self.assertTrue("Player 0's hand: {}".format(g4.hands[0]) in str4)
        self.assertTrue("Player 1's hand: {}".format(g4.hands[1]) in str4)
        self.assertTrue("Player 2's hand: {}".format(g4.hands[2]) in str4)
        self.assertTrue("Player 3's hand: {}".format(g4.hands[3]) in str4)
        self.assertFalse("Player 0's turn" in str4)
        self.assertTrue('Player 0 stuck the game and won the opposing team 20 points!' in str4)
        self.assertEqual(str4, repr4)

        self.assertRaises(domino.GameOverException, g4.make_move, d7, True)

        self.assertEqual(g4.board.left_end(), d5.first)
        self.assertEqual(g4.board.right_end(), d5.second)
        self.assertEqual(len(g4.board), 1)
        self.assertEqual(len(g4.hands[0]), 1)
        self.assertEqual(len(g4.hands[1]), 1)
        self.assertEqual(len(g4.hands[2]), 1)
        self.assertEqual(len(g4.hands[3]), 1)
        self.assertEqual(g4.result, domino.game.Result(0, False, -20))
        self.assertEqual(g4.turn, 0)

if __name__ == '__main__':
    unittest.main()
