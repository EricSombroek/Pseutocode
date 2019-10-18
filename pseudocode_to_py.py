from textx.metamodel import metamodel_from_file
import ast
import astor

from classes import *


class PseudoToPy:
    def __init__(self):
        self.py_ast = ast.Module(body=[])
        self.variables = []
        self.pseudo_mm = metamodel_from_file('pseudocode.tx',
                                             classes=[Num, Expression, LogicalTerm, LogicalFactor, BooleanEntity, ArithmeticExpression, Term, Factor, Statement, PrintStatement,
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
        
        elif isinstance(value, Statement):
            node = self.statement_to_node(value)
        elif hasattr(value, 'id'):
            node = ast.Name(id=value.id, ctx='Load')
        else:
            node = ast.Str(s=value.s)
        return node

    def create_expression_node(self, expression):
        if (len(expression.logicalTerms) == 1):
            return self.to_node(expression.logicalTerms[0])
        logicalTermsNodes = []
        for t in expression.logicalTerms:
            logicalTermsNodes.append(self.to_node(t))
        return ast.BoolOp(ast.Or(), logicalTermsNodes)

    def create_logical_term_node(self, logicalTerm):
        if (len(logicalTerm.logicalFactors) == 1):
            return self.to_node(logicalTerm.logicalFactors[0])
        logicalFactorsNodes = []
        for f in logicalTerm.logicalFactors:
            logicalFactorsNodes.append(self.to_node(f))
        return ast.BoolOp(ast.And(), logicalFactorsNodes)

    def create_logical_factor_node(self, logicalFactor):
        if (logicalFactor.sign in ['!', 'not']):
            return ast.UnaryOp(ast.Not(), self.to_node(logicalFactor.operand))
        elif (logicalFactor.sign == None):
            return self.to_node(logicalFactor.operand)
        else:
            raise

    def create_boolean_entity_node(self, booleanEntity):
        pythonCmpOp = None;
        leftNode = self.to_node(booleanEntity.left)
        if (booleanEntity.operator == None):
            return leftNode
        elif (booleanEntity.operator in ['==', 'is equal to']):
            pythonCmpOp = ast.Eq()
        elif (booleanEntity.operator in ['!=', 'is not equal to', 'is different from']):
            pythonCmpOp = ast.NotEq()
        elif (booleanEntity.operator in ['>', 'is greater than']):
            pythonCmpOp = ast.Gt();
        elif (booleanEntity.operator in ['>=', 'is greater or equal to']):
            pythonCmpOp = ast.GtE();
        elif (booleanEntity.operator in ['<', 'is lower than']):
            pythonCmpOp = ast.Lt();
        elif (booleanEntity.operator in ['<=', 'is lower or equal to']):
            pythonCmpOp = ast.LtE();
        else:
            raise
        
        rightNode = self.to_node(booleanEntity.right)
        return ast.Compare(leftNode, (pythonCmpOp,), (rightNode,))

    def create_arithmetic_expression_node(self, arith_expr):
        lastTermIndex = len(arith_expr.terms)
        node = self.to_node(arith_expr.terms[0])
        if lastTermIndex == 0:
            return node
        for i in range (1, lastTermIndex ):
            if (arith_expr.operators[i-1] in ['+', 'plus']):
                node = ast.BinOp(node, ast.Add(), self.to_node(arith_expr.terms[i]))
            elif (arith_expr.operators[i-1] in ['-', 'minus']):
                node = ast.BinOp(node, ast.Sub(), self.to_node(arith_expr.terms[i]))
        return node
    
    def create_term_node(self, term):
        lastFactorIndex = len(term.factors)
        node = self.to_node(term.factors[0])
        if lastFactorIndex == 0:
            return node
        for i in range (1, lastFactorIndex ):
            if (term.operators[i-1] in ["*", "times"]):
                node = ast.BinOp(node, ast.Mult(), self.to_node(term.factors[i]))
            elif (term.operators[i-1] in ["/", "divided by"]):
                node = ast.BinOp(node, ast.Div(), self.to_node(term.factors[i]))
            elif (term.operators[i-1] in ["%", "modulo"]):
                node = ast.BinOp(node, ast.Mod(), self.to_node(term.factors[i]))
            else :
                raise
        return node

    def create_factor_node(self, factor):
        if (factor.sign in ['-', 'minus']):
            return ast.UnaryOp(ast.USub(), self.to_node(factor.operand))
        else:
            return self.to_node(factor.operand)


pseudo_to_py = PseudoToPy()
newAst = pseudo_to_py.convert('test.pseudo')
newCode = astor.to_source(newAst)
print(ast.dump(newAst))
print(newCode)
print("##########")
exec(newCode)
