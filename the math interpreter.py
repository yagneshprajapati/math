# Define the supported operators and their precedence
OPERATORS = {
    "+": 10,
    "-": 10,
    "*": 20,
    "/": 20,
}

# Define the Node class to represent nodes in the AST
class Node:
    def evaluate(self):
        raise NotImplementedError()

class Number(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class BinaryOperator(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self):
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()
        if self.op == "+":
            return left_value + right_value
        elif self.op == "-":
            return left_value - right_value
        elif self.op == "*":
            return left_value * right_value
        elif self.op == "/":
            return left_value / right_value

# Define the function to parse the input string and generate the AST
def parse_expression(expr):
    tokens = expr.split()
    if not tokens:
        raise ValueError("Empty expression")
    elif len(tokens) == 1:
        try:
            return Number(float(tokens[0]))
        except ValueError:
            raise ValueError(f"Invalid token: {tokens[0]}")
    else:
        # Handle parentheses
        paren_count = 0
        for i in range(len(tokens)):
            if tokens[i] == "(":
                paren_count += 1
            elif tokens[i] == ")":
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unmatched parentheses")
            elif paren_count == 0 and tokens[i] in OPERATORS:
                # Find the operator with the lowest precedence
                if OPERATORS[tokens[i]] <= min(OPERATORS[op] for op in OPERATORS if op in tokens):
                    min_precedence = OPERATORS[tokens[i]]
                    min_index = i

        if paren_count != 0:
            raise ValueError("Unmatched parentheses")
        elif min_index is None:
            raise ValueError("No operators found")

        # Recursively parse the left and right sub-expressions
        left = parse_expression(" ".join(tokens[:min_index]))
        right = parse_expression(" ".join(tokens[min_index+1:]))

        # Construct a BinaryOperator node
        return BinaryOperator(tokens[min_index], left, right)

# Define the function to interpret the input expression
def interpret_expression(expr):
    ast = parse_expression(expr)
    return ast.evaluate()

# Test the interpreter with some sample expressions
if __name__ == "__main__":
    print(interpret_expression("9.0 + 388.0"))
   
