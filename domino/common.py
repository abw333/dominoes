import contextlib
import time

@contextlib.contextmanager
def stopwatch(message):
    print(message)
    start = time.time()
    yield
    elapsed = time.time() - start
    print(message, 'took {:.2f} seconds'.format(elapsed))
