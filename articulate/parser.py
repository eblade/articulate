"""
Parse a file into instructions, one per line. Indentation is important,
as it controls scoping.
"""

from parse import parse, compile
from itertools import product
import re

from .instruction import Instruction


INDENTATION = 4

re_general = re.compile(r'<([A-Za-z0-9_]+)>')
re_typed = re.compile(r'<([A-Za-z0-9_]+)\:([A-Za-z0-9_]+)>')


parse_type_map = {
    'str': '',
    'int': ':d',
    'float': ':f',
}


class Pattern:
    def __init__(self, pattern, directive):
        self.pattern = pattern
        self.expand()
        print("Pattern:", pattern)
        print("Expanded:", self._expanded)
        self._p = [compile(pattern) for pattern in self._expanded]
        if len(self._p) == 0:
            self._p = [compile(pattern)]
        self.directive = directive

    def __repr__(self):
        return "<Pattern %s>" % self.pattern

    def parse(self, t):
        for p in self._p:
            result = p.parse(t)
            if result:
                return result

    def expand(self):
        self._expanded = []
        pointers = []

        general = re_general.findall(self.pattern)
        for name in general:
            pointers.append(('<' + name + '>', name, 'str'))

        typed = re_typed.findall(self.pattern)
        for name, type in typed:
            pointers.append(('<' + name + ':' + type + '>', name, type))

        #print("Pointers:", pointers)

        direct = []
        indirect = []
        for sub, name, type in pointers:
            if type == 'str':
                direct.append((sub, '"{' + name + '}"'))
            elif type in parse_type_map.keys():
                direct.append((sub, '{' + name + parse_type_map.get(type, '') + '}'))
                indirect.append((sub, '{' + name + '}'))
            else:
                direct.append((sub, '{' + name + '}'))
                
        for subs in product(direct, indirect):
            pattern = self.pattern
            for sub in subs:
                pattern = pattern.replace(*sub)
            self._expanded.append(pattern)


system_patterns = [
    Pattern('require {module}', 'require'),
    Pattern('using {using}', 'using'),
    Pattern('define {function}', 'define'),
    Pattern('return {expression}', 'return'),
    Pattern('given', 'given'),
    Pattern('for {entry} in {list}', 'for-in'),
    Pattern('{target} = {expression}', 'set'),
    Pattern('print {expression}', 'print'),
    Pattern('if {expression}', 'if'),
]


def parse_line(line, patterns=system_patterns):
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
