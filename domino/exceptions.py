class EmptyBoardException(Exception):
    '''
    Exception to be raised for
    errors involving an empty board.
    '''
    pass

class EndsMismatchException(Exception):
    '''
    Exception to be raised for errors
    involving mismatched domino ends.
    '''
    pass

class GameInProgressException(Exception):
    '''
    Exception to be raised for errors
    involving a game that is in progress.
    '''
    pass

class GameOverException(Exception):
    '''
    Exception to be raised for errors
    involving a game that has ended.
    '''
    pass

class NoSuchDominoException(Exception):
    '''
    Exception to be raised for errors
    involving a specific missing domino.
    '''
    pass

class NoSuchPlayerException(Exception):
    '''
    Exception to be raised for errors
    involving a specific missing player.
    '''
    pass

class SeriesOverException(Exception):
    '''
    Exception to be raised for errors
    involving a series that has ended.
    '''
    pass
