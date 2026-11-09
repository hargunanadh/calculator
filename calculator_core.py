"""
Calculator Core Module
Provides safe mathematical evaluation, basic and scientific operations,
memory operations, and history tracking.
"""

import ast
import math
import operator
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

# Supported operators for safe AST evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Supported mathematical functions and constants
SAFE_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "exp": math.exp,
    "fact": math.factorial,
}

SAFE_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


class CalculatorEngine:
    """Core mathematical calculator engine."""

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    @staticmethod
    def power(base: float, exp: float) -> float:
        return base ** exp

    @staticmethod
    def modulo(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot perform modulo by zero")
        return a % b

    @staticmethod
    def square_root(a: float) -> float:
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(a)

    @staticmethod
    def percentage(a: float) -> float:
        return a / 100.0

    @staticmethod
    def reciprocal(a: float) -> float:
        if a == 0:
            raise ZeroDivisionError("Cannot calculate reciprocal of zero")
        return 1.0 / a

    @staticmethod
    def factorial(n: int) -> int:
        if not isinstance(n, int) and not (isinstance(n, float) and n.is_integer()):
            raise ValueError("Factorial requires an integer")
        n_int = int(n)
        if n_int < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n_int > 100:
            raise OverflowError("Factorial input too large (max 100)")
        return math.factorial(n_int)

    @staticmethod
    def format_result(val: Union[int, float]) -> Union[int, float]:
        """Formats result to int if it has no fractional part, or rounded float."""
        if isinstance(val, (int, float)):
            if math.isnan(val) or math.isinf(val):
                return val
            if isinstance(val, float) and val.is_integer():
                return int(val)
            # Round float precision to eliminate floating point artifacts like 0.1 + 0.2 = 0.30000000000000004
            rounded = round(val, 10)
            if rounded.is_integer():
                return int(rounded)
            return rounded
        return val

    @classmethod
    def evaluate_expression(cls, expr: str) -> Tuple[Optional[Union[int, float]], Optional[str]]:
        """
        Safely evaluates an algebraic mathematical expression string using AST parsing.
        Returns (result, error_message).
        """
        if not expr or not expr.strip():
            return None, "Empty expression"

        # Sanitize & normalize characters
        normalized = (
            expr.strip()
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
            .replace("^", "**")
            .replace("π", "pi")
        )

        try:
            tree = ast.parse(normalized, mode="eval")
            result = cls._eval_ast_node(tree.body)
            formatted = cls.format_result(result)
            return formatted, None
        except ZeroDivisionError:
            return None, "Error: Division by zero"
        except (ValueError, TypeError, OverflowError) as e:
            return None, f"Error: {str(e)}"
        except SyntaxError:
            return None, "Error: Invalid syntax"
        except Exception as e:
            return None, f"Error: {str(e)}"

    @classmethod
    def _eval_ast_node(cls, node: ast.AST) -> Any:
        """Recursively evaluates safe AST nodes."""
        if isinstance(node, ast.Constant):  # Python 3.8+ numbers/constants
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant value")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
            left = cls._eval_ast_node(node.left)
            right = cls._eval_ast_node(node.right)
            op_func = SAFE_OPERATORS[op_type]
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            if op_type == ast.Pow and abs(right) > 1000:
                raise OverflowError("Exponent too large")
            return op_func(left, right)

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            operand = cls._eval_ast_node(node.operand)
            return SAFE_OPERATORS[op_type](operand)

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function call")
            func_name = node.func.id.lower()
            if func_name not in SAFE_FUNCTIONS:
                raise ValueError(f"Unsupported function: {func_name}")
            args = [cls._eval_ast_node(arg) for arg in node.args]
            return SAFE_FUNCTIONS[func_name](*args)

        elif isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower in SAFE_CONSTANTS:
                return SAFE_CONSTANTS[name_lower]
            raise ValueError(f"Unsupported variable or constant: {node.id}")

        else:
            raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")


class CalculatorState:
    """Manages calculator display, memory, and calculation history."""

    def __init__(self):
        self.expression: str = "0"
        self.memory: float = 0.0
        self.history: List[Dict[str, Any]] = []
        self.last_result: Optional[Union[int, float]] = None
        self.just_calculated: bool = False

    def handle_input(self, action: str) -> None:
        """Processes button presses or inputs."""
        if action == "C":
            # Clear current entry
            self.expression = "0"
            self.just_calculated = False

        elif action == "AC":
            # Clear all
            self.expression = "0"
            self.last_result = None
            self.just_calculated = False

        elif action == "⌫" or action == "BACKSPACE":
            if self.just_calculated or len(self.expression) <= 1:
                self.expression = "0"
                self.just_calculated = False
            else:
                self.expression = self.expression[:-1]
                if not self.expression:
                    self.expression = "0"

        elif action == "=":
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if err:
                self.last_result = None
                self.expression = err
                self.just_calculated = True
            else:
                self.record_history(self.expression, res)
                self.last_result = res
                self.expression = str(res)
                self.just_calculated = True

        elif action == "±":
            # Toggle negation
            if self.expression in ("0", "Error: Division by zero", "Error: Invalid syntax") or self.expression.startswith("Error:"):
                return
            if self.expression.startswith("-(") and self.expression.endswith(")"):
                self.expression = self.expression[2:-1]
            elif self.expression.startswith("-") and not any(op in self.expression[1:] for op in "+-×÷*/^ "):
                self.expression = self.expression[1:]
            elif not any(op in self.expression for op in "+-×÷*/^ "):
                # Single positive number
                self.expression = f"-{self.expression}"
            else:
                self.expression = f"-({self.expression})"
            self.just_calculated = False

        elif action == "%":
            # Convert current expression to percentage
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if not err and res is not None:
                val = CalculatorEngine.percentage(res)
                formatted = CalculatorEngine.format_result(val)
                self.record_history(f"{res}%", formatted)
                self.expression = str(formatted)
                self.just_calculated = True

        elif action == "√" or action == "sqrt":
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if not err and res is not None:
                try:
                    val = CalculatorEngine.square_root(res)
                    formatted = CalculatorEngine.format_result(val)
                    self.record_history(f"√({res})", formatted)
                    self.expression = str(formatted)
                    self.just_calculated = True
                except ValueError as e:
                    self.expression = f"Error: {str(e)}"
                    self.just_calculated = True

        elif action == "1/x":
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if not err and res is not None:
                try:
                    val = CalculatorEngine.reciprocal(res)
                    formatted = CalculatorEngine.format_result(val)
                    self.record_history(f"1/({res})", formatted)
                    self.expression = str(formatted)
                    self.just_calculated = True
                except ZeroDivisionError as e:
                    self.expression = f"Error: {str(e)}"
                    self.just_calculated = True

        elif action == "x²":
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if not err and res is not None:
                val = CalculatorEngine.power(res, 2)
                formatted = CalculatorEngine.format_result(val)
                self.record_history(f"({res})²", formatted)
                self.expression = str(formatted)
                self.just_calculated = True

        elif action == "MC":
            self.memory = 0.0

        elif action == "MR":
            mem_formatted = CalculatorEngine.format_result(self.memory)
            if self.expression == "0" or self.just_calculated:
                self.expression = str(mem_formatted)
            else:
                self.expression += str(mem_formatted)
            self.just_calculated = False

        elif action == "M+":
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if not err and res is not None:
                self.memory += float(res)
                self.just_calculated = True

        elif action == "M-":
            res, err = CalculatorEngine.evaluate_expression(self.expression)
            if not err and res is not None:
                self.memory -= float(res)
                self.just_calculated = True

        else:
            # Digits, operators (+, -, ×, ÷, ^, ., (, ))
            operators = {"+", "-", "×", "÷", "*", "/", "^"}

            if self.expression.startswith("Error:"):
                self.expression = "0"
                self.just_calculated = False

            if self.just_calculated:
                if action in operators:
                    # Continue calculation with previous result
                    self.just_calculated = False
                    self.expression += f" {action} "
                else:
                    # Start fresh calculation
                    self.expression = action
                    self.just_calculated = False
                return

            if self.expression == "0" and action not in operators and action != ".":
                self.expression = action
            elif action in operators:
                self.expression += f" {action} "
            else:
                self.expression += action

    def record_history(self, expr: str, result: Union[int, float]) -> None:
        self.history.append({
            "expression": expr,
            "result": result,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

    def clear_history(self) -> None:
        self.history.clear()

    def insert_result(self, result_val: Union[int, float, str]) -> None:
        """Instantly inserts a tapped result value into current expression."""
        val_str = str(result_val)
        if self.expression in ("0", "Error: Division by zero", "Error: Invalid syntax") or self.expression.startswith("Error:") or self.just_calculated:
            self.expression = val_str
        elif self.expression[-1] in "+-×÷*/^ ":
            self.expression += val_str
        else:
            self.expression += f" {val_str}"
        self.just_calculated = False

    def append_result(self, result_val: Union[int, float, str], op: str = "+") -> None:
        """Appends operator and tapped result value to active calculation."""
        val_str = str(result_val)
        if self.expression in ("0", "Error: Division by zero", "Error: Invalid syntax") or self.expression.startswith("Error:"):
            self.expression = val_str
        else:
            self.expression += f" {op} {val_str}"
        self.just_calculated = False

    def load_expression(self, expr: str) -> None:
        """Loads a previous equation string back into active expression for editing."""
        self.expression = expr
        self.just_calculated = False
