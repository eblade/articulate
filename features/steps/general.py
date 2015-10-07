from behave import *
from hamcrest import *

@then('it raises a {expected_type} with message "{msg}"')
def step(context, expected_type, msg):
    """
    Expects that the "when" step was run with the @testing.catch_all decorator.
    """
    assert isinstance(context.exc, eval(expected_type)),\
        "Invalid exception %s - expected %s"\
        % (type(context.exc).__name__, expected_type)
    assert_that(context.exc.msg,
       equal_to(msg))

@then('it raises a {expected_type}')
def step(context, expected_type):
    """
    Expects that the "when" step was run with the @testing.catch_all decorator.
    """
    assert isinstance(context.exc, eval(expected_type)),\
        "Invalid exception %s - expected %s"\
        % (type(context.exc).__name__, expected_type)

