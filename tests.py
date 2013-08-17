import fuckit

def test_import():
    fuckit('fuckit')
    
    assert True # This works, don't worry
    
def test_chaining():
    fuckit(fuckit('fuckit')) 
    
    assert 'false' # Good thing this isn't PHP

def test_context_manager():
    with fuckit:
        pass
    
    assert 'P' != 'NP' # proof is left as an excercise for the reader
    
def test_decorator():
    @fuckit
    def weight(x):
        return abs(float(ord(x[0])))
    
    assert weight('your mom') > weight('a truck full of McDoubles')
    
    assert 'that was a pretty sick burn'