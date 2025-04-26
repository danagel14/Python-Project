from abc import ABC, abstractmethod
from numpy import double

class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass

class Num(Expression):
    def __init__(self, value):
        self.value = double(value)
    
    def calc(self) -> double:
        return self.value

class Plus(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def calc(self) -> double:
        return self.left.calc() + self.right.calc()

class Minus(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def calc(self) -> double:
        return self.left.calc() - self.right.calc()

class Mul(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def calc(self) -> double:
        return self.left.calc() * self.right.calc()

class Div(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def calc(self) -> double:
        right_val = self.right.calc()
        if right_val == 0:
            raise ValueError("Division by zero")
        return self.left.calc() / right_val

def parser(expression: str) -> double:
    def tokenize(s: str) -> list:
        s = s.replace(' ', '')
        tokens = []
        i = 0
        while i < len(s):
            if s[i].isdigit() or s[i] == '.' or (s[i] == '-' and (i == 0 or s[i-1] in '(+-*/')):
                start = i
                if s[i] == '-':
                    i += 1
                while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                    i += 1
                tokens.append(s[start:i])
                continue
            elif s[i] in '+-*/()':
                tokens.append(s[i])
                i += 1
            else:
                i += 1
        return tokens

    def precedence(op: str) -> int:
        if op in '+-':
            return 1
        if op in '*/':
            return 2
        return 0

    def apply_op(a: Expression, b: Expression, op: str) -> Expression:
        if op == '+':
            return Plus(a, b)
        if op == '-':
            return Minus(a, b)
        if op == '*':
            return Mul(a, b)
        if op == '/':
            return Div(a, b)
        raise ValueError(f"Unknown operator: {op}")

    def parse_tokens(tokens: list) -> Expression:
        values = []
        ops = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '(':
                ops.append(token)
            elif token.replace('.', '', 1).replace('-', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                values.append(Num(float(token)))
            elif token == ')':
                while ops and ops[-1] != '(' and len(values) >= 2:
                    op = ops.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(apply_op(val1, val2, op))
                if ops and ops[-1] == '(':
                    ops.pop() 
            elif token in '+-*/':
                while (ops and ops[-1] != '(' and len(values) >= 2 and
                       precedence(ops[-1]) >= precedence(token)):
                    op = ops.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(apply_op(val1, val2, op))
                ops.append(token)
            i += 1

        while ops and len(values) >= 2:
            op = ops.pop()
            val2 = values.pop()
            val1 = values.pop()
            values.append(apply_op(val1, val2, op))

        if not values:
            raise ValueError("Invalid expression")
        return values[0]

    tokens = tokenize(expression)
    expr = parse_tokens(tokens)
    return expr.calc()