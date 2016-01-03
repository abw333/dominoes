import domino
import random

def play_random_game(game):
    while True:
        random_move = random.choice(game.valid_moves())
        if game.make_move(*random_move) is not None:
            return

series = domino.Series()
game = series.games[0]
while True:
    play_random_game(game)
    game = series.next_game()

    if game is None:
        break

print(series)
