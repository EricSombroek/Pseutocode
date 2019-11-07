from tests.util import ast_check

import pytest


class TestVarDeclaration:

    def test_basic_declaration(self, ptp):
        pseudo_str = "declare myVar"

        py_str = "myVar = None"

        assert ast_check(ptp, py_str, pseudo_str)

    def test_basic_declarations_in_a_row(self, ptp):

        pseudo_str = """
declare myVar1
declare myVar2
"""
        py_str = """
myVar1 = None
myVar2 = None
"""

        assert ast_check(ptp, py_str, pseudo_str)

    def test_declare_twice_same(self, ptp):
        pseudo_str = """
declare myVar
declare myVar
"""

        with pytest.raises(Exception) as e_info:
            ptp.str_convert(pseudo_str)
