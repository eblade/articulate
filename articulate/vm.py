
class Evaluator:
    def __init__(self):
        self.current_scope = dict()

    def evaluate(self, instruction):
        directive = instruction.directive
        if directive == 'print':
            result = self.resolve(instruction.arguments['expression'])
            print(result)
        elif directive == 'set':
            target = instruction.arguments['target']
            result = self.resolve(instruction.arguments['expression'])
            self.current_scope[target] = result
        else:
            raise RuntimeError('Unsupported directive "%s".' % instruction.directive)
    
    def resolve(self, expression):
        return eval(expression, self.current_scope)


