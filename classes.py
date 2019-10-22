class Num(object):
    def __init__(self, parent, n):
        self.parent = parent
        self.n = n

class Expression(object):
    def __init__(self, parent, logicalTerms, operators):
        self.parent = parent
        self.logicalTerms = logicalTerms
        self.operators = operators

class LogicalTerm(object):
    def __init__(self, parent, logicalFactors, operators):
        self.parent = parent
        self.logicalFactors = logicalFactors
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
    def __init__(self, parent, test, body):
        super().__init__(parent)
        self.test = test
        self.body = body
