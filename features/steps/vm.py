from behave import *
from hamcrest import assert_that, equal_to, has_key, not_, is_
from mock import Mock
from io import StringIO

from articulate.vm import evaluate, resolve, substitute, DEBUG
from articulate.scope import Scope
from articulate.redirect import redirector


@given('a VM')
def step_impl(context):
    context.scope = Scope()
    context.vm_out = StringIO()
    context.vm_err = StringIO()
    context.resolve = resolve

@given('the current scope has some variable {variable} = {value:d}')
def step_impl(context, variable, value):
    context.scope[variable] = value

@given('a resolver that returns "{value}"')
def step_impl(context, value):
    context.resolver = Mock(return_value=value)

@given('the substituter as resolver')
def step_impl(context):
    context.resolver = resolve

@given('the normal resolver is used')
def step_impl(context):
    context.resolver = substitute

@when('the instruction is fed to the VM')
def step_impl(context):
    with redirector(out=context.vm_out, err=context.vm_err):
        evaluate(context.instruction, context.scope)

@when('the instructions are fed to the VM')
def step_impl(context):
    with redirector(out=context.vm_out, err=context.vm_err):
        for instruction in context.instructions:
            evaluate(instruction, context.scope)

@when('the tree is fed to the VM')
def step_impl(context):
    with redirector(out=context.vm_out, err=context.vm_err):
        for instruction in context.tree.instructions:
            evaluate(instruction, context.scope)

@then(u'the output from the VM should be')
def step_impl(context):
    assert_that(context.vm_out.getvalue(),
       equal_to(context.text + ('\n' if context.text else '')))

@then(u'the variable "{variable}" should be undefined')
def step_impl(context, variable):
    assert variable not in context.scope.keys(),\
        'Variable "%s" was defined in current scope while it should not have been!' % variable

@then(u'the variable "{variable}" should have the value {value:d}')
def step_impl(context, variable, value):
    assert_that(context.scope.get(variable),
       equal_to(value))

@then(u'the variable "{variable}" should have the value {value:f}')
def step_impl(context, variable, value):
    assert_that(context.scope.get(variable),
       equal_to(value))

@then(u'the variable "{variable}" should have the value "{value}"')
def step_impl(context, variable, value):
    assert_that(context.scope.get(variable),
       equal_to(value))

@then(u'there should be a function called {pattern}')
def step_impl(context, pattern):
    assert_that(context.scope.functions, 
        has_key(pattern))

# Resolver

@given(u'an expression {expression}')
def step_impl(context, expression):
    context.expression = expression

@when(u'the expression is resolved')
def step_impl(context):
    context.result = resolve(context.expression, context.scope)

@when('the expression is substituted')
def step_impl(context):
    context.expression = substitute(context.expression, context.scope, resolve=context.resolver)

@then('the expression should be {expression}')
def step_impl(context, expression):
    assert_that(context.expression,
       equal_to(expression))

@then(u'the result should have the value {value:d}')
def step_impl(context, value):
    assert_that(context.result,
       equal_to(value))

@then(u'the result should have the value True')
def step_impl(context):
    assert context.result is True

@then(u'the result should have the value False')
def step_impl(context):
    assert context.result is False

@then(u'the result should be an integer')
def step_impl(context):
    assert_that(context.result,
            is_(int))

@then(u'the result should be a boolean')
def step_impl(context):
    assert_that(context.result,
            is_(bool))

@then('the resolver was called with "{expression}"')
def step_impl(context, expression):
    assert_that(context.resolver.was_called_with(expression))
