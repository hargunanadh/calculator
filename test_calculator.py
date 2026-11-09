"""
Unit tests for Calculator Core logic.
"""

import pytest
import math
from calculator_core import CalculatorEngine, CalculatorState


class TestCalculatorEngine:
    """Tests for CalculatorEngine static and class methods."""

    def test_basic_arithmetic(self):
        assert CalculatorEngine.add(10, 5) == 15
        assert CalculatorEngine.add(-4, 9) == 5
        assert CalculatorEngine.subtract(10, 4) == 6
        assert CalculatorEngine.subtract(5, 12) == -7
        assert CalculatorEngine.multiply(6, 7) == 42
        assert CalculatorEngine.multiply(-3, 8) == -24
        assert CalculatorEngine.divide(20, 4) == 5.0
        assert CalculatorEngine.divide(7, 2) == 3.5

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            CalculatorEngine.divide(10, 0)

        with pytest.raises(ZeroDivisionError):
            CalculatorEngine.modulo(10, 0)

        with pytest.raises(ZeroDivisionError):
            CalculatorEngine.reciprocal(0)

    def test_power_and_root(self):
        assert CalculatorEngine.power(2, 3) == 8
        assert CalculatorEngine.power(5, 0) == 1
        assert CalculatorEngine.square_root(25) == 5.0
        assert CalculatorEngine.square_root(0) == 0.0

        with pytest.raises(ValueError):
            CalculatorEngine.square_root(-4)

    def test_modulo_and_percentage(self):
        assert CalculatorEngine.modulo(10, 3) == 1
        assert CalculatorEngine.percentage(50) == 0.5
        assert CalculatorEngine.percentage(200) == 2.0

    def test_reciprocal_and_factorial(self):
        assert CalculatorEngine.reciprocal(2) == 0.5
        assert CalculatorEngine.reciprocal(4) == 0.25
        assert CalculatorEngine.factorial(5) == 120
        assert CalculatorEngine.factorial(0) == 1

        with pytest.raises(ValueError):
            CalculatorEngine.factorial(-1)

        with pytest.raises(ValueError):
            CalculatorEngine.factorial(3.5)

    def test_format_result(self):
        assert CalculatorEngine.format_result(5.0) == 5
        assert CalculatorEngine.format_result(3.14159) == 3.14159
        # Precision floating point fix test
        assert CalculatorEngine.format_result(0.1 + 0.2) == 0.3

    def test_evaluate_expression_basic(self):
        res, err = CalculatorEngine.evaluate_expression("12 + 8")
        assert err is None
        assert res == 20

        res, err = CalculatorEngine.evaluate_expression("100 - 35")
        assert err is None
        assert res == 65

        res, err = CalculatorEngine.evaluate_expression("7 * 8")
        assert err is None
        assert res == 56

        res, err = CalculatorEngine.evaluate_expression("15 / 4")
        assert err is None
        assert res == 3.75

    def test_evaluate_operator_precedence(self):
        res, err = CalculatorEngine.evaluate_expression("2 + 3 * 4")
        assert err is None
        assert res == 14

        res, err = CalculatorEngine.evaluate_expression("(2 + 3) * 4")
        assert err is None
        assert res == 20

        res, err = CalculatorEngine.evaluate_expression("2 ^ 3 + 1")
        assert err is None
        assert res == 9

    def test_evaluate_custom_symbols(self):
        res, err = CalculatorEngine.evaluate_expression("12 × 4 ÷ 2")
        assert err is None
        assert res == 24

        res, err = CalculatorEngine.evaluate_expression("10 − 3")
        assert err is None
        assert res == 7

    def test_evaluate_scientific_functions(self):
        res, err = CalculatorEngine.evaluate_expression("sqrt(144)")
        assert err is None
        assert res == 12

        res, err = CalculatorEngine.evaluate_expression("abs(-42)")
        assert err is None
        assert res == 42

        res, err = CalculatorEngine.evaluate_expression("sin(0)")
        assert err is None
        assert res == 0

        res, err = CalculatorEngine.evaluate_expression("cos(0)")
        assert err is None
        assert res == 1

        res, err = CalculatorEngine.evaluate_expression("log(100)")
        assert err is None
        assert res == 2

        res, err = CalculatorEngine.evaluate_expression("fact(5)")
        assert err is None
        assert res == 120

        # Constants pi and e
        res, err = CalculatorEngine.evaluate_expression("pi")
        assert err is None
        assert round(res, 4) == 3.1416

    def test_evaluate_complex_nested_expression(self):
        res, err = CalculatorEngine.evaluate_expression("((10 + 20) * 3) / (2 ^ 3 + 2)")
        assert err is None
        # ((30) * 3) / (8 + 2) = 90 / 10 = 9
        assert res == 9

    def test_evaluate_errors(self):
        res, err = CalculatorEngine.evaluate_expression("10 / 0")
        assert "Division by zero" in err
        assert res is None

        res, err = CalculatorEngine.evaluate_expression("10 % 0")
        assert "Division by zero" in err or "zero" in err.lower()
        assert res is None

        res, err = CalculatorEngine.evaluate_expression("sqrt(-16)")
        assert "negative" in err.lower() or "math domain" in err.lower()
        assert res is None

        res, err = CalculatorEngine.evaluate_expression("10 + * 5")
        assert "Invalid syntax" in err
        assert res is None

        res, err = CalculatorEngine.evaluate_expression("__import__('os')")
        assert err is not None
        assert res is None

        res, err = CalculatorEngine.evaluate_expression("")
        assert "Empty" in err
        assert res is None


