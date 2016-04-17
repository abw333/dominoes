import common
import copy
import domino

with common.stopwatch('Computing all possible games'):
    in_progress = [domino.Game()]
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
