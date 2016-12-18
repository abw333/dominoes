import collections

Result = collections.namedtuple('Result', ['player', 'won', 'points'])
Result.__doc__ = \
'''
namedtuple to represent the result of a dominoes game.

:var player: the last player to make a move
:var won: True if the game ended due to an empty hand;
          False if the game ended due to being stuck
:var points: the absolute value of this quantity indicates
             the amount of points earned by the winning team.
             This quantity is positive if the last player to
             make a move is part of the winning team, and
             negative otherwise. If it is 0, it means the
             game ended in a tie

.. code-block:: python

    >>> import dominoes
    >>> dominoes.Result(1, True, 25)
    Result(player=1, won=True, points=25)
'''
