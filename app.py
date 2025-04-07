import streamlit as st
import base64
import time
import json
from PIL import Image
import streamlit.components.v1 as components
import requests
from api_helper import get_api_call_with_cookie, post_api_call_with_cookie
import os
from dotenv import load_dotenv
from sidebar import renderSidebar
from Azure_SSO import azure_sso_handler

load_dotenv()

BASE_URL=os.getenv("BASE_URL")
DISCLAIMER_ENDPOINT=os.getenv("DISCLAIMER_ENDPOINT")
NEW_CHAT_ENDPOINT=os.getenv("NEW_CHAT_ENDPOINT")
RECENT_CHATS_ENDPOINT=os.getenv("RECENT_CHATS_ENDPOINT")
FETCH_CHAT_ENDPOINT=os.getenv("FETCH_CHAT_ENDPOINT")
CHAT_RESPONSE_ENDPOINT=os.getenv("CHAT_RESPONSE_ENDPOINT")
RECORD_FEEDBACK_ENDPOINT=os.getenv("RECORD_FEEDBACK_ENDPOINT")
API_KEY=os.getenv("API_KEY")




def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

menu_icon_base64 = get_base64_image("assets/sidenav/menu_icon.png")
compass_icon_base64 = get_base64_image("assets/sidenav/compas_icon.png")

def newChat():
    st.session_state.messages = []  # Clear chat history
    st.session_state.suggestions = []
    st.session_state.logged_in = True
    #call new chat API
    url = f"{BASE_URL}{NEW_CHAT_ENDPOINT}"
    response = post_api_call_with_cookie(url)
    print("Response :",response)
    if isinstance(response, dict) and "user_chat_id" in response:
        st.session_state.CHAT_ID = response.get("user_chat_id", "")
        #st.session_state.USER_ID = response.get("user_id", "")  # Store user_id
    else:
        st.error("Failed to create new chat.")
    st.rerun()

def continueChat(text):
    if not text:
        return
    
    st.session_state.current_message = text
    st.switch_page("old_chat.py")


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
azure_sso_handler()
st.write("user details:",st.experimental_user)
with open("static/css/sidebar.css") as css_file:
    st.html(f"<style>{css_file.read()}</style>")

with open("static/css/app.css") as app_css_file:
    st.html(f"<style>{app_css_file.read()}</style>")

