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

st.set_page_config(page_title="Review Insights ChatBOT - Login", page_icon="🤖", layout="centered")

logo_base64 = get_base64_image("static/login/microsoft.png")
background_base64 = get_base64_image("static/login/Background.png")
vystar_logo_base64 = get_base64_image("static/login/Vystar-logo.png")

poppins_light_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Light.ttf")
poppins_regular_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Regular.ttf")
poppins_medium_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Medium.ttf")
poppins_semibold_base64 = get_base64_font("assets/fonts/Poppins/Poppins-SemiBold.ttf")
poppins_bold_base64 = get_base64_font("assets/fonts/Poppins/Poppins-Bold.ttf")
poppins_extralight_base64 = get_base64_font("assets/fonts/Poppins/Poppins-ExtraLight.ttf")

st.markdown(
    f"""
    <style>
        @font-face {{
            font-family: 'Poppins';
            font-style: normal;
            font-weight: 300;
            src: url(data:font/ttf;base64,{poppins_light_base64}) format('truetype');
        }}
        @font-face {{
            font-family: 'Poppins';
            font-style: normal;
            font-weight: 200;
            src: url(data:font/ttf;base64,{poppins_extralight_base64}) format('truetype');
        }}

        @font-face {{
            font-family: 'Poppins';
            font-style: normal;
            font-weight: 400;
            src: url(data:font/ttf;base64,{poppins_regular_base64}) format('truetype');
        }}
        @font-face {{
            font-family: 'Poppins';
            font-style: normal;
            font-weight: 500;
            src: url(data:font/ttf;base64,{poppins_medium_base64}) format('truetype');
        }}
        @font-face {{
            font-family: 'Poppins';
            font-style: normal;
            font-weight: 600;
            src: url(data:font/ttf;base64,{poppins_semibold_base64}) format('truetype');
        }}
        @font-face {{
            font-family: 'Poppins';
            font-style: normal;
            font-weight: 700;
            src: url(data:font/ttf;base64,{poppins_bold_base64}) format('truetype');
        }}

        body, html, .stApp {{
            font-family: 'Poppins', sans-serif;
            background: url(data:image/png;base64,{background_base64}) no-repeat center center fixed;
            background-size:cover;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            color: white;
        }}

        .login-title-container {{
            position: fixed;
            left: 181px;
            bottom: 411px;
        }}

        .login-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 300;
            font-size: 36px;
            line-height: 54px;
            color: white;
            margin-bottom: 8px;
            text-align: center;
        }}

        .login-subtitle-container {{
            position: fixed;
            left: 182px;
            bottom: 351px;
        }}

        .login-subtitle {{
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            font-weight: 200;
            line-height: 24px;
            color: white;
        }}
        .footer{{
        display: flex;
        align-items: center;
        justify-content: center;
        }}
        .footer-text{{
            // © 2025 Vystar, Incorporated and its Affiliates. All Rights Reserved
            color: white;
            font-size: 10px;
            font-family: Poppins;
            font-weight: 400;
            word-wrap: break-word
        }}
        div[data-testid="stButton"] {{
            position: fixed;
            left: 168px;
            bottom: 280px;
        }}

        div[data-testid="stButton"] > button {{
            background-color: #006EF5 !important;
            color: white;
            font-size: 16px;
            font-weight: 600;
            border-radius: 5px;
            border: none;
            padding: 12px;
            width: 300px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .vystar-logo-container {{
            position: fixed;
            left: 243px;
            bottom: 553px;
        }}

        .vystar-logo-container img {{
            width: 150px; /* Adjust size as needed */
        }}

        .footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100vw;
            height: 62px;
            background: #006EF5;
        }}

        header {{visibility: hidden;}}
    </style>
    <div class="vystar-logo-container">
        <img src="data:image/png;base64,{vystar_logo_base64}" alt="VyStar Logo">
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
        #azure_sso_handler()

    st.markdown('<div class="footer"><div class= "footer-text" style="width: 381.65px; text-align: center; color: white; font-size: 10px; font-family: Poppins; font-weight: 400; word-wrap: break-word">© 2025 Vystar, Incorporated and its Affiliates. All Rights Reserved</div></div>', unsafe_allow_html=True)

else:
    st.switch_page("app.py")
