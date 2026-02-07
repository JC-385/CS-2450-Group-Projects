from pytest import MonkeyPatch,raises
# from Main import *
from Operators import *
# import Unittest



def test_read(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    assert memory[5] == 1234

def test_read_invalid(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: 'abc')

    with raises(ValueError):
        READ(5, memory)

def test_write(monkeypatch,capsys):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    WRITE(5, memory)
    printed = capsys.readouterr()
    
    assert printed.out == "1234\n"

def test_write_fail(monkeypatch,capsys):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    with raises(IndexError):
        WRITE(200, memory)

def test_load(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    assert LOAD(5, memory) == 1234

def test_load_fail(monkeypatch):
    memory = [0] *100
        
    monkeypatch.setattr('builtins.input', lambda _: '1234')

    READ(5, memory)

    with raises(IndexError):
        LOAD(150, memory)

def test_store(monkeypatch):
    memory = [0] *100

    accumulator = 1234
       
    STORE(5, memory, accumulator)
    
    assert memory[5] == 1234


def test_store_invaild(monkeypatch):
    memory = [0] *100

    accumulator = "abc"
       
    store = STORE(5, memory, accumulator)
    
    def invalid_data(data):
        if not isinstance(data, int):
            raise TypeError("Data must be an Int")
     
    with raises(TypeError, match="Data must be an Int"):
        invalid_data(memory[5])

def test_add(monkeypatch):
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1234
    
    
    assert ADD(5, memory, accumulator) == 2468

def test_add_fail(monkeypatch):
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1234
    
    
    with raises(IndexError):
        ADD(200, memory, accumulator)

def test_subtract():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1000

    assert SUBTRACT(5, memory, accumulator) == 234

def test_subtract_fail():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 1000

    with raises(IndexError):
        SUBTRACT(150, memory, accumulator)

def test_muliply():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    assert MULTIPLY(5, memory, accumulator) == 2468

def test_multiply_fail():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    with raises(IndexError):
        MULTIPLY(150, memory, accumulator)

def test_divide():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    assert DIVIDE(5, memory, accumulator) == 617

def test_divide_fail():
    memory = [0] *100

    accumulator = 1234
       
    memory[5] = 2

    with raises(IndexError):
        DIVIDE(150, memory, accumulator)