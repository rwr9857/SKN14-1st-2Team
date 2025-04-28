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

# DB 연결
conn = init_db()
cur = conn.cursor(dictionary=True) if conn else None

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

# 기본 정보와 차량 선택 저장 함수
def save_user_info():
    try:
        cur.execute("""
            INSERT INTO USER_INFO (USER_AGE, USER_GENDER, USER_PURPOSE, USER_MIN_BUDGET, USER_MAX_BUDGET, 
            USER_ENGINE_TYPE, USER_BODY_TYPE, USER_FIRST_PREF, USER_SECOND_PREF, USER_THIRD_PREF)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (st.session_state.age, st.session_state.gender, st.session_state.purpose,
              st.session_state.min_val, st.session_state.max_val, st.session_state.engine_type,
              st.session_state.body_type, st.session_state.first, st.session_state.second, st.session_state.third))
        conn.commit()
    except mysql.connector.Error as e:
        st.error(f"DB 저장 실패: {e}")

# 차량 추천 함수 (예산, 연료, 바디타입, 선호도 순으로 정렬)
def get_filtered_cars():
    try:
        query = f"""
            SELECT * FROM CAR_INFO 
            WHERE CAR_PRICE BETWEEN {st.session_state.min_val } AND {st.session_state.max_val }
            AND FUEL_TYPE_NAME = %s
            AND BODY_TYPE = %s
            ORDER BY 
                CASE WHEN {st.session_state.first} = '연비 (최저)' THEN CAR_FUEL_EFFICIENCY END,
                CASE WHEN {st.session_state.first} = '가격 (최저)' THEN CAR_PRICE END,
                CASE WHEN {st.session_state.first} = '평점 (네이버 평점 기준)' THEN CAR_RATING END,
                CASE WHEN {st.session_state.first} = '차체 크기 (실내 공간 기준)' THEN CAR_SIZE END,
                CASE WHEN {st.session_state.first} = '성능 (출력-최저)' THEN CAR_HORSEPOWER END
        """
        cur.execute(query, (st.session_state.engine_type, st.session_state.body_type))
        cars = cur.fetchall()
        return cars
    except mysql.connector.Error as e:
        st.error(f"차량 추천 쿼리 실패: {e}")
        return []

# 추천 차량 세션
def recommended_cars():
    try:
        # 추천 차량을 가져와서 session_state에 저장
        cars = get_filtered_cars()
        st.session_state.recommended_cars = cars
        return cars
    except Exception as e:
        st.error(f"차량 추천 오류: {e}")
        return []

# # 추천 차량 세션
# def recommended_cars():
#     try:
#         cur.execute("select * from teamdb.CAR_INFO")
#         cars = cur.fetchall()
#         return cars
#     except mysql.connector.Error as e:
#         st.error(f'데이터베이스 쿼리 실패:{e}')
#         return[]


# 페이지 상태관리
if "page" not in st.session_state:
    st.session_state.page = "home"

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
                    price_in_million = car["CAR_PRICE"] / 10000  # 원 단위에서 만원 단위로 변환
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