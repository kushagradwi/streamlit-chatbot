import streamlit as st
import base64
import time
from PIL import Image

def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

background_base64 = get_base64_image("assets/landing/background.png")
menu_icon_base64 = get_base64_image("assets/sidenav/menu_icon.png")
compass_icon_base64 = get_base64_image("assets/sidenav/compas_icon.png")

def logout():
    st.session_state.messages = []  # Clear chat history on logout
    st.session_state.logged_in = False
    st.session_state.redirect = True
    st.rerun()

def newChat():
    st.session_state.messages = []  # Clear chat history
    st.session_state.logged_in = True
    st.rerun()



def run_app():
    st.set_page_config(layout="wide")
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');

            body, html, .stApp {{
                font-family: 'Poppins', sans-serif;
                background: url(data:image/png;base64,{background_base64}) no-repeat center center fixed;
                background-size: cover;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                color: white;
            }}
            #hi-how-can-i-assist-you-today{{
                margin-top: 60px;
            }}
            section[data-testid="stSidebar"]:hover .sidebar-container-bottom{{
                background: none;
            }} 
            [data-testid="stMainBlockContainer"] {{
                padding-top: 9px;
                padding-left: 25px; 
            }}
            .info-box-wrap {{
                margin-top: 123px;
                display: flex;
                justify-content: center;
            }}
            .styled-input-container-wrap{{
                display: flex;
                justify-content: center;
            }}
            .stAppHeader {{
                display: none;
            }}
            footer {{
                visibility: hidden;
            }}
            /* Sidebar Styling */
            section[data-testid="stSidebar"] {{
                min-width: 70px !important;
                max-width: 50px !important;
                background: linear-gradient(174.59deg, #003684 0%, #0060D6 100%) !important;
                overflow: hidden;
                transition: max-width 0.3s ease-in-out;
            }}
            section[data-testid="stSidebar"]:hover {{
                max-width: 250px !important;
            }}
            section[data-testid="stSidebar"]:hover .welcome-wrap {{
                position: absolute;
                top: -81px;
                left: 0px;
                display:block !important;
            }}
            section[data-testid="stSidebar"]:hover .new-chat{{
                display:inline !important;
            }} 
            .new-chat {{
                display: none; 
            }}
            .new-chat-button{{
                width: 100%; 
                height: 50px; 
                background: #F6FAFF; 
                border-left: 5px #006EF5 solid; 
                font-size: 16px; 
                font-weight: 600; 
                color: #006EF5;
            }}
            .welcome-wrap {{
                display:none !important;
            }}
            .stAppHeader {{
                display: none;
            }}
            footer {{
                visibility: hidden;
            }}
            /* Sidebar Styling */
            section[data-testid="stSidebar"] {{
                min-width: 240px !important;
                max-width: 240px !important;
                background: linear-gradient(174.59deg, #003684 0%, #0060D6 100%) !important;
                padding-top: 20px;
            }}
            [data-testid="stSidebarNav"] {{
                display: none !important;
            }}
            .stAppHeader {{ display: none; }}
            footer {{ visibility: hidden; }}
            /* Sidebar Styling */
            section[data-testid="stSidebar"] {{
                width: 56px !important;
                height: 100vh !important;
                padding-top: 16px;
                padding-bottom: 24px;
                background: linear-gradient(175deg, #003684 0%, #0060D6 100%);
                flex-direction: column;
                justify-content: flex-start;
                align-items: flex-start;
                gap: 13px;
                display: inline-flex;
                transition: width 0.3s ease-in-out;
            }}
            section[data-testid="stSidebar"]:hover {{
                width: 250px !important;
            }}
            .sidebar-container {{
                width: 240px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                align-items: center;
                flex-grow: 1;
            }}
            [data-testid="stSidebarHeader"]{{
                padding: calc(1.375rem) 1rem 1.5rem;
            }}
            .sidebar-title {{
                color: white;
                font-size: 16px;
                font-family: Poppins;
                font-weight: 700;
                line-height: 24px;
            }}
            [data-testid="stSidebarUserContent"] {{
                padding-left:  0px;
                padding-right: 0px;
                padding-bottom: 0px;
            }}
            [data-testid="stSidebarCollapseButton"] {{
                display: block;
            }}
            section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"]{{
                padding-left: 10px;
                padding-right: 10px;
            }}
            [data-testid="stBaseButton-headerNoPadding"] svg {{
                display: none;
            }}
            [data-testid="stBaseButton-headerNoPadding"] {{
                background: url("app/static/landing/menu_icon.png") no-repeat center center;
            }}
            .sidebar-custom-wrap {{
                display: flex;
                flex-direction: column;
                height: calc(100vh - 177px);
                
            }}
            .sidebar-content {{
                width: 100%;
                padding-left: 0px;
                padding-right: 0px;
                display: flex;
                flex-direction: column;
                gap: 14px;
            }}
            section[data-testid="stSidebar"]:hover .sidebar-content{{
                padding-left: 14px;
                padding-right: 14px;
            }}
            .sidebar-title {{
                color: white;
                font-size: 16px;
                font-family: Poppins;
                font-weight: 700;
                line-height: 24px;
            }}
            [data-testid="stSidebarNav"] {{
                display: none !important;
            }}
            h1 {{
                color: #002C6C !important;
                text-align: center;

            }}
            section[data-testid="stSidebar"] {{
                min-width: 70px !important;
                max-width: 250px !important;
                background: linear-gradient(174.59deg, #003684 0%, #0060D6 100%) !important;
                overflow: hidden;
                transition: max-width 0.3s ease-in-out;
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
            section[data-testid="stSidebar"]:hover {{
                max-width: 250px !important;
            }}
            /* Hide Sidebar Collapse Button */
            [data-testid="stSidebarNav"] {{
                display: none !important;
            }}
            /* Styled Input Box */
            .styled-input-container {{
                width: 874px;
                height: 52px;
                padding: 10px;
                background: #FEFEFE;
                box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.15);
                border-radius: 8px;
                border-bottom: 2px #006EF5 solid;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
            }}
            .styled-input {{
                width: 100%;
                height: 100%;
                border: none;
                outline: none;
                font-size: 14px;
                font-family: 'Poppins', sans-serif;
                padding-left: 10px;
                background: transparent;
                color: #000;
            }}
            .info-box {{
                width: 823px;
                height: 138px;
                padding: 20px 63px;
                background: rgba(255, 255, 255, 0.64);
                box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.15);
                border-radius: 7px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-start;
                gap: 5px;
            }}
            /* Send Icon */
            .send-icon {{
                width: 32px;
                height: 32px;
                cursor: pointer;
                margin-right: 10px;
            }}
            .send-button {{
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                border: none;
                background: none;
                outline: none;
            }}
            .model-info {{
            width: 283px;
            height: 41px;
            padding: 4px 10px;
            background: rgba(134, 134, 134, 0.10);
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 20px auto;
        }}
        .model-info svg {{
            width: 30px;
            height: 31px;
        }}
        .model-text-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }}
        .model-name {{
            color: #212121;
            font-size: 12px;
            font-family: Poppins;
            font-weight: 400;
        }}
        .model-training {{
            color: #868686;
            font-size: 10px;
            font-family: Poppins;
            font-weight: 400;
        }}
        .model-training strong {{
            font-weight: 700;
        }}
        .model-info {{
            position: absolute;
            top: 0px;
            left: 0px;
            width: 283px;
            height: 41px;
            padding: 17px 10px;
            background: rgba(134, 134, 134, 0.1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .model-info svg {{
            width: 30px;
            height: 31px;
        }}
        .model-text-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }}
        .model-name {{
            color: #212121;
            font-size: 12px;
            font-family: Poppins;
            font-weight: 400;
        }}
        
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
    """
        <div style="width: 283px; height: 41px; padding-left: 10px; padding-right: 10px; padding-top: 17px; padding-bottom: 17px; background: rgba(134, 134, 134, 0.10); border-radius: 12px; flex-direction: column; justify-content: center; align-items: flex-start; gap: 2px; display: inline-flex">
            <div style="justify-content: flex-start; align-items: center; gap: 8px; display: inline-flex">
                <div data-svg-wrapper>
                <svg width="30" height="31" viewBox="0 0 30 31" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect y="0.5" width="30" height="30" rx="15" fill="#E4E4E4"/>
                <path fill-rule="evenodd" clip-rule="evenodd" d="M18.058 15.1626C17.8892 15.1626 17.7415 15.0187 17.7415 14.8307C17.7415 12.8171 16.1697 11.1798 14.2286 11.1798C13.8066 11.1798 13.8066 10.516 14.2286 10.516C16.1697 10.516 17.7415 8.86755 17.7415 6.8319C17.7415 6.38937 18.3745 6.38937 18.3745 6.8319C18.3745 8.86755 19.9569 10.516 21.898 10.516C22.3095 10.516 22.3095 11.1798 21.898 11.1798C19.9253 11.1798 18.3745 12.784 18.3745 14.8307C18.3745 15.0187 18.2374 15.1626 18.058 15.1626Z" fill="#212121" stroke="#212121" stroke-width="0.25"/>
                </svg>
                </div>
                <div style="flex-direction: column; justify-content: center; align-items: flex-start; display: inline-flex">
                    <div style="color: #212121; font-size: 12px; font-family: Poppins; font-weight: 400; word-wrap: break-word">Llama 3.3</div>
                    <div><span style="color: #868686; font-size: 10px; font-family: Poppins; font-weight: 400; word-wrap: break-word">Trained on last 2 months of data till </span><span style="color: #868686; font-size: 10px; font-family: Poppins; font-weight: 700; word-wrap: break-word">Dec 2024</span></div>
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
    
    # Sidebar with logout button
    with st.sidebar:
        st.markdown(
            
            """
            <div class="sidebar-custom-wrap">
            <div >
                <div class="welcome-wrap" style="padding-left: 14px;padding-right: 14px;font-size: 16px;justify-content: center;align-items: center;gap: 10px;display: flex;">
                    <div style="border-radius: 7px; flex-direction: column; justify-content: center; align-items: flex-start; gap: 4px; display: inline-flex">
                        <div style="color: rgba(255, 255, 255, 0.46); font-size: 14px; font-weight: 400; line-height: 24px; word-wrap: break-word">Welcome to,</div>
                        <div style="justify-content: center; align-items: center; gap: 8px; display: inline-flex">
                            <img style="width: 19px; height: 20px" src="app/static/landing/compas_icon.png" />
                            <div><span style="color: white; font-size: 16px; font-weight: 400; line-height: 24px; word-wrap: break-word">VyStar AI -</span><span style="color: white; font-size: 16px; font-weight: 700; line-height: 24px; word-wrap: break-word">VAI </span></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="sidebar-container">
                <div class="sidebar-content">
                    <div>
                        <button class="new-chat-button" onclick="window.location.reload();" >
                        <i class="new-chat-icon"><img src=""/></i>
                        <span class="new-chat">New Chat</span>
                        </button>
                    </div>
                </div>
                <div style="width: 200px; height: 52px; padding-left: 8px; padding-right: 8px; padding-top: 10px; padding-bottom: 10px; background: rgba(0, 0, 0, 0.20); border-radius: 7px; justify-content: flex-start; align-items: center; gap: 11px; display: inline-flex">
                    <div style="justify-content: flex-start; align-items: center; gap: 7px; display: flex">
                        <div style="width: 32px; height: 32px; padding: 3.37px; background: #F6F5FF; box-shadow: 1.684px -1.684px 3.368px rgba(64, 64, 65, 0.10); border-radius: 58.32px; flex-direction: column; justify-content: center; align-items: center; display: inline-flex">
                            <img style="width: 26.95px; height: 26.95px; border-radius: 26.95px" src="app/static/landing/user-profile.png" />
                        </div>
                        <div style="flex-direction: column; justify-content: center; align-items: flex-start; display: inline-flex">
                            <div style="width: 116px; color: #E7E7E7; font-size: 12px; font-family: Poppins; font-weight: 600; word-wrap: break-word">Stephen Johnson</div>
                            <div style="width: 116px; color: #E7E7E7; font-size: 8px; font-family: Poppins; font-weight: 400; word-wrap: break-word">johnson.s@vystarcu.org</div>
                        </div>
                    </div>
                    <div data-svg-wrapper>
                        <svg width="10" height="20" viewBox="0 0 10 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4 10H6M4 4H6M4 16H6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                </div>
            </div>
            </div>
            <div style="width: 200px; height: 26px; justify-content: flex-start; align-items: center; gap: 10px; display: inline-flex">
                <div style="width: 72px; color: white; font-size: 12.20px; font-family: Poppins; font-weight: 400; word-wrap: break-word">Powered by</div>
                <div style="width: 68px; justify-content: flex-start; align-items: center; gap: 10px; display: flex">
                    <img style="width: 68px; height: 22px" src="app/static/landing/Vystar-logo.png" />
                </div>
            </div>
        </div>
        </div>
            """,
            unsafe_allow_html=True
        )
        new_button= st.button("New Chat", key="new_chat", icon=":material/maps_ugc:")
        
       

        if new_button:
            st.experimental_rerun()
            
            
    
    # Display welcome message if no chat history exists
    if not st.session_state.messages:
        st.markdown("<h1>Hi! How can I assist you today?</h1>", unsafe_allow_html=True)

    # Styled Input Box with Send Icon
    st.markdown(
        """
        <div class="styled-input-container-wrap">
        <div class="styled-input-container">
            <input class="styled-input" type="text" placeholder="You can ask me anything" id="user-input"/>
            <button class="send-button" onclick="sendMessage()">
                <svg class="send-icon" width="32" height="33" viewBox="0 0 32 33" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.0296 9.09627C9.84587 8.37965 10.5514 7.76756 11.1933 8.0868L25.5253 15.2152C26.1582 15.53 26.1582 16.47 25.5253 16.7848L11.1933 23.9132C10.5515 24.2324 9.84587 23.6204 10.0296 22.9037L11.7999 16L10.0296 9.09627ZM12.7013 16.5216L11.089 22.8093L24.7794 16L11.089 9.19074L12.7013 15.4784H20.1673C20.4434 15.4784 20.6673 15.7119 20.6673 16C20.6673 16.2881 20.4434 16.5216 20.1673 16.5216H12.7013Z" fill="#006EF5"/>
                </svg>
            </button>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    

    if "chat_input" in st.session_state and st.session_state.chat_input:
        prompt = st.session_state.chat_input
        st.session_state.chat_input = ""

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Echo Bot repeats the input
        response = f"🔁 {prompt}"

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()

run_app()
