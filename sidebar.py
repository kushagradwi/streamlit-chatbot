import streamlit as st


def logout():
    st.session_state.messages = []  # Clear chat history on logout
    st.session_state.suggestions = []
    st.session_state.logged_in = False
    st.session_state.redirect = True
    st.rerun()

def renderSidebar():
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
                <a class="vy-sidebar-link" href="/dashboard" target="_self">
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