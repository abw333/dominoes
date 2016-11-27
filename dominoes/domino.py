import collections

# for convenience, immutability, and performance
DominoBase = collections.namedtuple('DominoBase', ['first', 'second'])

class Domino(DominoBase):
    '''
    Python class for objects that represent a domino. Each
    domino is a rectangular tile with a line dividing its
    face into two square ends. Each end is marked with an
    integer value, typically ranging from 0 to 6 or 9.

    :param int first: value on one end
    :param int second: value on the other end
    :var first: value on one end
    :var second: value on the other end

    .. code-block:: python

        >>> import dominoes
        >>> d = dominoes.Domino(1, 2)
        >>> d
        [1|2]
        >>> d_inv = d.inverted()
        >>> d_inv
        [2|1]
        >>> d == d_inv
        True
        >>> other_d = dominoes.Domino(1, 3)
        >>> d == other_d
        False
        >>> 2 in d
        True
    '''
    def inverted(self):
        '''
        :return: a new Domino, with the same values, but in inverted positions
        '''
        return Domino(self.second, self.first)

    def __str__(self):
        return '[{}|{}]'.format(self.first, self.second)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        # order of values does not matter
        # e.g. Domino(1, 2) == Domino(2, 1)
        return sorted((self.first, self.second)) == \
            sorted((other.first, other.second))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        # order of values does not matter
        # e.g. hash(Domino(1, 2)) == hash(Domino(2, 1))
        return hash(tuple(sorted((self.first, self.second))))

    def __contains__(self, key):
        return key == self.first or key == self.second
