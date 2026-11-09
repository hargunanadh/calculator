"""
HARGUNS CALCULATOR 🤍
Pastel Blue Ocean Theme featuring animated flying seagulls, gentle ocean waves,
an illuminated high-contrast display, an infinite scrollable running tape,
and bright, high-visibility buttons.
"""

import streamlit as st
from calculator_core import CalculatorEngine, CalculatorState

# Page configuration
st.set_page_config(
    page_title="HARGUNS CALCULATOR 🤍",
    page_icon="🤍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    /* =========================================
       PAGE FLOW & HEADER CLEARANCE
       Prevents title from being cut off at the top
       ========================================= */
    header[data-testid="stHeader"],
    [data-testid="stHeader"] {
        background: transparent !important;
        position: static !important;
        height: auto !important;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        position: relative;
        z-index: 10;
    }

    /* Background & Global Container */
    .stApp {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 30%, #bae6fd 65%, #7dd3fc 100%) fixed !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
        color: #0c4a6e;
    }

    /* Sidebar matching Pastel Ocean Theme */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%) !important;
        border-right: 2px solid #bae6fd !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #0369a1 !important;
    }

    /* =========================================
       ANIMATED FLYING SEAGULLS IN THE SKY
       ========================================= */
    .seagull-sky {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 45vh;
        pointer-events: none;
        z-index: 2;
        overflow: hidden;
    }

    .seagull {
        position: absolute;
        will-change: transform, left;
    }

    .seagull svg {
        display: block;
        filter: drop-shadow(0 3px 6px rgba(2, 132, 199, 0.28));
        animation: seagull-flap 1.4s ease-in-out infinite alternate;
    }

    .seagull-1 {
        top: 8%;
        left: -80px;
        width: 48px;
        animation: fly-across-1 22s linear infinite;
    }

    .seagull-2 {
        top: 18%;
        left: -80px;
        width: 34px;
        animation: fly-across-2 29s linear infinite;
        animation-delay: 5s;
    }

    .seagull-3 {
        top: 13%;
        left: -80px;
        width: 42px;
        animation: fly-across-3 20s linear infinite;
        animation-delay: 11s;
    }

    .seagull-4 {
        top: 5%;
        left: -80px;
        width: 26px;
        opacity: 0.85;
        animation: fly-across-4 36s linear infinite;
        animation-delay: 17s;
    }

    @keyframes seagull-flap {
        0% { transform: scaleY(1) rotate(0deg); }
        50% { transform: scaleY(0.45) rotate(-2deg); }
        100% { transform: scaleY(0.95) rotate(1deg); }
    }

    @keyframes fly-across-1 {
        0% { left: -80px; transform: translateY(0); }
        30% { transform: translateY(-16px); }
        70% { transform: translateY(12px); }
        100% { left: 105vw; transform: translateY(-5px); }
    }

    @keyframes fly-across-2 {
        0% { left: -80px; transform: translateY(0); }
        40% { transform: translateY(20px); }
        80% { transform: translateY(-15px); }
        100% { left: 105vw; transform: translateY(5px); }
    }

    @keyframes fly-across-3 {
        0% { left: -80px; transform: translateY(0); }
        50% { transform: translateY(-24px); }
        100% { left: 105vw; transform: translateY(8px); }
    }

    @keyframes fly-across-4 {
        0% { left: -80px; transform: translateY(0); }
        50% { transform: translateY(10px); }
        100% { left: 105vw; transform: translateY(-8px); }
    }

    /* =========================================
       OCEAN WAVES ANIMATION AT THE BOTTOM
       ========================================= */
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

    /* =========================================
       ILLUMINATED HIGH-CONTRAST SCREEN
       (Pure Glowing White Characters on Deep Ocean Screen)
       ========================================= */
    .calc-screen {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #075985 100%) !important;
        border: 2.5px solid #7dd3fc !important;
        border-radius: 22px !important;
        padding: 20px 26px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 30px rgba(2, 132, 199, 0.35), inset 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        text-align: right;
        font-family: 'SF Mono', 'Courier New', monospace;
    }

    .screen-mem-tag {
        color: #e0f2fe !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        text-shadow: 0 0 8px rgba(224, 242, 254, 0.6);
    }

    .screen-main {
        color: #ffffff !important;
        font-size: 3.1rem !important;
        font-weight: 900 !important;
        line-height: 1.2 !important;
        word-break: break-all !important;
        letter-spacing: 0.02em;
        text-shadow: 0 0 16px rgba(255, 255, 255, 0.85), 0 0 28px rgba(56, 189, 248, 0.9) !important;
    }

    /* =========================================
       UNIVERSAL BUTTON STYLING (CRISP WHITE BUTTONS, HIGH VISIBILITY)
       Works across both Light Mode and Dark Mode!
       ========================================= */
    .stButton > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="stBaseButton-secondary"],
    button[kind="secondary"],
    div[data-testid="column"] button,
    div[data-testid="stColumn"] button,
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important;
        height: 56px !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: 2.5px solid #bae6fd !important;
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #0284c7 !important;
        transition: all 0.16s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.14) !important;
        margin-bottom: 7px !important;
    }

    /* Force button inner text to be large, bright, and bold */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    div[data-testid="column"] button p,
    div[data-testid="stColumn"] button p,
    div[data-testid="stColumn"] button span {
        color: #0284c7 !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
    }

    /* Hover State for Buttons */
    .stButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover,
    div[data-testid="stColumn"] button:hover {
        transform: translateY(-2px);
        background: #e0f2fe !important;
        background-color: #e0f2fe !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 8px 18px rgba(2, 132, 199, 0.25) !important;
    }

    .stButton > button:hover p,
    .stButton > button:hover span,
    div[data-testid="stColumn"] button:hover p {
        color: #0369a1 !important;
    }

    /* Primary Accent Button (Equals =) */
    .stButton > button[kind="primary"],
    button[data-testid="baseButton-primary"],
    button[data-testid="stBaseButton-primary"],
    div[data-testid="stColumn"] button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45) !important;
    }

    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    button[data-testid="baseButton-primary"] p,
    div[data-testid="stColumn"] button[kind="primary"] p {
        color: #ffffff !important;
        font-size: 1.75rem !important;
        font-weight: 900 !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }

    .stButton > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #7dd3fc 0%, #0369a1 100%) !important;
        background-color: #0369a1 !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.55) !important;
    }

    /* =========================================
       RUNNING TAPE / INFINITE HISTORY CARDS
       ========================================= */
    .tape-item {
        background: #ffffff !important;
        border: 2px solid #bae6fd !important;
        border-radius: 16px !important;
        padding: 14px 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.1) !important;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }

    .tape-item:hover {
        transform: scale(1.01);
        border-color: #38bdf8 !important;
    }

    .tape-time {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .tape-equation {
        color: #0c4a6e !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        word-break: break-all;
    }

    .tape-result {
        color: #0284c7 !important;
        font-size: 1.65rem !important;
        font-weight: 900 !important;
        word-break: break-all;
        text-shadow: 0 1px 2px rgba(2, 132, 199, 0.15);
    }
</style>

<!-- Animated Flying Seagulls HTML in the Sky -->
<div class="seagull-sky">
    <div class="seagull seagull-1">
        <svg viewBox="0 0 80 30">
            <path d="M 0 16 Q 20 0 40 12 Q 60 0 80 16 Q 60 7 40 16 Q 20 7 0 16 Z" fill="#ffffff"/>
        </svg>
    </div>
    <div class="seagull seagull-2">
        <svg viewBox="0 0 80 30">
            <path d="M 0 16 Q 20 0 40 12 Q 60 0 80 16 Q 60 7 40 16 Q 20 7 0 16 Z" fill="#ffffff"/>
        </svg>
    </div>
    <div class="seagull seagull-3">
        <svg viewBox="0 0 80 30">
            <path d="M 0 16 Q 20 0 40 12 Q 60 0 80 16 Q 60 7 40 16 Q 20 7 0 16 Z" fill="#ffffff"/>
        </svg>
    </div>
    <div class="seagull seagull-4">
        <svg viewBox="0 0 80 30">
            <path d="M 0 16 Q 20 0 40 12 Q 60 0 80 16 Q 60 7 40 16 Q 20 7 0 16 Z" fill="#ffffff"/>
        </svg>
    </div>
</div>

<!-- Animated Ocean Waves HTML in the Background -->
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
    st.markdown("## HARGUNS CALCULATOR 🤍")
    st.caption("Pastel Ocean Edition • Precision AST Engine")

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
    st.markdown("### 👆 Tappable History Guide")
    st.markdown("""
    - **Tap 📥 Insert**: Sets the active display to that past result.
    - **Tap ➕ Add**: Chains `+ [Result]` straight into your ongoing formula.
    - **Tap 🔁 Reload**: Reloads the full equation to inspect or edit.
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

# Header Banner with HARGUNS CALCULATOR 🤍 (plenty of clearance, fully visible)
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("<h1 style='color: #0284c7; font-size: 2.5rem; font-weight: 800; margin-top: 0; margin-bottom: 2px;'>HARGUNS CALCULATOR 🤍</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #0369a1; font-size: 1.05rem; font-weight: 600; margin-top: 0;'>Pastel Ocean • Flying Seagulls • High-Contrast Screen • Infinite History Tape</p>", unsafe_allow_html=True)
with header_col2:
    mode = st.radio("Input Mode", ["Keypad", "Formula Bar"], horizontal=True, label_visibility="collapsed")

# Two-Column Layout: Left = Calculator, Right = Infinite Running History Tape
col_calc, col_tape = st.columns([7, 5], gap="large")

with col_calc:
    # Illuminated High-Contrast Screen
    mem_tag = f"MEM: {CalculatorEngine.format_result(calc.memory)}" if calc.memory != 0 else ""
    preview_tag = f"Ans: {calc.last_result}" if calc.last_result is not None else ""

    st.markdown(f"""
    <div class="calc-screen">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span class="screen-mem-tag">{mem_tag}</span>
            <span class="screen-mem-tag" style="color: #bae6fd;">{preview_tag}</span>
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
        st.markdown(f"<h4 style='color: #0284c7; font-weight: 800; margin-bottom: 0;'>📜 Running Tape ({history_count})</h4>", unsafe_allow_html=True)
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
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
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
                <div style="font-size: 2.6rem; margin-bottom: 8px;">🕊️ 🌊</div>
                <div style="font-weight: 700; font-size: 1.15rem; color: #0284c7;">Tape is Ready</div>
                <div style="font-size: 0.9rem; margin-top: 4px;">Calculate on the left, and every past result will be recorded here to tap and reuse!</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #0369a1; font-size: 0.9rem; font-weight: 600;'>"
    "🤍 HARGUNS CALCULATOR • High-Contrast Illuminated Display • Pastel Ocean & Flying Seagulls"
    "</div>",
    unsafe_allow_html=True
)
