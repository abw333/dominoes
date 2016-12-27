import copy
import operator

def make_moves(game, player=lambda g: None):
    '''
    For each of a Game object's valid moves, yields
    a tuple containing the move and the Game object
    obtained by playing the move on the original Game
    object. The original Game object will be modified.

    :param Game game: the game to make moves on
    :param callable player: a player to call on the
                            game before making any
                            moves, to determine the
                            order in which they get
                            made.
    '''
    # determine the order in which to make moves
    player(game)

    # copy the original game before making all
    # but the last move
    for move in game.valid_moves[:-1]:
        new_game = copy.deepcopy(game)
        new_game.make_move(*move)
        yield move, new_game

    # don't copy the original game before making
    # the last move
    move = game.valid_moves[-1]
    game.make_move(*move)
    yield move, game

def alphabeta(game, alpha_beta=(-float('inf'), float('inf')), player=lambda g: None):
    if game.result is not None:
        return [], pow(-1, game.result.player) * game.result.points

    if game.turn % 2:
        best_value = float('inf')
        op = operator.lt
        update = lambda ab, v: (ab[0], min(ab[1], v))
    else:
        best_value = -float('inf')
        op = operator.gt
        update = lambda ab, v: (max(ab[0], v), ab[1])

    for move, new_game in make_moves(game, player):
        moves, value = alphabeta(new_game, alpha_beta, player)
        if op(value, best_value):
            best_value = value
            best_moves = moves
            best_moves.insert(0, move)
            alpha_beta = update(alpha_beta, best_value)
            if alpha_beta[1] <= alpha_beta[0]:
                break
    return best_moves, best_value
