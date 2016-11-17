import collections
import dominoes

class Hand(collections.abc.Sequence):
    '''
    Python class for objects that represent a hand of dominoes.

    :param Sequence dominoes: sequence of dominoes in the hand

    .. code-block:: python

        >>> import dominoes
        >>> d1 = dominoes.Domino(1, 2)
        >>> d2 = dominoes.Domino(1, 3)
        >>> h = dominoes.Hand([d1, d2])
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
        :return: the index within the hand of the played domino
        :raises NoSuchDominoException: if the domino is not in the hand
        '''
        try:
            i = self._dominoes.index(d)
        except ValueError:
            raise dominoes.NoSuchDominoException('Cannot make move -'
                                                 ' {} is not in hand!'.format(d))

        self._dominoes.pop(i)
        return i

    def draw(self, d, i=None):
        '''
        Adds a domino to the hand.

        :param Domino d: domino to add to the hand
        :param int i: index at which to add the domino;
                      by default adds to the end of the hand
        :return: None
        '''
        if i is None:
            self._dominoes.append(d)
        else:
            self._dominoes.insert(i, d)

    def __getitem__(self, i):
        return self._dominoes[i]

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self._dominoes)

    def __str__(self):
        return ''.join(str(d) for d in self._dominoes)

    def __repr__(self):
        return str(self)