st.markdown(
"""
    <div style="padding-left: 10px; padding-right: 10px; padding-top: 17px; padding-bottom: 17px; background: rgba(134, 134, 134, 0.10); border-radius: 12px; flex-direction: column; justify-content: center; align-items: flex-start; gap: 2px; display: inline-flex">
        <div style="justify-content: flex-start; align-items: center; gap: 8px; display: inline-flex">
            <div data-svg-wrapper>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="19" viewBox="0 0 20 19" fill="none">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.058 9.16257C12.8892 9.16257 12.7415 9.01875 12.7415 8.83067C12.7415 6.81715 11.1697 5.17978 9.22857 5.17978C8.80659 5.17978 8.80659 4.51598 9.22857 4.51598C11.1697 4.51598 12.7415 2.86755 12.7415 0.831899C12.7415 0.389367 13.3745 0.389367 13.3745 0.831899C13.3745 2.86755 14.9569 4.51598 16.898 4.51598C17.3095 4.51598 17.3095 5.17978 16.898 5.17978C14.9253 5.17978 13.3745 6.78396 13.3745 8.83067C13.3745 9.01875 13.2374 9.16257 13.058 9.16257ZM7.04484 18.1238C6.87604 18.1238 6.72835 17.98 6.72835 17.7919C6.72835 14.6389 4.30198 12.0833 1.31648 12.0833C0.894506 12.0833 0.894506 11.4195 1.31648 11.4195C4.30198 11.4195 6.72835 8.86386 6.72835 5.73294C6.72835 5.30148 7.36132 5.30148 7.36132 5.73294C7.36132 8.86386 9.79824 11.4195 12.7837 11.4195C13.1952 11.4195 13.1952 12.0833 12.7837 12.0833C9.79824 12.0833 7.36132 14.6389 7.36132 17.7919C7.36132 17.98 7.22418 18.1238 7.04484 18.1238ZM3.24703 11.7514C5.02989 12.382 6.44352 13.8755 7.04484 15.7563C7.6567 13.8755 9.07033 12.382 10.8532 11.7514C9.05978 11.1208 7.64615 9.63829 7.04484 7.75753C6.44352 9.63829 5.02989 11.1208 3.24703 11.7514ZM15.5582 18.5C15.3789 18.5 15.2418 18.3451 15.2418 18.1681C15.2418 16.5418 13.9653 15.2142 12.3934 15.2142C11.9714 15.2142 11.9714 14.5504 12.3934 14.5504C13.9653 14.5504 15.2418 13.2117 15.2418 11.5633C15.2418 11.1208 15.8747 11.1208 15.8747 11.5633C15.8747 13.2117 17.1407 14.5504 18.6914 14.5504C19.1029 14.5504 19.1029 15.2142 18.6914 15.2142C17.1407 15.2142 15.8747 16.5418 15.8747 18.1681C15.8747 18.3451 15.7376 18.5 15.5582 18.5ZM13.8492 14.8823C14.5982 15.2474 15.2101 15.878 15.5582 16.6524C15.8958 15.8669 16.4971 15.2363 17.2462 14.8823C16.5077 14.5172 15.8958 13.8755 15.5582 13.09C15.2101 13.8866 14.6088 14.5172 13.8492 14.8823ZM10.8215 4.84788C11.8237 5.29041 12.636 6.13122 13.058 7.17117C13.4695 6.12016 14.2818 5.27935 15.284 4.84788C14.2818 4.40535 13.4695 3.55347 13.058 2.50246C12.636 3.56454 11.8343 4.40535 10.8215 4.84788Z" fill="#212121" stroke="#212121" stroke-width="0.25"/>
            </svg>
            </div>
            <div style="flex-direction: column; justify-content: center; align-items: flex-start; display: inline-flex">
                <div style="color: rgb(33, 33, 33);font-size: 12px;font-family: Poppins;font-weight: 400;overflow-wrap: break-word;line-height: 18px;">Llama 3.3</div>
                <div style="
                    font-size: 10px;
                    line-height: 10px;
                "><span style="color: #868686; font-size: 10px; font-family: Poppins; font-weight: 400; word-wrap: break-word">Trained on last 12 months of data till </span><span style="color: #868686; font-size: 10px; font-family: Poppins; font-weight: 700; word-wrap: break-word">Feb 2025</span></div>
            </div>
        </div>
    </div>
""",
unsafe_allow_html=True,
)
if "redirect" in st.session_state and st.session_state.redirect:
    st.session_state.redirect = False
    st.markdown("<script>window.location.href = 'http://localhost:8501/'</script>", unsafe_allow_html=True)
    time.sleep(1)
    st.stop()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "CHAT_ID" not in st.session_state:
    st.session_state.CHAT_ID = ""    

renderSidebar('app')

# Display welcome message if no chat history exists
if not st.session_state.messages:
    st.markdown("<h1>Hi! How can I assist you today...</h1>", unsafe_allow_html=True)

if not st.session_state.messages:
    with st.form("my_form"):
        with st.container(key="vy-chat-container"):
            text = st.text_input(label="", placeholder="You can ask me more...", key="vy-chat-input-up")
            if st.form_submit_button(label="", icon=":material/send:"):
                continueChat(text)
            st.markdown("""<div class="vy-chat-info">VAI can make mistakes. Check important information.</div>""",unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        """
        <div class="info-box-wrap">
        <div class="info-box">
            <div>
                <div style="text-align: center; color: #5E6670; font-size: 14px; font-family: Poppins; font-weight: 600;">
                    VyStar AI (VAI) – Payment Review Insights
                </div>
                <div style="text-align: center; color: #5E6670; font-size: 12px; font-family: Poppins; font-weight: 400;">
                    VAI focuses exclusively on payment-related reviews, providing insights into credit cards, debit cards, ACH, Zelle, and ATM services. It helps track customer sentiment, and highlight key feedback, enabling you to improve VyStar’s payment products and enhance user experience.
                </div>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )
