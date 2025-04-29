import streamlit as st
import base64

# 파일 경로
background_image_path = "../../docs/background.png"
logo_image_path = "../../docs/차근차근 로고.png"

# base64 인코딩 함수
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 배경 및 로고 CSS
def set_background_and_logo(bg_path, logo_path):
    bg_base64 = get_base64_of_bin_file(bg_path)
    logo_base64 = get_base64_of_bin_file(logo_path)
    st.markdown(f"""
        <style>
        .block-container {{
            max-width: 1200px !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }}
        .stApp {{
            background-image: url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
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
            height: 40vh;
            margin-left: 120px;
        }}
        .main-title {{
            width : 400px;
            font-size: 2.6em;
            font-weight: bold;
            color: #111;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px #f3d16c33;
            text-align: center;
        }}
        .sub-title {{
            width : 400px;
            font-size: 1.3em;
            color: #222;
            margin-bottom: 40px;
            text-align: center;
        }}
        
        .stButton {{
            margin-left : 120px;
        }}
        
        div.stButton > button {{
            background-color: #111;
            color: #fff;
            padding: 18px 0px;
            width: 400px;
            height: 60px;
            border: none;
            border-radius: 40px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-top: 20px;
            margin-bottom: 16px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
            display: block;
        }}
        div.stButton > button:hover {{
            background-color: #333;
            color: #FFD600;
        }}
        </style>
        <img src="data:image/png;base64,{logo_base64}" class="custom-logo">
        """, unsafe_allow_html=True)

set_background_and_logo(background_image_path, logo_image_path)

# 중앙 컨텐츠 (HTML+Streamlit 버튼)
st.markdown("""
<div class="center-box">
    <div class="main-title">당신의 첫 차,<br>차근차근 함께 찾아요</div>
    <div class="sub-title">나에게 맞는 첫 차를<br>3분 만에 찾아드립니다.</div>
</div>
""", unsafe_allow_html=True)

# 반드시 Streamlit 버튼으로!
if st.button("찾으러 가기"):
    st.switch_page("pages/2_second_page.py")  # pages/second_page.py가 존재해야 함

