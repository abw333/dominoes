dominoes: a Python library for the game of dominoes, with an accompanying CLI and AI players
============================================================================================

[![Build Status](https://travis-ci.org/abw333/dominoes.svg?branch=master)](https://travis-ci.org/abw333/dominoes)
[![Test Code Coverage](https://codecov.io/gh/abw333/dominoes/branch/master/graph/badge.svg)](https://codecov.io/gh/abw333/dominoes)
[![PyPI version](https://badge.fury.io/py/dominoes.svg)](https://badge.fury.io/py/dominoes)
[![Python version](https://img.shields.io/badge/python-3.6%2C%203.7-brightgreen.svg)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/dominoes/badge/?version=latest)](https://dominoes.readthedocs.io/en/latest/?badge=latest)

Dominoes have been around for hundreds of years, and many variations of the game have been played all over the world. This library is based on a popular variation commonly played in San Juan, Puerto Rico, and surrounding municipalities, such as Guaynabo.

It is played with a double six set of dominoes. The 28 dominoes are shuffled and distributed evenly between the 4 players, who form 2 teams. The players then take turns placing dominoes in a single chain. The first player to play all their dominoes wins the points in the remaining hands for their team. If the game is stuck, the team with the fewest points remaining in its players' hands wins the points in all the remaining hands. For more details, see the [full documentation](https://dominoes.readthedocs.io/en/latest/#game).

This library provides a	``Game`` class to represent a single dominoes game. It is built on top of ``Domino``, ``Hand``, and ``Board`` classes. Furthermore, you can string various games together and play up to a target score using the ``Series`` class.

Additionally, this package provides a command line interface to a dominoes series. Not only is it a great way to play a quick game, but it is also a comprehensive example of how to use this library's API.

The command line interface features various artificial intelligence players. For more information on how these work, see the [full documentation](https://dominoes.readthedocs.io/en/latest/#players).

## Install

```
$ pip install dominoes
```

## Usage Example

```
>>> import dominoes
>>> d = dominoes.Domino(6, 6)
>>> g = dominoes.Game.new(starting_domino=d)
>>> g
Board: [6|6]
Player 0's hand: [2|4][5|5][2|3][1|3][1|6][1|2]
Player 1's hand: [1|1][3|4][0|5][0|6][2|5][1|5][2|6]
Player 2's hand: [0|4][0|3][4|4][3|6][0|2][4|5][1|4]
Player 3's hand: [5|6][3|5][3|3][0|0][0|1][2|2][4|6]
Player 1's turn
>>> g.board
[6|6]
>>> g.hands
[[2|4][5|5][2|3][1|3][1|6][1|2], [1|1][3|4][0|5][0|6][2|5][1|5][2|6], [0|4][0|3][4|4][3|6][0|2][4|5][1|4], [5|6][3|5][3|3][0|0][0|1][2|2][4|6]]
>>> g.turn
1
>>> g.result
>>> g.valid_moves # True is for the left of the board, False is for the right
[([0|6], True), ([2|6], True)]
>>> g.make_move(*g.valid_moves[0])
>>> g.moves
[([6|6], True), ([0|6], True)]
>>> g
Board: [0|6][6|6]
Player 0's hand: [2|4][5|5][2|3][1|3][1|6][1|2]
Player 1's hand: [1|1][3|4][0|5][2|5][1|5][2|6]
Player 2's hand: [0|4][0|3][4|4][3|6][0|2][4|5][1|4]
Player 3's hand: [5|6][3|5][3|3][0|0][0|1][2|2][4|6]
Player 2's turn
>>> g.make_move(*g.valid_moves[0])
...
>>> g.make_move(*g.valid_moves[0])
Result(player=1, won=True, points=-32)
>>> g.result
Result(player=1, won=True, points=-32)
>>> g
Board: [2|6][6|3][3|4][4|1][1|1][1|6][6|4][4|5][5|2][2|4][4|0][0|6][6|6][6|5][5|0][0|3][3|5][5|5][5|1][1|0]
Player 0's hand: [2|3][1|3][1|2]
Player 1's hand:
Player 2's hand: [4|4][0|2]
Player 3's hand: [3|3][0|0][2|2]
Player 1 won and scored 32 points!
```

## Command Line Interface

```
$ dominoes
Welcome! Proceeding will clear all text from this terminal session. If you are OK with this, press enter to continue.
```

```
Up to how many points would you like to play: 100
Player settings:
0) Human
1) AI: random
2) AI: omniscient
Select a setting for player 0: 0
Select a setting for player 1: 1
Select a setting for player 2: 0
Select a setting for player 3: 1
Press enter to begin game 0.
```

```
Player 3 had the [6|6] and made the first move.
Board:
[6|6]
Player 0 has 7 dominoes in his/her hand.
Player 1 has 7 dominoes in his/her hand.
Player 2 has 7 dominoes in his/her hand.
Player 3 has 6 dominoes in his/her hand.
It is now player 0's turn. Press enter to continue.
```

```
Board:
[6|6]
Player 0's hand:
0) [3|6]
1) [4|4]
2) [0|1]
3) [2|6]
4) [1|1]
5) [2|5]
6) [3|3]
Choose which domino you would like to play: 3
Choose what end of the board you would like to play on (l or r): r
Press enter to end player 0's turn.
```

```
Board:
[6|6][6|2]
Player 1 (AI: random) chose to play [2|4] on the right end of the board.
Press enter to end player 1's turn.
```

```
Game over!
Board: [0|2][2|2][2|5][5|5][5|6][6|0][0|0][0|3][3|6][6|1][1|4][4|4][4|6][6|6][6|2][2|4][4|5][5|3][3|3][3|2][2|1][1|1][1|3][3|4]
Player 0's hand: [0|1]
Player 1's hand: [1|5][0|5]
Player 2's hand: [0|4]
Player 3's hand:
Player 3 won and scored 16 points!
The current state of the series:
Series to 100 points:
Team 0 has 0 points.
Team 1 has 16 points.
Press enter to begin game 1.
```

```
Game over!
Board: [5|3][3|3][3|6][6|5][5|5][5|0][0|4][4|3][3|1][1|6][6|2][2|5][5|4][4|6][6|0][0|3][3|2][2|0][0|0][0|1][1|4][4|2][2|2][2|1][1|1]
Player 0's hand: [1|5]
Player 1's hand: [4|4]
Player 2's hand:
Player 3's hand: [6|6]
Player 2 won and scored 26 points!
The current state of the series:
Series to 100 points:
Team 0 has 107 points.
Team 1 has 95 points.
Team 0 wins!
$
```

## Artificial Intelligence Players

Players are Python objects with a ``__call__`` method defined to accept a Game instance as the sole argument. Players return None, and leave the input Game unmodified, except for its valid_moves attribute. This value may be replaced with another tuple containing the same moves, but sorted in decreasing order of preference. Players may be applied one after another for easy composability.

For more information on how these work, see the [full documentation](https://dominoes.readthedocs.io/en/latest/#players).

```
>>> import dominoes
>>> g = dominoes.Game.new()
>>> g.valid_moves
(([0|0], True), ([3|4], True), ([1|3], True), ([2|2], True), ([3|3], True), ([2|3], True), ([5|6], True))
>>> dominoes.players.random(g)
>>> g.valid_moves
(([5|6], True), ([1|3], True), ([3|3], True), ([2|2], True), ([0|0], True), ([2|3], True), ([3|4], True))
```

```
def double(game):
    '''
    Prefers to play doubles.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))
```

## Questions, Comments, Ideas?

Feel free to create an [issue](https://github.com/abw333/dominoes/issues) or a [pull request](https://github.com/abw333/dominoes/pulls).
