import streamlit as st

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    div[data-testid="stVerticalBlock"] { gap: 0.3rem; }
    .calc-display {
        background: #16213e;
        border-radius: 12px;
        padding: 20px;
        text-align: right;
        margin-bottom: 15px;
        border: 1px solid #0f3460;
    }
    .expression { color: #888; font-size: 16px; min-height: 24px; }
    .result { color: #fff; font-size: 42px; font-weight: bold; }
    .stButton > button {
        width: 100%;
        height: 65px;
        font-size: 20px;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.1s;
    }
    .stButton > button:active { transform: scale(0.95); }
</style>
""", unsafe_allow_html=True)

# State initialization
for key, val in [("expression", ""), ("display", "0"), ("new_input", True)]:
    if key not in st.session_state:
        st.session_state[key] = val

def press(btn):
    e = st.session_state.expression
    d = st.session_state.display
    ni = st.session_state.new_input

    if btn == "C":
        st.session_state.expression = ""
        st.session_state.display = "0"
        st.session_state.new_input = True
    elif btn == "⌫":
        if d != "0" and not ni:
            st.session_state.display = d[:-1] if len(d) > 1 else "0"
    elif btn == "=":
        try:
            full = e + d
            result = eval(full.replace("×", "*").replace("÷", "/").replace("%", "/100"))
            result = int(result) if result == int(result) else round(result, 10)
            st.session_state.expression = ""
            st.session_state.display = str(result)
            st.session_state.new_input = True
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""
            st.session_state.new_input = True
    elif btn in ("+", "-", "×", "÷", "%"):
        st.session_state.expression = e + d + btn
        st.session_state.new_input = True
    elif btn == "+/-":
        if d != "0":
            st.session_state.display = str(-float(d)) if "-" not in d else d[1:]
    elif btn == ".":
        if ni:
            st.session_state.display = "0."
            st.session_state.new_input = False
        elif "." not in d:
            st.session_state.display = d + "."
    else:  # digits
        if ni or d == "0":
            st.session_state.display = btn
            st.session_state.new_input = False
        else:
            st.session_state.display = d + btn

# Display
st.markdown(f"""
<div class="calc-display">
    <div class="expression">{st.session_state.expression}</div>
    <div class="result">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# Buttons layout
buttons = [
    ["C", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["⌫", "0", ".", "="],
]

operator_style = "background-color: #e67e22; color: white;"
special_style = "background-color: #34495e; color: white;"
number_style = "background-color: #2c3e50; color: white;"
equals_style = "background-color: #27ae60; color: white;"
back_style = "background-color: #c0392b; color: white;"

for row in buttons:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        with cols[i]:
            if btn in ("÷", "×", "-", "+"):
                st.button(btn, key=f"btn_{btn}", on_click=press, args=(btn,),
                         help=btn, use_container_width=True)
            elif btn in ("C", "+/-", "%"):
                st.button(btn, key=f"btn_{btn}", on_click=press, args=(btn,),
                         use_container_width=True)
            elif btn == "=":
                st.button(btn, key="btn_eq", on_click=press, args=(btn,),
                         use_container_width=True)
            elif btn == "⌫":
                st.button(btn, key="btn_back", on_click=press, args=(btn,),
                         use_container_width=True)
            else:
                st.button(btn, key=f"btn_{btn}", on_click=press, args=(btn,),
                         use_container_width=True)
