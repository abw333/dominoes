import collections
import copy
import dominoes
import unittest

class TestGame(unittest.TestCase):
    def test_randomized_hands(self):
        hands = dominoes.game._randomized_hands()

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
            self.assertIsNone(dominoes.game._validate_player(i))

        self.assertRaises(dominoes.NoSuchPlayerException,
                          dominoes.game._validate_player, -1)
        self.assertRaises(dominoes.NoSuchPlayerException,
                          dominoes.game._validate_player, 4)

    def test_domino_hand(self):
        d1 = dominoes.Domino(1, 1)
        d2 = dominoes.Domino(1, 2)
        d3 = dominoes.Domino(1, 3)
        d4 = dominoes.Domino(1, 4)
        d5 = dominoes.Domino(1, 5)

        h1 = dominoes.Hand([d1, d2])
        h2 = dominoes.Hand([d3, d4])
        hands = [h1, h2]

        self.assertEqual(dominoes.game._domino_hand(d1, hands), 0)
        self.assertEqual(dominoes.game._domino_hand(d4, hands), 1)

        self.assertRaises(dominoes.NoSuchDominoException,
                          dominoes.game._domino_hand, d5, hands)

    def test_remaining_points(self):
        h1 = []

        self.assertEqual(dominoes.game._remaining_points(h1), [])

        d1 = dominoes.Domino(0, 1)
        d2 = dominoes.Domino(1, 3)
        d3 = dominoes.Domino(3, 6)
        h2 = [dominoes.Hand([]), dominoes.Hand([d1]), dominoes.Hand([d2, d3])]

        self.assertEqual(dominoes.game._remaining_points(h2), [0, 1, 13])

    def test_result(self):
        p = 0
        w = True
        pts = 100
        r = dominoes.game.Result(p, w, pts)

        self.assertEqual(r.player, p)
        self.assertEqual(r.won, True)
        self.assertEqual(r.points, pts)

    def test_init(self):
        g1 = dominoes.Game.new()

        self.assertEqual(len(g1.board), 0)
        self.assertEqual(len(g1.hands), 4)
        self.assertEqual(g1.moves, [])
        self.assertEqual(g1.turn, 0)
        self.assertEqual(len(g1.valid_moves), 7)
        for d in g1.hands[g1.turn]:
            self.assertTrue((d, True) in g1.valid_moves)
        self.assertEqual(g1.starting_player, 0)
        self.assertIsNone(g1.result)

        p1 = 3
        g2 = dominoes.Game.new(starting_player=p1)

        self.assertEqual(len(g2.board), 0)
        self.assertEqual(len(g2.hands), 4)
        self.assertEqual(g2.moves, [])
        self.assertEqual(g2.turn, p1)
        self.assertEqual(len(g2.valid_moves), 7)
        for d in g2.hands[g2.turn]:
            self.assertTrue((d, True) in g2.valid_moves)
        self.assertEqual(g2.starting_player, p1)
        self.assertIsNone(g2.result)

        d1 = dominoes.Domino(6, 6)
        g3 = dominoes.Game.new(starting_domino=d1)

        self.assertEqual(len(g3.board), 1)
        self.assertEqual(len(g3.hands), 4)
        self.assertEqual(g3.moves[0], (d1, True))
        for m in g3.moves[1:]:
            self.assertIsNone(m)
        hand_lengths1 = collections.Counter(len(h) for h in g3.hands)
        self.assertEqual(hand_lengths1[6], 1)
        self.assertEqual(hand_lengths1[7], 3)
        self.assertTrue(g3.turn in range(4))
        self.assertTrue(bool(g3.valid_moves))
        for i, h in enumerate(g3.hands):
            if len(h) == 6:
                self.assertEqual(g3.starting_player, i)
                break
        self.assertIsNone(g3.result)

        g4 = dominoes.Game.new(starting_domino=d1, starting_player=p1)

        self.assertEqual(len(g4.board), 1)
        self.assertEqual(len(g4.hands), 4)
        self.assertEqual(g4.moves[0], (d1, True))
        for m in g4.moves[1:]:
            self.assertIsNone(m)
        hand_lengths2 = collections.Counter(len(h) for h in g4.hands)
        self.assertEqual(hand_lengths2[6], 1)
        self.assertEqual(hand_lengths2[7], 3)
        self.assertTrue(g4.turn in range(4))
        self.assertTrue(bool(g4.valid_moves))
        for i, h in enumerate(g4.hands):
            if len(h) == 6:
                self.assertEqual(g4.starting_player, i)
                break
        self.assertIsNone(g4.result)

        p2 = 4
        self.assertRaises(dominoes.NoSuchPlayerException,
                          dominoes.Game.new, starting_player=p2)

        d2 = dominoes.Domino(7, 7)
        self.assertRaises(dominoes.NoSuchDominoException,
                          dominoes.Game.new, starting_domino=d2)

    def test_eq(self):
        g1 = dominoes.Game.new()
        g2 = dominoes.Game.new()
        g3 = dominoes.Game.new()
        g4 = dominoes.Game.new()
        g5 = dominoes.Game.new()
        g6 = dominoes.Game.new()
        g7 = dominoes.Game.new()
        g8 = dominoes.Game.new()
        g9 = dominoes.Game.new()

        PseudoGame = collections.namedtuple('PseudoGame',
                                            ['board', 'hands', 'moves', 'result',
                                             'turn', 'valid_moves', 'starting_player'])

        pg = PseudoGame(g1.board, g1.hands, g1.moves, g1.result,
                        g1.turn, g1.valid_moves, g1.starting_player)

        g2.hands = g1.hands
        g3.hands = g1.hands
        g4.hands = g1.hands
        g5.hands = g1.hands
        g6.hands = g1.hands
        g7.hands = g1.hands
        g8.hands = g1.hands
        g9.hands = g1.hands

        g2.valid_moves = g1.valid_moves
        g3.valid_moves = g1.valid_moves
        g4.valid_moves = g1.valid_moves
        g5.valid_moves = g1.valid_moves
        g6.valid_moves = g1.valid_moves
        g7.valid_moves = g1.valid_moves
        g8.valid_moves = g1.valid_moves
        g9.valid_moves = g1.valid_moves

        self.assertEqual(g1, g2)

        self.assertNotEqual(g1, pg)

        g3.skinny_board()
        self.assertNotEqual(g1, g3)

        g4.hands = g4.hands[1:] + g4.hands[:1]
        self.assertNotEqual(g1, g4)

        g5.result = True
        self.assertNotEqual(g1, g5)

        g6.turn = 1
        self.assertNotEqual(g1, g6)

        g7.starting_player = 1
        self.assertNotEqual(g1, g7)

        g8.valid_moves = ()
        self.assertNotEqual(g1, g8)

        g9.moves = ()
        self.assertNotEqual(g1, g9)

    def test_skinny_board(self):
        d = dominoes.Domino(1, 2)
        g = dominoes.Game.new(starting_domino=d)

        g.skinny_board()

        ends = [g.board.left_end(), g.board.right_end()]
        self.assertTrue(d.first in ends)
        self.assertTrue(d.second in ends)

        self.assertEqual(len(g.board), 1)

    def test_deepcopy(self):
        # Board
        g1 = dominoes.Game.new()
        g2 = copy.deepcopy(g1)

        self.assertEqual(g1, g2)

        p1 = g2.turn
        g2.make_move(*g2.valid_moves[0])

        self.assertNotEqual(g1.board, g2.board)
        for p in range(len(g1.hands)):
            if p == p1:
                self.assertNotEqual(g1.hands[p], g2.hands[p])
            else:
                self.assertEqual(g1.hands[p], g2.hands[p])
        self.assertTrue(len(g2.moves) > len(g1.moves))
        self.assertNotEqual(g1.valid_moves, g2.valid_moves)
        self.assertEqual(g1.starting_player, g2.starting_player)
        self.assertEqual(g1.result, g2.result)

        # empty SkinnyBoard
        g3 = dominoes.Game.new()
        g3.skinny_board()
        g4 = copy.deepcopy(g3)

        self.assertEqual(g3, g4)

        p2 = g4.turn
        g4.make_move(*g4.valid_moves[0])

        self.assertNotEqual(g3.board, g4.board)
        for p in range(len(g3.hands)):
            if p == p2:
                self.assertNotEqual(g3.hands[p], g4.hands[p])
            else:
                self.assertEqual(g3.hands[p], g4.hands[p])
        self.assertTrue(len(g4.moves) > len(g3.moves))
        self.assertNotEqual(g3.valid_moves, g4.valid_moves)
        self.assertEqual(g3.starting_player, g4.starting_player)
        self.assertEqual(g3.result, g4.result)

        # non-empty SkinnyBoard
        g5 = dominoes.Game.new()
        g5.skinny_board()
        g5.make_move(*g5.valid_moves[0])
        g6 = copy.deepcopy(g5)

        self.assertEqual(g5, g6)

        p3 = g6.turn
        g6.make_move(*g6.valid_moves[0])

        self.assertNotEqual(g5.board, g6.board)
        for p in range(len(g5.hands)):
            if p == p3:
                self.assertNotEqual(g5.hands[p], g6.hands[p])
            else:
                self.assertEqual(g5.hands[p], g6.hands[p])
        self.assertTrue(len(g6.moves) > len(g5.moves))
        self.assertNotEqual(g5.valid_moves, g6.valid_moves)
        self.assertEqual(g5.starting_player, g6.starting_player)
        self.assertEqual(g5.result, g6.result)

    def test_update_valid_moves(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(2, 3)

        p = 3
        g = dominoes.Game.new(starting_player=p)

        g.board.add_left(d1)

        h = dominoes.Hand([d1, d2])
        g.hands[p] = h

        g._update_valid_moves()

        # left end of board != right end of board
        self.assertEqual(len(g.valid_moves), 3)
        self.assertTrue((d1, True) in g.valid_moves)
        self.assertTrue((d1, False) in g.valid_moves)
        self.assertTrue((d2, False) in g.valid_moves)

        g.board.add_left(d1)

        g._update_valid_moves()

        # left end of board == right end of board
        self.assertEqual(len(g.valid_moves), 2)
        self.assertTrue((d1, True) in g.valid_moves)
        self.assertTrue((d2, True) in g.valid_moves)

    def test_make_move(self):
        g1 = dominoes.Game.new()

        d1 = dominoes.Domino(7, 7)
        g1.board.add_left(d1)

        d2 = dominoes.Domino(7, 6)
        p1 = g1.turn
        len_hand1 = len(g1.hands[p1])
        g1.hands[p1].draw(d2)

        # make a move on the left end of the board
        g1.make_move(d2, True)

        self.assertEqual(g1.board.left_end(), d2.second)
        self.assertEqual(g1.board.right_end(), d1.second)
        self.assertEqual(len(g1.board), 2)
        self.assertEqual(len(g1.hands[p1]), len_hand1)
        self.assertFalse(d2 in g1.hands[p1])
        self.assertEqual(g1.moves[0], (d2, True))
        for m in g1.moves[1:]:
            self.assertIsNone(m)
        self.assertTrue(bool(g1.valid_moves))
        self.assertIsNone(g1.result)

        d3 = dominoes.Domino(7, 5)
        p2 = g1.turn
        len_hand2 = len(g1.hands[p2])
        len_moves1 = len(g1.moves)
        g1.hands[p2].draw(d3)

        # make a move on the right end of the board
        g1.make_move(d3, False)
        str1 = str(g1)
        repr1 = repr(g1)

        self.assertEqual(g1.board.left_end(), d2.second)
        self.assertEqual(g1.board.right_end(), d3.second)
        self.assertEqual(len(g1.board), 3)
        self.assertEqual(len(g1.hands[p2]), len_hand2)
        self.assertFalse(d3 in g1.hands[p2])
        self.assertEqual(g1.moves[0], (d2, True))
        for m in g1.moves[1:len_moves1]:
            self.assertIsNone(m)
        self.assertEqual(g1.moves[len_moves1], (d3, False))
        for m in g1.moves[len_moves1 + 1:]:
            self.assertIsNone(m)
        self.assertTrue(bool(g1.valid_moves))
        self.assertIsNone(g1.result)
        self.assertTrue('Board: {}'.format(g1.board) in str1)
        self.assertTrue("Player 0's hand: {}".format(g1.hands[0]) in str1)
        self.assertTrue("Player 1's hand: {}".format(g1.hands[1]) in str1)
        self.assertTrue("Player 2's hand: {}".format(g1.hands[2]) in str1)
        self.assertTrue("Player 3's hand: {}".format(g1.hands[3]) in str1)
        self.assertTrue("Player {}'s turn".format(g1.turn) in str1)
        self.assertFalse('Player {} won'.format(p2) in str1)
        self.assertFalse('Player {} stuck'.format(p2) in str1)
        self.assertEqual(str1, repr1)

        d4 = dominoes.Domino(7, 7)
        p3 = g1.turn
        len_hand3 = len(g1.hands[p3])
        before = copy.deepcopy(g1)

        # try to play a domino that is not in the player's hand
        self.assertRaises(dominoes.NoSuchDominoException, g1.make_move, d4, True)

        self.assertEqual(before, g1)
        self.assertEqual(g1.board.left_end(), d2.second)
        self.assertEqual(g1.board.right_end(), d3.second)
        self.assertEqual(len(g1.board), 3)
        self.assertEqual(len(g1.hands[p3]), len_hand3)
        self.assertFalse(d4 in g1.hands[p3])
        self.assertEqual(g1.turn, p3)
        self.assertEqual(g1.moves[0], (d2, True))
        for m in g1.moves[1:len_moves1]:
            self.assertIsNone(m)
        self.assertEqual(g1.moves[len_moves1], (d3, False))
        for m in g1.moves[len_moves1 + 1:]:
            self.assertIsNone(m)
        self.assertTrue(bool(g1.valid_moves))
        self.assertIsNone(g1.result)

        g1.hands[p3].draw(d4)
        before = copy.deepcopy(g1)

        # try to play a domino that does not match the board
        self.assertRaises(dominoes.EndsMismatchException, g1.make_move, d4, True)

        self.assertEqual(before, g1)
        self.assertEqual(g1.board.left_end(), d2.second)
        self.assertEqual(g1.board.right_end(), d3.second)
        self.assertEqual(len(g1.board), 3)
        self.assertEqual(len(g1.hands[p3]), len_hand3 + 1)
        self.assertTrue(d4 in g1.hands[p3])
        self.assertEqual(g1.turn, p3)
        self.assertEqual(g1.moves[0], (d2, True))
        for m in g1.moves[1:len_moves1]:
            self.assertIsNone(m)
        self.assertEqual(g1.moves[len_moves1], (d3, False))
        for m in g1.moves[len_moves1 + 1:]:
            self.assertIsNone(m)
        self.assertTrue(bool(g1.valid_moves))
        self.assertIsNone(g1.result)

    def test_make_move_endgame(self):
        d1 = dominoes.Domino(1, 2)
        d2 = dominoes.Domino(2, 3)
        d3 = dominoes.Domino(3, 4)
        d4 = dominoes.Domino(4, 5)
        h1 = dominoes.Hand([d1])
        h2 = dominoes.Hand([d2])
        h3 = dominoes.Hand([d3])
        h4 = dominoes.Hand([d4])
        g1 = dominoes.Game.new()
        g1.hands = [h1, h2, h3, h4]

        g1.make_move(d1, True)
        str1 = str(g1)
        repr1 = repr(g1)

        self.assertEqual(g1.board.left_end(), d1.first)
        self.assertEqual(g1.board.right_end(), d1.second)
        self.assertEqual(len(g1.board), 1)
        self.assertEqual(len(g1.hands[0]), 0)
        self.assertEqual(len(g1.hands[1]), 1)
        self.assertEqual(len(g1.hands[2]), 1)
        self.assertEqual(len(g1.hands[3]), 1)
        self.assertEqual(g1.moves, [(d1, True)])
        self.assertFalse(bool(g1.valid_moves))
        self.assertEqual(g1.result, dominoes.game.Result(0, True, 21))
        self.assertEqual(g1.turn, 0)
        self.assertTrue('Board: {}'.format(g1.board) in str1)
        self.assertTrue("Player 0's hand: {}".format(g1.hands[0]) in str1)
        self.assertTrue("Player 1's hand: {}".format(g1.hands[1]) in str1)
        self.assertTrue("Player 2's hand: {}".format(g1.hands[2]) in str1)
        self.assertTrue("Player 3's hand: {}".format(g1.hands[3]) in str1)
        self.assertFalse("Player 0's turn" in str1)
        self.assertTrue('Player 0 won and scored 21 points!' in str1)
        self.assertEqual(str1, repr1)

        d5 = dominoes.Domino(7, 7)
        d6 = dominoes.Domino(1, 1)
        d7 = dominoes.Domino(2, 2)
        d8 = dominoes.Domino(3, 3)
        d9 = dominoes.Domino(4, 4)
        h5 = dominoes.Hand([d5, d6])
        h6 = dominoes.Hand([d7])
        h7 = dominoes.Hand([d8])
        h8 = dominoes.Hand([d9])
        g2 = dominoes.Game.new()
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
        self.assertEqual(g2.moves, [(d5, True)])
        self.assertFalse(bool(g2.valid_moves))
        self.assertEqual(g2.result, dominoes.game.Result(0, False, 20))
        self.assertEqual(g2.turn, 0)
        self.assertTrue('Board: {}'.format(g2.board) in str2)
        self.assertTrue("Player 0's hand: {}".format(g2.hands[0]) in str2)
        self.assertTrue("Player 1's hand: {}".format(g2.hands[1]) in str2)
        self.assertTrue("Player 2's hand: {}".format(g2.hands[2]) in str2)
        self.assertTrue("Player 3's hand: {}".format(g2.hands[3]) in str2)
        self.assertFalse("Player 0's turn" in str2)
        self.assertTrue('Player 0 stuck the game and scored 20 points!' in str2)
        self.assertEqual(str2, repr2)

        h9 = dominoes.Hand([d5, d6])
        h10 = dominoes.Hand([d7])
        h11 = dominoes.Hand([d9])
        h12 = dominoes.Hand([d8])
        g3 = dominoes.Game.new()
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
        self.assertEqual(g3.moves, [(d5, True)])
        self.assertFalse(bool(g3.valid_moves))
        self.assertEqual(g3.result, dominoes.game.Result(0, False, 0))
        self.assertEqual(g3.turn, 0)
        self.assertTrue('Board: {}'.format(g3.board) in str3)
        self.assertTrue("Player 0's hand: {}".format(g3.hands[0]) in str3)
        self.assertTrue("Player 1's hand: {}".format(g3.hands[1]) in str3)
        self.assertTrue("Player 2's hand: {}".format(g3.hands[2]) in str3)
        self.assertTrue("Player 3's hand: {}".format(g3.hands[3]) in str3)
        self.assertFalse("Player 0's turn" in str3)
        self.assertTrue('Player 0 stuck the game and tied (0 points)!' in str3)
        self.assertEqual(str3, repr3)

        h13 = dominoes.Hand([d5, d7])
        h14 = dominoes.Hand([d6])
        h15 = dominoes.Hand([d9])
        h16 = dominoes.Hand([d8])
        g4 = dominoes.Game.new()
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
        self.assertEqual(g4.moves, [(d5, True)])
        self.assertFalse(bool(g4.valid_moves))
        self.assertEqual(g4.result, dominoes.game.Result(0, False, -20))
        self.assertEqual(g4.turn, 0)
        self.assertTrue('Board: {}'.format(g4.board) in str4)
        self.assertTrue("Player 0's hand: {}".format(g4.hands[0]) in str4)
        self.assertTrue("Player 1's hand: {}".format(g4.hands[1]) in str4)
        self.assertTrue("Player 2's hand: {}".format(g4.hands[2]) in str4)
        self.assertTrue("Player 3's hand: {}".format(g4.hands[3]) in str4)
        self.assertFalse("Player 0's turn" in str4)
        self.assertTrue('Player 0 stuck the game and scored 20 points for the opposing team!' in str4)
        self.assertEqual(str4, repr4)

        before = copy.deepcopy(g4)

        self.assertRaises(dominoes.GameOverException, g4.make_move, d7, True)

        self.assertEqual(before, g4)
        self.assertEqual(g4.board.left_end(), d5.first)
        self.assertEqual(g4.board.right_end(), d5.second)
        self.assertEqual(len(g4.board), 1)
        self.assertEqual(len(g4.hands[0]), 1)
        self.assertEqual(len(g4.hands[1]), 1)
        self.assertEqual(len(g4.hands[2]), 1)
        self.assertEqual(len(g4.hands[3]), 1)
        self.assertEqual(g4.moves, [(d5, True)])
        self.assertFalse(bool(g4.valid_moves))
        self.assertEqual(g4.result, dominoes.game.Result(0, False, -20))
        self.assertEqual(g4.turn, 0)

if __name__ == '__main__':
    unittest.main()
