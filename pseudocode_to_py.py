from textx.metamodel import metamodel_from_file
import ast
from classes import *


class PseudoToPy:
    def __init__(self):
        self.py_ast = ast.Module(body=[])
        self.variables = []
        self.pseudo_mm = metamodel_from_file('pseudocode.tx',
                                             classes=[
                                                 Num,
                                                 Name,
                                                 BooleanConstant,
                                                 Expression,
                                                 LogicalTerm,
                                                 LogicalFactor,
                                                 BooleanEntity,
                                                 ArithmeticExpression,
                                                 Term,
                                                 Factor,
                                                 ExponentiationBase,
                                                 ExponentiationExponent,
                                                 Statement,
                                                 DeclarationStatement,
                                                 PrintStatement,
                                                 AssignmentStatement,
                                                 IfStatement,
                                                 ElseStatement,
                                                 ElseIfStatement])
        self.pseudo_mm.register_obj_processors({
            'RootStatement': self.handle_root_statement,
        })

    def reset_ast(self):
        self.py_ast = ast.Module(body=[])
        self.variables = []

    def convert(self, filename):
        self.reset_ast()
        self.pseudo_mm.model_from_file(filename)
        return self.py_ast

    def str_convert(self, pseudo_str):
        self.reset_ast()
        self.pseudo_mm.model_from_str(pseudo_str)
        return self.py_ast

    def add_to_ast(self, node):
        self.py_ast.body.append(node)
        return node

    def handle_root_statement(self, root_statement):
        self.add_to_ast(self.statement_to_node(root_statement))

    def statement_to_node(self, statement):
        if type(statement) is PrintStatement:
            node = self.print_to_node(statement)
        elif type(statement) is DeclarationStatement:
            node = self.declaration_to_node(statement)
        elif type(statement) is AssignmentStatement:
            node = self.assignment_to_node(statement)
        elif type(statement) is IfStatement:
            node = self.if_to_node(statement)

        else:
            raise
        return node

    def declaration_to_node(self, declaration_statement):
        var_id = declaration_statement.name.id

        if var_id not in self.variables:
            self.variables.append(var_id)
        else:
            raise Exception('You cannot declare the same variable twice')

        node = ast.Assign(
            targets=[ast.Name(id=var_id, ctx='Store')], value=ast.Constant(None))
        return node

    def print_to_node(self, print_statement):
        arg = print_statement.arg
        node = ast.Expr(value=ast.Call(func=ast.Name(
            id='print', ctx='Load'), args=[self.to_node(arg)], keywords=[]))
        return node

    def assignment_to_node(self, assignment):
        target_id = assignment.target.id
        value = assignment.value

        # UNCOMMENT TO FORCE DECLARATION OF VARIABLES
        # if target_id not in self.variables:
        #   raise Exception ('You must declare variable ' + target_id + ' before assigning it a value')

        node = ast.Assign(
            targets=[ast.Name(id=target_id, ctx='Store')], value=self.to_node(value))
        return node

    def if_to_node(self, if_statement):
        test_node = self.to_node(if_statement.test)
        body_node = list(
            map(lambda stmt: self.to_node(stmt), if_statement.body))
        orelse_node = self.orelse_to_node(if_statement.orelse)
        node = ast.If(test=test_node, body=body_node, orelse=orelse_node)
        return node

    def orelse_to_node(self, orelse_list):
        if len(orelse_list) == 0:
            return orelse_list
        current_orelse = orelse_list.pop(0)
        if isinstance(current_orelse, ElseIfStatement):
            new_if = IfStatement(
                current_orelse.parent, current_orelse.test, current_orelse.body, orelse_list)
            node = [self.if_to_node(new_if)]
        elif isinstance(current_orelse, ElseStatement):
            node = list(
                map(lambda stmt: self.to_node(stmt), current_orelse.body))
        else:
            raise
        return node

    def to_node(self, value):
        if isinstance(value, Num):
            node = ast.Num(n=value.n)

        elif isinstance(value, Expression):
            node = self.create_expression_node(value)
        elif isinstance(value, LogicalTerm):
            node = self.create_logical_term_node(value)
        elif isinstance(value, LogicalFactor):
            node = self.create_logical_factor_node(value)
        elif isinstance(value, BooleanEntity):
            node = self.create_boolean_entity_node(value)
        elif isinstance(value, ArithmeticExpression):
            node = self.create_arithmetic_expression_node(value)
        elif isinstance(value, Term):
            node = self.create_term_node(value)
        elif isinstance(value, Factor):
            node = self.create_factor_node(value)
        elif isinstance(value, ExponentiationBase):
            node = self.create_exponentiation_base_node(value)
        elif isinstance(value, ExponentiationExponent):
            node = self.create_exponentiation_exponent_node(value)
        elif isinstance(value, Statement):
            node = self.statement_to_node(value)
        elif isinstance(value, Name):
            node = ast.Name(id=value.id, ctx='Load')
        elif isinstance(value, BooleanConstant):
            node = ast.NameConstant(value=value.boolean_value == 'true')
        else:
            node = ast.Str(s=value.s)
        return node

    def create_expression_node(self, expression):
        if len(expression.logical_terms) == 1:
            return self.to_node(expression.logical_terms[0])
        logical_terms_nodes = []
        for t in expression.logical_terms:
            logical_terms_nodes.append(self.to_node(t))
        return ast.BoolOp(ast.Or(), logical_terms_nodes)

    def create_logical_term_node(self, logical_term):
        if len(logical_term.logical_factors) == 1:
            return self.to_node(logical_term.logical_factors[0])
        logical_factors_nodes = []
        for f in logical_term.logical_factors:
            logical_factors_nodes.append(self.to_node(f))
        return ast.BoolOp(ast.And(), logical_factors_nodes)

    def create_logical_factor_node(self, logical_factor):
        if logical_factor.sign in ['!', 'not']:
            return ast.UnaryOp(ast.Not(), self.to_node(logical_factor.operand))
        elif logical_factor.sign is None:
            return self.to_node(logical_factor.operand)
        else:
            raise

    def create_boolean_entity_node(self, boolean_entity):
        left_node = self.to_node(boolean_entity.left)
        if boolean_entity.operator is None:
            return left_node
        elif boolean_entity.operator in ['==', 'is equal to']:
            python_cmp_op = ast.Eq()
        elif boolean_entity.operator in ['!=', 'is not equal to', 'is different from']:
            python_cmp_op = ast.NotEq()
        elif boolean_entity.operator in ['>', 'is greater than']:
            python_cmp_op = ast.Gt()
        elif boolean_entity.operator in ['>=', 'is greater or equal to']:
            python_cmp_op = ast.GtE()
        elif boolean_entity.operator in ['<', 'is lower than']:
            python_cmp_op = ast.Lt()
        elif boolean_entity.operator in ['<=', 'is lower or equal to']:
            python_cmp_op = ast.LtE()
        else:
            raise

        right_node = self.to_node(boolean_entity.right)
        return ast.Compare(left_node, (python_cmp_op,), (right_node,))

    def create_arithmetic_expression_node(self, arith_expr):
        last_term_index = len(arith_expr.terms)
        node = self.to_node(arith_expr.terms[0])
        if last_term_index == 0:
            return node
        for i in range(1, last_term_index):
            if arith_expr.operators[i - 1] in ['+', 'plus']:
                node = ast.BinOp(
                    node, ast.Add(), self.to_node(arith_expr.terms[i]))
            elif arith_expr.operators[i - 1] in ['-', 'minus']:
                node = ast.BinOp(
                    node, ast.Sub(), self.to_node(arith_expr.terms[i]))
        return node

    def create_term_node(self, term):
        last_factor_index = len(term.factors)
        node = self.to_node(term.factors[0])
        if last_factor_index == 0:
            return node
        for i in range(1, last_factor_index):
            if term.operators[i - 1] in ["*", "times"]:
                node = ast.BinOp(node, ast.Mult(),
                                 self.to_node(term.factors[i]))
            elif term.operators[i - 1] in ["/", "divided by"]:
                node = ast.BinOp(
                    node, ast.Div(), self.to_node(term.factors[i]))
            elif term.operators[i - 1] in ["%", "modulo"]:
                node = ast.BinOp(
                    node, ast.Mod(), self.to_node(term.factors[i]))
            else:
                raise
        return node

    def create_factor_node(self, factor):
        base_node = self.to_node(factor.base)
        # When no parenthesis, exponentiations are read from right to left
        if len(factor.exponents) != 0:
            last_exponent_index = len(factor.exponents) - 1
            right_node = self.to_node(factor.exponents[last_exponent_index])
            for i in range(last_exponent_index - 1, -1, -1):
                right_node = ast.BinOp(self.to_node(
                    factor.exponents[i]), ast.Pow(), right_node)
            base_node = ast.BinOp(base_node, ast.Pow(), right_node)

        if factor.sign in ['-', 'minus']:
            return ast.UnaryOp(ast.USub(), base_node)
        elif factor.sign in ['+', 'plus']:
            return ast.UnaryOp(ast.UAdd(), base_node)
        elif factor.sign is None:
            return base_node
        else:
            raise

    def create_exponentiation_base_node(self, base):
        return self.to_node(base.operand)

    def create_exponentiation_exponent_node(self, exponent):
        node = self.to_node(exponent.operand)
        if exponent.sign in ['-', 'minus']:
            return ast.UnaryOp(ast.USub(), node)
        elif exponent.sign in ['+', 'plus']:
            return ast.UnaryOp(ast.UAdd(), node)
        elif exponent.sign is None:
            return node
        else:
            raise
