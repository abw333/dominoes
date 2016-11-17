import dominoes

class SkinnyBoard:
    '''
    Python class for objects that represent a domino board.
    A domino board consists of a series of dominoes placed
    end to end such that the values on connected ends match.
    This class reduces the memory required by each instance
    by remembering only the values at the ends of the board.

    :param int left: value on the left end of the board
    :param int right: value on the right end of the board
    :param int length: amount of dominoes on the board

    .. code-block:: python

        >>> import dominoes
        >>> d1 = dominoes.Domino(1, 2)
        >>> d2 = dominoes.Domino(1, 3)
        >>> b = dominoes.SkinnyBoard()
        >>> repr(b)
        ''
        >>> b.add_left(d1)
        >>> b
        [1|2]
        >>> b.add_right(d2)
        EndsMismatchException: [1|3] cannot be added to the right of the board - values do not match!
        >>> b.add_left(d2)
        >>> b
        [3|?][?|2]
        >>> b.left_end()
        3
        >>> b.right_end()
        2
        >>> len(b)
        2
    '''
    def __init__(self, left=None, right=None, length=0):
        self._left = left
        self._right = right
        self._length = length

    @classmethod
    def from_board(cls, board):
        '''
        :param Board board: board to represent
        :return: SkinnyBoard to represent the given Board
        '''
        if len(board):
            left = board.left_end()
            right = board.right_end()
        else:
            left = None
            right = None

        return cls(left, right, len(board))

    def left_end(self):
        '''
        :return: the outward-facing value on the left end of the board
        :raises EmptyBoardException: if the board is empty
        '''
        if not self:
            raise dominoes.EmptyBoardException('Cannot retrieve the left end of'
                                               ' the board because it is empty!')

        return self._left

    def right_end(self):
        '''
        :return: the outward-facing value on the right end of the board
        :raises EmptyBoardException: if the board is empty
        '''
        if not self:
            raise dominoes.EmptyBoardException('Cannot retrieve the right end of'
                                               ' the board because it is empty!')

        return self._right

    def add_left(self, d):
        '''
        Adds the provided domino to the left end of the board.

        :param Domino d: domino to add
        :return: None
        :raises EndsMismatchException: if the values do not match
        '''
        if not self:
            self._left = d.first
            self._right = d.second
        elif d.second == self.left_end():
            self._left = d.first
        elif d.first == self.left_end():
            self._left = d.second
        else:
            raise dominoes.EndsMismatchException(
                '{} cannot be added to the left of'
                ' the board - values do not match!'.format(d)
            )

        self._length += 1

    def add_right(self, d):
        '''
        Adds the provided domino to the right end of the board.

        :param Domino d: domino to add
        :return: None
        :raises EndsMismatchException: if the values do not match
        '''
        if not self:
            self._left = d.first
            self._right = d.second
        elif d.first == self.right_end():
            self._right = d.second
        elif d.second == self.right_end():
            self._right = d.first
        else:
            raise dominoes.EndsMismatchException(
                '{} cannot be added to the right of'
                ' the board - values do not match!'.format(d)
            )

        self._length += 1

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return self._length

    def __str__(self):
        if not self:
            return ''
        elif self._length == 1:
            return str(dominoes.Domino(self._left, self._right))
        else:
            left_domino = dominoes.Domino(self._left, '?')
            right_domino = dominoes.Domino('?', self._right)
            middle_dominoes = [dominoes.Domino('?', '?')] * (self._length - 2)
            all_dominoes = [left_domino] + middle_dominoes + [right_domino]
            return ''.join(str(d) for d in all_dominoes)

    def __repr__(self):
        return str(self)
