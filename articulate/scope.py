"""
A scope is a local set of variables and functions.
"""

from .parser import Pattern

class Scope(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions = {}
        self.return_value = None
        self.returning = False

    def define(self, define):
        function = Function(define)
        self.functions[define] = function
        return function

    def copy(self):
        scope = Scope(self)
        scope.functions = self.functions.copy()
        return scope

class Function(Pattern):
    def __init__(self, pattern):
        super().__init__(pattern, 'function')
        self.instructions = []
