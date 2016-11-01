import collections
import domino
import random

def randomized_hands():
    dominoes = [domino.Domino(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(dominoes)
    return [Hand(dominoes[0:7]), Hand(dominoes[7:14]),
            Hand(dominoes[14:21]), Hand(dominoes[21:28])]

Result = collections.namedtuple('Result', ['player', 'type', 'points'])

class Hand:
    def __init__(self, dominoes):
        self.dominoes = dominoes

    def play(self, d):
        try:
            self.dominoes.remove(d)
        except ValueError:
            raise Exception('Cannot make move -'
                            ' {} is not in hand!'.format(d))

    def __contains__(self, d):
        return d in self.dominoes

    def __iter__(self):
        return iter(self.dominoes)

    def __len__(self):
        return len(self.dominoes)

    def __str__(self):
        return ''.join(str(d) for d in self.dominoes)

    def __repr__(self):
        return str(self)

class Game:
    def __init__(self, starting_domino=None, starting_player=0):
        self.board = domino.Board()

        self.hands = randomized_hands()

        if starting_domino is None:
            self.turn = starting_player
        else:
            self.turn = self.domino_hand(starting_domino)
            self.make_move(starting_domino, True)

        self.result = None

    def skinny_board(self):
        self.board = domino.SkinnyBoard.from_board(self.board)

    def domino_hand(self, d):
        for i, hand in enumerate(self.hands):
            if d in hand:
                return i

    def remaining_points(self):
        points = []
        for hand in self.hands:
            points.append(sum(d.first + d.second for d in hand))

        return points

    def has_valid_move(self):
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

        if left:
            self.board.add_left(d)
        else:
            self.board.add_right(d)

        if not self.hands[self.turn]:
            self.result = Result(self.turn, 'WON', sum(self.remaining_points()))
            return self.result

        num_players = len(self.hands)
        stuck = True
        for _ in range(num_players):
            self.turn = (self.turn + 1) % num_players
            if self.has_valid_move():
                stuck = False
                break

        if stuck:
            player_points = self.remaining_points()
            team_points = [player_points[0] + player_points[2],
                           player_points[1] + player_points[3]]

            if team_points[0] < team_points[1]:
                self.result = Result(self.turn, 'STUCK', -1 ** self.turn * sum(team_points))
            elif team_points[0] == team_points[1]:
                self.result = Result(self.turn, 'STUCK', 0)
            else:
                self.result = Result(self.turn, 'STUCK', -1 ** (1 + self.turn) * sum(team_points))

            return self.result

    def __str__(self):
        string_list = ['Board:', str(self.board)]
        for i, hand in enumerate(self.hands):
            string_list.extend(["Player {}'s hand:".format(i), str(hand)])

        if self.result is None:
            string_list.append("Player {}'s turn".format(self.turn))
        else:
            if self.result.type == 'WON':
                string_list.append(
                    'Player {} won and scored {} points!'.format(self.result.player,
                                                                 self.result.points)
                )
            elif self.result.type == 'STUCK':
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
                        'Player {} stuck the game and lost {} points!'.format(self.result.player,
                                                                              self.result.points)
                    )

        return '\n'.join(string_list)

    def __repr__(self):
        return str(self)
