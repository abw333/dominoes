import domino

class SkinnyBoard:
    def __init__(self, left=None, right=None, length=0):
        self.left = left
        self.right = right
        self.length = length

    @classmethod
    def from_board(cls, board):
        if len(board):
            left = board.left_end()
            right = board.right_end()
        else:
            left = None
            right = None

        return cls(left, right, len(board))

    def left_end(self):
        if not self:
            raise domino.EmptyBoardException('Cannot retrieve the left end of'
                                             ' the board because it is empty!')

        return self.left

    def right_end(self):
        if not self:
            raise domino.EmptyBoardException('Cannot retrieve the right end of'
                                             ' the board because it is empty!')

        return self.right

    def add_left(self, d):
        if not self:
            self.left = d.first
            self.right = d.second
        elif d.second == self.left_end():
            self.left = d.first
        elif d.first == self.left_end():
            self.left = d.second
        else:
            raise domino.EndsMismatchException(
                '{} cannot be added to the left of'
                ' the board - values do not match!'.format(d)
            )

        self.length += 1

    def add_right(self, d):
        if not self:
            self.left = d.first
            self.right = d.second
        elif d.first == self.right_end():
            self.right = d.second
        elif d.second == self.right_end():
            self.left = d.first
        else:
            raise domino.EndsMismatchException(
                '{} cannot be added to the right of'
                ' the board - values do not match!'.format(d)
            )

        self.length += 1

    def __len__(self):
        return self.length

    def __str__(self):
        if not self:
            return ''
        elif self.length == 1:
            return str(domino.Domino(self.left, self.right))
        else:
            left_domino = domino.Domino(self.left, '?')
            right_domino = domino.Domino('?', self.right)
            middle_dominoes = [domino.Domino('?', '?')] * (self.length - 2)
            dominoes = [left_domino] + middle_dominoes + [right_domino]
            return ''.join(str(d) for d in dominoes)

    def __repr__(self):
        return str(self)
