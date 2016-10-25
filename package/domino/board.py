import collections

class Board:
    def __init__(self):
        self.board = collections.deque()

    def left_end(self):
        return self.board[0].first

    def right_end(self):
        return self.board[-1].second

    def ends(self):
        return self.left_end(), self.right_end()

    def add_left(self, domino):
        if not self.board or domino.second == self.left_end():
            self.board.appendleft(domino)
        elif domino.first == self.left_end():
            self.board.appendleft(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the left of'
                            ' the board - numbers do not match!'.format(domino))

    def add_right(self, domino):
        if not self.board or domino.first == self.right_end():
            self.board.append(domino)
        elif domino.second == self.right_end():
            self.board.append(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the right of'
                            ' the board - numbers do not match!'.format(domino))

    def __len__(self):
        return len(self.board)

    def __str__(self):
        return ''.join([str(domino) for domino in self.board])
