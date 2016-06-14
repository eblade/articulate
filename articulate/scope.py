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

    def define_python(self, python_thing):
        if hasattr(python_thing, '__init__'):
            self.define_python_class(python_thing)
        else:
            self.define_python_function(python_thing)
    
    def define_python_function(self, function):
        python_function = PythonFunction(function)
        self.functions[python_function.pattern] = python_function
        return python_function

    def define_python_class(self, klass):
        python_class = PythonClass(klass)
        self.functions[python_class.pattern] = python_class
        return python_class

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


class PythonFunction(Pattern):
    def __init__(self, python_function):
        super().__init__(python_function.__pattern__, 'python-function')
        self.python_function = python_function
        self.varnames = python_function.__code__.co_varnames[:python_function.__code__.co_argcount]

    def run(self, scope):
        arguments = [scope[argument] for argument in self.varnames]
        return self.python_method(*arguments)


class PythonMethod(Pattern):
    def __init__(self, python_method):
        super().__init__(python_method.__pattern__, 'python-method')
        self.python_method = python_method
        self.varnames = python_method.__code__.co_varnames[:python_method.__code__.co_argcount]

    def run(self, scope):
        arguments = [scope[argument] for argument in self.varnames]
        return self.python_method(*arguments)


class PythonClass(Pattern):
    def __init__(self, python_class):
        super().__init__(python_class.__pattern__, 'python')
        self.python_class = python_class
        self.varnames = python_class.__init__.__code__.co_varnames[:python_class.__init__.__code__.co_argcount]

        # Import all defined methods
        self.functions = {}
        for name in dir(python_class):
            if name.startswith('_'):
                continue
            obj = getattr(python_class, name)
            if not hasattr(obj, '__pattern__'):
                continue
            
            self.functions[obj.__pattern__] = PythonMethod(obj)
    
    def run(self, scope):
        arguments = [scope[argument] for argument in self.varnames if argument != 'self']
        return self.python_class(*arguments)
