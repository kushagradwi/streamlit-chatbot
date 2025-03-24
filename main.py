import streamlit as st

pg = st.navigation([st.Page("login.py"),st.Page("app.py"),st.Page("old_chat.py")])
pg.run()