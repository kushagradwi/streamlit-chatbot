import streamlit as st

pg = st.navigation([st.Page("login.py"),st.Page("app.py"),st.Page("old_chat.py"),st.Page("dashboard.py")])
pg.run()