from domino.domino import Domino
from domino.game import Game

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
