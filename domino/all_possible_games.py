import common
import copy
import domino
import itertools
import multiprocessing
import random

FIXED_MOVES = 5

def compute_all_possible_games(game):
    games = [game]
    completed = []

    while games:
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

        games = new_games

    return completed

with common.stopwatch('Initializing random game'):
    game = domino.Game(skinny_board=True)

    for i in range(FIXED_MOVES):
        moves = game.valid_moves()
        move = random.choice(moves)
        game.make_move(*move)

with common.stopwatch('Computation of all possible games'):
    games = [game]
    for i in range(2):
        new_games = []
        for game in games:
            moves = game.valid_moves()
            for move in moves:
                new_game = copy.deepcopy(game)
                new_game.make_move(*move)
                new_games.append(new_game)

        games = new_games

    with multiprocessing.Pool(len(games)) as pool:
        completed = pool.map(compute_all_possible_games, games)

    completed = itertools.chain(*completed)

    print(len(list(completed)))
