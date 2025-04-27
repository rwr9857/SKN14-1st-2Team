import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import base64
import os
from dotenv import load_dotenv

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


# 배경 이미지 설정 함수 (Base64) - gpt
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    # 절대 경로로 변경
    abs_path = os.path.abspath(png_file)
    bin_str = get_base64_of_bin_file(abs_path)
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

# 기존에 정의한 set_background 함수 활용
def clear_background():
    st.markdown("""
        <style>
        .stApp {
            background: none;
        }
        </style>
    """, unsafe_allow_html=True)


# 스타일 설정 (폰트,버튼) - 버튼은 잘 구현된건지 모르겠음...
def set_custom_styles():
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

        .car-info-container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .car-info-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .car-specs {
            display: flex; 
            flex-direction: column; 
            gap: 5px; 
        }

        .spec-item {
            padding: 5px 0;
            font-size: 16px; 
        }

        .spec-label {
            font-weight: bold;
            color: #555;
        }
        </style>
    """, unsafe_allow_html=True)



# 배경 초기화 상태 세팅
if "background_cleared" not in st.session_state:
    st.session_state.background_cleared = False

# 초기 배경 이미지 설정 (background_cleared가 False일 때만)
if not st.session_state.background_cleared:
    set_background('../docs/background.png')

st.image("../docs/차근차근 로고.png", width=150) # 차근차근 로고 적용

# DB 연결
conn = init_db()
cur = conn.cursor(dictionary=True) if conn else None

# 세션 상태 초기화
def init_session():
    default_values = {
        'age': 20,
        'gender': None,
        'purpose': None,
        'min_val': 1000,
        'max_val': 5000,
        'engine_type': None,
        'body_type': None,
        'first': None,
        'second': None,
        'third': None,
        'recommend_cars': []
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# 페이지 상태관리
if "page" not in st.session_state:
    st.session_state.page = "home"

# 밸런스(옵션선택) 화면
elif st.session_state.page == "balance":
    if not st.session_state.background_cleared:
        clear_background()
        st.session_state.background_cleared = True

    selected = option_menu(
        menu_title=None,
        options=["기본 정보", "예산 범위", "연료 타입", "바디타입", "선호도"],
        icons=["info-circle", "cash-coin", "ev-station", "car-front-fill", "heart"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F8B94A"},
            "icon": {"color": "#444", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px"},
            "nav-link-selected": {"background-color": "#FFCC66"},
        }
    )

    # 페이지 내용 업데이트
    if selected == "기본 정보":
        st.header("기본 정보")
        st.session_state.age = st.number_input("나이(세)", 20, 40, st.session_state.age)
        st.session_state.gender = st.radio("성별", ["남", "여"], horizontal=True, index=["남", "여"].index(
            st.session_state.gender) if st.session_state.gender else 0)
        st.session_state.purpose = st.selectbox("주 사용 용도", ["출퇴근", "여행/나들이", "업무용", "주말 드라이브"],
                                                index=["출퇴근", "여행/나들이", "업무용", "주말 드라이브"].index(
                                                    st.session_state.purpose) if st.session_state.purpose else 0)

    elif selected == "예산 범위":
        st.markdown("### 차량 구매 예산")
        col1, col2 = st.columns([1, 1.3])
        with col1:
            st.image("예산_아이콘.png", width=100)
        with col2:
            st.session_state.min_val, st.session_state.max_val = st.slider(
                "구매 예산 범위 설정 (단위: 만 원)", 1000, 5000, (st.session_state.min_val, st.session_state.max_val), step=500
            )

    elif selected == "연료 타입":
        st.header("연료 타입 선택")
        st.session_state.engine_type = st.radio(
            "원하는 연료 타입을 선택하세요",
            ["디젤", "가솔린", "하이브리드", "전기"],
            horizontal=True,
            index=["디젤", "가솔린", "하이브리드", "전기"].index(
                st.session_state.engine_type) if st.session_state.engine_type else 0
        )

    elif selected == "바디타입":
        st.header("바디타입 선택")
        st.session_state.body_type = st.radio(
            "선호하는 바디타입을 선택하세요",
            ["경차", "승용차", "SUV", "기타"],
            horizontal=True,
            index=["경차", "승용차", "SUV", "기타"].index(st.session_state.body_type) if st.session_state.body_type else 0
        )

    elif selected == "선호도":
        st.header("선호도 선택")
        st.markdown("### 중요하게 생각하는 항목을 순서대로 3개 선택해주세요!")
        preference_options = [
            "연비 (최저)",
            "가격 (최저)",
            "평점 (네이버 평점 기준)",
            "차체 크기 (실내 공간 기준 = 축거/전장*100)",
            "성능 (출력-최저)"
        ]
        # 1순위 선택
        first_priority = st.selectbox(
            "🏆 1순위",
            options=preference_options,
            key="first"
        )

        # 2순위 선택
        second_priority = st.selectbox(
            "🥈 2순위",
            options=[opt for opt in preference_options if opt != st.session_state.first],
            key="second"
        )

        # 3순위 선택
        third_priority = st.selectbox(
            "🥉 3순위",
            options=[opt for opt in preference_options if opt not in (st.session_state.first, st.session_state.second)],
            key="third"
        )

        # 선택 결과 출력
        st.write("#### 🔎 선택한 중요도 순위")
        st.write(f"1순위: **{st.session_state.first}**")
        st.write(f"2순위: **{st.session_state.second}**")
        st.write(f"3순위: **{st.session_state.third}**")

    # 모든 항목 완료 체크 및 다음 단계 버튼
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👉 모든 입력을 마치셨나요?")
    required_fields = [
        st.session_state.age,
        st.session_state.gender,
        st.session_state.purpose,
        st.session_state.min_val,
        st.session_state.max_val,
        st.session_state.engine_type,
        st.session_state.body_type,
        st.session_state.first,
        st.session_state.second,
        st.session_state.third
    ]

    if st.sidebar.button("다음 페이지로 이동"):
        if all(required_fields):
            st.sidebar.success("✅ 다음 페이지로 이동합니다!")
            recommended_cars()
            st.session_state.page = "recommendation"
            st.rerun()
        else:
            st.sidebar.error("⚠️ 모든 값을 입력 후 버튼을 눌러주세요.")