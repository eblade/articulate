from behave import *
from hamcrest import *
from testing import catch_all

from articulate.parser import parse_line, parse_string

@given('the line {line}')
def step_impl(context, line):
    context.line = line

@given('an empty line')
def step_impl(context):
    context.line = ''

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

@then(u'there should not be an instruction')
def step_impl(context):
    assert_that(context.instruction,
         is_(None))

@then('the directive should be "{directive}"')
def step_impl(context, directive):
    assert_that(context.instruction.directive,
       equal_to(directive))

@then('"{key}" should be {value}')
def step_impl(context, key, value):
    assert_that(context.instruction.args.get(key),
       equal_to(value))

@then('the indentation should be {indentation:d}')
def step_impl(context, indentation):
    assert_that(context.instruction.indentation,
       equal_to(indentation))

@given('the following code')
def step_impl(context):
    context.code = context.text

@when('the code is parsed')
def step_impl(context):
    context.instructions = parse_string(context.code, source='behave')

