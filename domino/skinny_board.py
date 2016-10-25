class SkinnyBoard:
    def __init__(self, left=None, right=None, length=0):
        self.left = left
        self.right = right
        self.length = length

    @classmethod
    def from_board(cls, board):
        if len(board):
            left, right = board.ends()
        else:
            left, right = None, None

        return cls(left, right, len(board))

    def left_end(self):
        return self.left

    def right_end(self):
        return self.right

    def ends(self):
        return self.left, self.right

    def add_left(self, domino):
        if not self.length:
            self.left = domino.first
            self.right = domino.second
        elif domino.second == self.left:
            self.left = domino.first
        elif domino.first == self.left:
            self.left = domino.second
        else:
            raise Exception('{0} cannot be added to the left of'
                            ' the board - numbers do not match!'.format(domino))

        self.length += 1

    def add_right(self, domino):
        if not self.length:
            self.left = domino.first
            self.right = domino.second
        elif domino.first == self.right:
            self.right = domino.second
        elif domino.second == self.right:
            self.left = domino.first
        else:
            raise Exception('{0} cannot be added to the right of'
                            ' the board - numbers do not match!'.format(domino))

        self.length += 1

    def __len__(self):
        return self.length

    def __str__(self):
        if not self.length:
            return ''
        elif self.length == 1:
            return str(Domino(self.left, self.right))
        else:
            left_domino = Domino(self.left, '?')
            right_domino = Domino('?', self.right)
            middle_dominos = [Domino('?', '?')] * (self.length - 2)
            dominos = [left_domino] + middle_dominos + [right_domino]
            return ''.join([str(domino) for domino in dominos])
