# FuckIt.py

[![Build Status](https://img.shields.io/travis/ajalt/fuckitpy/master.svg)](https://travis-ci.org/ajalt/fuckitpy)
[![PyPI version](https://img.shields.io/badge/pypi-4.8.1-brightgreen.svg)](https://pypi.python.org/pypi/fuckit/4.8.1)
[![Coverage Status](https://img.shields.io/badge/coverage-110%25-brightgreen.svg)](https://coveralls.io/r/ajalt/fuckitpy?branch=master)
[![Downloads](https://img.shields.io/badge/downloads-1.1M%2Fmonth-brightgreen.svg)](https://pypi.python.org/pypi/fuckit)

### The Python Error Steamroller
FuckIt.py uses state-of-the-art technology to make sure your Python code runs
whether it has any right to or not. Some code has an error? Fuck it.

## Technology
FuckIt.py uses a combination of dynamic compilation, Abstract Syntax Tree rewriting, live call stack modification, and love to get rid of all those pesky errors that make programming _so hard_.

## API
All functionality is provided through the fuckit module. Add `import fuckit` to the top of your script, then use fuckit in any of the following ways:

### As a replacement for import
Use fuckit to replace an import when a module has errors.
Just change `import some_shitty_module` to `fuckit('some_shitty_module')`. Note that you have to surround the module name with quotes and parentheses.

```python
import fuckit
#import some_shitty_module
fuckit('some_shitty_module')
some_shitty_module.some_function()
```

Still getting errors? Chain fuckit calls. This module is like violence: if it doesn't work, you just need more of it.

```python
import fuckit
fuckit(fuckit('some_shitty_module'))
# This is definitely going to run now.
some_shitty_module.some_function()
```

### As a decorator
Use fuckit as a function decorator when a single function is giving you trouble. Exceptions will be silenced, and in most cases the function will continue to run, skipping the statements that cause errors.

```python
@fuckit
def func():
    problem_solved
```

You can use fuckit as a class decorator, too.

```python
@fuckit
class C(object):
    def __init__(self):
        everything_works_now
```

Keep in mind that the decorator form of fuckit can't stop syntax errors. For those, you have to use the import form.

### As a context manager
Use fuckit as a context manager to save yourself from having to type out try/except block to silence exceptions yourself.

```python
with fuckit:
    some_code
```

This is functionally equivalent to the following:

```python
try:
    some_code
except Exception:
    pass
```

The context manager form of fuckit can't allow the code to continue past an error like the decorator and import forms can. If you want the code to continue after an exception, wrap the code block in a function and use the decorator instead.



## License
                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                       Version 2, December 2004

	Copyright (C) 2014-2018 AJ Alt

	Everyone is permitted to copy and distribute verbatim or modified
	copies of this license document, and changing it is allowed as long
	as the name is changed.

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 	0. You just DO WHAT THE FUCK YOU WANT TO.

## Attribution

This module is inspired by Matt Diamond's [FuckIt.js](https://github.com/mattdiamond/fuckitjs).
