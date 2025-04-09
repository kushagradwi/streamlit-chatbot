import streamlit as st

def info_button(header, info):
    """
    Creates an HTML-based info button that shows a tooltip on hover,
    using a smaller Google Material Icon, aligned on the same line as the header.
    """
    html_code = f"""
    <style>
        .info-container {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}

        .header {{
            font-family: Poppins, sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: black;
            margin-right: 5px;
        }}

        .info-button {{
            display: inline-block;
            
        }}

        .info-popup {{
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            color: #333;
            font-size: 12px;
            border: 1px solid #ddd;
            padding: 8px;
            border-radius: 5px;
            margin-top: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 250px;
            z-index: 10;
        }}

        .info-button:hover + .info-popup {{
            display: block;
        }}
    </style>
    <div class="info-container">
        <div class="header">{header}</div>
        <div style="position: relative; display: inline-block;">
            <div class="info-button"><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#007bff"><path d="M440-280h80v-240h-80v240Zm40-320q17 0 28.5-11.5T520-640q0-17-11.5-28.5T480-680q-17 0-28.5 11.5T440-640q0 17 11.5 28.5T480-600Zm0 520q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg></div>
            <div class="info-popup">{info}</div>
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


# div class="info-container">
#         <div class="header">{header}</div>
#         <div style="position: relative; display: inline-block;">
#             <span class="info-button material-icons" style="font-size: 18px;">info</span>
#             <div class="info-popup">{info}</div>
#         </div>
#     </div>