"""
Parse a file into instructions, one per line. Indentation is important,
as it controls scoping.
"""


from .pattern import Pattern
from .instruction import Instruction


INDENTATION = 4



system_patterns = [
    Pattern('require {module}', 'require'),
    Pattern('using {function}', 'using'),
    Pattern('define {function}', 'define'),
    Pattern('return {expression}', 'return'),
    Pattern('given', 'given'),
    Pattern('for {entry} in {list}', 'for-in'),
    Pattern('{target} = {expression}', 'set'),
    Pattern('print {expression}', 'print'),
    Pattern('if {expression}', 'if'),
    Pattern('expose {names}', 'expose'),
]


def parse_line(line, patterns=system_patterns):
    line = line.rstrip()
    indentation = _get_indentation(line)
    line = line.lstrip()
    line = _strip_comment(line)

    if not line:
        return None

    for pattern in patterns:
        result, expansion = pattern.parse(line)
        if result is not None:
            return Instruction(pattern.directive, result.named, indentation)

    return Instruction('void', {'expression': line}, indentation)

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
    return int(spaces / INDENTATION)

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
