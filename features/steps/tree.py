from behave import *
from hamcrest import assert_that, equal_to
from testing import catch_all

from articulate.tree import Tree


@when('the instructions are converted to a tree (expecting trouble)')
@catch_all
def step_impl(context):
    context.tree = Tree(context.instructions)

@when('the instructions are converted to a tree')
def step_impl(context):
    context.tree = Tree(context.instructions)

@then('the tree should have {number:d} root instructions')
@then('the tree should have {number:d} root instruction')
def step_impl(context, number):
    assert_that(len(context.tree),
       equal_to(number))

@then('the tree should look like this')
def step_impl(context):
    assert_that(context.tree.to_pretty().rstrip(),
       equal_to(context.text))
    
