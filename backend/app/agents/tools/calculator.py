import ast
import math
import operator


class CalculatorError(ValueError):
    """Raised when an expression is not permitted by the calculator tool."""


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression: str) -> str:
    if not expression or len(expression) > 200:
        raise CalculatorError("Expression must contain between 1 and 200 characters")
    try:
        tree = ast.parse(expression, mode="eval")
        if sum(1 for _ in ast.walk(tree)) > 50:
            raise CalculatorError("Calculator expression is too complex")
        result = _evaluate(tree.body)
    except (ArithmeticError, SyntaxError, ValueError, TypeError) as exc:
        raise CalculatorError("Invalid calculator expression") from exc
    if not math.isfinite(result):
        raise CalculatorError("Calculator result must be finite")
    return str(int(result)) if result.is_integer() else f"{result:.10g}"


def _evaluate(node: ast.expr) -> float:
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    ):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        return UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise CalculatorError("Exponent is too large")
        return BINARY_OPERATORS[type(node.op)](left, right)
    raise CalculatorError("Only numeric arithmetic is supported")
