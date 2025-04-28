from pathlib import Path
import streamlit as st
import base64
import mysql.connector
import base64
import os
from dotenv import load_dotenv
import pandas as pd
import altair as alt

# 환경변수 로드 (.env 파일)
load_dotenv()

# db 초기화 함수
def init_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),  # skn14
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET", "utf8mb4")
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
        return None


#
# # 페이지 기본 설정
# st.set_page_config(page_title="두 번째 페이지 - 예산 범위", page_icon="🚗", layout="centered")
# logo_image_path = Path(__file__).parent.parent / "images" / "차근차근 로고.png"
# logo_image_path = str(logo_image_path)
#
# # base64 인코딩 함수
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
#
# # 로고 CSS 및 삽입
# def set_logo(logo_path):
#     logo_base64 = get_base64_of_bin_file(logo_path)
#     st.markdown(f"""
#         <style>
#         .st-emotion-cache-mtjnbi{{
#             padding: 2rem 1rem 10rem !important;
#         }}
#         .block-container {{
#             max-width: 1200px !important;
#             padding-left: 2rem;
#             padding-right: 2rem;
#         }}
#         .custom-logo {{
#             position: absolute;
#             top: 20px;
#             left: 40px;
#             width: 180px;
#             z-index: 10;
#         }}
#         /* 탭 스타일 */
#         .tab-menu {{
#             display: flex;
#             margin-top: 100px;
#             margin-bottom: 0px;
#             gap: 0px;
#             font-size: 1.1em;
#             font-weight: bold;
#         }}
#         .tab {{
#             background: #FFD98C;
#             border-radius: 18px 18px 0 0;
#             padding: 12px 32px;
#             margin-right: 6px;
#             color: #222;
#             border: 2px solid #FFD98C;
#             border-bottom: none;
#             box-shadow: 0px 2px 8px #ffeabf44;
#             display: flex;
#             align-items: center;
#             gap: 8px;
#         }}
#         .tab.selected {{
#             background: #FFE7B5;
#             color: #111;
#         }}
#         .tab .dot {{
#             width: 13px;
#             height: 13px;
#             border-radius: 50%;
#             display: inline-block;
#             margin-right: 4px;
#         }}
#         .tab .dot.green {{ background: #3CB371; }}
#         .tab .dot.red {{ background: #F36E6E; }}
#         .tab .dot.blue {{ background: #5DB6F7; }}
#         .tab .dot.gray {{ background: #ccc; }}
#         .tab .dot.purple {{ background: #b761ff; }}
#         .main-box {{
#             background: #FFE7B5;
#             border-radius: 0 28px 28px 28px;
#             padding: 32px 32px 2px 32px;
#             margin-top: 0px;
#             box-shadow: 0px 4px 24px #ffeabf44;
#             margin-left: auto;
#             margin-right: auto;
#         }}
#         .question {{
#             background: #fff9ee;
#             border-radius: 18px;
#             padding: 16px 24px;
#             font-size: 1.1em;
#             margin-bottom: 32px;
#             text-align: center;
#         }}
#         .range-box {{
#             background: #fffbe9;
#             border-radius: 18px;
#             display: flex;
#             align-items: center;
#             padding: 32px 40px;
#             gap: 40px;
#             justify-content: center;
#         }}
#         .money-img {{
#             width: 120px;
#             height: 120px;
#             background: #fff;
#             border-radius: 50%;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             margin-right: 24px;
#             box-shadow: 0 2px 8px #ffeabf44;
#         }}
#         .amount-setting {{
#             flex: 1;
#             min-width: 300px;
#         }}
#         .amount-labels {{
#             display: flex;
#             justify-content: space-between;
#             margin-bottom: 12px;
#             font-size: 1.1em;
#             font-weight: 600;
#             color: #B89000;
#             padding-left: 200px;
#             padding-right: 200px;
#             padding-top: 20px;
#         }}
#         .copyright {{
#             text-align: center;
#             margin-top: 48px;
#             color: #888;
#             font-size: 1em;
#         }}
#         .st-ae.st-af{{
#             padding-left: 120px;
#             padding-right: 120px;
#         }}
#         .st-emotion-cache-1s2v671 {{
#             min-height: 0px !important;
#         }}
#
#         /* 슬라이더 스타일 일부 개선 */
#         [data-baseweb="slider"] > div {{
#             margin-top: 18px;
#         }}
#
#         </style>
#         <img src="data:image/png;base64,{logo_base64}" class="custom-logo">
#     """, unsafe_allow_html=True)
#
# set_logo(logo_image_path)
#
# # 탭 메뉴 (디자인용)
# st.markdown("""
# <div class="tab-menu">
#     <div class="tab selected"><span class="dot green"></span>예산 범위</div>
#     <div class="tab"><span class="dot red"></span>엔진 타입</div>
#     <div class="tab"><span class="dot blue"></span>바디타입</div>
#     <div class="tab"><span class="dot gray"></span>용도체크</div>
#     <div class="tab"><span class="dot purple"></span>선호도</div>
# </div>
# """, unsafe_allow_html=True)
#
# # 메인 박스 및 질문
# st.markdown("""
# <div class="main-box">
#     <div class="question">예산 차량 구매 예산은 어느 정도 생각하고 계신가요?</div>
# </div>
# """, unsafe_allow_html=True)
#
# st.markdown(f"""
# <div class="amount-setting">
#             <div class="amount-labels">
#                 <div>최소 금액<br><span style="font-size:1.7em; color:#B89000; font-weight:bold;">1,000</span>만원</div>
#                 <div>최대 금액<br><span style="font-size:1.7em; color:#B89000; font-weight:bold;">5,000</span>만원</div>
#             </div>
# </div>
# """, unsafe_allow_html=True)
#
# # 금액 슬라이더 (실제 입력)
# min_price, max_price = st.slider(
#     "", 1000, 5000, (1000, 5000), step=500, format="%d"
# )
#
# # 금액 설정 텍스트
# st.markdown(f"""
# <div style="font-size: 1.2em; font-weight: bold; text-align: center; color: #B89000;">
#     설정된 금액: {min_price} 만원 ~ {max_price}만원
# </div>
# """, unsafe_allow_html=True)
#
# # 저작권
# st.markdown("""
# <div class="copyright">
# Copyright 2025. Chageun. All rights reserved.
# </div>
# """, unsafe_allow_html=True)
