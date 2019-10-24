import glob
import astor
from pseudocode_to_py import PseudoToPy


def test_run_all():
    for pseudoFileName in glob.iglob('tests/' + '**/*.pseudo', recursive=True):

        ast_builder = PseudoToPy()

        py_file_name = pseudoFileName.replace('pseudo', 'py.txt')

        python_file = open(py_file_name)
        expected_py_code = python_file.read().rstrip()
        python_file.close()

        ast = ast_builder.convert(pseudoFileName)
        actual_py_code = astor.to_source(ast).rstrip()

        try:
            assert expected_py_code == actual_py_code
        except AssertionError as e:
            e.args = (
                'For file :' + pseudoFileName,
                'Expected :' + expected_py_code,
                'Actual :' + actual_py_code
            )
            print('Expected:\n' + expected_py_code)
            print('Actual:\n' + actual_py_code)
            raise
