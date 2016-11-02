import collections
import domino
import random

def randomized_hands():
    dominoes = [domino.Domino(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(dominoes)
    return [domino.Hand(dominoes[0:7]), domino.Hand(dominoes[7:14]),
            domino.Hand(dominoes[14:21]), domino.Hand(dominoes[21:28])]

Result = collections.namedtuple('Result', ['player', 'won', 'points'])

class Game:
    def __init__(self, starting_domino=None, starting_player=0):
        self.board = domino.Board()

        self.hands = randomized_hands()

        if starting_domino is None:
            self.turn = starting_player
        else:
            self.turn = self._domino_hand(starting_domino)
            self.make_move(starting_domino, True)

        self.result = None

    def skinny_board(self):
        self.board = domino.SkinnyBoard.from_board(self.board)

    def _domino_hand(self, d):
        for i, hand in enumerate(self.hands):
            if d in hand:
                return i

    def _remaining_points(self):
        points = []
        for hand in self.hands:
            points.append(sum(d.first + d.second for d in hand))

        return points

    def _has_valid_move(self):
        if not self.board:
            return True

        for d in self.hands[self.turn]:
            if self.board.left_end() in d or \
               self.board.right_end() in d:
                return True

        return False

    def valid_moves(self):
        if not self.board:
            return [(d, True) for d in self.hands[self.turn]]

        moves = []
        for d in self.hands[self.turn]:
            if self.board.left_end() in d:
                moves.append((d, True))
            if self.board.right_end() in d and \
               self.board.left_end() != self.board.right_end():
                moves.append((d, False))

        return moves

    def make_move(self, d, left):
        self.hands[self.turn].play(d)

        try:
            if left:
                self.board.add_left(d)
            else:
                self.board.add_right(d)
        except domino.EndsMismatchException as error:
            self.hands[self.turn].draw(d)

            raise error

        if not self.hands[self.turn]:
            self.result = Result(self.turn, True, sum(self._remaining_points()))
            return self.result

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
