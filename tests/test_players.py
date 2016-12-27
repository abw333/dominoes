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

    def test_identity(self):
        self._test_player_interface(dominoes.players.identity)

        g = dominoes.Game.new()
        d1 = dominoes.Domino(1, 1)
        d2 = dominoes.Domino(2, 2)
        d3 = dominoes.Domino(3, 3)

        valid_moves_before = [
            ((d1, True),),
            ((d1, True), (d2, False)),
            ((d1, True), (d2, False), (d3, False))
        ]
        valid_moves_after = [
            ((d1, True),),
            ((d1, True), (d2, False)),
            ((d1, True), (d2, False), (d3, False))
        ]

        for vmb, vma in zip(valid_moves_before, valid_moves_after):
            g.valid_moves = vmb
            dominoes.players.identity(g)
            self.assertEqual(g.valid_moves, vma)

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

    def test_bota_gorda(self):
        self._test_player_interface(dominoes.players.bota_gorda)

        g = dominoes.Game.new()
        d1 = dominoes.Domino(1, 1)
        d2 = dominoes.Domino(2, 0)
        d3 = dominoes.Domino(1, 0)

        valid_moves_before = [
            ((d1, True),),
            ((d1, True), (d1, False)),
            ((d1, True), (d2, True)),
            ((d1, True), (d3, True)),
            ((d3, True), (d1, True))
        ]
        valid_moves_after = [
            ((d1, True),),
            ((d1, True), (d1, False)),
            ((d1, True), (d2, True)),
            ((d1, True), (d3, True)),
            ((d1, True), (d3, True))
        ]
        for vmb, vma in zip(valid_moves_before, valid_moves_after):
            g.valid_moves = vmb
            dominoes.players.bota_gorda(g)
            self.assertEqual(g.valid_moves, vma)

    def test_double(self):
        self._test_player_interface(dominoes.players.double)

        g = dominoes.Game.new()
        d1 = dominoes.Domino(1, 1)
        d2 = dominoes.Domino(2, 2)
        d3 = dominoes.Domino(1, 0)

        valid_moves_before = [
            ((d1, True),),
            ((d1, True), (d1, False)),
            ((d1, True), (d2, True)),
            ((d1, True), (d3, True)),
            ((d3, True), (d1, True))
        ]
        valid_moves_after = [
            ((d1, True),),
            ((d1, True), (d1, False)),
            ((d1, True), (d2, True)),
            ((d1, True), (d3, True)),
            ((d1, True), (d3, True))
        ]
        for vmb, vma in zip(valid_moves_before, valid_moves_after):
            g.valid_moves = vmb
            dominoes.players.double(g)
            self.assertEqual(g.valid_moves, vma)

if __name__ == '__main__':
    unittest.main()
