import argparse
import ast
import astor

from pseudocode_to_py import PseudoToPy

parser = argparse.ArgumentParser(description='A pseudocode to Python converter written in Python using textX.')
parser.add_argument('input', help="Pseudocode file to use as an input")
parser.add_argument('-a', '--ast', action='store_true', help="Prints out the generated Python AST")
parser.add_argument('-e', '--exec', action='store_true', help="Execute the generated Python code")
parser.add_argument('-q', '--quiet', action='store_true', help="Don't print the generated Python code")
args = parser.parse_args()

pseudo_to_py = PseudoToPy()
generated_ast = pseudo_to_py.convert(args.input)
generated_code = astor.to_source(generated_ast)

if args.ast:
    print(ast.dump(generated_ast))
if not args.quiet:
    print(generated_code)
if args.exec:
    exec(generated_code)
