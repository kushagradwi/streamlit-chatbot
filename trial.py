import streamlit as st
import openai
import threading

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with st.secrets["openai_api_key"]

st.set_page_config(page_title="ChatGPT Chatbot 💬", layout="centered")
st.title("🤖 Chat with ChatGPT")
st.caption("Now with Cancel button + Spinner!")

# --- Session State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "generating" not in st.session_state:
    st.session_state.generating = False
if "stop_signal" not in st.session_state:
    st.session_state.stop_signal = False

# --- Chat History Display ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
user_input = st.chat_input("Type your message...", disabled=st.session_state.generating)

if user_input and not st.session_state.generating:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Set up placeholders for assistant response and spinner
    with st.chat_message("assistant"):
        placeholder = st.empty()
        spinner_placeholder = st.empty()
        stop_btn_placeholder = st.empty()

    def generate():
        st.session_state.generating = True
        st.session_state.stop_signal = False
        full_reply = ""

        try:
            with spinner_placeholder.spinner("Generating response..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # or "gpt-3.5-turbo"
                    messages=st.session_state.messages,
                    stream=True,
                )
                for chunk in response:
                    if st.session_state.stop_signal:
                        full_reply = "_❌ Generation stopped by user._"
                        break
                    content = chunk["choices"][0].get("delta", {}).get("content")
                    if content:
                        full_reply += content
                        placeholder.markdown(full_reply + "▌")
        except Exception as e:
            full_reply = f"⚠️ Error: {str(e)}"
        finally:
            spinner_placeholder.empty()
            placeholder.markdown(full_reply)
            if not st.session_state.stop_signal:
                st.session_state.messages.append({"role": "assistant", "content": full_reply})
            st.session_state.generating = False
            st.session_state.stop_signal = False
            stop_btn_placeholder.empty()

    # Start generation thread
    thread = threading.Thread(target=generate)
    thread.start()

    # Stop button (rendered after thread starts)
    with stop_btn_placeholder:
        if st.button("⛔ Stop Generating"):
            st.session_state.stop_signal = True
