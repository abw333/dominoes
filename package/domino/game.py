import domino
import random

def randomized_hands():
    dominoes = [domino.Domino(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(dominoes)
    return dominoes[0:7], dominoes[7:14], dominoes[14:21], dominoes[21:28]

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

    def has_empty_hand(self):
        for hand in self.hands:
            if not hand:
                return True

        return False

    def remaining_points(self):
        points = []
        for hand in self.hands:
            points.append(sum(d.first + d.second for d in hand))

        return points

    def has_valid_move(self, turn):
        if not self.board:
            return True

        for d in self.hands[turn]:
            if self.board.left_end() in d or \
               self.board.right_end() in d:
                return True

        return False

    def is_stuck(self):
        for turn in range(len(self.hands)):
            if self.has_valid_move(turn):
                return False

        return True

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
        if d not in self.hands[self.turn]:
            raise Exception('Cannot make move - {} is not'
                            ' in the hand of player {}.'.format(d, self.turn))

        if left:
            self.board.add_left(d)
        else:
            self.board.add_right(d)

        self.hands[self.turn].remove(d)

        result = None
        if self.has_empty_hand():
            result = (self.turn, 'WON', sum(self.remaining_points()))
        elif self.is_stuck():
            player_points = self.remaining_points()
            team_points = [player_points[0] + player_points[2],
                           player_points[1] + player_points[3]]
            if team_points[0] < team_points[1]:
                result = (self.turn, 'STUCK', -1 ** self.turn * sum(team_points))
            elif team_points[0] == team_points[1]:
                result = (self.turn, 'STUCK', 0)
            else:
                result = (self.turn, 'STUCK', -1 ** (1 + self.turn) * sum(team_points))

        if result is not None:
            self.result = result
            return result

        while True:
            self.turn = (self.turn + 1) % 4
            if self.has_valid_move(self.turn):
                break

    def __str__(self):
        string_list = ['Board:', str(self.board)]
        for i, hand in enumerate(self.hands):
            hand_string = ''.join(str(d) for d in hand)
            string_list.extend(["Player {}'s hand:".format(i), hand_string])

        if self.result is None:
            string_list.append("Player {}'s turn".format(self.turn))
        else:
            last_mover, result_type, points = self.result
            if result_type == 'WON':
                string_list.append('Player {} won and '
                                   'scored {} points!'.format(last_mover, points))
            elif result_type == 'STUCK':
                if points > 0:
                    string_list.append('Player {} stuck the '
                                       'game and won {} points!'.format(last_mover, points))
                elif not points:
                    string_list.append('Player {} stuck the game and tied!'.format(last_mover))
                else:
                    string_list.append('Player {} stuck the '
                                       'game and lost {} points!'.format(last_mover, points))

        return '\n'.join(string_list)

    def __repr__(self):
        return str(self)
