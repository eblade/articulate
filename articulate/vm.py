"""
This is the Virtual Machine that holds the evaluation loop.
"""

class Evaluator:
    def __init__(self, scope=None):
        self.current_scope = scope.copy() if scope is not None else dict()

    def evaluate(self, instruction):
        # Executing according to directives
        directive = instruction.directive
        if directive == 'print':
            result = self.resolve(instruction.arguments['expression'])
            print(result)

        elif directive == 'set':
            target = instruction.arguments['target']
            result = self.resolve(instruction.arguments['expression'])
            self.current_scope[target] = result

        elif directive == 'nop':
            pass

        else:
            raise RuntimeError('Unsupported directive "%s".' % instruction.directive)

        # Handle scoping
        if len(instruction.instructions) > 0:
            sub_evaluator = Evaluator(self.current_scope)
            for instruction in instruction.instructions:
                sub_evaluator.evaluate(instruction)

    
    def resolve(self, expression):
        return eval(expression, self.current_scope)


