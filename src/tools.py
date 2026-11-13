import ast
import operator

_ALLOWED = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def calculator(expression):
    """Evaluate basic arithmetic safely; never use eval()."""
    try:
        tree = ast.parse(expression, mode="eval")
        def visit(node):
            if isinstance(node, ast.Expression):
                return visit(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
                return _ALLOWED[type(node.op)](visit(node.left), visit(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
                return _ALLOWED[type(node.op)](visit(node.operand))
            raise ValueError("Only basic arithmetic is supported.")
        return visit(tree)
    except Exception as exc:
        return f"Could not calculate: {exc}"
