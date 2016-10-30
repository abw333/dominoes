import collections

class Board:
    def __init__(self):
        self.board = collections.deque()

    def left_end(self):
        return self.board[0].first

    def right_end(self):
        return self.board[-1].second

    def add(self, domino):
        if not self.board:
            self.board.append(domino)
        elif domino.first == self.left_end():
            self.board.appendleft(domino.inverted())
        elif domino.second == self.left_end():
            self.board.appendleft(domino)
        elif domino.first == self.right_end():
            self.board.append(domino)
        elif domino.second == self.right_end():
            self.board.append(domino.inverted())
        else:
            raise Exception('{} cannot be added to the board'
                            ' - ends do not match!'.format(domino))

    def __len__(self):
        return len(self.board)

    def __str__(self):
        return ''.join([str(domino) for domino in self.board])

    def __repr__(self):
        return str(self)
