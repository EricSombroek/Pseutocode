class Num(object):
    def __init__(self, parent, n):
        self.parent = parent
        self.n = n


class BinOp(object):
    def __init__(self, parent, left, op, right):
        self.parent = parent
        self.left = left
        self.op = op
        self.right = right


class Compare(object):
    def __init__(self, parent, left, op, right):
        self.parent = parent
        self.left = left
        self.op = op
        self.right = right


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
