import collections
import dominoes
import unittest

class TestSeries(unittest.TestCase):
    def test_init(self):
        s1 = dominoes.Series()

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

        s2 = dominoes.Series(target_score=100)

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

        d = dominoes.Domino(1, 2)
        s3 = dominoes.Series(starting_domino=d)

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
        s = dominoes.Series()

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
        s = dominoes.Series()
        str1 = str(s)
        repr1 = repr(s)

        self.assertRaises(dominoes.GameInProgressException, s.next_game)
        self.assertEqual(len(s.games), 1)
        self.assertEqual(len(s.games[0].board), 1)
        self.assertIsNone(s.games[0].result)
        self.assertEqual(s.scores, [0, 0])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str1)
        self.assertTrue('Team 0 has 0 points.' in str1)
        self.assertTrue('Team 1 has 0 points.' in str1)
        self.assertEqual(str1, repr1)

        scores = [200, 200]
        s.scores = scores
        str2 = str(s)
        repr2 = repr(s)

        self.assertRaises(dominoes.SeriesOverException, s.next_game)
        self.assertEqual(len(s.games), 1)
        self.assertEqual(len(s.games[0].board), 1)
        self.assertIsNone(s.games[0].result)
        self.assertEqual(s.scores, scores)
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str2)
        self.assertTrue('Team 0 has 200 points.' in str2)
        self.assertTrue('Team 1 has 200 points.' in str2)
        self.assertEqual(str2, repr2)

        s.scores = [0, 0]
        s.games[0].result = dominoes.game.Result(0, True, 50)
        g1 = s.next_game()
        str3 = str(s)
        repr3 = repr(s)

        self.assertEqual(len(s.games), 2)
        self.assertEqual(len(g1.board), 0)
        self.assertEqual(g1.turn, 0)
        self.assertIsNone(g1.result)
        self.assertEqual(s.scores, [50, 0])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str3)
        self.assertTrue('Team 0 has 50 points.' in str3)
        self.assertTrue('Team 1 has 0 points.' in str3)
        self.assertEqual(str3, repr3)

        s.games[1].result = dominoes.game.Result(1, False, 50)
        g2 = s.next_game()
        str4 = str(s)
        repr4 = repr(s)

        self.assertEqual(len(s.games), 3)
        self.assertEqual(len(g2.board), 0)
        self.assertEqual(g2.turn, 1)
        self.assertIsNone(g2.result)
        self.assertEqual(s.scores, [50, 50])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str4)
        self.assertTrue('Team 0 has 50 points.' in str4)
        self.assertTrue('Team 1 has 50 points.' in str4)
        self.assertEqual(str4, repr4)

        s.games[2].result = dominoes.game.Result(2, True, -50)
        g3 = s.next_game()
        str5 = str(s)
        repr5 = repr(s)

        self.assertEqual(len(s.games), 4)
        self.assertEqual(len(g3.board), 0)
        self.assertEqual(g3.turn, 2)
        self.assertIsNone(g3.result)
        self.assertEqual(s.scores, [50, 100])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str5)
        self.assertTrue('Team 0 has 50 points.' in str5)
        self.assertTrue('Team 1 has 100 points.' in str5)
        self.assertEqual(str5, repr5)

        s.games[3].result = dominoes.game.Result(3, False, -50)
        g4 = s.next_game()
        str6 = str(s)
        repr6 = repr(s)

        self.assertEqual(len(s.games), 5)
        self.assertEqual(len(g4.board), 0)
        self.assertEqual(g4.turn, 0)
        self.assertIsNone(g4.result)
        self.assertEqual(s.scores, [100, 100])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str6)
        self.assertTrue('Team 0 has 100 points.' in str6)
        self.assertTrue('Team 1 has 100 points.' in str6)
        self.assertEqual(str6, repr6)

        s.games[4].result = dominoes.game.Result(2, False, 0)
        g5 = s.next_game()
        str7 = str(s)
        repr7 = repr(s)

        self.assertEqual(len(s.games), 6)
        self.assertEqual(len(g5.board), 0)
        self.assertEqual(g5.turn, 0)
        self.assertIsNone(g5.result)
        self.assertEqual(s.scores, [100, 100])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str7)
        self.assertTrue('Team 0 has 100 points.' in str7)
        self.assertTrue('Team 1 has 100 points.' in str7)
        self.assertEqual(str7, repr7)

        s.games[5].result = dominoes.game.Result(0, True, 100)

        self.assertIsNone(s.next_game())

        str8 = str(s)
        repr8 = repr(s)

        self.assertEqual(len(s.games), 6)
        self.assertEqual(s.scores, [200, 100])
        self.assertEqual(s.target_score, 200)
        self.assertTrue('Series to 200 points:' in str8)
        self.assertTrue('Team 0 has 200 points.' in str8)
        self.assertTrue('Team 1 has 100 points.' in str8)
        self.assertEqual(str8, repr8)

if __name__ == '__main__':
    unittest.main()
