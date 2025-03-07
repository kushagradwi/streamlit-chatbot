import streamlit as st

pg = st.navigation([st.Page("login.py"),st.Page("app.py")])
pg.run()