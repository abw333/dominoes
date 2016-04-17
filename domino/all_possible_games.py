import common
import copy
import domino
import itertools
import multiprocessing
import os
import random

FIXED_MOVES = 0
SERIAL_DEPTH = 2

def bfs_step(games, completed):
    new_games = []

    def list_to_update(result):
        if result is None:
            return new_games
        else:
            return completed

    for game in games:
        moves = game.valid_moves()
        for move in moves[:-1]:
            new_game = copy.deepcopy(game)
            result = new_game.make_move(*move)
            list_to_update(result).append(new_game)

        result = game.make_move(*moves[-1])
        list_to_update(result).append(game)

    return new_games, completed

def compute_all_possible_games(game):
    pid = os.getpid()
    games = [game]
    completed = []

    depth = 0
    while games:
        games, completed = bfs_step(games, completed)

        depth += 1
        print('Process {}, Depth {}: {} games, {} completed'.format(
                pid, depth, len(games), len(completed)))

    return completed

with common.stopwatch('Initializing random game'):
    game = domino.Game(skinny_board=True)

    for i in range(FIXED_MOVES):
        moves = game.valid_moves()
        move = random.choice(moves)
        game.make_move(*move)

with common.stopwatch('Computation of all possible games'):
    games = [game]
    for i in range(SERIAL_DEPTH):
        games, _ = bfs_step(games, [])

    with multiprocessing.Pool(len(games)) as pool:
        completed = pool.map(compute_all_possible_games, games)

    completed = itertools.chain(*completed)

    print(len(list(completed)))
