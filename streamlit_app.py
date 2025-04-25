import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
import pandas as pd


# --- DB 연결 ---
def init_db():
    conn = sqlite3.connect('teamdb')
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

    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .styled-button {
        border: none;
        background-color: #4CAF50;
        color: white;
        padding: 15px 30px;
        font-size: 20px;
        cursor: pointer;
        border-radius: 10px;
    }

    .styled-button:hover {
        background-color: #45a049;
    }

    .stApp {
        background-image: url("docs/차근차근_배경화면.jpg"); /* 경로 확인 */
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }

    </style>
""", unsafe_allow_html=True)

# --- 로고 삽입 ---
# 로고 넣기
logo_path = "docs/차근차근_로고.png"  # 업로드된 첫 이미지 파일 이름
st.image("docs/차근차근_로고.png", width=150)

# --- 첫 화면 ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차,</h1>", unsafe_allow_html=True)
    st.markdown("<h1>차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")

    # 스타일이 적용된 버튼을 가운데에 배치
    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("찾으러 가기", key="styled-button"):
            st.session_state.page = "budget"
        st.markdown('</div>', unsafe_allow_html=True)

# 상단 탭 메뉴
selected = option_menu(
    menu_title=None,
    options=["기본 정보","예산 범위", "엔진 타입", "바디타입", "용도체크", "선호도"],
    icons=["info-circle", "cash-coin", "ev-station", "car-front-fill", "clipboard-check", "heart"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#F8B94A"},
        "icon": {"color": "#444", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px"},
        "nav-link-selected": {"background-color": "#FFCC66"},
    }
)


# ── “기본 정보” 입력 UI ──
if selected == "기본 정보":
    st.header("📝 기본 정보")

    # 나이 입력: 최소20, 최대40, 기본값 20
    age = st.number_input(
        label="나이(세)",
        min_value=20,
        max_value=40,
        value=20,
        step=1,
        format="%d"
    )

    # 성별 선택: 가로 방향 라디오
    gender = st.radio(
        label="성별",
        options=["남", "여"],
        horizontal=True
    )

    # 용도 선택: 단일 선택만 가능
    purpose = st.selectbox(
        label="주 사용 용도",
        options=["출퇴근", "여행/나들이", "업무용", "주말 드라이브"]
    )

    # 입력된 값 출력 (디버깅/확인용)
    st.write(f"▶ 나이: {age}세")
    st.write(f"▶ 성별: {gender}")
    st.write(f"▶ 용도: {purpose}")

# 예산 범위 탭
if selected == "예산 범위":
    st.markdown("### 예산 차량 구매 예산은 어느 정도 생각하고 계신가요?")

    col1, col2 = st.columns([1,1.3])

    with col1:
        st.image("docs/예산_아이콘.png", width=100)

    with col2:
        st.markdown("#### 금액 설정")
        min_val, max_val = st.slider(
            "구매 예산 범위 설정 (단위: 만 원)",
            min_value=0,
            max_value=5000,
            value=(0, 5000),
            step=1000,
            format="%d"
        )
        st.write(f"선택한 예산: **{min_val}만원 ~ {max_val}만원**")