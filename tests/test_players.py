import copy
import dominoes
import unittest

def _new_game_with_fixed_moves(fixed_moves):
    while True:
        g = dominoes.Game.new()

        for _ in range(fixed_moves):
            g.make_move(*g.valid_moves[0])

            if g.result is not None:
                break

        if g.result is None:
            return g

class TestPlayers(unittest.TestCase):
    def _test_player_interface(self, player, fixed_moves=0):
        g = _new_game_with_fixed_moves(fixed_moves)

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

    def test_counter(self):
        self._test_player_interface(dominoes.players.counter())

        self.assertEqual(dominoes.players.counter(name='test').__name__, 'test')

        bgc = dominoes.players.counter(dominoes.players.bota_gorda)

        self.assertEqual(bgc.__name__, 'counter')
        self.assertEqual(bgc.count, 0)

        # there is a small chance that the valid moves are already
        # sorted in bota gorda order, in which case this won't
        # test anything interesting. this test suite gets run
        # often enough that the danger is negligible.
        g = dominoes.Game.new()
        g_copy = copy.deepcopy(g)

        bgc(g)
        dominoes.players.bota_gorda(g_copy)

        self.assertEqual(g, g_copy)
        self.assertEqual(bgc.count, 1)

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

    def test_omniscient(self):
        # game cannot have ended after 6 fixed moves.
        self._test_player_interface(dominoes.players.omniscient(), 6)

        self.assertEqual(dominoes.players.omniscient(name='test').__name__, 'test')
        self.assertEqual(dominoes.players.omniscient().__name__, 'omniscient')

        cp1 = dominoes.players.counter()
        op1 = dominoes.players.omniscient(start_move=1, player=cp1)

        g1 = dominoes.Game.new()
        op1(g1)

        self.assertEqual(cp1.count, 0)

        # due to passes, the amount of total moves will be greater
        # than or equal to 6 after playing 6 fixed moves. therefore,
        # the following will not test the boundary condition every time.
        # this test suite gets run often enough that the danger is negligible.
        cp2 = dominoes.players.counter()
        op2 = dominoes.players.omniscient(start_move=6, player=cp2)

        while True:
            g2 = dominoes.Game.new()
            for _ in range(6):
                g2.make_move(*g2.valid_moves[0])

            # the omniscient player is smart enough not
            # to run when there is only one valid move.
            if len(g2.valid_moves) > 1:
                break
        op2(g2)

        self.assertNotEqual(cp2.count, 0)

        d1 = dominoes.Domino(7, 0)
        d2 = dominoes.Domino(0, 0)
        d3 = dominoes.Domino(0, 1)
        d4 = dominoes.Domino(0, 8)
        d5 = dominoes.Domino(1, 9)

        h1 = dominoes.Hand([d1, d2])
        h2 = dominoes.Hand([d3, d2])
        h3 = dominoes.Hand([d3, d4, d5])
        h4 = dominoes.Hand([d2])

        g3 = dominoes.Game.new(starting_player=0)
        g3.hands = [h1, h2, h3, h4]
        g3.make_move(d1, True)

        op3 = dominoes.players.omniscient()

        self.assertEqual(g3.valid_moves, ((d3, False), (d2, False)))

        op3(g3)

        self.assertEqual(g3.valid_moves, ((d2, False), (d3, False)))

    def test_probabilistic_alphabeta(self):
        # test player interface
        self._test_player_interface(dominoes.players.probabilistic_alphabeta(), 15)

        # test name
        self.assertEqual(dominoes.players.probabilistic_alphabeta(name='test').__name__, 'test')
        self.assertEqual(dominoes.players.probabilistic_alphabeta().__name__, 'probabilistic_alphabeta')

        # test that start move can prevent running of player
        cp1 = dominoes.players.counter()
        pap1 = dominoes.players.probabilistic_alphabeta(start_move=1, player=cp1)

        g1 = dominoes.Game.new()
        pap1(g1)

        self.assertEqual(cp1.count, 0)

        # test that player can still run even with a start move.
        # due to passes, the amount of total moves will be greater
        # than or equal to 15 after playing 15 fixed moves. therefore,
        # the following will not test the boundary condition every time.
        # this test suite gets run often enough that the danger is negligible.
        cp2 = dominoes.players.counter()
        pap2 = dominoes.players.probabilistic_alphabeta(start_move=15, player=cp2)

        while True:
            g2 = _new_game_with_fixed_moves(15)

            # the probabilistic_alphabeta player is smart enough
            # not to run when there is only one valid move.
            if len(g2.valid_moves) > 1:
                break
        pap2(g2)

        self.assertNotEqual(cp2.count, 0)

if __name__ == '__main__':
    unittest.main()
