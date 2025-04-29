import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import base64
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# DB 연결 함수
def team_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET", "utf8mb4")
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
        return None

# 스타일 설정
def set_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: white;
            min-height: 100vh;
            position: relative;
            padding-bottom: 60px;
        }
        .block-container {
            max-width: calc(100% - 400px) !important;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .st-emotion-cache-t1wise {
            padding: 2rem 1rem 10rem;
        }
        .main-content {
            margin-top: 20px;
            padding-bottom: 60px;
        }
        .copyright {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 1200px;
            text-align: center;
            padding: 1rem;
            background-color: white;
            color: #888;
            font-size: 1em;
            border-top: 1px solid #eee;
        }
        </style>
    """, unsafe_allow_html=True)

# 직업 ID와 이름 매핑
JOB_MAPPING = {
    "대학생": 1,
    "사무직": 2,
    "IT/개발": 3,
    "서비스직": 4,
    "생산직": 5,
    "기타": 6
}

# 세션 상태 초기화
def team_session():
    default_values = {
        'age': 20,
        'gender': None,
        'job': None,
        'job_id': None,  # 직업 ID 저장용
        'purpose': None,
        'min_val': 1000,
        'max_val': 5000,
        'fuel_type': None,
        'body_type': None,
        'first': None,
        'second': None,
        'third': None,
        'recommend_cars': []
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

# 페이지 설정
st.set_page_config(page_title="차근차근 - 옵션 선택", layout="wide")
set_custom_styles()

# 로고 표시
st.image("../../docs/차근차근 로고.png", width=180)

# 세션 초기화
team_session()

# 옵션 메뉴
selected = option_menu(
    menu_title=None,
    options=["기본 정보", "예산 범위", "연료 타입", "바디타입", "선호도"],
    icons=["info-circle", "cash-coin", "ev-station", "car-front-fill", "heart"],
    orientation="horizontal",
    default_index=0,
    key="menu_selection",
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
    
    # 직업 선택 추가
    job_options = ["대학생", "사무직", "IT/개발", "서비스직", "생산직", "기타"]
    st.session_state.job = st.selectbox("직업", 
        job_options,
        index=job_options.index(st.session_state.job) if st.session_state.job in job_options else 0
    )
    # 선택된 직업의 ID 저장
    st.session_state.job_id = JOB_MAPPING[st.session_state.job]
    
    st.session_state.purpose = st.selectbox("주 사용 용도", ["출퇴근", "여행/나들이", "업무용", "주말 드라이브"],
                                            index=["출퇴근", "여행/나들이", "업무용", "주말 드라이브"].index(
                                                st.session_state.purpose) if st.session_state.purpose else 0)

elif selected == "예산 범위":
    st.markdown("### 차량 구매 예산")
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.image("../../docs/예산_아이콘.png", width=100)
    with col2:
        st.session_state.min_val, st.session_state.max_val = st.slider(
            "구매 예산 범위 설정 (단위: 만 원)", 1000, 5000, (st.session_state.min_val, st.session_state.max_val), step=500
        )

elif selected == "연료 타입":
    st.header("연료 타입 선택")
    st.session_state.fuel_type = st.radio(
        "원하는 연료 타입을 선택하세요",
        ["디젤", "가솔린", "하이브리드", "전기"],
        horizontal=True,
        index=["디젤", "가솔린", "하이브리드", "전기"].index(
            st.session_state.fuel_type) if st.session_state.fuel_type else 0
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

# DB에 사용자 정보 저장
def save_user_info():
    try:
        conn = team_db()
        if conn:
            cur = conn.cursor()
            
            # user_info 테이블에 저장
            insert_user_query = """
            INSERT INTO teamdb.user_info 
            (USER_AGE, USER_GENDER, user_job, user_purpose)
            VALUES (%s, %s, %s, %s)
            """
            
            user_values = (
                st.session_state.age,
                st.session_state.gender,
                st.session_state.job_id,  # job_id 사용
                st.session_state.purpose
            )
            
            cur.execute(insert_user_query, user_values)
            user_id = cur.lastrowid
            
            conn.commit()
            conn.close()
            
            # 세션에 user_id 저장
            st.session_state.user_id = user_id
            return user_id
            
    except mysql.connector.Error as e:
        st.error(f"사용자 정보 저장 실패: {e}")
        return None

# 모든 항목 완료 체크 및 다음 단계 버튼
st.sidebar.markdown("---")
st.sidebar.markdown("### 👉 모든 입력을 마치셨나요?")
required_fields = [
    st.session_state.age,
    st.session_state.gender,
    st.session_state.job_id,
    st.session_state.purpose,
    st.session_state.min_val,
    st.session_state.max_val,
    st.session_state.fuel_type,
    st.session_state.body_type,
    st.session_state.first,
    st.session_state.second,
    st.session_state.third
]

if st.sidebar.button("다음 페이지로 이동"):
    if all(required_fields):
        # 사용자 정보 저장
        user_id = save_user_info()
        if user_id:
            st.sidebar.success("✅ 다음 페이지로 이동합니다!")
            st.switch_page("pages/3_third_page.py")
    else:
        st.sidebar.error("⚠️ 모든 값을 입력 후 버튼을 눌러주세요.")

# 저작권 표시
st.markdown("""
    <div class="copyright">
    Copyright 2025. Chageun. All rights reserved.
    </div>
""", unsafe_allow_html=True)