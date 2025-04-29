import streamlit as st


def set_styles(bg_base64, logo_base64):
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bg_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            .block-container {{
                max-width: 1200px !important;
                padding-left: 2rem;
                padding-right: 2rem;
            }}
            .custom-logo {{
                position: absolute;
                top: 20px;
                left: 40px;
                width: 180px;
                z-index: 10;
            }}
            .center-box {{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                justify-content: center;
                margin-top: 120px;
                margin-left: 120px;
                height: 40vh;
            }}
            .main-title {{
                width: 400px;
                font-size: 2.6em;
                font-weight: bold;
                color: #111;
                margin-bottom: 20px;
                text-shadow: 2px 2px 10px #f3d16c33;
                text-align: center;
            }}
            .sub-title {{
                width: 400px;
                font-size: 1.3em;
                color: #222;
                margin-bottom: 40px;
                text-align: center;
            }}
            div.stButton > button {{
                background-color: #111;
                color: #fff;
                width: 400px;
                height: 60px;
                padding: 18px 0;
                border: none;
                border-radius: 40px;
                font-weight: bold;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                margin-left: 120px;
                margin-top: 20px;
                margin-bottom: 16px;
                cursor: pointer;
                transition: 0.2s;
                display: block;
                text-align: center;
            }}
            div.stButton > button:hover {{
                background-color: #333;
                color: #FFD600;
            }}
        </style>
        <img src="data:image/png;base64,{logo_base64}" class="custom-logo">
        """,
        unsafe_allow_html=True,
    )
