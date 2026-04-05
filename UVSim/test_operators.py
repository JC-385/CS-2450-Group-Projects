"""Test suite for BasicML operations.

Comprehensive pytest test suite covering all 13 operations in the Operators
class, including success cases, error handling, and boundary conditions.
Uses pytest fixtures and monkeypatching for I/O mocking.
"""

from pytest import MonkeyPatch, raises
from Operators import *


class Tests:
    """Test cases for all BasicML operations."""

    def __init__(self):
        """Initialize test fixtures."""
        self.op = Operators()
        self.memory = [0] * 100

    def test_read(self, monkeypatch):
        """Test READ operation with valid input."""
        self.memory = [0] * 100
        
        monkeypatch.setattr('builtins.input', lambda _: '1234')

        self.op.READ(5, self.memory, input)

        assert self.memory[5] == 1234

    def test_read_invalid(self, monkeypatch):
        """Test READ operation with invalid input (outside range)."""
        self.memory = [0] * 100
        
        monkeypatch.setattr('builtins.input', lambda _: 'abc')

        with raises(ValueError):
            self.op.READ(5, self.memory, input)
    #Test 3
    def test_write(self, monkeypatch,capsys):
        memory = [0] *100
        
        monkeypatch.setattr('builtins.input', lambda _: '1234')

        self.op.READ(5, memory)

        self.op.WRITE(5, memory)
        printed = capsys.readouterr()
    
        assert printed.out == "1234\n"
    #Test 4
    def test_write_fail(self, monkeypatch,capsys):
        memory = [0] *100
        
        monkeypatch.setattr('builtins.input', lambda _: '1234')

        self.op.READ(5, memory)

        with raises(IndexError):
            self.op.WRITE(200, memory)
    #Test 5
    def test_load(self, monkeypatch):
        memory = [0] *100
        
        monkeypatch.setattr('builtins.input', lambda _: '1234')

        self.op.READ(5, memory)

        assert self.op.LOAD(5, memory) == 1234
    #Test 6
    def test_load_fail(self, monkeypatch):
        memory = [0] *100
        
        monkeypatch.setattr('builtins.input', lambda _: '1234')

        self.op.READ(5, memory)

        with raises(IndexError):
            self.op.LOAD(150, memory)
    #Test 7
    def test_store(self,monkeypatch):
        memory = [0] *100

        accumulator = 1234
       
        self.op.STORE(5, memory, accumulator)
    
        assert memory[5] == 1234
    #Test 8
    def test_store_invaild(self,monkeypatch):
        memory = [0] *100

        accumulator = "abc"
       
        store = self.op.STORE(5, memory, accumulator)
    
        def invalid_data(data):
            if not isinstance(data, int):
                raise TypeError("Data must be an Int")
     
        with raises(TypeError, match="Data must be an Int"):
            invalid_data(memory[5])
    #Test 9
    def test_add(self, monkeypatch):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 1234
    
    
        assert self.op.ADD(5, memory, accumulator) == 2468
    #Test 10
    def test_add_fail(self,monkeypatch):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 1234
    
    
        with raises(IndexError):
            self.op.ADD(200, memory, accumulator)
    #Test 11
    def test_subtract(self):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 1000

        assert self.op.SUBTRACT(5, memory, accumulator) == 234
    #Test 12
    def test_subtract_fail(self):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 1000

        with raises(IndexError):
            self.op.SUBTRACT(150, memory, accumulator)
    #Test 13
    def test_muliply(self):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 2

        assert self.op.MULTIPLY(5, memory, accumulator) == 2468
    #Test 14
    def test_multiply_fail(self):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 2

        with raises(IndexError):
            self.op.MULTIPLY(150, memory, accumulator)
    #Test 15
    def test_divide(self):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 2

        assert self.op.DIVIDE(5, memory, accumulator) == 617
    #Test 16
    def test_divide_fail(self):
        memory = [0] *100

        accumulator = 1234
       
        memory[5] = 2

        with raises(IndexError):
            self.op.DIVIDE(150, memory, accumulator)
    #Test 17
    def test_branch(self):
        memory = [0] *100

        assert self.op.BRANCH(5) == 5
    #Test 18
    def test_branch_fail(self):
        memory = [0] *100


     
        with raises(ValueError):
            self.op.BRANCH("abc")
    #Test 19
    def test_branchneg(self):
        memory = [0] *100

        accumulator = -5

        assert self.op.BRANCHNEG(5, accumulator) == 5

        accumulator = 10 

        assert self.op.BRANCHNEG(5, accumulator) == None
    #Test 20
    def test_branchneg_fail(self):
        memory = [0] *100

        accumulator = 'abc'

        with raises(TypeError):
            self.op.BRANCHNEG(5, accumulator)
    #Test 21
    def test_branchzero(self):
        memory = [0] * 100

        accumulator = 0

        assert self.op.BRANCHZERO(10, accumulator) == 10
    #Test 22
    def test_branchzero_fail(self):
        memory = [0] * 100

        accumulator = 0

        with raises(ValueError):
            self.op.BRANCHZERO('fail', accumulator)
    #Test 23
    def test_halt(self):
    
        assert self.op.HALT() is True