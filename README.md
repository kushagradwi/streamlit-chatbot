
import streamlit as st

# Hide the sidebar using CSS
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.write("Sidebar is disabled!")
