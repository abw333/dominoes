import collections
import domino
import random

def _randomized_hands():
    '''
    :return: 4 hands, obtained by shuffling the 28 dominoes used in
             this variation of the game, and distributing them evenly
    '''
    dominoes = [domino.Domino(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(dominoes)
    return [domino.Hand(dominoes[0:7]), domino.Hand(dominoes[7:14]),
            domino.Hand(dominoes[14:21]), domino.Hand(dominoes[21:28])]

def _validate_player(player):
    '''
    Checks that a player is a valid player. Valid players are: 0, 1, 2, and 3.

    :param int player: player to be validated
    :return: None
    :raises NoSuchPlayerException: if the player is invalid
    '''
    valid_players = range(4)
    if player not in valid_players:
        valid_players = ', '.join(str(p) for p in valid_players)
        raise domino.NoSuchPlayerException('{} is not a valid player. Valid players'
                                           ' are: {}'.format(player, valid_players))

def _domino_hand(d, hands):
    '''
    :param Domino d: domino to find within the hands
    :param list hands: hands to find domino in
    :return: index of the hand that contains the specified domino
    :raises NoSuchDominoException: if no hand contains the specified domino
    '''
    for i, hand in enumerate(hands):
        if d in hand:
            return i

    raise domino.NoSuchDominoException('{} is not in any hand!'.format(d))

'''
namedtuple to represent the result of a dominoes game.

:var player: the last player to make a move
:var won: True if the game ended due to an empty hand;
          False if the game ended due to being stuck
:var points: the absolute value of this quantity indicates
             the amount of points earned by the winning team.
             This quantity is positive if the last player to
             make a move is part of the winning team, and
             negative otherwise. If it is 0, it means the
             game ended in a tie
'''
Result = collections.namedtuple('Result', ['player', 'won', 'points'])

class Game:
    '''
    Python class for objects that represent a dominoes game.

    This variation of the dominoes game is played
    using 28 dominoes, which use values from 0 to 6:
    [0|0][0|1][0|2][0|3][0|4][0|5][0|6]
    [1|1][1|2][1|3][1|4][1|5][1|6]
    [2|2][2|3][2|4][2|5][2|6]
    [3|3][3|4][3|5][3|6]
    [4|4][4|5][4|6]
    [5|5][5|6]
    [6|6]

    These dominoes are shuffled, and distributed evenly among
    4 players. These players then sit on the edges of a square.
    Players sitting opposite of each other are on the same team,
    and the center of the square is the game board. Throughout
    the game, each player will only be able to see their hand,
    the game board, and the amount of dominoes left in the hands
    of the other players. Note that no player can see the values
    on the dominoes in the hands of the other players.

    The 4 players will then take turns placing dominoes from their
    hands onto the game board. The game board consists of a chain
    of dominoes placed end to end such that the values on connected
    ends always match.

    Prior to distributing the dominoes, the 4 players will agree on
    which player will play first, either by designating a specific
    player or a specific domino that must be played first (often [6|6]).
    After the game starts, play proceeds clockwise.

    If a player is able to place a domino on the board, he/she must.
    Only if they have no possible moves, can the pass on their turn.

    The game ends either when a player runs out of dominoes or when no
    player can play a domino (in which case we say the game is stuck).

    If a player runs out of dominoes, his/her team will earn a number
    of points computed by adding all the values of all the dominoes
    remaining in the hands of the 3 other players.

    If the game is stuck, each team will add up all the values of
    all the dominoes remaining in their hands. The team with the
    lower score wins, and earns a number of points computed by
    adding both teams' scores. If both teams have the same score,
    the game is declared a tie, and neither team earns any points.

    :param Domino starting_domino: the domino that should be played
                                   to start the game. The player
                                   with this domino in their hand
                                   will play first.
    :param int starting_player: the player that should play first.
                                This value is ignored if a starting
                                domino is provided. Players are
                                referred to by their indexes: 0, 1,
                                2, and 3. 0 and 2 are on one team,
                                and 1 and 3 are on another team.
    :var board: the game board
    :var hands: a list containing each player's hand
    :var turn: the player whose turn it is
    :var result: None if the game is in progress; otherwise a
                 Result object indicating the outcome of the game
    '''
    def __init__(self, starting_domino=None, starting_player=0):
        self.board = domino.Board()

        self.hands = _randomized_hands()

        if starting_domino is None:
            _validate_player(starting_player)
            self.turn = starting_player
        else:
            self.turn = _domino_hand(starting_domino, self.hands)
            self.make_move(starting_domino, True)

        self.result = None

    def skinny_board(self):
        '''
        Converts the board representation used by this game from a regular
        Board to a less descriptive but more memory efficient SkinnyBoard.

        :return: None
        '''
        self.board = domino.SkinnyBoard.from_board(self.board)

    def _remaining_points(self):
        '''
        :return: a list indicating the amount of points
                 left in the hands of each of the 4 players
        '''
        points = []
        for hand in self.hands:
            points.append(sum(d.first + d.second for d in hand))

        return points

    def _has_valid_move(self):
        '''
        :return: a boolean indicating whether the player
                 whose turn it is has any valid moves
        '''
        if not self.board:
            return True

        for d in self.hands[self.turn]:
            if self.board.left_end() in d or \
               self.board.right_end() in d:
                return True

        return False

    def valid_moves(self):
        '''
        :return: a list of valid moves for the player whose turn it is.
                 Moves are represented by a tuple of Domino and bool. The
                 Domino indicates the domino that can be played, and the
                 bool indicates on what end of the board the domino can be
                 played (True for left, False for right).
        '''
        if not self.board:
            return [(d, True) for d in self.hands[self.turn]]

        moves = []
        for d in self.hands[self.turn]:
            if self.board.left_end() in d:
                moves.append((d, True))
            # do not double count moves if both of the board's ends have
            # the same value, and a domino can be placed on both of them
            if self.board.right_end() in d and \
               self.board.left_end() != self.board.right_end():
                moves.append((d, False))

        return moves

    def make_move(self, d, left):
        '''
        Plays a domino from the hand of the player whose turn it is onto one
        end of the game board. If the game does not end, the turn is advanced
        to the next player who has a valid move.

        :param Domino d: domino to be played
        :param bool left: end of the board on which to play the
                          domino (True for left, False for right)
        :return: a Result object if the game ends; None otherwise
        :raises GameOverException: if the game has already ended
        :raises NoSuchDominoException: if the domino to be played is not in
                                       the hand of the player whose turn it is
        :raises EndsMismatchException: if the domino cannot be placed on
                                       the specified position in the board
        '''
        if self.result is not None:
            raise domino.GameOverException('Cannot make a move - the game is over!')

        self.hands[self.turn].play(d)

        try:
            if left:
                self.board.add_left(d)
            else:
                self.board.add_right(d)
        except domino.EndsMismatchException as error:
            # return the domino to the hand if it cannot be placed on the board
            self.hands[self.turn].draw(d)

            raise error

        # check if the game ended due to a player running out of dominoes
        if not self.hands[self.turn]:
            self.result = Result(self.turn, True, sum(self._remaining_points()))
            return self.result

        # advance the turn to the next player with a valid move.
        # if no player has a valid move, the game is stuck.
        num_players = len(self.hands)
        stuck = True
        for _ in range(num_players):
            self.turn = (self.turn + 1) % num_players
            if self._has_valid_move():
                stuck = False
                break

        if stuck:
            player_points = self._remaining_points()
            team_points = [player_points[0] + player_points[2],
                           player_points[1] + player_points[3]]

            if team_points[0] < team_points[1]:
                self.result = Result(self.turn, False, pow(-1, self.turn) * sum(team_points))
            elif team_points[0] == team_points[1]:
                self.result = Result(self.turn, False, 0)
            else:
                self.result = Result(self.turn, False, pow(-1, self.turn + 1) * sum(team_points))

            return self.result

    def __str__(self):
        string_list = ['Board: {}'.format(self.board)]

        for i, hand in enumerate(self.hands):
            string_list.append("Player {}'s hand: {}".format(i, hand))

        if self.result is None:
            string_list.append("Player {}'s turn".format(self.turn))
        else:
            if self.result.won:
                string_list.append(
                    'Player {} won and scored {} points!'.format(self.result.player,
                                                                 self.result.points)
                )
            else:
                if self.result.points > 0:
                    string_list.append(
                        'Player {} stuck the game and won {} points!'.format(self.result.player,
                                                                             self.result.points)
                    )
                elif not self.result.points:
                    string_list.append(
                        'Player {} stuck the game and tied!'.format(self.result.player)
                    )
                else:
                    string_list.append(
                        'Player {} stuck the game and won'
                        ' the opposing team {} points!'.format(self.result.player,
                                                               -1 * self.result.points)
                    )

        return '\n'.join(string_list)

    def __repr__(self):
        return str(self)
