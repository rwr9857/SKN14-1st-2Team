import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import base64

# --- 데이터베이스 초기화 함수 ---
def init_db():
    conn = sqlite3.connect('teamdb')
    conn.execute("PRAGMA foreign_keys = ON;")  # FK 활성화 추가
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
            user_id INTEGER PRIMARY KEY,  -- AUTOINCREMENT 삭제 (자동증가 기본적용)
            user_age INTEGER,
            user_gender TEXT,
            car_id INTEGER,
            FOREIGN KEY (car_id) REFERENCES car_info(car_id)
        );
    ''')

    conn.commit()
    return conn

# --- 배경 이미지 설정 함수 (Base64) ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# DB 연결 (앱 시작할 때)
conn = init_db()

# --- 스타일 설정 (폰트 등) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
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
    </style>
""", unsafe_allow_html=True)

# --- 배경 이미지 적용 ---
set_background('docs/background.png')

# --- 로고 삽입 ---
st.image("docs/logo.png", width=150)

# --- 페이지 상태관리 ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- 메인화면 ---
if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차, 차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")

    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("찾으러 가기", key="start_button"):
            st.session_state.page = "balance"
        st.markdown('</div>', unsafe_allow_html=True)

# --- 밸런스(설문) 화면 ---
elif st.session_state.page == "balance":
    selected = option_menu(
        menu_title=None,
        options=["예산 범위", "엔진 타입", "바디타입", "용도 체크", "선호도"],
        icons=["cash-coin", "ev-station", "car-front", "clipboard-check", "heart"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F8B94A"},
            "icon": {"color": "#444", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px"},
            "nav-link-selected": {"background-color": "#FFCC66"},
        }
    )

    # --- 예산 범위 입력 ---
    if selected == "예산 범위":
        st.header("예산 설정")
        st.write("예산 차량 구매 예산은 어느 정도 생각하고 계신가요?")

        min_val, max_val = st.slider(
            "구매 예산 범위 설정 (단위: 만원)",
            0, 5000, (0, 5000), step=100
        )
        st.write(f"선택한 예산: **{min_val}만원 ~ {max_val}만원**")

    # --- 엔진 타입 선택 ---
    if selected == "엔진 타입":
        st.header("엔진 타입 선택")
        engine = st.selectbox("선호하는 엔진 타입을 선택하세요.", ["가솔린", "디젤", "친환경"])
        st.write(f"선택한 엔진 타입: **{engine}**")

    # --- 바디타입 선택 ---
    if selected == "바디타입":
        st.header("바디타입 선택")
        body = st.selectbox("선호하는 바디타입을 선택하세요.", ["승용차", "SUV", "경차"])
        st.write(f"선택한 바디타입: **{body}**")

    # --- 용도 체크 ---
    if selected == "용도 체크":
        st.header("차량 사용 용도 체크")
        purpose = st.radio("주 사용 용도를 선택하세요.", ["출퇴근", "여행/나들이", "업무용", "주말 드라이브"], horizontal=True)
        st.write(f"선택한 용도: **{purpose}**")

    # --- 선호도 ---
    if selected == "선호도":
        st.header("선호도 입력")
        st.write("특별히 원하는 옵션이나 스타일을 입력해주세요.")
        preference = st.text_input("예: 연비 좋은 차, 튼튼한 차 등")
        if preference:
            st.success(f"입력된 선호도: {preference}")

        if st.button("추천 차량 보기"):
            st.success("추천 페이지로 이동합니다!")
            # 향후 추천 차량 페이지 연결 가능