from behave import *
from hamcrest import *

from articulate.parser import parse_line


@given('the line {line}')
def step_impl(context, line):
    context.line = line

@when('the line is parsed')
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
