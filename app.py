import streamlit as st
import sqlite3
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Dashboard", layout="wide")

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
conn.commit()

# =========================
# CSS
# =========================
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}

.block-container {padding-top: 0rem !important;}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
}

/* AUTH BOX */
.auth-box {
    max-width: 350px;
    margin: auto;
    margin-top: 60px;
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(139,92,246,0.2);
}

/* BUTTONS */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 8px;
    padding: 8px;
}

/* TOOL BUTTON (hidden click layer) */
.tool-btn button {
    height: 120px;
    opacity: 0;
    position: absolute;
}

/* TOOL CARD */
.tool-card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #e9d5ff;
    height: 120px;
    transition: 0.3s;
}
.tool-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(139,92,246,0.2);
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "mode" not in st.session_state:
    st.session_state.mode = "login"

if "tool" not in st.session_state:
    st.session_state.tool = None

# =========================
# AUTH PAGE
# =========================
def auth_page():
    st.markdown('<div class="auth-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.mode = "login"
    with col2:
        if st.button("Signup"):
            st.session_state.mode = "signup"

    st.markdown(f"### {'🔐 Login' if st.session_state.mode=='login' else '📝 Signup'}")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # LOGIN
    if st.session_state.mode == "login":
        if st.button("Login Now"):
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if c.fetchone():
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    else:
        if st.button("Create Account"):
            if username == "" or password == "":
                st.warning("Enter valid details")
            else:
                try:
                    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
                    conn.commit()
                    st.success("Account created! Please login")
                    st.session_state.mode = "login"
                except:
                    st.error("User already exists")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TOOL CARD FUNCTION
# =========================
def tool_card(name, icon, key):
    col = st.container()
    with col:
        st.markdown('<div class="tool-btn">', unsafe_allow_html=True)
        if st.button("", key=key):
            st.session_state.tool = key
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-card">{icon}<br>{name}</div>', unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.markdown("## ✨ AI Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("### 🧰 Tools")

    c1, c2, c3 = st.columns(3)
    with c1: tool_card("Background", "🎨", "bg")
    with c2: tool_card("Enhance", "✨", "enh")
    with c3: tool_card("Erase", "🧽", "erase")

    c4, c5, c6 = st.columns(3)
    with c4: tool_card("Blur", "🌫", "blur")
    with c5: tool_card("Remove", "❌", "remove")
    with c6: tool_card("BG Tool", "🖼", "bgtool")

    st.markdown("---")

    uploaded_file = st.file_uploader("Upload Image")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        colA, colB = st.columns(2)

        with colA:
            st.image(image)

        if st.session_state.tool == "bg":
            color_hex = st.color_picker("Color", "#8b5cf6")
            color = tuple(int(color_hex[i:i+2], 16) for i in (1,3,5))

            if st.button("Apply"):
                arr = np.array(image)
                mask = np.mean(arr, axis=2) > 200
                arr[mask] = color
                result = Image.fromarray(arr)
                with colB: st.image(result)

        elif st.session_state.tool == "enh":
            if st.button("Enhance"):
                result = image.filter(ImageFilter.SHARPEN)
                with colB: st.image(result)

        elif st.session_state.tool == "erase":
            st.link_button("Open Tool", "https://skyhostpro32-dev.github.io/erase-tool/")

        elif st.session_state.tool == "blur":
            st.link_button("Open Tool", "https://skyhostpro32-dev.github.io/index./")

        elif st.session_state.tool == "remove":
            st.link_button("Open Tool", "https://l3c2ddsnh8gkka5rnezbak.streamlit.app/")

        elif st.session_state.tool == "bgtool":
            st.link_button("Open Tool", "https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/")

# =========================
# ROUTER
# =========================
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
