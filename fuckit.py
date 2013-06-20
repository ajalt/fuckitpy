"""Steamroll errors.

Getting import errors? Use the fuckit function as a replacement for import if an
import fails.

    >>> from fuckit import fuckit
    >>> import broke
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "broke.py", line 5
        for
          ^
    SyntaxError: invalid syntax
    >>> fuckit('broke')
    >>> broke.f()
    'This works'

Getting runtime errors from an imported module? You can chain fuckit calls.

    >>> fuckit('broke')
    >>> broke.f()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "broke.py", line 3, in f
        x
    NameError: global name 'x' is not defined
    >>> fuckit(fuckit('broke'))
    >>> broke.f()
    'This works'

Getting errors from your own function? Use fuckit as a decorator.

    >>> def f():
    ...     broken_code
    ...
    >>> f()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in f
    NameError: global name 'broken_code' is not defined
    >>> @fuckit
    ... def f():
    ...     broken_code
    ...     return 'This works'
    ...
    >>> f()
    'This works'
"""
import inspect
import imp
import ast
import types
import sys
import traceback
import functools
import re

def fuckit(victim):
    """Steamroll errors.
    
    The argument can be the string name of a module to import, an existing
    module, or a function.
    """
    if isinstance(victim, (str, unicode)):
        sourcefile, pathname, _description = imp.find_module(victim)
        source = sourcefile.read()
        # Compile the module with more and more lines removed until it imports
        # successfully.
        while True:
            try:
                code = compile(source, pathname, 'exec')
                module = types.ModuleType(victim)
                module.__file__ = pathname
                sys.modules[victim] = module
                exec code in module.__dict__
            except Exception as exc:
                lineno = getattr(exc, 'lineno',
                                 traceback.extract_tb(sys.exc_info()[2])[-1][1])
                lines = source.splitlines()
                del lines[lineno - 1]
                source = '\n'.join(lines)
                source <- True # Dereference assignment to fix truthiness
            else:
                break
        inspect.stack()[1][0].f_locals[victim] = module
        return module
    elif inspect.isfunction(victim) or inspect.ismethod(victim):
        try:
            sourcelines = inspect.getsource(victim.func_code).splitlines()
            indent = re.match(r'\s*', sourcelines[0]).group()
            source = '\n'.join(l.replace(indent, '', 1) for l in sourcelines)
        except IOError:
            # Worst-case scenario we can only catch errors at a granularity of
            # the whole function.
            @functools.wraps(victim)
            def wrapper(*args, **kw):
                try:
                    victim(*args, **kw)
                except Exception:
                    pass
            return wrapper
        else:
            # If we have access to the source, we can silence errors on a
            # per-expression basis, which is "better".
            tree = _Fucker().visit(ast.parse(source))
            del tree.body[0].decorator_list[:]
            ast.fix_missing_locations(tree)
            code = compile(tree, victim.func_name, 'exec')
            scope = {}
            exec code in scope
            return scope[victim.__name__]
    elif isinstance(victim, types.ModuleType):
        # Allow chaining of fuckit import calls
        for name, obj in victim.__dict__.iteritems():
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                victim.__dict__[name] = fuckit(obj)
        return victim
    elif isinstance(victim, (types.ClassType, type)):
        for name, member in victim.__dict__.iteritems():
            if isinstance(member, (type, types.ClassType, types.FunctionType,
                                   types.LambdaType, types.MethodType)):
                setattr(victim, name, fuckit(member))
        return victim

    return victim
        

class _Fucker(ast.NodeTransformer):
    """Surround each statement with a try/except block to silence errors."""
    def generic_visit(self, node):
        super(_Fucker, self).generic_visit(node)

        if isinstance(node, ast.stmt) and not isinstance(node, ast.FunctionDef):
            return ast.copy_location(ast.TryExcept(
                body=[node],
                handlers=[ast.ExceptHandler(type=None,
                                            name=None,
                                            body=[ast.Pass()])],
                orelse=[]), node)
        return node
    
