import domino

class Series:
    def __init__(self, target_score=200, starting_domino=None):
        if starting_domino is None:
            starting_domino = domino.Domino(6, 6)

        self.games = [domino.Game(starting_domino=starting_domino)]
        self.scores = [0, 0]
        self.target_score = target_score

    def is_over(self):
        return max(self.scores) >= self.target_score

    def next_game(self):
        if self.is_over():
            raise domino.SeriesOverException(
                'Cannot start a new game - series ended with a score of {} to {}'.format(*self.scores)
            )

        result = self.games[-1].result
        if result is None:
            raise domino.GameInProgressException(
                'Cannot start a new game - the latest one has not finished!'
            )

        if result.points >= 0:
            self.scores[result.player % 2] += result.points
        else:
            self.scores[(result.player + 1) % 2] -= result.points

        if self.is_over():
            return

        if result.won:
            self.games.append(domino.Game(starting_player=result.player))
        else:
            if result.points >= 0:
                self.games.append(domino.Game(starting_player=result.player))
            else:
                self.games.append(domino.Game(starting_player=(result.player + 1) % 4))

        return self.games[-1]

    def __str__(self):
        string_list = ['Series to {} points'.format(self.target_score)]

        for i, score in enumerate(self.scores):
            string_list.append('Team {} has {} points'.format(i, score))

        for i, game in enumerate(self.games):
            string_list.extend(['Game {}'.format(i), str(game)])

        return '\n'.join(string_list)
