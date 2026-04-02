import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

st.set_page_config(page_title="AI Dashboard", layout="wide")

# =========================
# 💜 CSS
# =========================
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
}

/* LOGIN CARD */
.login-container {
    display:flex;
    justify-content:center;
    align-items:center;
    height:80vh;
}
.login-card {
    background: rgba(255,255,255,0.7);
    padding:30px;
    border-radius:20px;
    width:350px;
    text-align:center;
}

/* TOOL CARDS */
.tool-card {
    background:white;
    padding:20px;
    border-radius:18px;
    border:1px solid #e9d5ff;
    text-align:center;
    transition:0.3s;
    height:130px;
}
.tool-card:hover {
    transform: translateY(-5px);
    box-shadow:0 10px 25px rgba(139,92,246,0.2);
}

/* HIDE BUTTON */
.stButton>button {
    width:100%;
    height:130px;
    opacity:0;
    position:absolute;
}

/* TITLE */
.title {
    text-align:center;
    font-size:32px;
    font-weight:bold;
    color:#5b21b6;
}
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    st.session_state.users = {"admin":"1234"}

if "mode" not in st.session_state:
    st.session_state.mode = "login"

if "tool" not in st.session_state:
    st.session_state.tool = None

# =========================
# LOGIN / SIGNUP
# =========================
def auth():
    st.markdown('<div class="login-container"><div class="login-card">', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.mode="login"
    with col2:
        if st.button("Signup"):
            st.session_state.mode="signup"

    st.markdown(f"### {'🔐 Login' if st.session_state.mode=='login' else '📝 Signup'}")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.session_state.mode=="login":
        if st.button("Enter"):
            if u in st.session_state.users and st.session_state.users[u]==p:
                st.session_state.logged_in=True
                st.session_state.user=u
                st.rerun()
            else:
                st.error("Invalid login")

    else:
        if st.button("Create"):
            if u in st.session_state.users:
                st.error("User exists")
            else:
                st.session_state.users[u]=p
                st.success("Created! Login now")
                st.session_state.mode="login"

    st.markdown("</div></div>", unsafe_allow_html=True)

# =========================
# DASHBOARD WITH 6 TOOLS
# =========================
def dashboard():

    st.markdown('<div class="title">✨ AI Image Dashboard</div>', unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()

    st.markdown("### 🧰 Tools")

    col1,col2,col3 = st.columns(3)

    with col1:
        if st.button("", key="bg"):
            st.session_state.tool="bg"
        st.markdown('<div class="tool-card">🎨<br>Background Change</div>', unsafe_allow_html=True)

    with col2:
        if st.button("", key="enh"):
            st.session_state.tool="enh"
        st.markdown('<div class="tool-card">✨<br>Enhance Image</div>', unsafe_allow_html=True)

    with col3:
        if st.button("", key="erase"):
            st.session_state.tool="erase"
        st.markdown('<div class="tool-card">🧽<br>Erase Tool</div>', unsafe_allow_html=True)

    col4,col5,col6 = st.columns(3)

    with col4:
        if st.button("", key="blur"):
            st.session_state.tool="blur"
        st.markdown('<div class="tool-card">🌫<br>Blur Tool</div>', unsafe_allow_html=True)

    with col5:
        if st.button("", key="remove"):
            st.session_state.tool="remove"
        st.markdown('<div class="tool-card">❌<br>Remove Object</div>', unsafe_allow_html=True)

    with col6:
        if st.button("", key="bgtool"):
            st.session_state.tool="bgtool"
        st.markdown('<div class="tool-card">🖼<br>Background Tool</div>', unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # TOOL LOGIC
    # =========================
    uploaded_file = st.file_uploader("Upload Image")

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        colA,colB = st.columns(2)

        with colA:
            st.image(image)

        if st.session_state.tool=="bg":
            color_hex = st.color_picker("Color", "#8b5cf6")
            color = tuple(int(color_hex[i:i+2],16) for i in (1,3,5))

            if st.button("Apply"):
                arr=np.array(image)
                gray=np.mean(arr,axis=2)
                mask=gray>200
                arr[mask]=color
                result=Image.fromarray(arr)

                with colB:
                    st.image(result)

        elif st.session_state.tool=="enh":
            if st.button("Enhance"):
                result=image.filter(ImageFilter.SHARPEN)
                with colB:
                    st.image(result)

        elif st.session_state.tool=="erase":
            st.link_button("Open Tool","https://skyhostpro32-dev.github.io/erase-tool/")

        elif st.session_state.tool=="blur":
            st.link_button("Open Tool","https://skyhostpro32-dev.github.io/index./")

        elif st.session_state.tool=="remove":
            st.link_button("Open Tool","https://l3c2ddsnh8gkka5rnezbak.streamlit.app/")

        elif st.session_state.tool=="bgtool":
            st.link_button("Open Tool","https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/")

# =========================
# ROUTER
# =========================
if not st.session_state.logged_in:
    auth()
else:
    dashboard()
