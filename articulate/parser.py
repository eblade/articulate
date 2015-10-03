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
    def __init__(self, directive, args, indent):
        self.directive = directive
        self.args = args
        self.indent = indent
        self.line_number = 0
        self.source_file = None

def parse_line(line):
    line = line.rstrip()
    indent = _get_indent(line)
    line = line.lstrip()
    line = _strip_comment(line)

    for pattern in patterns:
        r = pattern.parse(line)
        if r is not None:
            return Instruction(pattern.directive, r.named, indent)

def _get_indent(line):
    spaces = 0
    for c in line:
        if c == ' ':
            spaces += 1
        elif c == '\t':
            raise SyntaxError("Indentation must only consist of spaces")
        else:
            break
    if spaces % INDENTATION != 0:
        raise SyntaxError("Indentation must be a factor of %i (was %i)" % (INDENTATION, spaces))
    return spaces / INDENTATION

def _strip_comment(line):
    return line

def parse_string(string, source=None):
    instructions = []
    for n, line in enumerate(string.split('\n')):
        instruction = parse_line(line)
        instruction.source = source
        instruction.line_number = n + 1
        instructions.append(instruction)
    return instructions
