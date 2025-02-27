import streamlit as st
import base64
import time
from PIL import Image

def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

background_base64 = get_base64_image("assets/landing/background.png")

def logout():
    st.session_state.messages = []  # Clear chat history on logout
    st.session_state.logged_in = False
    st.session_state.redirect = True
    st.session_state.show_info_box = True  # Reset info box visibility on logout
    st.rerun()

def newChat():
    st.session_state.messages = []  # Clear chat history
    st.session_state.logged_in = True
    st.session_state.show_info_box = True  # Reset info box visibility for new chat
    st.rerun()

def run_app():
    st.markdown(
        f"""
        <style>
            body, html, .stApp {{
                font-family: 'Poppins', sans-serif;
                background: url(data:image/png;base64,{background_base64}) no-repeat center center fixed;
                background-size: cover;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                color: white;
            }}
            .stAppHeader {{
                display: none;
            }}
            footer {{
                visibility: hidden;
            }}
            /* Gradient Sidebar */
            section[data-testid="stSidebar"] {{
                min-width: 70px !important;
                max-width: 250px !important;
                background: linear-gradient(174.59deg, #003684 0%, #0060D6 100%) !important;
                overflow: hidden;
                transition: max-width 0.3s ease-in-out;
            }}
            section[data-testid="stSidebar"]:hover {{
                max-width: 250px !important;
            }}
            /* Hide Sidebar Collapse Button */
            [data-testid="stSidebarNav"] {{
                display: none !important;
            }}
            h1 {{
                color: #002C6C !important;
                text-align: center;
            }}
            .stChatInputContainer textarea {{
                height: 150px !important;
            }}
            .stChatMessage {{
                background: none !important;
            }}
            div[data-testid="stBottomBlockContainer"] {{
                display: none !important;
            }}
            .centered-input-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }}
            .centered-input {{
                width: 450px !important;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}
            /* Info Box */
            .info-box {{
                width: 697px;
                height: 54px;
                border-radius: 7px;
                background-color: rgba(255, 255, 255, 0.5);
                padding: 10px;
                text-align: center;
                color: black;
                margin: 15px auto;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                line-height: 1.2;
                font-weight: 500;
            }}
        </style>
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

    if "show_info_box" not in st.session_state:
        st.session_state.show_info_box = True  # Show info box by default
    
    # Sidebar with logout button
    with st.sidebar:
        st.header("Vystar")
        
        if st.button("New Chat", key="newChat_button"):
            newChat()
        st.image("https://via.placeholder.com/100", width=100)  # Replace with actual profile image URL
        st.write("**Username:** John Doe")
        st.write("**Email:** johndoe@example.com")
        if st.button("Logout", key="logout_button"):
            logout()
    
    # Display welcome message if no chat history exists
    if not st.session_state.messages:
        st.markdown("<h1>Hi! How can I assist you today?</h1>", unsafe_allow_html=True)
    
    # Centered input box for user input
    st.markdown('<div class="centered-input-container">', unsafe_allow_html=True)
    prompt = st.text_input("", placeholder="You can ask me anything", label_visibility="collapsed", key="chat_input")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show the info box only if it's enabled in session state
    if st.session_state.show_info_box:
        st.markdown(
            '<div class="info-box">VAI provides insights into credit cards, debit cards, ACH, Zelle, and ATM services. It tracks sentiment and highlights feedback to improve VyStar\'s payment products.</div>',
            unsafe_allow_html=True
        )
    
    if prompt:
        # Hide the info box after first input
        st.session_state.show_info_box = False  

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Echo Bot repeats the input
        response = f"🔁 {prompt}"  # Simple echo response

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
            with st.expander("Source Explanation"):
                st.write(f"Explanation for: {response}")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear input box by resetting key
        del st.session_state["chat_input"]
        st.rerun()

if __name__ == "__main__":
    run_app()
