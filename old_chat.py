import streamlit as st
import base64
import time
import json
import streamlit.components.v1 as components
from api_helper import get_api_call_with_cookie, post_api_call_with_cookie
import os
from dotenv import load_dotenv

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


def logout():
    st.session_state.messages = []  # Clear chat history on logout
    st.session_state.suggestions = []
    st.session_state.logged_in = False
    st.session_state.redirect = True
    st.rerun()

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

# Function to send feedback using post_api_call_with_cookie
def sendFeedback(helpful):
    url = f"{BASE_URL}{RECORD_FEEDBACK_ENDPOINT}"
    payload = json.dumps({
        "user_id": "user-1",
        "user_chat_id": "user-1_chat2",
        "query_id": "query_1234",
        "response_id": "response_1234",
        "helpful": helpful
    })
    headers = {
        "accept": "application/json",
        "api-key": "884c0b4e-ecc2-44a7-bbbd-39835aec2518",
        "Content-Type": "application/json"
    }

    # Making the API call using the helper function
    response = post_api_call_with_cookie(url, headers=headers, payload=payload)
    print("Feedback :",response)
    # Handling the response
    

def apichat(text):
    try:
        url = BASE_URL+ CHAT_RESPONSE_ENDPOINT  # Use the endpoint from .env
        user_chat_id = "user-1-chat1"
        user_id = "user-1"  # Retrieve user_id

        if not user_id:
            st.error("User ID is missing.")
            return None
        
        headers = {
            "accept": "application/json",
            "api-key": "884c0b4e-ecc2-44a7-bbbd-39835aec2518",
            "Content-Type": "application/json"
        }
        
        def requestMsg(msg):
            return {
                "role": msg["role"], "content": msg["content"]
            } 
        print(st.session_state.messages)

        message_temp=list(map(requestMsg ,st.session_state.messages))
        message_temp.pop()
        payload = {
            "user_id": user_id,
            "user_chat_id": user_chat_id,
            "messages": message_temp
            #"messages": [{"role":"user","content":"what are people talking about the vystar credit card"}]
        }
        
        print("Payload :",payload)

        # time.sleep(5)
        response = post_api_call_with_cookie(url, headers=headers, payload=json.dumps(payload))
        
        # response = {'user_chat_id': 'user-1-chat1', 'query_id': 'query_34b74212-6306-4df2-ad90-cec8b5e9755d', 'messages': [{'role': 'user', 'content': 'hi'}, {'role': 'assistant', 'content': "This is out of my context. I'm a reviews analyst capable of answering questions related to Vystar Credit Union's products and services. Please ask a relevant question."}, {'role': 'user', 'content': 'what are people taking about vystar credit card'}, {'role': 'assistant', 'content': "**Summary of Feedbacks**: The reviews about Vystar Credit Union's credit card services reflect a range of experiences, from positive interactions with customer service representatives to concerns about fees and credit building options. Overall, customers appreciate the helpfulness and knowledge of Vystar's staff, but some express frustration with certain policies and limitations. The general sentiment is mixed, with some customers highly satisfied and others disappointed.\n\n- **Customer Service Experience**:\n  - Many customers praise the excellent service and helpfulness of Vystar's staff, mentioning specific representatives by name.\n  - Representatives are described as knowledgeable, polite, and efficient in handling customer inquiries and issues.\n- **Fees & Charges**:\n  - Some customers express dissatisfaction with the fees associated with Vystar's credit cards, particularly the charge for replacing a compromised card.\n  - Concerns are raised about the fairness of charging customers for services related to fraud that is not their fault.\n- **Credit Building Options**:\n  - A few customers mention that Vystar has limited options for building credit, with one reviewer noting that there is essentially only one option for those without good credit, which is a secured credit card.\n- **Positive Sentiments**:\n  - Several customers appreciate the benefits and discounts associated with Vystar's checking accounts and credit cards.\n  - The overall experience with Vystar is praised by many for its efficiency, helpful staff, and the feeling of being well taken care of.\n- **Negative Sentiments**:\n  - Disappointment and frustration are expressed regarding certain policies, such as fees for replacement cards and limited credit building options.\n  - Some customers feel that Vystar's growth has led to a decrease in the quality of service and an increase in fees."}], 'response_id': 'response_34b74212-6306-4df2-ad90-cec8b5e9755d', 'response_txt': "**Summary of Feedbacks**: The reviews about Vystar Credit Union's credit card services reflect a range of experiences, from positive interactions with customer service representatives to concerns about fees and credit building options. Overall, customers appreciate the helpfulness and knowledge of Vystar's staff, but some express frustration with certain policies and limitations. The general sentiment is mixed, with some customers highly satisfied and others disappointed.\n\n- **Customer Service Experience**:\n  - Many customers praise the excellent service and helpfulness of Vystar's staff, mentioning specific representatives by name.\n  - Representatives are described as knowledgeable, polite, and efficient in handling customer inquiries and issues.\n- **Fees & Charges**:\n  - Some customers express dissatisfaction with the fees associated with Vystar's credit cards, particularly the charge for replacing a compromised card.\n  - Concerns are raised about the fairness of charging customers for services related to fraud that is not their fault.\n- **Credit Building Options**:\n  - A few customers mention that Vystar has limited options for building credit, with one reviewer noting that there is essentially only one option for those without good credit, which is a secured credit card.\n- **Positive Sentiments**:\n  - Several customers appreciate the benefits and discounts associated with Vystar's checking accounts and credit cards.\n  - The overall experience with Vystar is praised by many for its efficiency, helpful staff, and the feeling of being well taken care of.\n- **Negative Sentiments**:\n  - Disappointment and frustration are expressed regarding certain policies, such as fees for replacement cards and limited credit building options.\n  - Some customers feel that Vystar's growth has led to a decrease in the quality of service and an increase in fees.", 'cited_reviews': [{'review_id': '66216b4097d7de66a0529e6c', 'review_text': 'I went to Vystar to have my niece open an account and we received the best service you could possible get, she explained everything in detail and explained to my niece about building credit and having credit cards and how to not get yourself in debt, I’ve been with vystar for almost 2 years and never experienced a problem, everyone here is wonderful and thank you Brittany “BJ” Jarrell for you help and expertise, you deserve all praise !!!!', 'review_date_time': '4/18/2024 18:49', 'rating': 5, 'review_src': None}, {'review_id': '67a22291973da10836fe69e5', 'review_text': "VyStar is an incredible banking facility that truly cares about their customers. I worked with PAOLA OSORIO and she was extremely caring and understanding of our situation. Don't waste time with other banks...go to your local VyStar. :)", 'review_date_time': None, 'rating': 5, 'review_src': 'GOOGLE'}, {'review_id': '677eae8b4d510b114efa5be3', 'review_text': 'Vystar has great customer service as well as plenty of benefits for their checking account! Discounts come with anything that they sponsor.', 'review_date_time': '1/8/2025 16:57', 'rating': 5, 'review_src': 'GOOGLE'}, {'review_id': '6753df57f4786b30876fbf40', 'review_text': 'Starting to get disappointed in VyStar and considering even changing banks. VyStar used to be a really good bank but because they are becoming bigger they think they can take advantage of their customers. They are not bringing back their fees for anything and everything. Now if your own card gets compromised and forced to get a new card they want to charge you to get a new card.. so it’s like you’re getting double fraud. Can anyone explain to me the thought process of “hey, if someone steals a credit card number and attempts to take their money, let’s also take their money and charge them for something that’s not our clients fault as to why they need an new card” ….. don’t even get me started with their new credit card interests. But hey! Everyone is always about taking peoples money when it’s already hard on most Americans.', 'review_date_time': '12/7/2024 5:38', 'rating': None, 'review_src': 'GOOGLE'}, {'review_id': '660f691568f21c57991cbfb8', 'review_text': 'Morgan M. is AWESOME! Vystar is a great place to build your credit and get personal needs handled efficiently. I have been a loyal customer for over three years after leaving a bank I did business with for ten years. Customer service is top notch! Email/text/phone communication are a priority whether handling a loan, banking issue or personal inquiries. Go to Morgan M. with anything and she will point you in the right direction if she cannot handle it herself.', 'review_date_time': '4/5/2024 2:59', 'rating': 5, 'review_src': 'GOOGLE'}], 'query_suggestions': ['Query Suggestion 1', 'Query Suggestion 2', 'Query Suggestion 3']}

        print("Response :",response)

        if isinstance(response, str) and response.startswith("Error!"):
            st.error(response)
            return None
        
        return response  # Returns the chatbot's response JSON

    except Exception as e:
        st.error(f"Request failed: {e}")
        return None
    
