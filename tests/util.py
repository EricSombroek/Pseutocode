import ast

import astor


def ast_check(ptp, py_str, pseudo_str):
    expected_ast = ast.parse(py_str)
    actual_ast = ptp.str_convert(pseudo_str)

    return astor.to_source(expected_ast) == astor.to_source(actual_ast)
