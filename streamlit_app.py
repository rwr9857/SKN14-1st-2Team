import streamlit as st
import sqlite3
import pandas as pd


# --- DB 연결 ---
def init_db():
    conn = sqlite3.connect('car_recommendation.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS car_info (
            car_id INTEGER PRIMARY KEY,
            car_model TEXT,
            car_body_type TEXT,
            car_fuel_type TEXT,
            car_price INTEGER,
            car_horsepower INTEGER,
            car_engine_type TEXT,
            car_fuel_efficiency REAL,
            car_size TEXT,
            car_img_url TEXT,
            car_brand TEXT
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_age INTEGER,
            user_gender TEXT,
            car_id INTEGER,
            FOREIGN KEY (car_id) REFERENCES car_info(car_id)
        );
    ''')

    conn.commit()
    return conn


# --- 스타일 설정 (Inter 폰트 + 기본 스타일) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .price-card {
        background-color: #FFE4B5;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 로고 삽입 ---
st.image("1.png", width=150)

# --- 첫 화면 ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차,</h1>", unsafe_allow_html=True)
    st.markdown("<h1>차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")

    if st.button("찾으러 가기"):
        st.session_state.page = "budget"

# --- 예산 설정 화면 ---
if st.session_state.page == "budget":
    st.markdown("## 예산 차량 구매 예산은 어느 정도 생각하고 계신가요?")

    with st.container():
        st.markdown('<div class="price-card">', unsafe_allow_html=True)

        st.markdown("#### 금액 설정")
        price_range = st.slider(
            "최소 ~ 최대 구매 예산 (만원)",
            1000, 5000, (1000, 5000),
            step=100,
            format="%d만원"
        )
        min_price, max_price = price_range

        st.markdown(f"**최소 금액:** {min_price:,}만원")
        st.markdown(f"**최대 금액:** {max_price:,}만원")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("다음 단계로 ➡️"):
        st.session_state.page = "next"  # 여기서 다음 단계로 넘겨줄 준비

# --- 다음 페이지 준비 (예: 바디타입 고르기) ---
if st.session_state.page == "next":
    st.header("엔진타입을 골라주세요!")

