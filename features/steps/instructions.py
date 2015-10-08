from behave import *
from hamcrest import assert_that, equal_to

from articulate.parser import Instruction

@given('a "{directive}" instruction')
def step_impl(context, directive):
    context.instruction = Instruction(directive, {}, 0)

@given('the instruction has an argument {argument} = {value}')
def step_impl(context, argument, value):
    context.instruction.arguments[argument] = value

@given('a specific sequence of instructions')
def step_impl(context):
    context.instructions = []
    for n, row in enumerate(context.table):
        arguments = {key: row[key] for key in context.table.headings}
        directive = arguments.pop('directive')
        indentation = int(arguments.pop('indentation'))
        instruction = Instruction(directive, arguments, indentation)
        instruction.line_number = n + 1
        instruction.source = 'behave'
        context.instructions.append(instruction)

@then('the instructions should be the following')
def step_impl(context):
    for n, row in enumerate(context.table):
        instruction = context.instructions[n]
        expected = {key: row[key] for key in context.table.headings}
        assert_that(instruction.source,
           equal_to('behave'),
                    'source for instruction %i' % n)
        assert_that(instruction.line_number,
           equal_to(int(expected.pop('line_number'))),
                    'line number for instruction %i' % n)
        assert_that(instruction.directive,
           equal_to(expected.pop('directive')),
                    'directive for instruction %i' % n)
        assert_that(instruction.indentation,
           equal_to(int(expected.pop('indentation'))),
                    'indentation for instruction %i' % n)
        for key, value in expected.items():
            assert_that(instruction.arguments.get(key),
               equal_to(value),
                        'arg "%s" for instruction %i' % (key, n))
