from .instruction import Instruction

SCOPING_DIRECTIVES = ('using', 'define', 'nop')
"""
Scoping directives are directives which "own" a scope and has a special
relation to it.
"""

class Tree:
    """
    The tree class defines a syntax tree where scoping becomes visible.
    """

    def __init__(self, instructions=None):
        self.directive = 'nop'
        self.indentation = -1
        self.target = self 
        self.instructions = []
        self.trace = [self]
        if instructions is not None:
            for instruction in instructions:
                self.append(instruction)

    def append(self, instruction):
        if instruction.indentation == self.target.indentation + 1:
            self.target.instructions.append(instruction)

        elif instruction.indentation == self.target.indentation + 2:
            last = self.target.instructions[-1]
            if last.directive not in SCOPING_DIRECTIVES:
                nop = Instruction('nop', None, last.indentation)
                nop.source = last.source
                nop.line_number = last.line_number
                self.target.append(nop)
                last = nop
            self.target = last
            self.trace.append(self.target)
            self.target.instructions.append(instruction)

        elif instruction.indentation <= self.target.indentation:
            self.trace = self.trace[:instruction.indentation+1]
            self.target = self.trace.pop()
            if len(self.trace) == 0:
                self.trace = [self]
            self.target.instructions.append(instruction)

        else:
            raise SyntaxError("Bad indentation transition (%i -> %i)."
                % (self.target.indentation + 1, instruction.indentation))

    def __len__(self):
        return len(self.instructions)

    def __repr__(self):
        return '<Tree>'

    def to_pretty(self):
        output = ''
        for instruction in self.instructions:
            output += instruction.to_pretty()
        return output