def continueChat(text):
    if not text:
        return
    
    user_id = "user-1"  # Retrieve user_id
    if not user_id:
        st.error("User ID is missing.")
        return

    # Display the user's message in the chat interface
    st.session_state.messages.append({"role": "user", "content": text, "id": len(st.session_state.messages)})

    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Analyzing...",  
        "id": len(st.session_state.messages)
    })

    # update chat UI 
    with st.container(key="vy-chat-msg-container-temp"):
        with st.chat_message(name="user",avatar="static/landing/user-profile.png"):
            st.markdown(text,unsafe_allow_html=True)
        with st.chat_message(name="assistant",avatar="assets/sidenav/compas_icon.png"):
            st.markdown('Analyzing...',unsafe_allow_html=True)
    
    # Get chatbot response
    res = apichat(text)
    
    # Error handling in case API response fails
    if (res is None) or ("response_txt" not in res.keys()) or (res["response_txt"] is None) :
        print("Error occured")
        st.session_state.messages[-1]={
            "role": "assistant", 
            "content": "Failed to get a response from the chatbot.",  
            "id": len(st.session_state.messages)
        }
        st.session_state.current_message = None
        st.rerun()   
        return

    # Add assistant response to chat history
    st.session_state.messages[-1]={
        "role": "assistant", 
        "content": res["response_txt"], 
        "source": res.get("cited_reviews", ""), 
        "id": len(st.session_state.messages)
    }
    
    # Update session state with suggestions if available
    st.session_state.suggestions = res.get("query_suggestions", [])
    st.session_state.current_message = None
    st.rerun()

