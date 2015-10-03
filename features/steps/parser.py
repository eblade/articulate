from behave import *
from hamcrest import *

from articulate.parser import parse_line, parse_string

def catch_all(func):
    def wrapper(context, *args, **kwargs):
        try:
            func(context, *args, **kwargs)
            context.exc = None
        except Exception as e:
            context.exc = e

    return wrapper

@given('the line {line}')
def step_impl(context, line):
    context.line = line

@given(u'{spaces:d} spaces are prepended')
def step_impl(context, spaces):
    context.line = ' '*spaces + context.line

@given(u'{tabs:d} tabs are prepended')
def step_impl(context, tabs):
    context.line = '\t'*tabs + context.line

@when('the line is parsed')
@catch_all
def step_impl(context):
    context.instruction = parse_line(context.line)

@then('there should be an instruction')
def step_impl(context):
    assert_that(context.instruction,
         is_not(None))

@then('the directive should be "{directive}"')
def step_impl(context, directive):
    assert_that(context.instruction.directive,
       equal_to(directive))

@then('"{key}" should be {value}')
def step_impl(context, key, value):
    assert_that(context.instruction.args.get(key),
       equal_to(value))

@then('the indentation should be {indent:d}')
def step_impl(context, indent):
    assert_that(context.instruction.indent,
       equal_to(indent))

@then('it raises a {expected_type} with message "{msg}"')
def step(context, expected_type, msg):
    assert isinstance(context.exc, eval(expected_type)), "Invalid exception %s - expected %s" % (type(context.exc).__name__, expected_type)
    assert_that(context.exc.msg,
       equal_to(msg))

@given('the following code')
def step_impl(context):
    context.code = context.text

@when('the code is parsed')
def step_impl(context):
    context.instructions = parse_string(context.code, source='behave')

@then('the instruction should be the following')
def step_impl(context):
    for n, row in enumerate(context.table):
        instruction = context.instructions[n]
        expected = {key: row[key] for key in context.table.headings}
        assert_that(instruction.source,
           equal_to('behave'),
                    'source for instruction %i' % n)
        assert_that(instruction.line_number,
           equal_to(int(expected.pop('lineno'))),
                    'line number for instruction %i' % n)
        assert_that(instruction.directive,
           equal_to(expected.pop('directive')),
                    'directive for instruction %i' % n)
        assert_that(instruction.indent,
           equal_to(int(expected.pop('indentation'))),
                    'indent for instruction %i' % n)
        for key, value in expected.items():
            assert_that(instruction.args.get(key),
               equal_to(value),
                        'arg "%s" for instruction %i' % (key, n))
