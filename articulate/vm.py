"""
This is the Virtual Machine that holds the evaluation loop.
"""

from .scope import Scope

DEBUG = False

def printi(recursion, *parts):
    if DEBUG: print('    '*recursion, *parts)


def evaluate(instruction, scope, recursion=0):
    scope = scope if scope is not None else Scope()

    printi(recursion, '***evaluate', instruction)
    printi(recursion, "Directive:", instruction.directive)
    printi(recursion, 'Scope:', {k: v for k, v in scope.items() if not k.startswith('_')})

    # Executing according to directives
    directive = instruction.directive
    function = None
    jump = False

    if directive == 'print':
        result = resolve(instruction.arguments['expression'], scope, recursion + 1)
        print(result)

    elif directive == 'set':
        target = instruction.arguments['target']
        result = resolve(instruction.arguments['expression'], scope, recursion + 1)
        scope[target] = result

    elif directive == 'define':
        function = scope.define(instruction.arguments['function'])

    elif directive == 'return':
        result = resolve(instruction.arguments['expression'], scope, recursion + 1)
        scope.returning = True
        return result

    elif directive == 'if':
        printi(recursion, "If", instruction.arguments['expression'])
        result = resolve(instruction.arguments['expression'], scope, recursion + 1)
        printi(recursion, "If result:", result)
        if not result:
            printi(recursion, "If fails, jumping")
            jump = True
        else:
            printi(recursion, "If holds")

    elif directive == 'nop':
        pass

    else:
        raise RuntimeError('Unsupported directive "%s".' % instruction.directive)

    # Functions should not execute sub-instructions, but store pointers to them
    if function is not None:
        function.instructions = instruction.instructions
        return

    # Handle scoping
    if not jump and len(instruction.instructions) > 0:
        sub_scope = scope.copy()
        result = step_in(instruction, sub_scope, recursion)
        if sub_scope.returning:
            printi(recursion, "ReturningE: ", result)
            scope.returning = True
            return result


def step_in(instruction, scope, recursion=0):
    printi(recursion, '***step_in', instruction)
    #printi(recursion, "Available functions:", list(scope.functions.values()))
    sub_scope = scope.copy()
    for instruction in instruction.instructions:
        result = evaluate(instruction, sub_scope, recursion + 1)
        if sub_scope.returning:
            printi(recursion, "ReturningS: ", result)
            scope.returning = True
            return result
    return None


def resolve(expression, scope, recursion=0):
    printi(recursion, "***resolve", expression)

    # First, try substitution
    expression = substitute(expression, scope, recursion + 1)
    printi(recursion, "Resolve after substitution:", expression)

    # Then, try with the function we have in the scope
    #printi(recursion, "Available functions:", list(scope.functions.values()))
    for function in scope.functions.values():
        printi(recursion, "Testing function:", function.pattern, function._expanded)
        r = function.parse(expression)
        if r is not None:
            printi(recursion, "Going in")
            sub_scope = scope.copy()
            sub_scope.update(r.named)
            printi(recursion, 'Scope:', {k: v for k, v in sub_scope.items() if not k.startswith('_')})
            for instruction in function.instructions:
                printi(recursion, "Instruction", instruction)
                result = evaluate(instruction, sub_scope, recursion + 1)
                if sub_scope.returning:
                    printi(recursion, "ReturningR: ", result)
                    scope.returning = True
                    return result
            raise RuntimeError('Function without return.')

    # Then, let python evaluate
    printi(recursion, "Eval:", expression)
    result = eval(expression, scope)
    printi(recursion, 'Substitute returning:', result)
    return result

def substitute(expression, scope, recursion=0, resolve=resolve):
    printi(recursion, "***substitute", expression)
    parenthesis_level = 0
    parenthesis_start = -1
    parenthesis_end = -1
    last_c = ' '
    parts = []
    for n, c in enumerate(expression):
        if c == '(':
            if parenthesis_level == 0 and last_c in ' +-/*%':
                printi(recursion, "Starting at", n)
                parenthesis_start = n
                printi(recursion, 'Parts before:', parenthesis_start, parenthesis_end, parts)
                parts.append(expression[parenthesis_end + 1:parenthesis_start])
                printi(recursion, 'Parts after:', parts)
            parenthesis_level += 1
        elif c == ')':
            parenthesis_level -= 1
            if parenthesis_level == 0:
                printi(recursion, "Ending at", n)
                parenthesis_end = n
                parenthesis = expression[parenthesis_start + 1:parenthesis_end]
                printi(recursion, "Group:", parenthesis)
                printi(recursion, 'Parts before group:', parenthesis_start, parenthesis_end, parts)
                parts.append(resolve(parenthesis, scope, recursion + 1))
                printi(recursion, 'Parts after group:', parts)

        last_c = c
            
    parts.append(expression[parenthesis_end + 1:])
    parts = [part for part in parts if part]
    printi(recursion, 'Parts:', parts)
    expression = ''.join([str(part) for part in parts])

    printi(recursion, 'Substiute returning:', expression)
    return expression

