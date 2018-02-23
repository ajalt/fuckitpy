__doc__ = """Steamroll errors.

Getting import errors? Use the fuckit function as a replacement for import if an
import fails.

    >>> import fuckit
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
    >>> f()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in f
    NameError: global name 'broken_code' is not defined
    >>> @fuckit
    ... def f():
    ...     broken_code
    ...     return 'This works'
    >>> f()
    'This works'
    
Getting errors in a block of code and don't want to write your own try/except
block? Use fuckit as a context manager.

    >>> with fuckit:
    ...     print('This works')
    ...     raise RuntimeError()
    This works
"""

import ast
import sys
import types


class _fuckit(types.ModuleType):
    # We overwrite the sys.modules entry for this function later, which will
    # cause all the values in globals() to be changed to None to allow garbage
    # collection. That forces us to do all of our imports into locals().
    class _Fucker(ast.NodeTransformer):
        """Surround each statement with a try/except block to silence errors."""

        def generic_visit(self, node):
            import ast
            import sys
            ast.NodeTransformer.generic_visit(self, node)

            if isinstance(node, ast.stmt) and not isinstance(node, ast.FunctionDef):
                if sys.version_info[0] == 3:
                    new_node = ast.Try(
                        body=[node],
                        handlers=[ast.ExceptHandler(type=None,
                                                    name=None,
                                                    body=[ast.Pass()])],
                        orelse=[],
                        finalbody=[ast.Pass()])
                else:
                    new_node = ast.TryExcept(
                        body=[node],
                        handlers=[ast.ExceptHandler(type=None,
                                                    name=None,
                                                    body=[ast.Pass()])],
                        orelse=[])
                return ast.copy_location(new_node, node)
            return node

    def __call__(self, victim):
        """Steamroll errors.

        The argument can be the string name of a module to import, an existing
        module, or a function.
        """
        import inspect
        import imp
        import ast
        import types
        import sys
        import traceback
        import functools
        import re

        PY3 = sys.version_info[0] == 3
        if PY3:
            basestring = str
            get_func_code = lambda f: f.__code__
            exec_ = __builtins__['exec']
            types.ClassType = type
        else:
            basestring = __builtins__['basestring']
            get_func_code = lambda f: f.func_code

            def exec_(_code_, _globs_):
                _locs_ = _globs_
                exec('exec _code_ in _globs_, _locs_')

        if isinstance(victim, basestring):
            sourcefile, pathname, (_, _, module_type) = imp.find_module(victim)
            if module_type == imp.PY_SOURCE:
                source = sourcefile.read()
                # If we have the source, we can silence SyntaxErrors by
                # compiling the module with more and more lines removed until
                # it imports successfully.
                while True:
                    try:
                        code = compile(source, pathname, 'exec')
                        module = types.ModuleType(victim)
                        module.__file__ = pathname
                        sys.modules[victim] = module
                        exec_(code, module.__dict__)
                    except Exception as exc:
                        extracted_ln = traceback.extract_tb(sys.exc_info()[2])[-1][1]
                        lineno = getattr(exc, 'lineno', extracted_ln)
                        lines = source.splitlines()
                        lines[lineno - 1] = ''
                        source = '\n'.join(lines)
                        if not PY3:
                            source <- True # Dereference assignment to fix truthiness in Py2
                    else:
                        break
            else:
                # If we don't have access to the source code, there's not much
                # we can do to stop import-time errors.
                try:
                    module = __import__(victim)
                except Exception:
                    # If the module doesn't import at this point, it's
                    # obviously not worth using anyway, so just return an
                    # empty module.
                    module = types.ModuleType(victim)
            inspect.stack()[1][0].f_locals[victim] = module
            return module
        elif inspect.isfunction(victim) or inspect.ismethod(victim):
            try:
                sourcelines = inspect.getsource(get_func_code(victim)).splitlines()
                indent = re.match(r'\s*', sourcelines[0]).group()
                source = '\n'.join(l.replace(indent, '', 1) for l in sourcelines)
            except IOError:
                # Worst-case scenario we can only catch errors at a granularity
                # of the whole function.
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
                tree = self._Fucker().visit(ast.parse(source))
                del tree.body[0].decorator_list[:]
                ast.fix_missing_locations(tree)
                code = compile(tree, victim.__name__, 'exec')
                namespace = dict(victim.__globals__)
                exec_(code, namespace)
                return namespace[victim.__name__]
        elif isinstance(victim, types.ModuleType):
            # Allow chaining of fuckit import calls
            for name, obj in victim.__dict__.items():
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    victim.__dict__[name] = self(obj)
            return victim
        elif isinstance(victim, (types.ClassType, type)):
            for name, member in victim.__dict__.items():
                if isinstance(member, (type, types.ClassType, types.FunctionType,
                                       types.LambdaType, types.MethodType)):
                    setattr(victim, name, self(member))
            return victim

        return victim

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        # Returning True prevents the error from propagating. Don't silence
        # KeyboardInterrupt or SystemExit. We aren't monsters.
        return exc_type is None or issubclass(exc_type, Exception)


sys.modules[__name__] = _fuckit('fuckit', __doc__)
