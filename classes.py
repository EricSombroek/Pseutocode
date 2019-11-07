class Num(object):
    def __init__(self, parent, n):
        self.parent = parent
        self.n = n


class Name(object):
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id


class BooleanConstant(object):
    def __init__(self, parent, boolean_value):
        self.parent = parent
        self.boolean_value = boolean_value


class Expression(object):
    def __init__(self, parent, logical_terms, operators):
        self.parent = parent
        self.logical_terms = logical_terms
        self.operators = operators


class LogicalTerm(object):
    def __init__(self, parent, logical_factors, operators):
        self.parent = parent
        self.logical_factors = logical_factors
        self.operators = operators


class LogicalFactor(object):
    def __init__(self, parent, sign, operand):
        self.parent = parent
        self.sign = sign
        self.operand = operand


class BooleanEntity(object):
    def __init__(self, parent, left, operator, right):
        self.parent = parent
        self.left = left
        self.operator = operator
        self.right = right


class ArithmeticExpression(object):
    def __init__(self, parent, terms, operators):
        self.parent = parent
        self.terms = terms
        self.operators = operators


class Term(object):
    def __init__(self, parent, factors, operators):
        self.parent = parent
        self.factors = factors
        self.operators = operators


class Factor(object):
    def __init__(self, parent, sign, base, operators, exponents):
        self.parent = parent
        self.sign = sign
        self.base = base
        self.operators = operators
        self.exponents = exponents


class ExponentiationBase(object):
    def __init__(self, parent, operand):
        self.parent = parent
        self.operand = operand


class ExponentiationExponent(object):
    def __init__(self, parent, sign, operand):
        self.parent = parent
        self.sign = sign
        self.operand = operand


class Statement(object):
    def __init__(self, parent):
        self.parent = parent


class DeclarationStatement(Statement):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name


class PrintStatement(Statement):
    def __init__(self, arg, parent):
        super().__init__(parent)
        self.arg = arg


class AssignmentStatement(Statement):
    def __init__(self, parent, target, value):
        super().__init__(parent)
        self.target = target
        self.value = value


class IfStatement(Statement):
    def __init__(self, parent, test, body, orelse):
        super().__init__(parent)
        self.test = test
        self.body = body
        self.orelse = orelse


class ElseStatement(Statement):
    def __init__(self, parent, body):
        super().__init__(parent)
        self.body = body


class ElseIfStatement(Statement):
    def __init__(self, parent, test, body):
        super().__init__(parent)
        self.test = test
        self.body = body


class WhileStatement(Statement):
    def __init__(self, parent, test, body, orelse):
        super().__init__(parent)
        self.test = test
        self.body = body
        self.orelse = orelse


class BreakStatement(Statement):
    def __init__(self, parent, _):
        super().__init__(parent)
        self._ = _


class ContinueStatement(Statement):
    def __init__(self, parent, _):
        super().__init__(parent)
        self._ = _
