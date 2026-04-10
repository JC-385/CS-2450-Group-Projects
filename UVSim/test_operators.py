from pytest import raises
from operators import Operators


class Tests:
    op = Operators()

    def test_read(self):
        memory = [0] * 250
        self.op.READ(5, memory, lambda _: "1234")
        assert memory[5] == 1234

    def test_write(self, capsys):
        memory = [0] * 250
        memory[5] = 1234

        self.op.WRITE(5, memory, print)
        printed = capsys.readouterr()

        assert printed.out == "1234\n"

    def test_load(self):
        memory = [0] * 250
        memory[5] = 1234
        assert self.op.LOAD(5, memory) == 1234

    def test_store(self):
        memory = [0] * 250
        self.op.STORE(5, memory, 1234)
        assert memory[5] == 1234

    def test_add(self):
        memory = [0] * 250
        memory[5] = 1234
        assert self.op.ADD(5, memory, 1234) == 2468

    def test_divide(self):
        memory = [0] * 250
        memory[5] = 2
        assert self.op.DIVIDE(5, memory, 1234) == 617

    def test_branch(self):
        assert self.op.BRANCH(5) == 5

    def test_halt(self):
        assert self.op.HALT() is True
