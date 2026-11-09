"""
Modern Streamlit Calculator Application
A feature-rich, beautifully styled calculator hosted with Streamlit.
"""

import streamlit as st
from calculator_core import CalculatorEngine, CalculatorState

# Page configuration
st.set_page_config(
    page_title="Modern Pro Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    /* Global Container styling */
    .block-container {
        max-width: 950px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Calculator Screen */
    .calc-screen {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        text-align: right;
        font-family: 'SF Mono', 'Courier New', monospace;
    }
    
    .screen-mem-tag {
        color: #38bdf8;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
        min-height: 1.2rem;
    }
    
    .screen-sub {
        color: #94a3b8;
        font-size: 1.05rem;
        min-height: 1.5rem;
        word-break: break-all;
    }
    
    .screen-main {
        color: #f8fafc;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
        word-break: break-all;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }
    
    /* Button Grid customisations */
    div[data-testid="column"] button {
        width: 100% !important;
        height: 52px !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: all 0.15s ease-in-out !important;
        margin-bottom: 6px !important;
    }
    
    div[data-testid="column"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    }

    div[data-testid="column"] button:active {
        transform: translateY(1px);
    }

    /* History Card */
    .history-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .history-expr {
        color: #cbd5e1;
        font-size: 0.95rem;
    }
    .history-res {
        color: #38bdf8;
        font-size: 1.15rem;
        font-weight: 700;
    }
    .history-time {
        color: #64748b;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "calc_state" not in st.session_state:
    st.session_state.calc_state = CalculatorState()

calc = st.session_state.calc_state

# Sidebar - Settings, History & Quick Guide
with st.sidebar:
    st.title("🧮 Calculator Pro")
    st.caption("Precision arithmetic & scientific calculations")
    
    st.markdown("---")
    st.subheader("💾 Memory Status")
    mem_val = CalculatorEngine.format_result(calc.memory)
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.info(f"Stored: **{mem_val}**")
    with col_m2:
        if st.button("Reset M", key="reset_mem_btn"):
            calc.handle_input("MC")
            st.rerun()

    st.markdown("---")
    st.subheader("📜 Calculation History")
    if calc.history:
        if st.button("🗑️ Clear History", key="clear_hist_btn", use_container_width=True):
            calc.clear_history()
            st.rerun()

        for idx, item in enumerate(reversed(calc.history)):
            st.markdown(f"""
            <div class="history-card">
                <div>
                    <div class="history-expr">{item['expression']} =</div>
                    <div class="history-res">{item['result']}</div>
                </div>
                <div class="history-time">{item['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Load {item['result']}", key=f"hist_load_{idx}", use_container_width=True):
                calc.expression = str(item['result'])
                calc.just_calculated = False
                st.rerun()
    else:
        st.write("No calculations yet.")

    st.markdown("---")
    with st.expander("ℹ️ Keyboard & Function Reference"):
        st.markdown("""
        - **Operators**: `+`, `-`, `*` or `×`, `/` or `÷`, `^` (power), `%` (modulo)
        - **Functions**: `sqrt(x)`, `abs(x)`, `sin(x)`, `cos(x)`, `tan(x)`, `log(x)`, `ln(x)`, `fact(n)`
        - **Constants**: `pi`, `e`
        - **Shortcuts**: Use direct formula bar or the touch keypad.
        """)

# Main Section
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("### Interactive Calculator")
with header_col2:
    mode = st.radio("Input Mode", ["Keypad", "Formula Bar"], horizontal=True, label_visibility="collapsed")

# Readout Screen
mem_indicator = f"MEMORY: {CalculatorEngine.format_result(calc.memory)}" if calc.memory != 0 else ""
last_calc_preview = f"Ans = {calc.last_result}" if calc.last_result is not None else ""

st.markdown(f"""
<div class="calc-screen">
    <div style="display: flex; justify-content: space-between;">
        <span class="screen-mem-tag">{mem_indicator}</span>
        <span class="screen-mem-tag" style="color: #94a3b8;">{last_calc_preview}</span>
    </div>
    <div class="screen-main">{calc.expression}</div>
</div>
""", unsafe_allow_html=True)

# Direct Formula Input Mode
if mode == "Formula Bar":
    st.markdown("##### ⌨️ Direct Expression Input")
    with st.form("formula_form", clear_on_submit=False):
        formula_input = st.text_input(
            "Enter formula (e.g., 25 * 4 + sqrt(144) - 2^3):",
            value=calc.expression if not calc.expression.startswith("Error:") else "",
            placeholder="e.g. 50 * 1.2 or sqrt(25) + 10"
        )
        submit_btn = st.form_submit_button("⚡ Evaluate Expression", use_container_width=True)
        if submit_btn and formula_input:
            calc.expression = formula_input
            calc.handle_input("=")
            st.rerun()

# Button Click Callback
def on_btn_click(btn_label: str):
    calc.handle_input(btn_label)

# Scientific Functions Toggle
with st.expander("🧪 Scientific Functions (Click to insert)"):
    sci_cols = st.columns(6)
    sci_buttons = [
        ("√x", "sqrt"), ("x²", "x²"), ("1/x", "1/x"), ("x^y", "^"), ("π", "3.14159"), ("e", "2.71828"),
        ("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("log", "log("), ("ln", "ln("), ("n!", "fact(")
    ]
    for i, (label, val) in enumerate(sci_buttons):
        with sci_cols[i % 6]:
            if st.button(label, key=f"sci_{label}", use_container_width=True):
                if label in ["x²", "1/x", "√x"]:
                    calc.handle_input(label.replace("x", "").replace("√x", "√"))
                else:
                    if calc.expression == "0" or calc.just_calculated:
                        calc.expression = val
                    else:
                        calc.expression += val
                    calc.just_calculated = False
                st.rerun()

# Keypad Layout
grid = [
    ["MC", "MR", "M+", "M-", "AC", "⌫"],
    ["(", ")", "%", "^", "±", "÷"],
    ["7", "8", "9", "×", "x²", "√"],
    ["4", "5", "6", "−", "1/x", "C"],
    ["1", "2", "3", "+", ".", "="],
    ["0", "00", "+", "-", "*", "/"]
]

# Cleaner Standard Keypad Layout: 5 columns
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
            if st.button(label, key=f"btn_{row_idx}_{col_idx}_{label}", type=btn_type, use_container_width=True):
                on_btn_click(val)
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "Built with Streamlit & Python • Safe AST Math Evaluation • Precision Guaranteed"
    "</div>",
    unsafe_allow_html=True
)

