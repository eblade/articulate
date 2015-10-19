"""
This module handles dynamic loading of articulate modules.
"""

import os
import importlib.machinery

from .parser import parse_string
from .tree import Tree
from .scope import Scope
from .pattern import Pattern

PATH = ['.', 'lib/articulate']

def require(module_path, scope, evaluate):
    """
    Load the module at module_path into scope. Supports:
    
     * Artiulate module files ending with .ar
     * Python module files ending with .py
    """
    parts = tuple(module_path.split('.'))
    
    file_path = None
    for root in PATH:
        for extension in ('.ar', '.py'):
            check = os.path.join(root, *parts) + extension
            if os.path.exists(check):
                file_path = check
                break
        if file_path is not None:
            break
        
    if file_path is None:
        raise ImportError('Could not find module "%s"' % module_path)

    print("Importing", file_path)
    if file_path.endswith('.ar'):
        with open(file_path, 'r') as f:
            source = f.read()

        instructions = parse_string(source, file_path)

        tree = Tree(instructions)

        local_scope = Scope()
        for instruction in tree.instructions:
            evaluate(instruction, local_scope)

        scope.functions.update(local_scope.functions)

    else:  # python module
        loader = importlib.machinery.SourceFileLoader(module_path, file_path)
        module = loader.load_module()

        # Import all defined functions into the scope
        for name, obj in module.__dict__.items():
            if name.startswith('_'):
                continue
            if not hasattr(obj, '__pattern__'):
                continue

            scope.define_python(obj)
