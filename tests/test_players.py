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

        gs = [dominoes.Game.new(starting_player=0) for _ in range(3)]
        valid_moves_before = tuple(g.valid_moves for g in gs)
        for g in gs:
            dominoes.players.random(g)
        valid_moves_after = tuple(g.valid_moves for g in gs)

        # this has a tiny, but nonzero, chance of failing
        self.assertNotEqual(valid_moves_before, valid_moves_after)

    def test_reverse(self):
        self._test_player_interface(dominoes.players.reverse)

        g = dominoes.Game.new()
        d1 = dominoes.Domino(1, 1)
        d2 = dominoes.Domino(2, 2)
        d3 = dominoes.Domino(3, 3)
        vms = [
            ((d1, True),),
            ((d1, True), (d2, False)),
            ((d1, True), (d2, False), (d3, False))
        ]
        rvms = [
            ((d1, True),),
            ((d2, False), (d1, True)),
            ((d3, False), (d2, False), (d1, True))
        ]

        for vm, rvm in zip(vms, rvms):
            g.valid_moves = vm
            dominoes.players.reverse(g)
            self.assertEqual(g.valid_moves, rvm)

if __name__ == '__main__':
    unittest.main()
