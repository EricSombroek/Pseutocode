from textx.metamodel import metamodel_from_file
import ast
import astor

from classes import *


class PseudoToPy:
    def __init__(self):
        self.py_ast = ast.Module(body=[])
        self.variables = []
        self.pseudo_mm = metamodel_from_file('pseudocode.tx',
                                             classes=[Num, BinOp, Compare, Statement, PrintStatement,
                                                      AssignmentStatement,
                                                      IfStatement])
        self.pseudo_mm.register_obj_processors({
            'RootStatement': self.handle_root_statement,
        })

    def convert(self, filename):
        self.pseudo_mm.model_from_file(filename)
        return self.py_ast

    def add_to_ast(self, node):
        self.py_ast.body.append(node)
        return node

    def handle_root_statement(self, root_statement):
        self.add_to_ast(self.statement_to_node(root_statement))

    def statement_to_node(self, statement):
        if type(statement) is PrintStatement:
            node = self.print_to_node(statement)
        elif type(statement) is AssignmentStatement:
            node = self.assignment_to_node(statement)
        elif type(statement) is IfStatement:
            node = self.if_to_node(statement)
        else:
            raise
        return node

    def print_to_node(self, print_statement):
        arg = print_statement.arg
        node = ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx='Load'), args=[self.to_node(arg)], keywords=[]))
        return node

    def assignment_to_node(self, assignment):
        target_id = assignment.target.id
        value = assignment.value

        if target_id not in self.variables:
            self.variables.append(target_id)

        node = ast.Assign(targets=[ast.Name(id=target_id, ctx='Store')], value=self.to_node(value))
        return node

    def if_to_node(self, if_statement):
        test_node = self.to_node(if_statement.test)
        body_node = list(map(lambda stmt: self.to_node(stmt), if_statement.body))
        node = ast.If(test=test_node, body=body_node, orelse=[])
        return node

    def to_node(self, value):
        if isinstance(value, Num):
            node = ast.Num(n=value.n)
        elif isinstance(value, BinOp):
            node = self.create_binop_node(value)
        elif isinstance(value, Compare):
            node = self.create_compare_node(value)
        elif isinstance(value, Statement):
            node = self.statement_to_node(value)
        elif hasattr(value, 'id'):
            node = ast.Name(id=value.id, ctx='Load')
        else:
            node = ast.Str(s=value.s)
        return node

    def create_binop_node(self, binop):
        # Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift
        #                  | RShift | BitOr | BitXor | BitAnd | FloorDiv
        def get_ast_op(x):
            return {
                '+': ast.Add(),
                'plus': ast.Add(),
                '-': ast.Sub(),
                'minus': ast.Sub()
            }.get(x)

        left_node = self.to_node(binop.left)
        right_node = self.to_node(binop.right)
        op = get_ast_op(binop.op)

        return ast.BinOp(left=left_node, op=op, right=right_node)

    def create_compare_node(self, comp):
        # Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
        def get_ast_op(x):
            return {
                '<': ast.Lt(),
                'lower than': ast.Lt(),
                'is lower than': ast.Lt(),
                '<=': ast.LtE(),
                '>': ast.Gt(),
                'greater than': ast.Gt(),
                'is greater than': ast.Gt(),
                '>=': ast.GtE(),
                '==': ast.Eq(),
                'equals': ast.Eq(),
                'is equal to': ast.Eq(),
                'is not equal to': ast.NotEq(),
            }.get(x)

        left_node = self.to_node(comp.left)
        right_node = self.to_node(comp.right)
        op = get_ast_op(comp.op)
        return ast.Compare(left=left_node, ops=[op], comparators=[right_node])


pseudo_to_py = PseudoToPy()
newAst = pseudo_to_py.convert('test.pseudo')
newCode = astor.to_source(newAst)
print(ast.dump(newAst))
print(newCode)
print("##########")
exec(newCode)
