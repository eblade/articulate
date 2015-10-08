from behave import *
from hamcrest import assert_that, equal_to
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

@then(u'the output from the VM should be')
def step_impl(context):
    assert_that(context.vm_out.getvalue(),
       equal_to(context.text + ('\n' if context.text else '')))

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