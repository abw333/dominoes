import dominoes
import unittest

class TestSearch(unittest.TestCase):
    def test_make_moves(self):
        game = dominoes.Game.new()

        for vm, (m, g) in zip(game.valid_moves, dominoes.search.make_moves(game)):
            self.assertEqual(vm, m)

            self.assertEqual(g.board.left_end(), m[0].first)
            self.assertEqual(g.board.right_end(), m[0].second)
            self.assertEqual(len(g.board), 1)
            self.assertEqual(len(g.hands[0]), 6)
            self.assertEqual(len(g.hands[1]), 7)
            self.assertEqual(len(g.hands[2]), 7)
            self.assertEqual(len(g.hands[3]), 7)
            self.assertEqual(g.moves[0], m)
            for p in g.moves[1:]:
                self.assertIsNone(p)
            self.assertIsNotNone(g.turn)
            self.assertTrue(bool(g.valid_moves))
            self.assertEqual(g.starting_player, 0)
            self.assertIsNone(g.result)

if __name__ == '__main__':
    unittest.main()
