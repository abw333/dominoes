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


if __name__ == '__main__':
    unittest.main()
