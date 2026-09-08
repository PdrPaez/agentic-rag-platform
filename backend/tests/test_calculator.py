import pytest

from app.agents.tools.calculator import CalculatorError, calculate


def test_calculate_supports_basic_arithmetic() -> None:
    assert calculate("(12 + 8) / 4") == "5"
    assert calculate("2 ** 3") == "8"


@pytest.mark.parametrize("expression", ["__import__('os')", "open('file')", "1 / 0", "2 ** 11"])
def test_calculate_rejects_unsafe_or_invalid_expressions(expression: str) -> None:
    with pytest.raises(CalculatorError):
        calculate(expression)
