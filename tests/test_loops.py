from tests.util import ast_check


class TestLoops:

    def test_basic_while(self, ptp):
        pseudo_str = """
while a is greater than b do
    a equals a minus 1
end
while b is greater than c :
    b equals b minus 1
end
        """

        py_str = """
while a > b:
    a = a - 1
while b > c:
    b = b - 1
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_while_else(self, ptp):
        pseudo_str = """
while a is greater than b do
    a equals a minus 1
else
    show a
end
        """

        py_str = """
while a > b:
    a = a - 1
else:
    print(a)
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_nested_while(self, ptp):
        pseudo_str = """
while a is greater than b do
    while b is greater than c do
        a equals a minus 1
    end
end
        """

        py_str = """
while a > b:
    while b > c:
        a = a - 1
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_break_continue(self, ptp):
        pseudo_str = """
while a is greater than b do
    if a is equal to 2 then
        break
    end
    if a is equal to 3 then
        continue
    end
end
        """

        py_str = """
while a > b:
    if a == 2:
        break
    if a == 3:
        continue
        """

        assert ast_check(ptp, py_str, pseudo_str)
