# 🧮 Modern Streamlit Calculator Pro

A feature-rich, interactive, and beautifully designed calculator application built with Python and Streamlit.

## ✨ Features

- **All Basic Arithmetic Operations**:
  - Addition (`+`), Subtraction (`−`), Multiplication (`×`), Division (`÷`)
  - Modulo (`%`), Exponentiation / Power (`x^y`), Square Root (`√`), Reciprocal (`1/x`), Negation (`±`)
  - Order of operations precedence and parentheses support: `(2 + 3) * 4`
- **Memory Operations**:
  - `M+` (Add to memory)
  - `M-` (Subtract from memory)
  - `MR` (Recall memory)
  - `MC` (Clear memory)
  - Active memory status indicator
- **Interactive Dual-Mode UI**:
  - **Keypad Mode**: Touch/Click buttons just like a physical or smartphone calculator.
  - **Formula Bar Mode**: Direct keyboard input for complex mathematical expressions.
- **Scientific Functions Drawer**:
  - Trigonometric: `sin`, `cos`, `tan`
  - Logarithmic: `log` (base 10), `ln` (natural log)
  - Math constants: `π` (pi), `e`
  - Factorial: `n!`
- **Calculation History**:
  - Chronological history with timestamps
  - One-click restore: load any past result straight back into the calculator
  - Clear history option
- **Safe & Robust Engine**:
  - Safe evaluation using Python AST (Abstract Syntax Tree) — zero arbitrary code execution (`no unsafe eval()`)
  - Division by zero and syntax error protection
  - Elimination of floating point precision artifacts (e.g. `0.1 + 0.2 = 0.3`)

---

## 🚀 How to Run the App

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit App
```bash
streamlit run app.py
```
Or with specific Python executable:
```bash
python -m streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the full test suite with pytest:

```bash
# Run all unit and UI tests
python -m pytest -v

# Run only core logic tests
python -m pytest test_calculator.py -v

# Run Streamlit UI integration tests
python -m pytest test_app.py -v
```

---

## 📁 Project Structure

```
├── app.py                 # Streamlit UI & interaction layer
├── calculator_core.py     # Core mathematical logic, AST evaluator, state & memory
├── test_calculator.py     # Unit tests for core operations and edge cases
├── test_app.py            # Streamlit AppTest headless UI tests
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

