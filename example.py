import fuckit
#import broke
fuckit(fuckit('broke'))

@fuckit
def broken_function():
    non_existant_variable # Let's create a NameError
    return 'Function decorator works'

@fuckit
class BrokenClass(object):
    def f(self):
        self.black_hole = 1 / 0
        return 'Class decorator works'
    
with fuckit:
    print('Context manager works')
    raise RuntimeError()
    
print(broken_function())
print(BrokenClass().f())
broke.f()
print(broke.var)
