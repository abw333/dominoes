import collections

class Board:
    '''
    Python class for objects that represent a domino board.
    A domino board consists of a series of dominoes placed
    end to end such that the values on connected ends match.

    Usage::
        >>> import domino
        >>> d1 = domino.Domino(1, 2)
        >>> d2 = domino.Domino(1, 3)
        >>> d3 = domino.Domino(2, 3)
        >>> d4 = domino.Domino(2, 2)
        >>> b = domino.Board()
        >>> b

        >>> b.add(d1)
        >>> b
        [1|2]
        >>> b.add(d2)
        >>> b
        [3|1][1|2]
        >>> b.add(d3)
        >>> b
        [2|3][3|1][1|2]
        >>> b.add(d4)
        >>> b
        [2|2][2|3][3|1][1|2]
        >>> b.left_end()
        2
        >>> b.right_end()
        2
        >>> len(b)
        4
    '''
    def __init__(self):
        self.board = collections.deque()

    def left_end(self):
        return self.board[0].first

    def right_end(self):
        return self.board[-1].second

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
