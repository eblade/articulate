"""
This module holds the publicly available API, e.g. things you can do in python-land.
"""

def define(pattern):
    """
    Docorator to create a python function that can be used in the 
    articulate scope like a native articulate function.

    my_python_module.py

        @define('<x:int> to the power of <y:int>')
        def power(x, y):
            return x ** y

    my_articulate_module.ar

        require my_python_module

        x = 4 to the power of 3
    """
    # function.__code__.co_varnames
    # function.__code__.co_argcount
    def wrapper(func):
        func.__pattern__ = pattern
        return func
    return wrapper
