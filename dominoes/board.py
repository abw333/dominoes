import collections
import dominoes

class Board:
    '''
    Python class for objects that represent a domino board.
    A domino board consists of a series of dominoes placed
    end to end such that the values on connected ends match.

    :var board: deque representing the game board

    .. code-block:: python

        >>> import dominoes
        >>> d1 = dominoes.Domino(1, 2)
        >>> d2 = dominoes.Domino(1, 3)
        >>> b = dominoes.Board()
        >>> repr(b)
        ''
        >>> b.add_left(d1)
        >>> b
        [1|2]
        >>> b.add_right(d2)
        EndsMismatchException: [1|3] cannot be added to the right of the board - values do not match!
        >>> b.add_left(d2)
        >>> b
        [3|1][1|2]
        >>> b.left_end()
        3
        >>> b.right_end()
        2
        >>> len(b)
        2
    '''
    def __init__(self):
        self.board = collections.deque()

    def left_end(self):
        '''
        :return: the outward-facing value on the left end of the board
        :raises EmptyBoardException: if the board is empty
        '''
        try:
            return self.board[0].first
        except IndexError:
            raise dominoes.EmptyBoardException('Cannot retrieve the left end of'
                                               ' the board because it is empty!')

    def right_end(self):
        '''
        :return: the outward-facing value on the right end of the board
        :raises EmptyBoardException: if the board is empty
        '''
        try:
            return self.board[-1].second
        except IndexError:
            raise dominoes.EmptyBoardException('Cannot retrieve the right end of'
                                               ' the board because it is empty!')

    def add_left(self, d):
        '''
        Adds the provided domino to the left end of the board.

        :param Domino d: domino to add
        :return: None
        :raises EndsMismatchException: if the values do not match
        '''
        if not self:
            self.board.append(d)
        elif d.first == self.left_end():
            self.board.appendleft(d.inverted())
        elif d.second == self.left_end():
            self.board.appendleft(d)
        else:
            raise dominoes.EndsMismatchException(
                '{} cannot be added to the left of'
                ' the board - values do not match!'.format(d)
            )

    def add_right(self, d):
        '''
        Adds the provided domino to the right end of the board.

        :param Domino d: domino to add
        :return: None
        :raises EndsMismatchException: if the values do not match
        '''
        if not self:
            self.board.append(d)
        elif d.first == self.right_end():
            self.board.append(d)
        elif d.second == self.right_end():
            self.board.append(d.inverted())
        else:
            raise dominoes.EndsMismatchException(
                '{} cannot be added to the right of'
                ' the board - values do not match!'.format(d)
            )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.board)

    def __str__(self):
        return ''.join(str(d) for d in self.board)

    def __repr__(self):
        return str(self)
