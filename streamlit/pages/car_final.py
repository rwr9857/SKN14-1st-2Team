import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import base64
import os
from dotenv import load_dotenv
import pandas as pd
import altair as alt


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
    set_background('../../docs/background.png')

st.image("차근차근 로고.png", width=150) # 차근차근 로고 적용

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
            INSERT INTO teamdb.user_info (USER_AGE, USER_GENDER,USER_PURPOSE,USER_ID, user_job)
            VALUES (%s, %s, %s, %s, %s)
        """, (st.session_state.age, st.session_state.gender,st.session_state.purpose, st.session_state.id, st.session_state.job))
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

        # 필터 조건 동적 생성
        filters = []
        params = []

        # 예산
        filters.append("car_info.CAR_PRICE BETWEEN %s AND %s")
        params.extend([st.session_state.min_val, st.session_state.max_val])

        # 바디타입
        if st.session_state.body_type and st.session_state.body_type != "전체":
            filters.append("body_info.body_type_category = %s")
            params.append(st.session_state.body_type)

        # 연료타입
        if st.session_state.fuel_type and st.session_state.fuel_type != "전체":
            filters.append("fuel_info.fuel_type_name = %s")
            params.append(st.session_state.fuel_type)

        where_clause = " AND ".join(filters)

        query = f"""
            SELECT 
                brand_info.brand_name AS BRAND_NAME,
                car_info.CAR_FULL_NAME, 
                car_info.CAR_PRICE, 
                car_info.CAR_IMG_URL, 
                car_info.CAR_FUEL_EFFICIENCY, 
                car_info.CAR_HORSEPOWER,
                car_info.CAR_ENGINE_TYPE AS ENGINE_NAME,
                fuel_info.fuel_type_name AS FUEL_TYPE_NAME,
                body_info.body_type_category AS BODY_TYPE_NAME
            FROM CAR_INFO car_info 
            JOIN BRAND_INFO brand_info 
                ON car_info.car_brand = brand_info.brand_id 
            JOIN BODY_TYPE_INFO body_info 
                ON car_info.car_body_type = body_info.body_name 
            JOIN FUEL_TYPE_INFO fuel_info
                ON car_info.car_fuel_type = fuel_info.fuel_type_id
            WHERE {where_clause}
        """

        if order_column:
            query += f" ORDER BY {order_column} {order_direction}"

        # 쿼리 및 파라미터 확인 (디버깅용)
        st.write("실행 쿼리:", query)
        st.write("파라미터:", params)

        cur.execute(query, tuple(params))
        cars = cur.fetchall()
        return cars

    except mysql.connector.Error as e:
        st.error(f"차량 추천 쿼리 실패: {e}")
        st.text_area("쿼리문", query)
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
        for idx, car in enumerate(st.session_state.recommended_cars):
            with st.container():
                st.markdown(f'<div class="car-info-container">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    if 'CAR_IMG_URL' in car and car['CAR_IMG_URL']:
                        st.image(car['CAR_IMG_URL'], width=300)
                    else:
                        st.image("대체이미지.png", width=300)
                with col2:
                    st.markdown(
                        f'<div class="car-info-header">{car["BRAND_NAME"]} {car["CAR_FULL_NAME"]}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="car-specs">', unsafe_allow_html=True)

                    # 가격 정보 (문자열 → float 변환)
                    price_in_million = car["CAR_PRICE"]
                    try:
                        price_in_million = float(price_in_million)
                    except (ValueError, TypeError):
                        price_in_million = 0
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">가격:</span> {price_in_million:,.1f}만원</div>',
                        unsafe_allow_html=True
                    )

                    # 연료 타입
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">연료:</span> {car["FUEL_TYPE_NAME"]}</div>',
                        unsafe_allow_html=True
                    )

                    # 엔진 타입
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">엔진:</span> {car["ENGINE_NAME"]}</div>',
                        unsafe_allow_html=True
                    )

                    # 연비
                    if 'CAR_FUEL_EFFICIENCY' in car:
                        st.markdown(
                            f'<div class="spec-item"><span class="spec-label">연비:</span> {car["CAR_FUEL_EFFICIENCY"]}km/L</div>',
                            unsafe_allow_html=True
                        )

                    # 출력 (마력/토크)
                    if 'CAR_HORSEPOWER' in car:
                        st.markdown(
                            f'<div class="spec-item"><span class="spec-label">출력:</span> {car["CAR_HORSEPOWER"]}hp</div>',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        if st.button("다른 모델 추천 받기"):
            # 추천 결과 등 이전 상태 초기화
            if "recommended_cars" in st.session_state:
                st.session_state.page = "차량 정보 조회"
                st.rerun()
    else:
        st.warning("추천 차량이 없습니다. 새로운 조건으로 다시 시도해보세요.")
        if st.button("다시 설정하기"):
            st.session_state.page = "balance"
            st.rerun()


# --- 필터용 고유값 조회 함수 ---
def get_distinct_values(query):
    conn = team_db()
    if conn is None:
        return []
    try:
        cur = conn.cursor()
        cur.execute(query)
        return [row[0] for row in cur.fetchall() if row[0] is not None]
    finally:
        conn.close()


body_types = ["전체"] + get_distinct_values("SELECT DISTINCT bt.body_type_category FROM teamdb.body_type_info bt JOIN teamdb.car_info c ON bt.body_name = c.car_body_type"
) # 중복 없이 4개만 나옴
fuel_types = ["전체"] + get_distinct_values("SELECT DISTINCT f.fuel_type_name FROM teamdb.fuel_type_info f JOIN teamdb.car_info c ON f.fuel_type_id = c.car_fuel_type")

# --- 사이드바 메뉴 및 페이지 라우팅 ---
if "page" not in st.session_state:
    st.session_state.page = "차량 정보 조회"

st.sidebar.title("메뉴")
if st.sidebar.button("차량 정보 조회"):
    st.session_state.page = "차량 정보 조회"
if st.sidebar.button("통계 정보"):
    st.session_state.page = "통계 정보"
if st.sidebar.button("리뷰와 평점"):
    st.session_state.page = "리뷰와 평점"




def get_review_summary():
    conn = team_db()
    if conn is None:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        query = """
        SELECT
            cri.car_name,
            cri.avg_score,
            cri.survey_people_count,
            cri.graph_info
        FROM teamdb.car_review_info cri
        JOIN teamdb.CAR_INFO ci ON cri.car_name = ci.CAR_FULL_NAME
        """
        cur.execute(query)
        return cur.fetchall()
    finally:
        if conn:
            conn.close()


def get_comments_by_car(car_name):
    conn = team_db()
    if conn is None:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        query = """
        SELECT
            ci.nickname,
            ci.comment_avg_score,
            ci.comment_text,
            ci.created_at
        FROM teamdb.comment_info ci
        JOIN teamdb.car_review_info cri ON cri.review_id = ci.review_id
        WHERE cri.car_name = %s
        """
        cur.execute(query, (car_name,))
        return cur.fetchall()
    except mysql.connector.Error as e:
        st.error(f"댓글 정보 조회 실패: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- 필터 조건 변환 함수 ---
def get_price_range(selected):
    if selected == "1000만원대":
        return (1000, 1999)
    elif selected == "2000만원대":
        return (2000, 2999)
    elif selected == "3000만원대":
        return (3000, 3999)
    elif selected == "4000만원 이상":
        return (4000, 1_000_000)
    return None


# --- 차량 정보 조회 페이지 ---
if st.session_state.page == "차량 정보 조회":
    # --- 필터 드롭다운 ---
    col1, col2, col3, col4= st.columns([1, 1, 1, 1])
    with col1:
        selected_body = st.selectbox("외형", body_types)
    with col2:
        selected_price = st.selectbox("가격", ["전체", "1000만원대", "2000만원대", "3000만원대", "4000만원 이상"])
    with col3:
        selected_eff = st.selectbox("연비", ["전체", "10이하", "10~15", "15이상"])
    with col4:
        selected_fuel = st.selectbox("유종", fuel_types)

    st.markdown("---")




    def get_min_efficiency(selected):
        if selected == "10이하":
            return 0
        elif selected == "10~15":
            return 10
        elif selected == "15이상":
            return 15
        return None


    # --- make_query 함수 ---
    def make_query(price_range=None, min_efficiency=None, body_type=None, fuel_type=None, limit=8, offset=0):
        query = """
        SELECT
            c.CAR_FULL_NAME,
            b.BRAND_NAME,
            bt.body_type_category,
            f.FUEL_TYPE_NAME,
            c.CAR_PRICE,
            c.CAR_FUEL_EFFICIENCY,
            c.CAR_IMG_URL
        FROM teamdb.CAR_INFO c
        JOIN teamdb.BRAND_INFO b ON c.car_brand = b.BRAND_ID
        JOIN teamdb.BODY_TYPE_INFO bt ON c.CAR_BODY_TYPE = bt.body_name
        JOIN teamdb.FUEL_TYPE_INFO f ON c.CAR_FUEL_TYPE = f.FUEL_TYPE_ID
        WHERE 1=1
        """
        if price_range:
            query += f" AND c.CAR_PRICE BETWEEN {price_range[0]} AND {price_range[1]}"
        if min_efficiency is not None:
            query += f" AND c.CAR_FUEL_EFFICIENCY >= {min_efficiency}"
        if body_type and body_type != "전체":
            query += f" AND bt.BODY_type_category = '{body_type}'"
        if fuel_type and fuel_type != "전체":
            query += f" AND f.FUEL_TYPE_NAME = '{fuel_type}'"
        query += f" ORDER BY c.CAR_PRICE LIMIT {limit} OFFSET {offset}"
        return query

    # --- 페이지네이션 상태 ---
    if "pagenation" not in st.session_state:
        st.session_state.pagenation = 1


    def set_pagenation(p):
        st.session_state.pagenation = p
        st.rerun()


    # --- 차량 목록 가져오기 ---
    page_size = 8
    offset = (st.session_state.pagenation - 1) * page_size

    query = make_query(
        price_range=get_price_range(selected_price) if selected_price != "전체" else None,
        min_efficiency=get_min_efficiency(selected_eff) if selected_eff != "전체" else None,
        body_type=selected_body if selected_body != "전체" else None,
        fuel_type=selected_fuel if selected_fuel != "전체" else None,
        limit=page_size,
        offset=offset
    )

    conn = team_db()
    cars_from_db = []
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(query)
            cars_from_db = cur.fetchall()
        except mysql.connector.Error as e:
            st.error(f"차량 정보 조회 실패: {e}")
        finally:
            conn.close()

    dummy_image_url = "https://dummyimage.com/220x110/eee/aaa"

    # --- 차량 카드 표시 ---
    if cars_from_db:
        for i in range(0, len(cars_from_db), 4):
            card_row = cars_from_db[i: i + 4]
            cols = st.columns(4)
            for idx, car in enumerate(card_row):
                with cols[idx]:
                    image_url = car.get("CAR_IMG_URL")
                    if image_url and image_url.strip().startswith("http"):
                        st.image(image_url.strip(), use_container_width=True)
                    else:
                        st.image(dummy_image_url, use_container_width=True)
                    st.markdown(f"**{car['CAR_FULL_NAME']}**")
                    st.markdown(f"{car['CAR_PRICE']}만원")
                    # 세부정보 버튼 추가
                    if st.button("세부정보", key=f"detail_{i}_{idx}"):
                        st.session_state.selected_car = car
    else:
        st.write("차량 정보가 없습니다.")

        # --- 세부정보 표시 (추천차량 레이아웃 참고) ---
    if "selected_car" in st.session_state:
        car = st.session_state.selected_car
        st.markdown("---")
        st.markdown("<h3>차량 세부정보</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            # 차량 이미지
            image_url = car.get("CAR_IMG_URL")
            if image_url and image_url.strip().startswith("http"):
                st.image(image_url.strip(), width=300)
            else:
                st.image(dummy_image_url, width=300)

        with col2:
            # 차량 정보 헤더
            st.markdown(f"### {car.get('BRAND_NAME', '')} {car['CAR_FULL_NAME']}")
            st.markdown(f"**가격:** {car['CAR_PRICE']}만원")
            st.markdown(f"**연료:** {car.get('FUEL_TYPE_NAME', '정보 없음')}")
            st.markdown(f"**차체:** {car.get('body_type_category', '정보 없음')}")
            st.markdown(f"**연비:** {car.get('CAR_FUEL_EFFICIENCY', '정보 없음')} km/L")

    # ⭐ 차량이 있든 없든 항상 페이지네이션 표시 ⭐
    page_size = 8
    offset = (st.session_state.pagenation - 1) * page_size

    # 전체 차량 수 계산 (쿼리에서 LIMIT과 OFFSET 제거)
    total_query = make_query(
        price_range=get_price_range(selected_price) if selected_price != "전체" else None,
        min_efficiency=get_min_efficiency(selected_eff) if selected_eff != "전체" else None,
        body_type=selected_body if selected_body != "전체" else None,
        fuel_type=selected_fuel if selected_fuel != "전체" else None,
        limit=1000000,  # 큰 숫자로 설정
        offset=0
    )

    # 마지막 ORDER BY 부분과 LIMIT 부분 제거
    total_query = total_query.split("ORDER BY")[0] + "ORDER BY 1"

    conn = team_db()
    total_cars = 0
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(*) FROM ({total_query}) as t")
            total_cars = cur.fetchone()[0]
        except mysql.connector.Error as e:
            st.error(f"전체 차량 수 조회 실패: {e}")
        finally:
            conn.close()

    total_pages = (total_cars - 1) // page_size + 1

    page_block = 5
    current_block = (st.session_state.pagenation - 1) // page_block
    start_page = current_block * page_block + 1
    end_page = min(start_page + page_block - 1, total_pages)  # 최대 페이지 수 동적 계산

    st.markdown("### ")
    pagination_cols = st.columns(page_block + 2)  # 이전 버튼과 다음 버튼 포함

    # '이전' 버튼
    if start_page > 1:
        with pagination_cols[0]:
            if st.button("이전", key="car_page_prev"):
                set_pagenation(start_page - 1)
    else:
        pagination_cols[0].markdown("&nbsp;")  # 빈칸

    # 페이지 버튼들
    for idx, p in enumerate(range(start_page, end_page + 1)):
        with pagination_cols[idx + 1]:
            # 현재 페이지 강조 또는 버튼 생성
            if p == st.session_state.pagenation:
                st.markdown(f"**[{p}]**")
            else:
                if st.button(str(p), key=f"car_page_btn_{p}"):
                    set_pagenation(p)

    # '다음' 버튼
    if end_page < total_pages:
        with pagination_cols[-1]:
            if st.button("다음", key="car_page_next"):
                set_pagenation(end_page + 1)
    else:
        pagination_cols[-1].markdown("&nbsp;")  # 빈칸

# --- 리뷰와 평점 페이지 ---
elif st.session_state.page == "리뷰와 평점":
    st.header("차량 리뷰 및 평점")

    # --- 필터 UI 확장 ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_body = st.selectbox("외형", body_types, key="review_body_filter")
    with col2:
        brand_names = ["전체"] + get_distinct_values("SELECT DISTINCT BRAND_NAME FROM teamdb.BRAND_INFO")
        selected_brand = st.selectbox("브랜드", brand_names, key="review_brand_filter")
    with col3:
        price_ranges = ["전체", "1000만원대", "2000만원대", "3000만원대", "4000만원 이상"]
        selected_price = st.selectbox("가격", price_ranges, key="review_price_filter")
    with col4:
        sort_options = {
            "평점 높은 순": "cri.avg_score DESC",
            "평점 낮은 순": "cri.avg_score ASC",
            "참여 인원 많은 순": "cri.survey_people_count DESC"
        }
        selected_sort = st.selectbox("정렬 기준", list(sort_options.keys()))


    # --- 필터링 로직 ---
    def get_filtered_reviews():
        price_range = get_price_range(selected_price) if selected_price != "전체" else None

        query = """
        SELECT 
            cri.car_name,
            cri.avg_score,
            cri.survey_people_count,
            cri.graph_info,
            bi.BRAND_NAME,
            bti.body_type_category
        FROM teamdb.car_review_info cri
        JOIN teamdb.car_info ci ON cri.car_name = ci.car_full_name
        JOIN teamdb.brand_info bi ON ci.car_brand = bi.BRAND_ID
        JOIN teamdb.body_type_info bti ON ci.CAR_BODY_TYPE = bti.body_name
        WHERE 1=1
        """

        # 필터 조건
        if selected_body != "전체":
            query += f" AND bti.body_type_category = '{selected_body}'"
        if selected_brand != "전체":
            query += f" AND bi.BRAND_NAME = '{selected_brand}'"
        if price_range:
            query += f" AND ci.CAR_PRICE BETWEEN {price_range[0]} AND {price_range[1]}"

        # 정렬 조건
        query += f" ORDER BY {sort_options[selected_sort]}"

        conn = team_db()
        reviews = []
        if conn:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute(query)
                reviews = cur.fetchall()
            except mysql.connector.Error as e:
                st.error(f"리뷰 조회 실패: {e}")
                st.text_area("실행 쿼리", query)  # 오류 발생 시 쿼리 내용 출력
            finally:
                conn.close()
        return reviews


    # --- 필터 적용 후 데이터 조회 ---
    reviews = get_filtered_reviews()

    # 차량명별 중복 제거
    unique_car_reviews = {}
    for review in reviews:
        car_name = review['car_name']
        if car_name not in unique_car_reviews:
            unique_car_reviews[car_name] = review
    unique_reviews = list(unique_car_reviews.values())

    # --- 페이지네이션 설정 (기존 로직 유지) ---
    if "review_pagenation" not in st.session_state:
        st.session_state.review_pagenation = 1


    def set_review_pagenation(p):
        st.session_state.review_pagenation = p
        st.rerun()


    review_page_size = 4
    total_reviews = len(unique_reviews)
    total_review_pages = (total_reviews + review_page_size - 1) // review_page_size if total_reviews > 0 else 1

    start_idx = (st.session_state.review_pagenation - 1) * review_page_size
    end_idx = start_idx + review_page_size
    current_reviews = unique_reviews[start_idx:end_idx] if unique_reviews else []

    # --- 리뷰 목록 표시 ---
    if unique_reviews:
        for i, review in enumerate(current_reviews):
            car_name = review['car_name']
            st.markdown(f"### {car_name} ({review['BRAND_NAME']})")
            st.metric("평균 평점", f"{review['avg_score']:.1f} ⭐️")
            st.write(f"설문 참여 인원: {review['survey_people_count']}명")

            # 그래프 데이터 파싱
            graph_labels = []
            graph_scores = []
            for line in review['graph_info'].split(','):
                parts = line.strip().split('\n')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    try:
                        graph_labels.append(key)
                        graph_scores.append(float(value))
                    except ValueError:
                        continue

            # 그래프 표시
            if graph_labels and graph_scores:
                df = pd.DataFrame({
                    '항목': graph_labels,
                    '점수': graph_scores
                })
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('항목', axis=alt.Axis(labelAngle=0)),
                    y='점수'
                ).properties(width=200, height=250)
                st.altair_chart(chart, use_container_width=True)

            # 리뷰 펼치기 버튼
            if f"show_reviews_{car_name}" not in st.session_state:
                st.session_state[f"show_reviews_{car_name}"] = False

            if st.button(f"{car_name} 리뷰 전체 보기", key=f"review_btn_{i}"):
                st.session_state[f"show_reviews_{car_name}"] = not st.session_state[f"show_reviews_{car_name}"]
                st.rerun()

            # 상세 리뷰 표시
            if st.session_state[f"show_reviews_{car_name}"]:
                all_reviews = [r for r in reviews if r['car_name'] == car_name]
                for idx, r in enumerate(all_reviews, 1):
                    st.markdown(f"**[리뷰 {idx}]** 평균 평점: {r['avg_score']} / 참여: {r['survey_people_count']}명")
                    st.write(r.get('graph_info', ''))
                    st.markdown("---")

                # 댓글 표시
                comments = get_comments_by_car(car_name)
                if comments:
                    st.markdown("#### 댓글")
                    for comment in comments:
                        st.markdown(
                            f"**{comment['nickname']}** ({comment['comment_avg_score']}⭐️) - {comment['created_at']}")
                        st.write(comment['comment_text'])
                        st.markdown("---")
                else:
                    st.write("댓글이 없습니다.")

    else:
        st.info("조건에 맞는 리뷰 정보가 없습니다.")

    # --- 페이지네이션 UI (기존 로직 유지) ---
    if total_reviews > 0:
        review_page_block = 5
        current_block = (st.session_state.review_pagenation - 1) // review_page_block
        start_page = current_block * review_page_block + 1
        end_page = min(start_page + review_page_block - 1, total_review_pages)

        st.markdown("### ")
        pagination_cols = st.columns(review_page_block + 2)

        # '이전' 버튼
        if start_page > 1:
            with pagination_cols[0]:
                if st.button("이전", key="review_prev_btn"):
                    set_review_pagenation(start_page - 1)
        else:
            pagination_cols[0].markdown("&nbsp;")

        # 페이지 번호 버튼
        for idx, p in enumerate(range(start_page, end_page + 1)):
            with pagination_cols[idx + 1]:
                if p == st.session_state.review_pagenation:
                    st.markdown(f"**[{p}]**")
                else:
                    if st.button(str(p), key=f"review_page_{p}"):
                        set_review_pagenation(p)

        # '다음' 버튼
        if end_page < total_review_pages:
            with pagination_cols[-1]:
                if st.button("다음", key="review_next_btn"):
                    set_review_pagenation(end_page + 1)
        else:
            pagination_cols[-1].markdown("&nbsp;")
# --- 통계 정보 페이지(예시) ---
elif st.session_state.page == "통계 정보":
    st.header("통계 정보")
    st.info("통계 기능은 추후 제공될 예정입니다.")
