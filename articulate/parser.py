"""
Parse a file into instructions, one per line. Indentation is important,
as it controls scoping.
"""


from parse import parse, compile

INDENTATION = 4

class Pattern:
    def __init__(self, pattern, directive):
        self.pattern = pattern
        self._p = compile(pattern)
        self.directive = directive

    def parse(self, t):
        return self._p.parse(t)

patterns = [
    Pattern('require {module}', 'require'),
    Pattern('using {using}', 'using'),
    Pattern('define {function}', 'define'),
    Pattern('given', 'given'),
    Pattern('for {entry} in {list}', 'for-in'),
    Pattern('{target} = {expression}', 'set'),
    Pattern('print {expression}', 'print'),
]

class Instruction:
    def __init__(self, directive, arguments, indentation):
        self.directive = directive
        self.arguments = arguments
        self.indentation = indentation
        self.line_number = 0
        self.source_file = None
        self.instructions = []

    def append(self, instruction):
        self.instructions.append(instruction)

    def __len__(self):
        return len(self.instructions)

    def __repr__(self):
        return '<Instruction %s +%i %s>' % (self.source, self.lineno, self.directive)

    def to_pretty(self, level=0):
        output = '%s%s\n' % ('.'*level, repr(self))
        for instruction in self.instructions:
            output += instruction.to_pretty(level + 1)
        return output

def parse_line(line):
    line = line.rstrip()
    indentation = _get_indentation(line)
    line = line.lstrip()
    line = _strip_comment(line)

    if not line:
        return None

    for pattern in patterns:
        r = pattern.parse(line)
        if r is not None:
            return Instruction(pattern.directive, r.named, indentation)

    raise SyntaxError('Could not parse the line "%s".' % line)

def _get_indentation(line):
    spaces = 0
    for c in line:
        if c == ' ':
            spaces += 1
        elif c == '\t':
            raise SyntaxError("Indentation must only consist of spaces.")
        else:
            break
    if spaces % INDENTATION != 0:
        raise SyntaxError("Indentation must be a factor of %i (was %i)." % (INDENTATION, spaces))
    return spaces / INDENTATION

def _strip_comment(line):
    parts = line.split('#', 1)
    return parts[0].strip() if len(parts) == 2 else line

def parse_string(string, source=None):
    instructions = []
    for n, line in enumerate(string.split('\n')):
        instruction = parse_line(line)
        if instruction is None:
            continue
        instruction.source = source
        instruction.line_number = n + 1
        instructions.append(instruction)
    return instructions
