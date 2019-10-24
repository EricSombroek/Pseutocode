import glob
import astor
from pseudocode_to_py import PseudoToPy


def test_run_all():

    for pseudoFileName in glob.iglob('tests/' + '**/*.pseudo', recursive=True):

        astBuilder = PseudoToPy()

        pyFileName = pseudoFileName.replace('pseudo', 'py.txt')

        pythonFile = open(pyFileName)
        expectedPyCode = ""
        expectedPyCode = pythonFile.read().rstrip()
        pythonFile.close()

        ast = astBuilder.convert(pseudoFileName)
        actualPyCode = ""
        actualPyCode = astor.to_source(ast).rstrip()

        try:
            assert expectedPyCode == actualPyCode
        except AssertionError as e:
            e.args = (
                'For file :' + pseudoFileName,
                'Expected :' + expectedPyCode,
                'Actual :' + actualPyCode
            )
            print('Expected:\n' + expectedPyCode)
            print('Actual:\n' + actualPyCode)
            raise
