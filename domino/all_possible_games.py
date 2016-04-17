import common
import copy
import domino
import random

FIXED_MOVES = 10

with common.stopwatch('Computing all possible games'):
    game = domino.Game()

    for i in range(FIXED_MOVES):
        moves = game.valid_moves()
        move = random.choice(moves)
        game.make_move(*move)

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

    print(len(completed))
