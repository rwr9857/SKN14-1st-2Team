import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import base64
import os
from dotenv import load_dotenv

# 환경변수 로드 (.env 파일)
load_dotenv()

# db 초기화 함수
def team_db():
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

st.image("차근차근_로고_(1).png", width=150) # 차근차근 로고 적용

# DB 연결
conn = team_db()
cur = conn.cursor(dictionary=True) if conn else None

# 세션 상태 초기화
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

# 기본 정보와 차량 선택 저장 함수     todo init에서 작성 후 수정
def save_user_info():
    try:
        cur.execute("""
            INSERT INTO USER_INFO (USER_AGE, USER_GENDER, 
            USER_PURPOSE)
            # , USER_MIN_BUDGET, USER_MAX_BUDGET, 
            # USER_FUEL_TYPE, USER_BODY_TYPE, USER_FIRST_PREF, USER_SECOND_PREF, USER_THIRD_PREF)
            VALUES (%s, %s, %s)
            # , %s, %s, %s, %s, %s, %s, %s)
        """, (st.session_state.age, st.session_state.gender,)
                                  , st.session_state.purpose)
              # st.session_state.min_val, st.session_state.max_val, st.session_state.fuel_type,
              # st.session_state.body_type, st.session_state.first, st.session_state.second, st.session_state.third))
        conn.commit()
    except mysql.connector.Error as e:
        st.error(f"DB 저장 실패: {e}")


def get_filtered_cars():
    try:
        # 선호도 1순위로 정렬할 컬럼 매칭
        order_column = {
            "연비 (최저)": "CAR_FUEL_EFFICIENCY",
            "평점 (네이버 평점 기준)": "CAR_RATING",
            "차체 크기 (실내 공간 기준 = 축거/전장*100)": "CAR_SIZE",
            "성능 (출력-최저)": "CAR_HORSEPOWER"
        }.get(st.session_state.first)

        # 정렬 방향 결정
        if st.session_state.first in ["평점 (네이버 평점 기준)", "차체 크기 (실내 공간 기준 = 축거/전장*100)", "성능 (출력-최저)"]:
            order_direction = "DESC"
        else:
            order_direction = "ASC"

        # 기본적인 가격, 연료, 바디 타입 필터링
        query = f"""
            SELECT car_info.*
            FROM CAR_INFO car_info
            JOIN BODY_TYPE_INFO body_info
              ON car_info.car_body_type = body_info.body_name
            JOIN FUEL_TYPE_INFO fuel_info
              ON car_info.car_fuel_type = fuel_info.fuel_type_id
            WHERE car_info.CAR_PRICE BETWEEN %s AND %s
              AND body_info.body_type_category = %s
              AND fuel_info.fuel_type_name = %s
        """

        if order_column:
            query += f" ORDER BY {order_column} {order_direction}"

        cur.execute(query, (
            st.session_state.min_val ,  # 만원 → 원
            st.session_state.max_val ,
            st.session_state.fuel_type,
            st.session_state.body_type
        ))

        cars = cur.fetchall()
        return cars

    except mysql.connector.Error as e:
        st.error(f"차량 추천 쿼리 실패: {e}")
        return []


def recommended_cars():
    try:
        cars = get_filtered_cars()
        st.session_state.recommended_cars = cars
        return cars
    except Exception as e:
        st.error(f"차량 추천 오류: {e}")
        return []


# 페이지 상태관리
if "page" not in st.session_state:
    st.session_state.page = "home"


# 첫 번째 페이지(찾으러 가기)
if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차, 차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")

    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("찾으러 가기", key="start_button"):
            st.session_state.page = "balance"
        st.markdown('</div>', unsafe_allow_html=True)

## 2 페이지, 성규님 코드 삽입

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
        key= "menu_selection",
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

    # 모든 항목 완료 체크 및 다음 단계 버튼
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👉 모든 입력을 마치셨나요?")
    required_fields = [
        st.session_state.age,
        st.session_state.gender,
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
            st.sidebar.success("✅ 다음 페이지로 이동합니다!")
            recommended_cars()
            st.session_state.page = "recommendation"
            st.rerun()
        else:
            st.sidebar.error("⚠️ 모든 값을 입력 후 버튼을 눌러주세요.")


# 추천 결과 페이지
elif st.session_state.page == "recommendation":
    st.markdown("<h1>나의 첫 차는?</h1>", unsafe_allow_html=True)

    # 추천 차량 목록이 있는지 확인
    if "recommended_cars" in st.session_state and st.session_state.recommended_cars:
        # 추천 차량 표시
        for idx, car in enumerate(st.session_state.recommended_cars):
            with st.container():
                st.markdown(f'<div class="car-info-container">', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 2])

                with col1:
                    # 차량 이미지가 있으면 표시, 없으면 기본 이미지
                    if 'CAR_IMG_URL' in car and car['CAR_IMG_URL']:
                        st.image(car['CAR_IMG_URL'], width=300)
                    else:
                        st.image("대체이미지주소", width=300)

                with col2:
                    # 차량 정보 헤더
                    st.markdown(f'<div class="car-info-header">{car["BRAND_NAME"]} {car["CAR_FULL_NAME"]}</div>',
                                unsafe_allow_html=True)

                    # 기본 정보 표시
                    st.markdown('<div class="car-specs">', unsafe_allow_html=True)

                    # 가격 정보
                    price_in_million = car["CAR_PRICE"]  # 원 단위에서 만원 단위로 변환
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">가격:</span> {price_in_million:,.1f}만원</div>',
                        unsafe_allow_html=True)

                    # 연료 타입
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">연료:</span> {car["FUEL_TYPE_NAME"]}</div>',
                        unsafe_allow_html=True)

                    # 엔진 타입
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">엔진:</span> {car["ENGINE_NAME"]}</div>',
                        unsafe_allow_html=True)

                    # 연비
                    if 'CAR_FUEL_EFFICIENCY' in car:
                        st.markdown(
                            f'<div class="spec-item"><span class="spec-label">연비:</span> {car["CAR_FUEL_EFFICIENCY"]}km/L</div>',
                            unsafe_allow_html=True)

                    # 출력 (마력/토크)
                    if 'CAR_HORSEPOWER' in car:
                        st.markdown(
                            f'<div class="spec-item"><span class="spec-label">출력:</span> {car["CAR_HORSEPOWER"]}hp</div>',
                            unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)


                st.markdown('</div>', unsafe_allow_html=True)

        # 새로운 추천 받기 버튼
        if st.button("같은 조건에 다른 모델 추천 받기"):
            # 4 페이지로 이동하는 로직 작성 - 준기님 코드와 연결 필요
            st.rerun()
    else:
        st.warning("추천 차량이 없습니다. 새로운 조건으로 다시 시도해보세요.")
        if st.button("다시 설정하기"):
            st.session_state.page = "balance"
            st.rerun()





