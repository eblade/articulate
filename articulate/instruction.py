class Instruction:
    def __init__(self, directive, arguments, indentation):
        self.directive = directive
        self.arguments = arguments or {}
        self.indentation = indentation
        self.line_number = 0
        self.source_file = None
        self.instructions = []

    def append(self, instruction):
        self.instructions.append(instruction)

    def __len__(self):
        return len(self.instructions)

    def __repr__(self):
        return '<Instruction %s +%i %s>' % (self.source, self.line_number, self.directive)

    def to_pretty(self, level=0):
        output = '%s%s\n' % ('.'*level, repr(self))
        for instruction in self.instructions:
            output += instruction.to_pretty(level + 1)
        return output

