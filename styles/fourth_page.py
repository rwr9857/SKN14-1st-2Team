import streamlit as st


# 스타일 설정
def set_custom_styles():
    # CSS
    with open("./styles/fourth_page.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)