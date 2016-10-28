class Domino:
    '''
    Python class representing a single domino.

    :param int first: first value on the domino
    :param int second: second value on the domino

    Usage::
        >>> import domino
        >>> d = domino.Domino(1, 2)
        >>> d
        [1|2]
        >>> d_inv = d.inverted()
        >>> d_inv
        [2|1]
        >>> d == d_inv
        True
        >>> other_d = domino.Domino(1, 3)
        >>> d == other_d
        False
        >>> 2 in d
        True
    '''
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def inverted(self):
        '''
        Returns a new Domino, with the same
        values, but in inverted positions.
        '''
        return Domino(self.second, self.first)

    def __str__(self):
        return '[{}|{}]'.format(self.first, self.second)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Domino):
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
