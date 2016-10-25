import random

from domino.board import Board
from domino.skinny_board import SkinnyBoard

class Domino:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def inverted(self):
        return Domino(self.second, self.first)

    def __str__(self):
        return '[{0}|{1}]'.format(self.first, self.second)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return sorted((self.first, self.second)) == sorted((other.first, other.second))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(sorted((self.first, self.second))))

    def __contains__(self, key):
        return key == self.first or key == self.second

class Game:
    def __init__(self, starting_player=0,
                 starting_domino=None, skinny_board=False):
        if skinny_board:
            self.board = SkinnyBoard()
        else:
            self.board = Board()

        self.hands = self.randomized_hands()

        if starting_domino is None:
            self.turn = starting_player
        else:
            self.turn = self.domino_hand(starting_domino)
            self.make_move(starting_domino, 'LEFT')

    def skinny_board(self):
        self.board = SkinnyBoard.from_board(self.board)

    def randomized_hands(self):
        dominos = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominos)
        return dominos[0:7], dominos[7:14], dominos[14:21], dominos[21:28]

    def domino_hand(self, domino):
        for i, hand in enumerate(self.hands):
            if domino in hand:
                return i

    def has_empty_hand(self):
        return bool([hand for hand in self.hands if not hand])

    def is_stuck(self):
        if not self.board:
            return False

        left_end, right_end = self.board.ends()
        for hand in self.hands:
            for domino in hand:
                if left_end in domino or right_end in domino:
                    return False

        return True

    def remaining_points(self):
        player_points = {}
        for i, hand in enumerate(self.hands):
            player_points[i] = sum([domino.first + domino.second for domino in hand])

        return player_points

    def valid_moves(self):
        if not self.board:
            return [(domino, 'LEFT') for domino in self.hands[self.turn]]

        moves = []

        left_end, right_end = self.board.ends()
        equal_ends = left_end == right_end
        for domino in self.hands[self.turn]:
            if left_end in domino:
                moves.append((domino, 'LEFT'))
            if right_end in domino and not equal_ends:
                moves.append((domino, 'RIGHT'))

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

    def make_move(self, domino, left_or_right):
        if domino not in self.hands[self.turn]:
            raise Exception('Cannot make move - {0} is not'
                            ' in the hand of player {1}.'.format(domino, self.turn))

        if left_or_right == 'LEFT':
            self.board.add_left(domino)
        elif left_or_right == 'RIGHT':
            self.board.add_right(domino)
        else:
            raise Exception('Cannot make move - `left_or_right` must be "LEFT" or "RIGHT".')

        self.hands[self.turn].remove(domino)
        return self.next_turn()

    def __str__(self):
        string_list = ['Board:', str(self.board)]
        for i, hand in enumerate(self.hands):
            hand_string = ''.join([str(domino) for domino in hand])
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

class Series:
    def __init__(self, target_score=200):
        self.games = [Game(starting_domino=Domino(6, 6))]
        self.scores = [0, 0]
        self.target_score = target_score

    def is_over(self):
        return max(self.scores) >= self.target_score

    def next_game(self):
        if self.is_over():
            raise Exception('Cannot start a new game - series '
                            'ended with a score of {0} to {1}'.format(*self.scores))

        result = self.games[-1].result()
        if result is None:
            raise Exception('Cannot start a new game - the latest one has not finished!')

        last_mover, result_type, points = result

        if points >= 0:
            self.scores[last_mover % 2] += points
        else:
            self.scores[(last_mover + 1) % 2] -= points

        if self.is_over():
            return

        if result_type == 'WON':
            self.games.append(Game(starting_player=last_mover))
        elif result_type == 'STUCK':
            if points >= 0:
                self.games.append(Game(starting_player=last_mover))
            else:
                self.games.append(Game(starting_player=(last_mover + 1) % 4))

        return self.games[-1]

    def __str__(self):
        string_list = ['Series to {0} points'.format(self.target_score)]

        for i, score in enumerate(self.scores):
            string_list.append('Team {0} has {1} points'.format(i, score))

        for i, game in enumerate(self.games):
            string_list.extend(['Game {0}'.format(i), str(game)])

        return '\n'.join(string_list)
