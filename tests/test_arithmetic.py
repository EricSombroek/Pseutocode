from tests.util import ast_check


class TestArithmetic:

    def test_boolean_expression(self, ptp):
        pseudo_str = """
myBool equals a plus 2 minus 3 is equal to b and d power 5 modulo 7 is equal to 7 or a is equal to 3 and b is different from -3 or e 
"""

        py_str = "myBool = a + 2 - 3 == b and d ** 5 % 7 == 7 or a == 3 and b != -3 or e"

        assert ast_check(ptp, py_str, pseudo_str)

    def test_multi_div_mod(self, ptp):
        pseudo_str = """
myvar equals a times 2 modulo 3 divided by 90 plus a minus 3 * 2 / someVar % 7
        """

        py_str = """
myvar = a * 2 % 3 / 90 + a - 3 * 2 / someVar % 7
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_parenthesis(self, ptp):
        pseudo_str = """
myVar equals (((((((a plus 4) times (5 plus 5) divided by 5) ** (3 * 4 - 5))))))
        """

        py_str = """
myVar = ((a + 4) * (5 + 5) / 5) ** (3 * 4 - 5)
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_plus_minus(self, ptp):
        pseudo_str = """
myvar equals a plus 2 - 3 + 90 - a minus 2
        """

        py_str = """
myvar = a + 2 - 3 + 90 - a - 2
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_power(self, ptp):
        pseudo_str = """
myvar equals a power 3 power 5
        """

        py_str = """
myvar = a ** 3 ** 5
        """

        assert ast_check(ptp, py_str, pseudo_str)

    def test_float(self, ptp):
        pseudo_str = """
myvar equals 2.25 plus 3.56
        """

        py_str = """
myvar = 2.25 + 3.56
        """

        assert ast_check(ptp, py_str, pseudo_str)
