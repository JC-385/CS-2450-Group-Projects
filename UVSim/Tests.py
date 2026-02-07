from pytest import MonkeyPatch,raises
from Operators import *

#Test 1
def test_read(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    assert memory[5] == 1234
#Test 2
def test_read_invalid(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: 'abc')

    with raises(ValueError):
        READ(5, memory)
#Test 3
def test_write(monkeypatch,capsys):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    WRITE(5, memory)
    printed = capsys.readouterr()
    
    assert printed.out == "1234\n"
#Test 4
def test_write_fail(monkeypatch,capsys):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    with raises(IndexError):
        WRITE(200, memory)
#Test 5
def test_load(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    assert LOAD(5, memory) == 1234
#Test 6
def test_load_fail(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    with raises(IndexError):
        LOAD(150, memory)
#Test 7
def test_store(monkeypatch):
    memory = [0] *100

    accumulator = 1234
       
    STORE(5, memory, accumulator)
    
    assert memory[5] == 1234
#Test 8
def test_store_invaild(monkeypatch):
    memory = [0] *100

    accumulator = "abc"
       
    store = STORE(5, memory, accumulator)
    
    def invalid_data(data):
        if not isinstance(data, int):
            raise TypeError("Data must be an Int")
     
    with raises(TypeError, match="Data must be an Int"):
        invalid_data(memory[5])
#Test 9
def test_add(monkeypatch):
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1234
    
    
    assert ADD(5, memory, accumulator) == 2468
#Test 10
def test_add_fail(monkeypatch):
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1234
    
    
    with raises(IndexError):
        ADD(200, memory, accumulator)
#Test 11
def test_subtract():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1000

    assert SUBTRACT(5, memory, accumulator) == 234
#Test 12
def test_subtract_fail():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1000

    with raises(IndexError):
        SUBTRACT(150, memory, accumulator)
#Test 13
def test_muliply():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    assert MULTIPLY(5, memory, accumulator) == 2468
#Test 14
def test_multiply_fail():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    with raises(IndexError):
        MULTIPLY(150, memory, accumulator)
#Test 15
def test_divide():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    assert DIVIDE(5, memory, accumulator) == 617
#Test 16
def test_divide_fail():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    with raises(IndexError):
        DIVIDE(150, memory, accumulator)
#Test 17
def test_branch():
    memory = [0] *100

    assert BRANCH(5) == 5
#Test 18
def test_branch_fail():
    memory = [0] *100


     
    with raises(ValueError):
        BRANCH("abc")
#Test 19
def test_branchneg():
    memory = [0] *100

    accumulator = -5

    assert BRANCHNEG(5, accumulator) == 5

    accumulator = 10 

    assert BRANCHNEG(5, accumulator) == None
#Test 20
def test_branchneg_fail():
    memory = [0] *100

    accumulator = 'abc'

    with raises(TypeError):
        BRANCHNEG(5, accumulator)
#Test 21
def test_branchzero():
    memory = [0] * 100

    accumulator = 0

    assert BRANCHZERO(10, accumulator) == 10
#Test 22
def test_branchzero_fail():
    memory = [0] * 100

    accumulator = 0

    with raises(ValueError):
        BRANCHZERO('fail', accumulator)
#Test 23
def test_halt():
    
    assert HALT() is True