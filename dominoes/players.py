'''
Players are Python objects with a __call__ method defined
to accept a Game instance as the sole argument. Players
return None, and leave the input Game unmodified, except
for its valid_moves attribute. This value may be replaced
with another tuple containing the same moves, but sorted
in decreasing order of preference.

.. code-block:: python

    >>> import dominoes
    >>> g = dominoes.Game.new()
    >>> g.valid_moves
    (([0|0], True), ([3|4], True), ([1|3], True), ([2|2], True), ([3|3], True), ([2|3], True), ([5|6], True))
    >>> dominoes.players.random(g)
    >>> g.valid_moves
    (([5|6], True), ([1|3], True), ([3|3], True), ([2|2], True), ([0|0], True), ([2|3], True), ([3|4], True))
'''
import random as rand

def random(game):
    '''
    Prefers moves randomly.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda _: rand.random()))

def reverse(game):
    '''
    Reverses move preferences.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(reversed(game.valid_moves))
