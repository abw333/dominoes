import common
import copy
import domino
import multiprocessing
import os
import random

FIXED_MOVES = 0
SERIAL_DEPTH = 2

def bfs_step(games, completed):
    new_games = []

    def update(result, game, new_games, completed):
        if result is None:
            new_games.append(game)
        else:
            completed += 1

        return new_games, completed

    for game in games:
        moves = game.valid_moves()
        for move in moves[:-1]:
            new_game = copy.deepcopy(game)
            result = new_game.make_move(*move)
            new_games, completed = update(result, new_game,
                                          new_games, completed)

        result = game.make_move(*moves[-1])
        new_games, completed = update(result, game,
                                      new_games, completed)

    return new_games, completed

def num_possible_games(game):
    pid = os.getpid()
    games = [game]
    completed = 0
    depth = 0

    while games:
        games, completed = bfs_step(games, completed)

        depth += 1
        print('Process {}, Depth {}: {} games, {} completed'.format(
                pid, depth, len(games), completed))

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
        games, _ = bfs_step(games, 0)

    with multiprocessing.Pool(len(games)) as pool:
        completed = pool.map(num_possible_games, games)

    print(sum(completed))
