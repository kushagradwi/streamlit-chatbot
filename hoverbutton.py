import streamlit as st

def info_button(header, info):
    """
    Creates an HTML-based info button that shows a tooltip on hover,
    using a smaller Google Material Icon, aligned on the same line as the header.
    """
    html_code = f"""
    <head>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>
    <style>
        .info-container {{
            display: flex;
            align-items: center;
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
            background-color: #007bff;
            color: white;
            border-radius: 50%;
            padding: 2px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-left: 5px;
            text-align: center;
            line-height: 1;
        }}

        .info-popup {{
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            color: #333;
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
            <span class="info-button material-icons" style="font-size: 18px;">info</span>
            <div class="info-popup">{info}</div>
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


