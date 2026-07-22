import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _eval(node.left),
            _eval(node.right),
        )

    if isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _eval(node.operand)
        )

    raise ValueError("Unsupported or unsafe math expression detected.")

def calculate(expression: str):
    """Safely computes complex math expressions without using raw unsafe eval."""
    # Strip unnecessary whitespaces or formatting wrappers safely
    cleaned_expression = expression.strip().replace(" ", "")
    tree = ast.parse(cleaned_expression, mode="eval")
    return _eval(tree.body)
