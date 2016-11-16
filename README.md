dominoes: a Python library for the dominoes game
================================================

[![Build Status](https://travis-ci.org/abw333/dominoes.svg?branch=master)](https://travis-ci.org/abw333/dominoes)
[![Test Code Coverage](https://codecov.io/gh/abw333/dominoes/branch/master/graph/badge.svg)](https://codecov.io/gh/abw333/dominoes)
[![PyPI version](https://badge.fury.io/py/dominoes.svg)](https://badge.fury.io/py/dominoes)
[![Python version](https://img.shields.io/badge/python-3.5-brightgreen.svg)](https://www.python.org/)

Dominoes have been around for hundreds of years, and many variations of the game have been played all over the world. This library is based on a popular variation commonly played in San Juan, Puerto Rico, and surrounding municipalities, such as Guaynabo.

It is played with a double six set of dominoes. The 28 dominoes are shuffled and distributed evenly between the 4 players, who form 2 teams. The players then take turns placing dominoes in a single chain. The first player to play all their dominoes wins the points in the remaining hands for their team. If the game is stuck, the team with the fewest points wins the points in the remaining hands. For more details, see the full documentation.

This library provides a	`Game` class to	represent a single dominoes game. It is built on top of `Domino`, `Hand`, and `Board` classes. Furthermore, you can string various games together and play up to a target score using the `Series` class.

Lastly, this package provides a command line interface to a dominoes series. Not only is it a great way to play a quick game, but it is also a comprehensive example of how to use this library's API.

## Install

```bash
$ pip install dominoes
```
