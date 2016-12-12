import copy
import dominoes
import unittest

class TestPlayers(unittest.TestCase):
    def _test_player_interface(self, player):
        g = dominoes.Game.new()

        g_copy = copy.deepcopy(g)

        player(g)

        self.assertEqual(type(g.valid_moves), tuple)
        self.assertEqual(len(g.valid_moves), len(g_copy.valid_moves))
        self.assertEqual(set(g.valid_moves), set(g_copy.valid_moves))

        g_copy.valid_moves = g.valid_moves

        self.assertEqual(g, g_copy)

    def test_random(self):
        self._test_player_interface(dominoes.players.random)

if __name__ == '__main__':
    unittest.main()
