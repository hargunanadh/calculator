# 🤍 HARGUNS CALCULATOR

A feature-rich, interactive, and beautifully designed calculator application built with Python and Streamlit, styled in a soothing pastel blue theme with animated ocean waves, flying seagulls, and an illuminated high-contrast display.

## ✨ Features

- **🤍 Custom Branded & Ocean Aesthetic**:
  - Branded **HARGUNS CALCULATOR 🤍**.
  - Animated white seagulls flying gracefully across the pastel sky with wing-flapping motion.
  - Multi-layered, perpetual undulating SVG ocean waves at the bottom of the viewport.
  - Calming pastel sky-to-ocean palette (`#f0f9ff`, `#e0f2fe`, `#bae6fd`, `#7dd3fc`, `#0284c7`).
- **💡 Illuminated High-Contrast Display**:
  - Glowing, ultra-readable white text (`#ffffff` with gentle cyan halo glow) on a deep ocean marine screen.
  - Large, bold 3.1rem typography so equations and results are crystal clear and easy to read.
  - Crisp, bold button fonts (`1.35rem`, font-weight 800) with clear contrast.
- **📜 Infinite Scrollable History (Running Tape)**:
  - Running tape of all past calculations that you can scroll through without losing previous work.
  - Item counter and one-click clear options.
- **👆 Tappable Previous Results & Equations**:
  - **📥 Insert**: Tap any past result to immediately set it as the active display value.
  - **➕ Add**: Chain `+ [Result]` directly into your current formula.
  - **🔁 Reload**: Re-load the original formula back onto the screen to modify or re-evaluate.
- **All Basic & Advanced Arithmetic Operations**:
  - Addition (`+`), Subtraction (`−`), Multiplication (`×`), Division (`÷`)
  - Modulo (`%`), Exponentiation / Power (`x^y`), Square Root (`√`), Reciprocal (`1/x`), Negation (`±`)
  - Order of operations precedence and parentheses support: `(2 + 3) * 4`
- **Memory Operations**:
  - `M+` (Add to memory), `M-` (Subtract from memory), `MR` (Recall memory), `MC` (Clear memory)
- **Dual-Mode Input**:
  - **Keypad Mode**: Touch/Click buttons just like a physical or smartphone calculator.
  - **Formula Bar Mode**: Direct keyboard input for complex mathematical expressions.
- **Scientific Functions Drawer**:
  - Trigonometric: `sin`, `cos`, `tan`
  - Logarithmic: `log` (base 10), `ln` (natural log)
  - Math constants: `π` (pi), `e`
  - Factorial: `n!`
- **Safe & Robust Engine**:
  - Safe evaluation using Python AST (Abstract Syntax Tree) — zero arbitrary code execution (`no unsafe eval()`)
  - Division by zero and syntax error protection
  - Floating point precision compensation (e.g. `0.1 + 0.2 = 0.3`)

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

