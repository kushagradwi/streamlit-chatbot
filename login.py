from PIL import Image
import base64
import streamlit as st
from Azure_SSO import azure_sso_handler

def mock_microsoft_sso():
    st.session_state["authenticated"] = True
    st.session_state["user"] = "microsoft_user@example.com"
    st.rerun()

def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_base64_font(path):
    with open(path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode("utf-8")

st.set_page_config(page_title="Review Insights ChatBOT - Login", page_icon="🤖", layout="wide")

with open("static/css/login.css") as login_css_file:
    st.html(f"<style>{login_css_file.read()}</style>")
    
poppins_light_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Light.ttf")
poppins_regular_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Regular.ttf")
poppins_medium_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Medium.ttf")
poppins_semibold_base64 = get_base64_font("assets/fonts/Poppins/Poppins-SemiBold.ttf")
poppins_bold_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Bold.ttf")
poppins_extralight_base64 = get_base64_font("assets/fonts/Poppins/Poppins-ExtraLight.ttf")

st.markdown(
    f"""
    <div class="vystar-logo-container">
        <img src="app/static/login/Vystar-logo.png" alt="VyStar Logo">
    </div>
    """,
    unsafe_allow_html=True,
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="login-title-container"><div class="login-title">Review Insights<br>ChatBOT</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle-container"><div class="login-subtitle">Sign in using Microsoft credentials</div></div>', unsafe_allow_html=True)

    if st.button("SIGN IN", key="microsoft-sign-in"):
        mock_microsoft_sso()
        # azure_sso_handler()

    st.markdown('<div class="footer"><div class= "footer-text" style="width: 381.65px; text-align: center; color: white; font-size: 10px; font-family: Poppins; font-weight: 400; word-wrap: break-word">© 2025 Vystar, Incorporated and its Affiliates. All Rights Reserved</div></div>', unsafe_allow_html=True)

else:
    st.switch_page("app.py")
