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
