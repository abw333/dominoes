'''
Players are Python objects with a ``__call__`` method
defined to accept a Game instance as the sole argument.
Players return None, and leave the input Game unmodified,
except for its valid_moves attribute. This value may be
replaced with another tuple containing the same moves,
but sorted in decreasing order of preference. Players
may be applied one after another for easy composability.

.. code-block:: python

    >>> import dominoes
    >>> g = dominoes.Game.new()
    >>> g.valid_moves
    (([0|0], True), ([3|4], True), ([1|3], True), ([2|2], True), ([3|3], True), ([2|3], True), ([5|6], True))
    >>> dominoes.players.random(g)
    >>> g.valid_moves
    (([5|6], True), ([1|3], True), ([3|3], True), ([2|2], True), ([0|0], True), ([2|3], True), ([3|4], True))

.. code-block:: python

    def double(game):
        \'\'\'
        Prefers to play doubles.

        :param Game game: game to play
        :return: None
        \'\'\'
        game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))
'''
import collections
import copy
import dominoes
import random as rand

def identity(game):
    '''
    Leaves move preferences unchanged.

    :param Game game: game to play
    :return: None
    '''
    return

class counter:
    '''
    Prefers moves in the same order as the passed-in player. Keeps
    a counter of the amount of times that this player gets called.
    An instance of this class must first be initialized before it
    can be called in the usual way.

    :param callable player: player that determines the move preferences of
                            this player. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var int count: the amount of times that this player has been called.
    :var str __name__: the name of this player.
    '''
    def __init__(self, player=identity, name=None):
        self.count = 0
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        self.count += 1
        return self._player(game)

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

def bota_gorda(game):
    '''
    Prefers to play dominoes with higher point values.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: -(m[0].first + m[0].second)))

def double(game):
    '''
    Prefers to play doubles.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))

class omniscient:
    '''
    Prefers to play the move that maximizes this player's final score,
    assuming that all other players play with the same strategy. This
    player "cheats" by looking at all hands to make its decision. An
    instance of this class must first be initialized before it can be
    called in the usual way.

    :param int start_move: move number at which to start applying this
                           player. If this player is called before the
                           specified move number, it will have no effect.
                           Moves are 0-indexed. The default is 0.
    :param callable player: player used to sort moves to be explored
                            in the underlying call to alphabeta search.
                            Ordering better moves first may significantly
                            reduce the amount of moves that need to be
                            explored. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var str __name__: the name of this player
    '''
    def __init__(self, start_move=0, player=identity, name=None):
        self._start_move = start_move
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        # do not perform a potentially slow operation if it is
        # too early in the game or if there is only one valid move
        if len(game.moves) < self._start_move or len(game.valid_moves) == 1:
            return

        # so that we don't modify the original game
        game_copy = copy.deepcopy(game)

        # for performance
        game_copy.skinny_board()

        # perform an alphabeta search to find the optimal move sequence
        moves, _ = dominoes.search.alphabeta(game_copy, player=self._player)

        # place the optimal move at the beginning of game.valid_moves,
        # while leaving the rest of the ordering unchanged
        game.valid_moves = (moves[0],) + tuple(m for m in game.valid_moves if m != moves[0])

class probabilistic_alphabeta:
    '''
    This player repeatedly assumes the other players' hands, runs alphabeta search,
    and prefers moves that are most frequently optimal. It takes into account all
    known information to determine what hands the other players could possibly have,
    including its hand, the sizes of the other players' hands, and the moves played
    by every player, including the passes. An instance of this class must first be
    initialized before it can be called in the usual way.

    :param int start_move: move number at which to start applying this
                           player. If this player is called before the
                           specified move number, it will have no effect.
                           Moves are 0-indexed. The default is 0.
    :param int sample_size: the number of times to assign random possible
                            hands to other players and run alphabeta search
                            before deciding move preferences. By default
                            considers all hands that other players could
                            possibly have.
    :param callable player: player used to sort moves to be explored
                            in the underlying call to alphabeta search.
                            Ordering better moves first may significantly
                            reduce the amount of moves that need to be
                            explored. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var str __name__: the name of this player
    '''
    def __init__(self, start_move=0, sample_size=float('inf'), player=identity, name=None):
        self._start_move = start_move
        self._sample_size = sample_size
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        # do not perform a potentially slow operation if it is
        # too early in the game or if there is only one valid move
        if len(game.moves) < self._start_move or len(game.valid_moves) == 1:
            return

        if self._sample_size == float('inf'):
            # by default consider all hands the other players could possibly have
            hands = game.all_possible_hands()
        else:
            # otherwise obtain a random sample
            hands = (game.random_possible_hands() for _ in range(self._sample_size))

        # iterate over the selected possible hands
        counter = collections.Counter()
        for h in hands:
            # do not modify the original game
            game_copy = copy.deepcopy(game)

            # set the possible hands
            game_copy.hands = h

            # for performance
            game_copy.skinny_board()

            # run alphabeta and record the optimal move
            counter.update([
                dominoes.search.alphabeta(game_copy, player=self._player)[0][0]
            ])

        # prefer moves that are more frequently optimal
        game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: -counter[m]))
