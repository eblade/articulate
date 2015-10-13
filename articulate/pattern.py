from parse import parse, compile
from itertools import product
import re

re_general = re.compile(r'<([A-Za-z0-9_]+)>')
re_typed = re.compile(r'<([A-Za-z0-9_]+)\:([A-Za-z0-9_]+)>')


parse_type_map = {
    'str': '',
    'int': ':d',
    'float': ':f',
}

class Parameter:
    def __init__(self, name, template, type, referenced):
        self.name = name
        self.template = template
        self.type = type
        self.referenced = referenced

    def __repr__(self):
        return '<%s%s %s>' % (':' if self.referenced else '', self.name, self.type)


class Expansion:
    def __init__(self, pattern):
        self.pattern = pattern
        self._parser = compile(pattern)
        self.parameters = {}

    def parse(self, expression):
        return self._parser.parse(expression)

    def __repr__(self):
        return '<Expansion %s>' % (self.pattern)


class Pattern:
    def __init__(self, pattern, directive):
        self.pattern = pattern
        self.expand()
        #print("Pattern:", pattern, self._expanded)
        self._p = [compile(expansion.pattern) for expansion in self._expanded]
        if len(self._p) == 0:
            self._p = [compile(pattern)]
        self.directive = directive

    def __repr__(self):
        return "<Pattern %s>" % self.pattern

    def parse(self, expression):
        for expansion in self._expanded:
            result = expansion.parse(expression)
            if result:
                return result, expansion
        return None, None

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

        all_templates = {}
        types = {}
        for pointer, name, type in pointers:
            types[pointer] = type
            templates = list()
            if type == 'str':
                templates.append(Parameter(name, '"{' + name + '}"', type, False))
            elif type in parse_type_map.keys():
                templates.append(Parameter(name, '{' + name + parse_type_map.get(type, '') + '}', type, False))
            templates.append(Parameter(name, ':{' + name + '}', type, True))
            all_templates[pointer] = templates
                
        all_templates = [
            [(k, w) for w in v]
            for k, v in all_templates.items()
        ]

        for subs in product(*all_templates):
            pattern = self.pattern
            parameters = {}
            for pointer, parameter in subs:
                pattern = pattern.replace(pointer, parameter.template)
                parameters[parameter.name] = parameter
            expansion = Expansion(pattern)
            expansion.parameters = parameters
            self._expanded.append(expansion)
