'''
This file contains players for the game of dominoes.

Players are Python objects with a __call__ method defined
to accept a Game instance as the sole argument. Players
return None, and leave the input Game unmodified, except
for its valid_moves attribute. This value may be replaced
with another tuple containing the same moves, but sorted
in decreasing order of preference.
'''
import random as rand

def random(game):
    '''
    Prefers moves randomly.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda _: rand.random()))
