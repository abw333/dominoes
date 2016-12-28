import copy
import dominoes
import unittest

class TestSearch(unittest.TestCase):
    def test_make_moves(self):
        game1 = dominoes.Game.new()

        for vm, (m, g) in zip(game1.valid_moves, dominoes.search.make_moves(game1)):
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

        game2 = dominoes.Game.new()
        game2.result = True

        self.assertEqual(list(dominoes.search.make_moves(game2)), [])

        game3 = dominoes.Game.new()
        game3_copy = copy.deepcopy(game3)

        # there is a small chance that the valid moves are already
        # sorted in bota gorda order, in which case this won't
        # test anything interesting. this test suite gets run
        # often enough that the danger is negligible.
        dominoes.players.bota_gorda(game3_copy)

        for vm, (m, g) in zip(game3_copy.valid_moves,
                              dominoes.search.make_moves(game3, dominoes.players.bota_gorda)):
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

    def test_alphabeta(self):
        g1 = dominoes.Game.new()
        g1.result = dominoes.Result(0, True, 10)

        self.assertEqual(([], 10), dominoes.search.alphabeta(g1))

        g2 = dominoes.Game.new()
        g2.result = dominoes.Result(1, True, -10)

        self.assertEqual(([], -10), dominoes.search.alphabeta(g2))

if __name__ == '__main__':
    unittest.main()
