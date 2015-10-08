import sys
from contextlib import contextmanager

@contextmanager
def redirector(out=None, err=None):
    old_stdout = sys.stdout
    if out is not None:
        sys.stdout = out
    old_stderr = sys.stderr
    if err is not None:
        sys.stderr = err
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
