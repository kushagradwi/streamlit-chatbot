import os
import requests
import streamlit as st
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI") # Should match the app URL

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
AUTH_ENDPOINT = f"{AUTHORITY}/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = f"{AUTHORITY}/oauth2/v2.0/token"
SCOPE = ["User.Read"]

def build_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": " ".join(SCOPE),
    }
    return f"{AUTH_ENDPOINT}?{urlencode(params)}"

def get_token_from_code(auth_code):
    data = {
        "client_id": CLIENT_ID,
        "scope": " ".join(SCOPE),
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_ENDPOINT, data=data)
    return response.json()

def azure_sso_handler():
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"]
        token_data = get_token_from_code(auth_code)

        if "access_token" in token_data:
            st.session_state["authenticated"] = True
            st.session_state["user"] = "Microsoft User"
            st.rerun()
        else:
            st.error("Authentication failed.")
    else:
        auth_url = build_auth_url()
        st.markdown(f"<meta http-equiv='refresh' content='0; URL={auth_url}'>", unsafe_allow_html=True)
