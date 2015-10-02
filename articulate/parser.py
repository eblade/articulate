from parse import parse, compile


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
    return 0

def _strip_comment(line):
    return line
