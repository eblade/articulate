
class Tree:
    """
    The tree class defines a syntax tree where scoping becomes visible.
    """

    def __init__(self, instructions=None):
        self.indentation = -1
        self.current = self 
        self.instructions = []
        self.trace = [self]
        if instructions is not None:
            for instruction in instructions:
                self.append(instruction)

    def append(self, instruction):
        print('%i -> %i' % (self.current.indentation, instruction.indentation))
        if instruction.indentation == self.current.indentation + 1:
            print('append')
            self.current.instructions.append(instruction)

        elif instruction.indentation == self.current.indentation + 2:
            print('step in, append')
            self.current = self.current.instructions[-1]
            self.trace.append(self.current)
            self.current.instructions.append(instruction)

        elif instruction.indentation <= self.current.indentation:
            print('step out, append')
            self.trace = self.trace[:instruction.indentation+1]
            self.current = self.trace.pop()
            if len(self.trace) == 0:
                self.trace = [self]
            self.current.instructions.append(instruction)

        else:
            raise SyntaxError("Bad indentation transition (%i -> %i)."
                % (self.current.indentation + 1, instruction.indentation))

        print(self.trace)
        print(self.to_pretty())

    def __len__(self):
        return len(self.instructions)

    def __repr__(self):
        return '<Tree>'

    def to_pretty(self):
        output = ''
        for instruction in self.instructions:
            output += instruction.to_pretty()
        return output
