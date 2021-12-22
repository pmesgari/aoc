class ExpressionNode:
    def __init__(self):
        self.val = None

    def value():
        pass

    def __repr__(self):
        return '<Expression Tree>'


class ConstNode(ExpressionNode):
    def __init__(self, val):
        super().__init__()
        self.number = val

    def value(self):
        return self.number

    def print_stack_commands(self):
        print(f"\t Push {self.number}")


class BinaryOpNode(ExpressionNode):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

    def value(self):
        left_value = self.left.value()
        right_value = self.right.value()
        if self.op == '+':
            return left_value + right_value
        elif self.op == '-':
            return left_value - right_value
        elif self.op == '*':
            return left_value * right_value
        elif self.op == '/':
            return left_value / right_value
        else:
            return None

    def print_stack_commands(self):
        self.left.print_stack_commands()
        self.right.print_stack_commands()
        print(f'\t Operator {self.op}')


class Tokenizer:
    def __init__(self, raw):
        self.raw = ''.join(raw.split())
        self.pos = 0

    def read(self, n):
        result = ''.join(self.raw[self.pos:self.pos + n])
        self.pos += n
        return result

    def peek(self):
        if self.pos >= len(self.raw):
            return '\n'
        return self.raw[self.pos]

    def get_operator(self):
        op = self.peek()
        if op in ['+', '-', '*', '/']:
            self.read(1)
            return op
        elif op == '\n':
            raise Exception('Missing operator at end of line.')
        else:
            raise Exception(
                f"Missing operator. Found {op} instead of +, -, * or /.")

    def expression_tree(self):
        exp = self.term_tree()

        while self.peek() == '+' or self.peek() == '-':
            op = self.read(1)
            next_val = self.term_tree()
            exp = BinaryOpNode(op, exp, next_val)

        return exp

    def term_tree(self):
        term = self.factor_tree()
        while self.peek() == '*' or self.peek() == '/':
            op = self.read(1)
            next_factor = self.factor_tree()
            term = BinaryOpNode(op, term, next_factor)

        return term

    def factor_tree(self):
        ch = self.peek()
        if ch.isdigit():
            value = ''
            while self.peek().isdigit():
                value += self.read(1)
            return ConstNode(int(value))
        elif self.peek() == '(':
            self.read(1)
            exp = self.expression_tree()
            if self.peek() != ')':
                raise Exception('Missing right paranthesis.')
            self.read(1)
            return exp
        elif ch == '\n':
            raise Exception(
                'End of line encountered in the middle of an expression')
        elif ch == ')':
            raise Exception('Extra right paranthesis.')
        elif ch in ['+', '-', '*', '/']:
            raise Exception('Misplaced operator.')
        else:
            raise Exception(f'Unexpected character {ch} encountered.')


tokens = Tokenizer('(((34-17)*8)+(2*7))')
result = tokens.expression_tree()
result.print_stack_commands()
print(result.value())