def setCurrentMessage(text):
    st.session_state.current_message = text


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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
                "><span style="color: #868686; font-size: 10px; font-family: Poppins; font-weight: 400; word-wrap: break-word">Trained on last 12 months of data till </span><span style="color: #868686; font-size: 10px; font-family: Poppins; font-weight: 700; word-wrap: break-word">Dec 2024</span></div>
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
    st.switch_page("app.py")

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "CHAT_ID" not in st.session_state:
    st.session_state.CHAT_ID = ""    

# Sidebar with logout button
with st.sidebar:
    st.markdown("""<div class="welcome-wrap">
                <div class="welcome-wrap-text-upper">
                    <div class="welcome-wrap-text-bottom">Welcome to</div>
                    <div class="welcome-wrap-text-image">
                        <img style="width: 19px; height: 20px" src="app/static/landing/compas_icon.png" />
                        <div><span style="color: white; font-size: 16px; font-weight: 400; line-height: 24px; word-wrap: break-word">VyStar AI - </span><span style="color: white; font-size: 16px; font-weight: 700; line-height: 24px; word-wrap: break-word">VAI </span></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown(
    """
    <div class="vy-sidebar-menu"> 
        <div class="vy-sidebar-list"> 
            <a class="vy-sidebar-link active" href="/app" target="_self">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M7.99998 4.49973C7.72384 4.49973 7.49998 4.72357 7.49998 4.99969V7.49949H4.99999C4.72385 7.49949 4.49999 7.72333 4.49999 7.99945C4.49999 8.27557 4.72385 8.49941 4.99999 8.49941H7.49998V10.9992C7.49998 11.2753 7.72384 11.4992 7.99998 11.4992C8.27612 11.4992 8.49998 11.2753 8.49998 10.9992V8.49941H11C11.2761 8.49941 11.5 8.27557 11.5 7.99945C11.5 7.72333 11.2761 7.49949 11 7.49949H8.49998V4.99969C8.49998 4.72357 8.27612 4.49973 7.99998 4.49973ZM8.00002 1C4.13404 1 1.00004 4.13376 1.00004 7.99945C1.00004 9.18427 1.29484 10.3016 1.81539 11.2807L1.02951 14.044C0.868796 14.6091 1.39089 15.1312 1.95605 14.9705L4.7202 14.1845C5.69899 14.7045 6.81579 14.9989 8.00002 14.9989C11.866 14.9989 15 11.8651 15 7.99945C15 4.13376 11.866 1 8.00002 1ZM2.00004 7.99945C2.00004 4.686 4.68632 1.99992 8.00002 1.99992C11.3137 1.99992 14 4.686 14 7.99945C14 11.3129 11.3137 13.999 8.00002 13.999C6.91819 13.999 5.90465 13.7131 5.02919 13.2132C4.91245 13.1465 4.77378 13.1297 4.64447 13.1665L2.1141 13.886L2.83352 11.3563C2.87031 11.227 2.85343 11.0883 2.7867 10.9715C2.28622 10.0958 2.00004 9.0818 2.00004 7.99945Z" stroke="currentColor"/>
                </svg>
                <span class="vy-sidebar-link-label">New Chat</span>
            </a>
        </div>
        <div class="vy-sidebar-list"> 
            <a class="vy-sidebar-link" href="/app" target="_self">
                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="16" viewBox="0 0 15 16" fill="none">
                <path d="M5.33333 8H2.15556C1.75107 8 1.54883 8 1.39434 8.07872C1.25845 8.14796 1.14796 8.25845 1.07872 8.39434C1 8.54883 1 8.75107 1 9.15556V13.3444C1 13.7489 1 13.9512 1.07872 14.1057C1.14796 14.2416 1.25845 14.352 1.39434 14.4213C1.54883 14.5 1.75107 14.5 2.15556 14.5H5.33333M5.33333 14.5H9.66667M5.33333 14.5L5.33333 5.54444C5.33333 5.13996 5.33333 4.93772 5.41205 4.78323C5.48129 4.64733 5.59178 4.53685 5.72767 4.46761C5.88217 4.38889 6.08441 4.38889 6.48889 4.38889H8.51111C8.91559 4.38889 9.11783 4.38889 9.27233 4.46761C9.40822 4.53685 9.51871 4.64733 9.58795 4.78323C9.66667 4.93772 9.66667 5.13996 9.66667 5.54444V14.5M9.66667 14.5H12.8444C13.2489 14.5 13.4512 14.5 13.6057 14.4213C13.7416 14.352 13.852 14.2416 13.9213 14.1057C14 13.9512 14 13.7489 14 13.3444V2.65556C14 2.25107 14 2.04883 13.9213 1.89434C13.852 1.75845 13.7416 1.64796 13.6057 1.57872C13.4512 1.5 13.2489 1.5 12.8444 1.5H10.8222C10.4177 1.5 10.2155 1.5 10.061 1.57872C9.92511 1.64796 9.81463 1.75845 9.74538 1.89434C9.66667 2.04883 9.66667 2.25107 9.66667 2.65556V5.11111" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="vy-sidebar-link-label">Analytics</span>
            </a>
        </div>
    </div>
    """
    ,
    unsafe_allow_html=True
    )
    with st.container(key="vy-logout-container"):
        st.markdown("""<div class="vy-profile-container">
            <img class="vy-profile-image" src="app/static/landing/user-profile.png" alt="user">
            <div class="vy-profile-info">
                <div class="vy-profile-name">
                    Stephen Johnson
                </div>
                <div class="vy-profile-email">
                    johnson.s@vystarcu.org
                </div>
            </div>
            <div class="vy-profile-icon"><svg xmlns="http://www.w3.org/2000/svg" width="4" height="14" viewBox="0 0 4 14"
                    fill="none">
                    <path d="M1 7H3M1 1H3M1 13H3" stroke="white" stroke-width="2" stroke-linecap="round"
                        stroke-linejoin="round" />
                </svg></div>
        </div>"""
                    ,
        unsafe_allow_html=True
        ) 
        with st.popover(label="", use_container_width=True):
            logoutButton=st.button(label="Logout", icon=":material/logout:")

    if logoutButton:
        logout()

    st.markdown("""<div class="vy-sidenav-footer">
            <div class="vy-sidenav-footer-text" >Powered by</div>
            <div class="vy-sidenav-footer-logo">
                <img style="width: 68px; height: 22px" src="app/static/landing/Vystar-logo.png" />
            </div>
        </div>""",
        unsafe_allow_html=True)

# Display chat messages from history on app rerun
with st.container(key="vy-chat-msg-container"):
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(name=message["role"],avatar="static/landing/user-profile.png"):
                st.markdown(message["content"],unsafe_allow_html=True)
        else:
            with st.chat_message(name=message["role"],avatar="assets/sidenav/compas_icon.png"):
                st.markdown(message["content"],unsafe_allow_html=True)
            if "source" in message.keys() and message["source"]:
                with st.expander("source",icon=":material/anchor:"):
                    st.html("""<div class="vy-source-main-header">Source Citations</div>""")
                    for msg in message["source"]:
                        r_source = msg["review_src"] if msg["review_src"] else 'Source'
                        r_rating = f'Rating {msg["rating"]}' if msg["rating"] else ''
                        r_datetime = f'Review Date  {msg["review_date_time"]}' if msg["review_date_time"] else ''
                        r_test = msg["review_text"] if msg["review_text"] else ''
                        st.markdown(f"""<div class="vy-source-citation">
                                        <div class="vy-source-citation-header-container">
                                            <div class="vy-source-citation-header">
                                                {r_source}
                                            </div>
                                            <div class="vy-source-citation-rating">{r_rating}</div>
                                            <div class="vy-source-citation-date">{r_datetime}</div>
                                        </div>
                                        <div class="vy-source-citation-info">
                                            {r_test}
                                        </div>
                                    </div>""",unsafe_allow_html=True)
            sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
            if "source" in message.keys() and message["source"]:
                with st.container(key=f"vy-chat-msg-container-thumbs-{message['id']}"):
                    selected = st.feedback("thumbs",key=f"{message['id']}-thumbs")
                    if selected is not None:
                        if selected == "thumbsUp":
                            sendFeedback(True)  # Call sendFeedback with True for thumbs-up
                        else:  # This covers the case where selected == "thumbsDown"
                            sendFeedback(False)  # Call sendFeedback with False for thumbs-down

    # if st.session_state.suggestions:
    #     with st.container(key="vy-suggestion-state"):
    #         st.html('<div class="vy-suggestion-container">Here are some suggestion to help you know more!</div>')
    #         with st.container(key="vy-suggestion-state-button-group"):
    #             for sug in st.session_state.suggestions:
    #                 if st.button(label=sug,key=f"{sug}"):
    #                     continueChat(sug)


if prompt := st.chat_input("You can ask me more..."):
    setCurrentMessage(prompt)
    st.rerun()

if st.session_state.current_message:
    continueChat(st.session_state.current_message)