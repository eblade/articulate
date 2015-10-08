from behave import *
from hamcrest import assert_that, equal_to, has_key, not_
from io import StringIO

from articulate.vm import Evaluator
from articulate.redirect import redirector


@given('a VM')
def step_impl(context):
    context.evaluator = Evaluator()
    context.vm_out = StringIO()
    context.vm_err = StringIO()

@given(u'the current scope has some variable {variable} = {value:d}')
def step_impl(context, variable, value):
    context.evaluator.current_scope[variable] = value

@when('the instruction is fed to the VM')
def step_impl(context):
    with redirector(out=context.vm_out, err=context.vm_err):
        context.evaluator.evaluate(context.instruction)

@when('the instructions are fed to the VM')
def step_impl(context):
    with redirector(out=context.vm_out, err=context.vm_err):
        for instruction in context.instructions:
            context.evaluator.evaluate(instruction)

@when('the tree is fed to the VM')
def step_impl(context):
    with redirector(out=context.vm_out, err=context.vm_err):
        for instruction in context.tree.instructions:
            context.evaluator.evaluate(instruction)

@then(u'the output from the VM should be')
def step_impl(context):
    assert_that(context.vm_out.getvalue(),
       equal_to(context.text + ('\n' if context.text else '')))

@then(u'the variable "{variable}" should be undefined')
def step_impl(context, variable):
    assert variable not in context.evaluator.current_scope.keys(),\
        'Variable "%s" was defined in current scope while it should not have been!' % variable

@then(u'the variable "{variable}" should have the value {value:d}')
def step_impl(context, variable, value):
    assert_that(context.evaluator.current_scope.get(variable),
       equal_to(value))

@then(u'the variable "{variable}" should have the value {value:f}')
def step_impl(context, variable, value):
    assert_that(context.evaluator.current_scope.get(variable),
       equal_to(value))

@then(u'the variable "{variable}" should have the value "{value}"')
def step_impl(context, variable, value):
    assert_that(context.evaluator.current_scope.get(variable),
       equal_to(value))
