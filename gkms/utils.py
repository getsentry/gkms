import sys

from contextlib import contextmanager


@contextmanager
def open_file(file_name, mode='r'):
    if file_name == '-':
        if mode == 'r':
            yield sys.stdin
        else:
            yield sys.stdout
    else:
        with open(file_name, mode) as f:
            yield f
