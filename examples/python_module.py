from articulate import define

@define('python function of <x:int>')
def python_function(x):
    return x * 3


@define('a place where x is half of <x:float>')
def python_using(x):
    return {
        'x': x/2.,
    }
