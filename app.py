"""
Modern Pastel Blue Ocean Calculator Application
Featuring an infinite scrollable running tape, tappable past calculations,
interactive pastel buttons, and an animated ocean wave background.
"""

import streamlit as st
from calculator_core import CalculatorEngine, CalculatorState

# Page configuration
st.set_page_config(
    page_title="Pastel Ocean Calculator",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS): Pastel Blue Aesthetic + Ocean Waves Animation
st.markdown("""
<style>
    /* Background & Global Container */
    .stApp {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 30%, #bae6fd 65%, #7dd3fc 100%) fixed !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
        color: #0c4a6e;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        position: relative;
        z-index: 10;
    }

    /* Ocean Waves Animation Container */
    .ocean-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 180px;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }

    .ocean-wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 100%;
        background-repeat: repeat-x;
        background-position: 0 bottom;
        transform-origin: center bottom;
    }

    .wave-back {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0 C150,90 350,-40 500,40 C650,120 900,10 1200,30 L1200,120 L0,120 Z' fill='%230284c7' fill-opacity='0.25'%3E%3C/path%3E%3C/svg%3E");
        background-size: 50% 110px;
        height: 110px;
        animation: ocean-drift 22s linear infinite reverse;
    }

    .wave-mid {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,30 C200,110 400,-20 600,50 C800,120 1000,0 1200,40 L1200,120 L0,120 Z' fill='%2338bdf8' fill-opacity='0.45'%3E%3C/path%3E%3C/svg%3E");
        background-size: 50% 95px;
        height: 95px;
        animation: ocean-drift 14s linear infinite;
    }

    .wave-front {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,50 C180,100 380,10 580,60 C780,110 980,20 1200,50 L1200,120 L0,120 Z' fill='%237dd3fc' fill-opacity='0.65'%3E%3C/path%3E%3C/svg%3E");
        background-size: 50% 75px;
        height: 75px;
        animation: ocean-drift 8s linear infinite;
    }

    @keyframes ocean-drift {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    /* Glassmorphism Calculator & Tape Card Containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.95);
        border-radius: 26px;
        padding: 24px;
        box-shadow: 0 18px 45px -10px rgba(2, 132, 199, 0.18), 0 4px 15px rgba(56, 189, 248, 0.15);
        margin-bottom: 1.5rem;
    }

    /* Calculator Display Screen */
    .calc-screen {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #bae6fd;
        border-radius: 20px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 6px rgba(2, 132, 199, 0.08), 0 4px 15px rgba(186, 230, 253, 0.5);
        text-align: right;
        font-family: 'SF Mono', 'Courier New', monospace;
    }

    .screen-mem-tag {
        color: #0284c7;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .screen-main {
        color: #0369a1;
        font-size: 2.7rem;
        font-weight: 800;
        line-height: 1.2;
        word-break: break-all;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
    }

    /* Button Styling: Soft Pastel Blue Palette */
    div[data-testid="column"] button {
        width: 100% !important;
        height: 52px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        border: 1.5px solid #bae6fd !important;
        background: #ffffff !important;
        color: #0c4a6e !important;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 3px 8px rgba(2, 132, 199, 0.08) !important;
        margin-bottom: 7px !important;
    }

    div[data-testid="column"] button:hover {
        transform: translateY(-2px);
        background: #e0f2fe !important;
        border-color: #7dd3fc !important;
        box-shadow: 0 8px 16px rgba(2, 132, 199, 0.16) !important;
        color: #0284c7 !important;
    }

    div[data-testid="column"] button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 5px rgba(2, 132, 199, 0.1) !important;
    }

    /* Primary Accent Button (Equals =) */
    div[data-testid="column"] button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.35) !important;
    }

    div[data-testid="column"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7dd3fc 0%, #0369a1 100%) !important;
        box-shadow: 0 8px 22px rgba(2, 132, 199, 0.45) !important;
    }

    /* Running Tape / Infinite History Card */
    .tape-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2px dashed #bae6fd;
    }

    .tape-item {
        background: rgba(240, 249, 255, 0.95);
        border: 1.5px solid #bae6fd;
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.06);
        transition: transform 0.15s ease;
    }

    .tape-item:hover {
        transform: scale(1.01);
        border-color: #38bdf8;
    }

    .tape-time {
        font-size: 0.72rem;
        color: #64748b;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .tape-equation {
        color: #334155;
        font-size: 1.05rem;
        font-weight: 600;
        word-break: break-all;
    }

    .tape-result {
        color: #0284c7;
        font-size: 1.4rem;
        font-weight: 800;
        word-break: break-all;
    }

    /* Compact tape action buttons */
    .stButton button.tape-action-btn {
        height: 32px !important;
        font-size: 0.82rem !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        margin-top: 4px !important;
    }
</style>

<!-- Animated Ocean Waves HTML injected into background -->
<div class="ocean-wrapper">
    <div class="ocean-wave wave-back"></div>
    <div class="ocean-wave wave-mid"></div>
    <div class="ocean-wave wave-front"></div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "calc_state" not in st.session_state:
    st.session_state.calc_state = CalculatorState()

calc = st.session_state.calc_state

# Sidebar - Settings, Memory, and Quick Reference
with st.sidebar:
    st.markdown("## 🌊 Ocean Calculator")
    st.caption("Pastel Blue Edition • Precision AST Math")

    st.markdown("---")
    st.markdown("### 💾 Memory Registers")
    mem_val = CalculatorEngine.format_result(calc.memory)
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.info(f"Memory: **{mem_val}**")
    with col_m2:
        if st.button("Clear M", key="sb_clear_m", use_container_width=True):
            calc.handle_input("MC")
            st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ Tappable History Guide")
    st.markdown("""
    - **Tap Result**: Instantly replaces the current display with that number.
    - **Tap (+ Add)**: Appends `+ [Result]` to chain into your active calculation.
    - **Tap Equation**: Reloads the full equation back onto the calculator.
    """)

    st.markdown("---")
    with st.expander("🧪 Supported Functions"):
        st.markdown("""
        - `sqrt(x)`: Square root
        - `sin(x)`, `cos(x)`, `tan(x)`: Trigonometry
        - `log(x)`: Base-10 log, `ln(x)`: Natural log
        - `fact(n)`: Factorial `n!`
        - `pi`: 3.14159, `e`: 2.71828
        """)

# Header Banner
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("<h2 style='color: #0369a1; margin-bottom: 4px;'>🌊 Pastel Ocean Calculator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #0284c7; font-size: 0.95rem; margin-top: 0;'>Interactive keypad • Infinite scrollable running tape • Tappable past calculations</p>", unsafe_allow_html=True)
with header_col2:
    mode = st.radio("Input Mode", ["Keypad", "Formula Bar"], horizontal=True, label_visibility="collapsed")

# Two-Column Layout: Left = Calculator, Right = Infinite Running History Tape
col_calc, col_tape = st.columns([7, 5], gap="large")

with col_calc:
    # Calculator Screen
    mem_tag = f"MEM: {CalculatorEngine.format_result(calc.memory)}" if calc.memory != 0 else ""
    preview_tag = f"Ans: {calc.last_result}" if calc.last_result is not None else ""

    st.markdown(f"""
    <div class="calc-screen">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span class="screen-mem-tag">{mem_tag}</span>
            <span class="screen-mem-tag" style="color: #64748b;">{preview_tag}</span>
        </div>
        <div class="screen-main">{calc.expression}</div>
    </div>
    """, unsafe_allow_html=True)

    # Formula Bar mode if active
    if mode == "Formula Bar":
        with st.form("formula_input_form", clear_on_submit=False):
            f_col1, f_col2 = st.columns([4, 1])
            with f_col1:
                formula_val = st.text_input(
                    "Formula",
                    value=calc.expression if not calc.expression.startswith("Error:") else "",
                    placeholder="e.g. (25 * 4) + sqrt(144) - 10",
                    label_visibility="collapsed"
                )
            with f_col2:
                eval_submit = st.form_submit_button("⚡ Solve", use_container_width=True)
            if eval_submit and formula_val:
                calc.expression = formula_val
                calc.handle_input("=")
                st.rerun()

    # Scientific Functions Expander
    with st.expander("✨ Scientific Functions & Constants (Click to insert)"):
        sci_cols = st.columns(6)
        sci_buttons = [
            ("√x", "√"), ("x²", "x²"), ("1/x", "1/x"), ("x^y", "^"), ("π", "3.14159"), ("e", "2.71828"),
            ("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("log", "log("), ("ln", "ln("), ("n!", "fact(")
        ]
        for idx, (label, val) in enumerate(sci_buttons):
            with sci_cols[idx % 6]:
                if st.button(label, key=f"sci_btn_{label}", use_container_width=True):
                    if label in ["x²", "1/x", "√x"]:
                        calc.handle_input(label.replace("x", ""))
                    else:
                        if calc.expression == "0" or calc.just_calculated:
                            calc.expression = val
                        else:
                            calc.expression += val
                        calc.just_calculated = False
                    st.rerun()

    # Standard Calculator Keypad Grid
    # 5 Columns: Memory/Clear, Parentheses/Ops, Digits, Operators, Equal
    layout = [
        [("MC", "MC"), ("MR", "MR"), ("M+", "M+"), ("M-", "M-"), ("AC", "AC")],
        [("(", "("), (")", ")"), ("%", "%"), ("⌫", "⌫"), ("÷", "÷")],
        [("7", "7"), ("8", "8"), ("9", "9"), ("^", "^"), ("×", "×")],
        [("4", "4"), ("5", "5"), ("6", "6"), ("±", "±"), ("−", "-")],
        [("1", "1"), ("2", "2"), ("3", "3"), ("x²", "x²"), ("+", "+")],
        [("0", "0"), (".", "."), ("00", "00"), ("√", "√"), ("=", "=")]
    ]

    for row_idx, row in enumerate(layout):
        cols = st.columns(len(row))
        for col_idx, (label, val) in enumerate(row):
            with cols[col_idx]:
                btn_type = "primary" if label == "=" else "secondary"
                if st.button(label, key=f"key_{row_idx}_{col_idx}_{label}", type=btn_type, use_container_width=True):
                    calc.handle_input(val)
                    st.rerun()

with col_tape:
    # Infinite Scrollable Running Tape Header
    history_count = len(calc.history)
    t_head_col1, t_head_col2 = st.columns([3, 1])
    with t_head_col1:
        st.markdown(f"<h4 style='color: #0284c7; margin-bottom: 0;'>📜 Running Tape ({history_count})</h4>", unsafe_allow_html=True)
        st.caption("Scrollable ledger • Tap any past value to insert")
    with t_head_col2:
        if history_count > 0:
            if st.button("🗑️ Clear", key="clear_tape_btn", use_container_width=True):
                calc.clear_history()
                st.rerun()

    # Infinite Scrollable Container (Fixed height with native smooth scrolling)
    with st.container(height=530):
        if calc.history:
            for idx, item in enumerate(reversed(calc.history)):
                real_idx = history_count - 1 - idx
                # Display Card
                st.markdown(f"""
                <div class="tape-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="tape-time">🕒 {item['timestamp']}</span>
                        <span class="tape-time" style="color: #0284c7;">#{real_idx + 1}</span>
                    </div>
                    <div class="tape-equation">{item['expression']} =</div>
                    <div class="tape-result">{item['result']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Interactive Tappable Actions for each card
                btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 1])
                with btn_c1:
                    if st.button(f"📥 Insert", key=f"tap_ins_{real_idx}", help=f"Set active display to {item['result']}", use_container_width=True):
                        calc.insert_result(item['result'])
                        st.rerun()
                with btn_c2:
                    if st.button(f"➕ Add", key=f"tap_add_{real_idx}", help=f"Append + {item['result']} to current calculation", use_container_width=True):
                        calc.append_result(item['result'], "+")
                        st.rerun()
                with btn_c3:
                    if st.button(f"🔁 Reload", key=f"tap_load_{real_idx}", help="Reload the original formula back onto screen", use_container_width=True):
                        calc.load_expression(item['expression'])
                        st.rerun()
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; color: #64748b;">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">🌊</div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #0284c7;">Tape is Ready</div>
                <div style="font-size: 0.88rem; margin-top: 4px;">Perform calculations on the left, and every equation will be preserved on this scrollable tape!</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #0369a1; font-size: 0.85rem; font-weight: 500;'>"
    "🌊 Pastel Ocean Calculator • Infinite Running Tape & Tappable Calculations • Precision Math"
    "</div>",
    unsafe_allow_html=True
)
