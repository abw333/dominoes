class Domino:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def inverted(self):
        return Domino(self.second, self.first)

    def __str__(self):
        return '[{0}|{1}]'.format(self.first, self.second)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return sorted((self.first, self.second)) == sorted((other.first, other.second))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(sorted((self.first, self.second))))

    def __contains__(self, key):
        return key == self.first or key == self.second