class TestCalculatorState:
    """Tests for CalculatorState interaction and memory."""

    def test_digit_and_clear_input(self):
        calc = CalculatorState()
        calc.handle_input("5")
        calc.handle_input("8")
        assert calc.expression == "58"

        calc.handle_input("+")
        calc.handle_input("2")
        assert calc.expression == "58 + 2"

        calc.handle_input("C")
        assert calc.expression == "0"

    def test_backspace(self):
        calc = CalculatorState()
        calc.handle_input("1")
        calc.handle_input("2")
        calc.handle_input("3")
        assert calc.expression == "123"

        calc.handle_input("⌫")
        assert calc.expression == "12"

        calc.handle_input("⌫")
        assert calc.expression == "1"

        calc.handle_input("⌫")
        assert calc.expression == "0"

    def test_calculation_and_chaining(self):
        calc = CalculatorState()
        calc.handle_input("1")
        calc.handle_input("0")
        calc.handle_input("×")
        calc.handle_input("5")
        calc.handle_input("=")
        assert calc.expression == "50"
        assert len(calc.history) == 1

        # Chaining operator after calculation
        calc.handle_input("+")
        calc.handle_input("1")
        calc.handle_input("0")
        calc.handle_input("=")
        assert calc.expression == "60"
        assert len(calc.history) == 2

    def test_negation_toggle(self):
        calc = CalculatorState()
        calc.handle_input("2")
        calc.handle_input("5")
        calc.handle_input("±")
        assert calc.expression == "-25"
        calc.handle_input("±")
        assert calc.expression == "25"

    def test_unary_operations(self):
        calc = CalculatorState()
        calc.handle_input("9")
        calc.handle_input("√")
        assert calc.expression == "3"

        calc.handle_input("x²")
        assert calc.expression == "9"

        calc.handle_input("%")
        assert calc.expression == "0.09"

    def test_memory_operations(self):
        calc = CalculatorState()
        calc.handle_input("1")
        calc.handle_input("0")
        calc.handle_input("M+")
        assert calc.memory == 10.0

        calc.handle_input("5")
        calc.handle_input("M+")
        assert calc.memory == 15.0

        calc.handle_input("2")
        calc.handle_input("M-")
        assert calc.memory == 13.0

        calc.handle_input("C")
        calc.handle_input("MR")
        assert calc.expression == "13"

        calc.handle_input("MC")
        assert calc.memory == 0.0

    def test_history_clear(self):
        calc = CalculatorState()
        calc.handle_input("3")
        calc.handle_input("+")
        calc.handle_input("4")
        calc.handle_input("=")
        assert len(calc.history) == 1

        calc.clear_history()
        assert len(calc.history) == 0

    def test_compound_calculation_flow(self):
        calc = CalculatorState()
        # Input 100
        for ch in "100":
            calc.handle_input(ch)
        calc.handle_input("÷")
        for ch in "4":
            calc.handle_input(ch)
        calc.handle_input("=")
        assert calc.expression == "25"

        # Square root of 25
        calc.handle_input("√")
        assert calc.expression == "5"

        # Multiply by 3
        calc.handle_input("×")
        calc.handle_input("3")
        calc.handle_input("=")
        assert calc.expression == "15"

        # Percentage
        calc.handle_input("%")
        assert calc.expression == "0.15"

    def test_error_recovery(self):
        calc = CalculatorState()
        calc.handle_input("5")
        calc.handle_input("÷")
        calc.handle_input("0")
        calc.handle_input("=")
        assert "Error:" in calc.expression

        # Pressing a new number clears the error and begins fresh
        calc.handle_input("8")
        assert calc.expression == "8"
