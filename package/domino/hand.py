import collections
import domino

class Hand(collections.abc.Sequence):
    '''
    Python class for objects that represent a hand of dominoes.

    :param Sequence dominoes: sequence of dominoes in the hand

    Usage::
        >>> import domino
        >>> d1 = domino.Domino(1, 2)
        >>> d2 = domino.Domino(1, 3)
        >>> h = domino.Hand([d1, d2])
        >>> h
        [1|2][1|3]
        >>> d1 in h
        True
        >>> len(h)
        2
        >>> for d in h: d
        [1|2]
        [1|3]
        >>> h.play(d1)
        >>> h
        [1|3]
    '''
    def __init__(self, dominoes):
        self._dominoes = list(dominoes)

    def play(self, d):
        '''
        Removes a domino from the hand.

        :param Domino d: domino to remove from the hand
        :raises NoSuchDominoException: if the domino is not in the hand
        '''
        try:
            self._dominoes.remove(d)
        except ValueError:
            raise domino.NoSuchDominoException('Cannot make move -'
                                               ' {} is not in hand!'.format(d))

    def draw(self, d):
        '''
        Adds a domino to the hand.

        :param Domino d: domino to add to the hand
        '''
        self._dominoes.append(d)

    def __getitem__(self, i):
        return self._dominoes[i]

    def __len__(self):
        return len(self._dominoes)

    def __str__(self):
        return ''.join(str(d) for d in self._dominoes)

    def __repr__(self):
        return str(self)
