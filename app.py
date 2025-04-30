import streamlit as st
from styles.app import set_styles
from utils.index import get_base64_image

# 페이지 설정
st.set_page_config(
    page_title="차근차근",
    layout="centered",
    initial_sidebar_state="collapsed",
)

BACKGROUND_PATH = "./resource/background.png"
LOGO_PATH = "./resource/logo.png"

# 이미지 불러오기
bg_b64 = get_base64_image(BACKGROUND_PATH)
logo_b64 = get_base64_image(LOGO_PATH)
set_styles(bg_b64, logo_b64)

# 본문 렌더링
st.markdown(
    """
    <div class="center-box">
        <div class="main-title">당신의 첫 차,<br>차근차근 함께 찾아요</div>
        <div class="sub-title">나에게 맞는 첫 차를<br>3분 만에 찾아드립니다.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("찾으러 가기"):
    st.switch_page("pages/2_second_page.py")
