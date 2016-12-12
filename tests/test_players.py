import dominoes
import unittest

class TestPlayers(unittest.TestCase):
    def test_random(self):
        g = dominoes.Game.new()

        dominoes.players.random(g)

if __name__ == '__main__':
    unittest.main()
