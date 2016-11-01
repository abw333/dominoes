class Hand:
    def __init__(self, dominoes):
        self.dominoes = dominoes

    def play(self, d):
        try:
            self.dominoes.remove(d)
        except ValueError:
            raise Exception('Cannot make move -'
                            ' {} is not in hand!'.format(d))

    def __contains__(self, d):
        return d in self.dominoes

    def __iter__(self):
        return iter(self.dominoes)

    def __len__(self):
        return len(self.dominoes)

    def __str__(self):
        return ''.join(str(d) for d in self.dominoes)

    def __repr__(self):
        return str(self)
