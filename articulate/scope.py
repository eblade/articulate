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
        self._exposed = []

    def define(self, define):
        function = Function(define)
        self.functions[define] = function
        function.functions = self.functions.copy()
        return function

    def copy(self):
        scope = Scope(self)
        scope.functions = self.functions.copy()
        return scope
    
    @property
    def exposed(self):
        return {k: v for k, v in self.items() if k in self._exposed}

    def expose(self, name):
        self._exposed.append(name.strip())

class Function(Pattern):
    def __init__(self, pattern):
        super().__init__(pattern, 'function')
        self.instructions = []
        self.functions = {}
