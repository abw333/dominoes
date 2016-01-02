import domino
import random

game = domino.Game(starting_domino=domino.Domino(6, 6))
print game

while True:
    valid_moves = game.valid_moves()
    random_move = random.choice(valid_moves)
    result = game.make_move(*random_move)

    print game

    if result is not None:
        break
