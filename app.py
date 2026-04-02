
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
# DATABASE SETUP
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# =========================
# CSS (PRO CLEAN UI)
# =========================
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}

.block-container {
    padding-top: 0rem !important;
}

/* Background */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
}

/* Auth container */
.auth-box {
    max-width: 350px;
    margin: auto;
    margin-top: 80px;
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(139,92,246,0.2);
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 8px;
}

/* Tool cards */
.tool-card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #e9d5ff;
    transition: 0.3s;
    height: 120px;
}
.tool-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(139,92,246,0.2);
}

/* Hide button overlay */
.stButton>button {
    height: 120px;
    opacity: 0;
    position: absolute;
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
            user = c.fetchone()

            if user:
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
# DASHBOARD
# =========================
def dashboard():

    st.markdown("## ✨ AI Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("### 🧰 Tools")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("", key="bg"):
            st.session_state.tool = "bg"
        st.markdown('<div class="tool-card">🎨<br>Background</div>', unsafe_allow_html=True)

    with col2:
        if st.button("", key="enh"):
            st.session_state.tool = "enh"
        st.markdown('<div class="tool-card">✨<br>Enhance</div>', unsafe_allow_html=True)

    with col3:
        if st.button("", key="erase"):
            st.session_state.tool = "erase"
        st.markdown('<div class="tool-card">🧽<br>Erase</div>', unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("", key="blur"):
            st.session_state.tool = "blur"
        st.markdown('<div class="tool-card">🌫<br>Blur</div>', unsafe_allow_html=True)

    with col5:
        if st.button("", key="remove"):
            st.session_state.tool = "remove"
        st.markdown('<div class="tool-card">❌<br>Remove</div>', unsafe_allow_html=True)

    with col6:
        if st.button("", key="bgtool"):
            st.session_state.tool = "bgtool"
        st.markdown('<div class="tool-card">🖼<br>BG Tool</div>', unsafe_allow_html=True)

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

                with colB:
                    st.image(result)

        elif st.session_state.tool == "enh":
            if st.button("Enhance"):
                result = image.filter(ImageFilter.SHARPEN)
                with colB:
                    st.image(result)

        elif st.session_state.tool == "erase":
            st.link_button("Open", "https://skyhostpro32-dev.github.io/erase-tool/")

        elif st.session_state.tool == "blur":
            st.link_button("Open", "https://skyhostpro32-dev.github.io/index./")

        elif st.session_state.tool == "remove":
            st.link_button("Open", "https://l3c2ddsnh8gkka5rnezbak.streamlit.app/")

        elif st.session_state.tool == "bgtool":
            st.link_button("Open", "https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/")

# =========================
# ROUTER
# =========================
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
