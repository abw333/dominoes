import domino
import random

class Game:
    def __init__(self, starting_player=0,
                 starting_domino=None, skinny_board=False):
        if skinny_board:
            self.board = domino.SkinnyBoard()
        else:
            self.board = domino.Board()

        self.hands = self.randomized_hands()

        if starting_domino is None:
            self.turn = starting_player
        else:
            self.turn = self.domino_hand(starting_domino)
            self.make_move(starting_domino, 'LEFT')

    def skinny_board(self):
        self.board = domino.SkinnyBoard.from_board(self.board)

    def randomized_hands(self):
        dominoes = [domino.Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominoes)
        return dominoes[0:7], dominoes[7:14], dominoes[14:21], dominoes[21:28]

    def domino_hand(self, d):
        for i, hand in enumerate(self.hands):
            if d in hand:
                return i

    def has_empty_hand(self):
        return bool([hand for hand in self.hands if not hand])

    def is_stuck(self):
        if not self.board:
            return False

        for hand in self.hands:
            for d in hand:
                if self.board.left_end() in d or \
                   self.board.right_end() in d:
                    return False

        return True

    def remaining_points(self):
        player_points = {}
        for i, hand in enumerate(self.hands):
            player_points[i] = sum([d.first + d.second for d in hand])

        return player_points

    def valid_moves(self):
        if not self.board:
            return [(d, 'LEFT') for d in self.hands[self.turn]]

        moves = []
        for d in self.hands[self.turn]:
            if self.board.left_end() in d:
                moves.append((d, 'LEFT'))
            if self.board.right_end() in d and \
               self.board.left_end() != self.board.right_end():
                moves.append((d, 'RIGHT'))

        return moves

    def result(self):
        if self.has_empty_hand():
            return self.turn, 'WON', sum(self.remaining_points().values())
        elif self.is_stuck():
            player_points = self.remaining_points()
            team0_points = player_points[0] + player_points[2]
            team1_points = player_points[1] + player_points[3]
            if team0_points < team1_points:
                return self.turn, 'STUCK', -1 ** self.turn * (team0_points + team1_points)
            elif team0_points == team1_points:
                return self.turn, 'STUCK', 0
            else:
                return self.turn, 'STUCK', -1 ** (1 + self.turn) * (team0_points + team1_points)

    def next_turn(self):
        result = self.result()
        if result is not None:
            return result

        while True:
            self.turn = (self.turn + 1) % 4
            if self.valid_moves():
                break

    def make_move(self, d, left_or_right):
        if d not in self.hands[self.turn]:
            raise Exception('Cannot make move - {0} is not'
                            ' in the hand of player {1}.'.format(d, self.turn))

        if left_or_right == 'LEFT':
            self.board.add_left(d)
        elif left_or_right == 'RIGHT':
            self.board.add_right(d)
        else:
            raise Exception('Cannot make move - `left_or_right` must be "LEFT" or "RIGHT".')

        self.hands[self.turn].remove(d)
        return self.next_turn()

    def __str__(self):
        string_list = ['Board:', str(self.board)]
        for i, hand in enumerate(self.hands):
            hand_string = ''.join([str(d) for d in hand])
            string_list.extend(["Player {0}'s hand:".format(i), hand_string])

        result = self.result()
        if result is None:
            string_list.append("Player {0}'s turn".format(self.turn))
        else:
            last_mover, result_type, points = result
            if result_type == 'WON':
                string_list.append('Player {0} won and '
                                   'scored {1} points!'.format(last_mover, points))
            elif result_type == 'STUCK':
                if points > 0:
                    string_list.append('Player {0} stuck the '
                                       'game and won {1} points!'.format(last_mover, points))
                elif not points:
                    string_list.append('Player {0} stuck the game and tied!'.format(last_mover))
                else:
                    string_list.append('Player {0} stuck the '
                                       'game and lost {1} points!'.format(last_mover, points))

        return '\n'.join(string_list)
