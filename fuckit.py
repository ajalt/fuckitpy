import inspect
import imp
import ast
import types
import sys
import traceback
import functools

def fuckit(victim):
    if isinstance(victim, (str, unicode)):
        file, pathname, description = imp.find_module(victim)
        source = file.read()
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
            else:
                break
        inspect.stack()[1][0].f_locals[victim] = module
