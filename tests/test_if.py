from tests.util import ast_check


class TestIf:

    def test_basic_if(self, ptp):
        pseudo_str = """
if a then
    show a
end
if b then :
    show b
end
if c then:
    show c
end
if d :
    show d
end
        """

        py_str = """
if a:
    print(a)
if b:
    print(b)
if c:
    print(c)
if d:
    print(d)
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_nested_ifs(self, ptp):
        pseudo_str = """
if a :
    if b :
        if c :
            show c
        end
    end
end
        """

        py_str = """
if a:
    if b:
        if c:
            print(c)
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_if_else(self, ptp):
        pseudo_str = """
if a then
    show a
else
    show "Not a"
end
if b then
    show b
else
    if c then
        show c
    else
        show d
    end
end
        """

        py_str = """
if a:
    print(a)
else:
    print('Not a')
if b:
    print(b)
elif c:
    print(c)
else:
    print(d)
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_elif(self, ptp):
        pseudo_str = """
if a then
    show a
else if b then
    show b
else
    show c
end
        """

        py_str = """
if a:
    print(a)
elif b:
    print(b)
else:
    print(c)
        """

        assert ast_check(ptp, py_str, pseudo_str)
