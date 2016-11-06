import collections
import domino
import unittest

class TestSeries(unittest.TestCase):
    def test_init(self):
        s1 = domino.Series()

        self.assertEqual(len(s1.games), 1)
        self.assertEqual(len(s1.games[0].board), 1)
        self.assertEqual(s1.games[0].board.left_end(), 6)
        self.assertEqual(s1.games[0].board.right_end(), 6)
        hand_lengths1 = collections.Counter(len(h) for h in s1.games[0].hands)
        self.assertEqual(hand_lengths1[6], 1)
        self.assertEqual(hand_lengths1[7], 3)
        self.assertTrue(s1.games[0].turn in range(4))
        self.assertIsNone(s1.games[0].result)
        self.assertEqual(s1.scores, [0, 0])
        self.assertEqual(s1.target_score, 200)

        s2 = domino.Series(target_score=100)

        self.assertEqual(len(s2.games), 1)
        self.assertEqual(len(s2.games[0].board), 1)
        self.assertEqual(s2.games[0].board.left_end(), 6)
        self.assertEqual(s2.games[0].board.right_end(), 6)
        hand_lengths2 = collections.Counter(len(h) for h in s2.games[0].hands)
        self.assertEqual(hand_lengths2[6], 1)
        self.assertEqual(hand_lengths2[7], 3)
        self.assertTrue(s2.games[0].turn in range(4))
        self.assertIsNone(s2.games[0].result)
        self.assertEqual(s2.scores, [0, 0])
        self.assertEqual(s2.target_score, 100)

        d = domino.Domino(1, 2)
        s3 = domino.Series(starting_domino=d)

        self.assertEqual(len(s3.games), 1)
        self.assertEqual(len(s3.games[0].board), 1)
        self.assertEqual(s3.games[0].board.left_end(), 1)
        self.assertEqual(s3.games[0].board.right_end(), 2)
        hand_lengths3 = collections.Counter(len(h) for h in s3.games[0].hands)
        self.assertEqual(hand_lengths3[6], 1)
        self.assertEqual(hand_lengths3[7], 3)
        self.assertTrue(s3.games[0].turn in range(4))
        self.assertIsNone(s3.games[0].result)
        self.assertEqual(s3.scores, [0, 0])
        self.assertEqual(s3.target_score, 200)

    def test_is_over(self):
        s = domino.Series()

        self.assertFalse(s.is_over())

        s.scores = [199, 199]

        self.assertFalse(s.is_over())

        s.scores = [200, 199]

        self.assertTrue(s.is_over())

        s.scores = [199, 200]

        self.assertTrue(s.is_over())

        s.scores = [200, 200]

        self.assertTrue(s.is_over())

        s.scores = [201, 201]

        self.assertTrue(s.is_over())

    def test_next_game(self):
        s = domino.Series()

        self.assertRaises(domino.GameInProgressException, s.next_game)
        self.assertEqual(len(s.games), 1)
        self.assertEqual(len(s.games[0].board), 1)
        self.assertIsNone(s.games[0].result)
        self.assertEqual(s.scores, [0, 0])
        self.assertEqual(s.target_score, 200)

        scores = [200, 200]
        s.scores = scores

        self.assertRaises(domino.SeriesOverException, s.next_game)
        self.assertEqual(len(s.games), 1)
        self.assertEqual(len(s.games[0].board), 1)
        self.assertIsNone(s.games[0].result)
        self.assertEqual(s.scores, scores)
        self.assertEqual(s.target_score, 200)

        s.scores = [0, 0]
        s.games[0].result = domino.game.Result(0, True, 50)
        g1 = s.next_game()

        self.assertEqual(len(s.games), 2)
        self.assertEqual(len(g1.board), 0)
        self.assertEqual(g1.turn, 0)
        self.assertIsNone(g1.result)
        self.assertEqual(s.scores, [50, 0])
        self.assertEqual(s.target_score, 200)

        s.games[1].result = domino.game.Result(1, True, 50)
        g2 = s.next_game()

        self.assertEqual(len(s.games), 3)
        self.assertEqual(len(g2.board), 0)
        self.assertEqual(g2.turn, 1)
        self.assertIsNone(g2.result)
        self.assertEqual(s.scores, [50, 50])
        self.assertEqual(s.target_score, 200)

        s.games[2].result = domino.game.Result(2, True, -50)
        g3 = s.next_game()

        self.assertEqual(len(s.games), 4)
        self.assertEqual(len(g3.board), 0)
        self.assertEqual(g3.turn, 2)
        self.assertIsNone(g3.result)
        self.assertEqual(s.scores, [50, 100])
        self.assertEqual(s.target_score, 200)

        s.games[3].result = domino.game.Result(3, True, -50)
        g4 = s.next_game()

        self.assertEqual(len(s.games), 5)
        self.assertEqual(len(g4.board), 0)
        self.assertEqual(g4.turn, 3)
        self.assertIsNone(g4.result)
        self.assertEqual(s.scores, [100, 100])
        self.assertEqual(s.target_score, 200)

        s.games[4].result = domino.game.Result(0, True, 100)

        self.assertIsNone(s.next_game())
        self.assertEqual(len(s.games), 5)
        self.assertEqual(s.scores, [200, 100])
        self.assertEqual(s.target_score, 200)

if __name__ == '__main__':
    unittest.main()
