from tests.util import ast_check


class TestVarDeclaration:

    def test_declaration(self, ptp):
        pseudo_str = "declare myVar"

        py_str = "myVar = None"

        assert ast_check(ptp, py_str, pseudo_str)
