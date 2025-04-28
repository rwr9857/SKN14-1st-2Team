import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import base64
import os
from dotenv import load_dotenv

# 환경변수 로드 (.env 파일)
load_dotenv()


# DB 초기화 함수
def team_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),  # 예시: skn14
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET", "utf8mb4")
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
        return None


# 파일 경로 (배경 이미지 및 로고)
background_image_path = "../../docs/background.png"
logo_image_path = "../../docs/차근차근 로고.png"


# base64 인코딩 함수 (이미지를 base64로 인코딩하여 HTML로 표시)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# 배경 이미지 및 로고 설정
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

# DB 연결
conn = team_db()
cur = conn.cursor(dictionary=True) if conn else None


# 세션 상태 초기화 함수
def team_session():
    default_values = {
        'age': 20,
        'gender': None,
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


team_session()


# 사용자 정보 저장 함수
def save_user_info():
    try:
        cur.execute("""
            INSERT INTO USER_INFO (USER_AGE, USER_GENDER, USER_PURPOSE)
            VALUES (%s, %s, %s)
        """, (st.session_state.age, st.session_state.gender, st.session_state.purpose))
        conn.commit()
    except mysql.connector.Error as e:
        st.error(f"DB 저장 실패: {e}")


# 차량 필터링 함수
def get_filtered_cars():
    try:
        # 선호도 1순위 정렬 컬럼 매칭
        order_column = {
            "연비 (최저)": "CAR_FUEL_EFFICIENCY",
            "평점 (네이버 평점 기준)": "CAR_RATING",
            "차체 크기 (실내 공간 기준 = 축거/전장*100)": "CAR_SIZE",
            "성능 (출력-최저)": "CAR_HORSEPOWER"
        }.get(st.session_state.first)

        # 정렬 방향 결정
        order_direction = "ASC" if st.session_state.first == "연비 (최저)" else "DESC"

        # 기본적인 필터링 쿼리
        query = f"""
            SELECT car_info.*
            FROM CAR_INFO car_info
            JOIN BODY_TYPE_INFO body_info ON car_info.car_body_type = body_info.body_name
            JOIN FUEL_TYPE_INFO fuel_info ON car_info.car_fuel_type = fuel_info.fuel_type_id
            WHERE car_info.CAR_PRICE BETWEEN %s AND %s
              AND body_info.body_type_category = %s
              AND fuel_info.fuel_type_name = %s
        """

        if order_column:
            query += f" ORDER BY {order_column} {order_direction}"

        cur.execute(query, (
            st.session_state.min_val,
            st.session_state.max_val,
            st.session_state.fuel_type,
            st.session_state.body_type
        ))

        cars = cur.fetchall()
        return cars
    except mysql.connector.Error as e:
        st.error(f"차량 추천 쿼리 실패: {e}")
        return []


# 추천 차량 함수
def recommended_cars():
    try:
        cars = get_filtered_cars()
        st.session_state.recommended_cars = cars
        return cars
    except Exception as e:
        st.error(f"차량 추천 오류: {e}")
        return []


# 페이지 상태 관리
if "page" not in st.session_state:
    st.session_state.page = "home"

# 첫 번째 페이지: 시작 버튼
if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차, 차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")
    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("찾으러 가기", key="start_button"):
            st.session_state.page = "balance"
        st.markdown('</div>', unsafe_allow_html=True)

# 두 번째 페이지: 옵션 선택
elif st.session_state.page == "balance":
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
            st.session_state.min_val, st.session_state.max_val = st.slider("구매 예산 범위 설정 (단위: 만 원)", 1000, 5000, (
            st.session_state.min_val, st.session_state.max_val), step=500)

    elif selected == "연료 타입":
        st.header("연료 타입 선택")
        st.session_state.fuel_type = st.radio("원하는 연료 타입을 선택하세요", ["디젤", "가솔린", "하이브리드", "전기"], horizontal=True,
                                              index=["디젤", "가솔린", "하이브리드", "전기"].index(
                                                  st.session_state.fuel_type) if st.session_state.fuel_type else 0)

    elif selected == "바디타입":
        st.header("바디타입 선택")
        st.session_state.body_type = st.radio("선호하는 바디타입을 선택하세요", ["경차", "승용차", "SUV", "기타"], horizontal=True,
                                              index=["경차", "승용차", "SUV", "기타"].index(
                                                  st.session_state.body_type) if st.session_state.body_type else 0)

    elif selected == "선호도":
        st.header("선호도 선택")
        st.markdown("### 중요하게 생각하는 항목을 순서대로 3개 선택해주세요!")
        preference_options = ["연비 (최저)", "가격 (최저)", "평점 (네이버 평점 기준)", "차체 크기 (실내 공간 기준 = 축거/전장*100)", "성능 (출력-최저)"]

        first_priority = st.selectbox("🏆 1순위", options=preference_options, key="first")
        second_priority = st.selectbox("🥈 2순위",
                                       options=[opt for opt in preference_options if opt != st.session_state.first],
                                       key="second")
        third_priority = st.selectbox("🥉 3순위", options=[opt for opt in preference_options if
                                                        opt not in (st.session_state.first, st.session_state.second)],
                                      key="third")

        st.write("#### 🔎 선택한 중요도 순위")
        st.write(f"1순위: **{st.session_state.first}**")
        st.write(f"2순위: **{st.session_state.second}**")
        st.write(f"3순위: **{st.session_state.third}**")

    st.sidebar.markdown("---")
