import streamlit as st
import time

def logout():
    st.session_state.messages = []  # Clear chat history on logout
    st.session_state.logged_in = False
    st.session_state.redirect = True
    st.rerun()

def newChat():
    st.session_state.messages = []  # Clear chat history
    st.session_state.logged_in = True
    st.rerun()

def inject_css():
    with open("assets/landing/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def run_app():
    inject_css()
    
    if "redirect" in st.session_state and st.session_state.redirect:
        st.session_state.redirect = False
        st.markdown("<script>window.location.href = 'http://localhost:8501/'</script>", unsafe_allow_html=True)
        time.sleep(1)
        st.stop()
    
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
    
    st.caption("VAI focuses exclusively on payment-related reviews, providing insights into credit cards, debit cards, ACH, Zelle, and ATM services. It helps track customer sentiment and highlight key feedback, enabling you to improve VyStar's payment products and enhance user experience.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if st.session_state.messages == []:
        st.markdown("<h1>Hi! How can I assist you today?</h1>", unsafe_allow_html=True)
    
    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                with st.expander("Source Explanation"):
                    st.write(f"Explanation for: {message['content']}")
    
    # Centered input box for user input
    st.markdown('<div class="centered-input-container">', unsafe_allow_html=True)
    prompt = st.text_input("", placeholder="You can ask me anything", label_visibility="collapsed", key="chat_input")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prompt:
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
