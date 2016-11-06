import collections
import domino
import unittest

class TestSeries(unittest.TestCase):
    def test_init(self):
        s = domino.Series()

        self.assertEqual(len(s.games), 1)
        self.assertEqual(len(s.games[0].board), 1)
        self.assertEqual(s.games[0].board.left_end(), 6)
        self.assertEqual(s.games[0].board.right_end(), 6)
        hand_lengths = collections.Counter(len(h) for h in s.games[0].hands)
        self.assertEqual(hand_lengths[6], 1)
        self.assertEqual(hand_lengths[7], 3)
        self.assertTrue(s.games[0].turn in range(4))
        self.assertIsNone(s.games[0].result)
        self.assertEqual(s.scores, [0, 0])
        self.assertEqual(s.target_score, 200)

if __name__ == '__main__':
    unittest.main()
