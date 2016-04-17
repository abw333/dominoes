import common
import copy
import domino
import itertools
import random
import threading

FIXED_MOVES = 10

def compute_all_possible_games(game, return_holder, return_key):
    in_progress = [game]
    completed = []

    while in_progress:
        game = in_progress.pop()
        moves = game.valid_moves()

        for move in moves:
            new_game = copy.deepcopy(game)
            result = new_game.make_move(*move)
            if result is None:
                in_progress.append(new_game)
            else:
                completed.append(new_game)

    return_holder[return_key] = completed

with common.stopwatch('Computing all possible games'):
    game = domino.Game()

    for i in range(FIXED_MOVES):
        moves = game.valid_moves()
        move = random.choice(moves)
        game.make_move(*move)

    completed = {}

    moves = game.valid_moves()

    threads = []
    for i, move in enumerate(moves):
        new_game = copy.deepcopy(game)
        new_game.make_move(*move)

        thread = threading.Thread(target=compute_all_possible_games,
                                  args=(new_game, completed, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    completed = completed.values()
    completed = itertools.chain(*completed)

    print(len(list(completed)))
