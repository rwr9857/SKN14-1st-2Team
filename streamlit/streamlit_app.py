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


# DB 연결
conn = init_db()
cur = conn.cursor(dictionary=True) if conn else None

# 스타일 설정 (폰트,버튼) - 버튼은 잘 구현된건지 모르겠음...
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
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }

    .spec-item {
        padding: 5px 0;
    }

    .spec-label {
        font-weight: bold;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# 차근차근 배경 이미지 적용 - 성공
set_background('../docs/background.png')

# 차근차근 로고 적용
st.image("../docs/logo.png", width=150)

# 사용자 입력 데이터 세션 상태 초기화
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {
        "budget_min": 0,
        "budget_max": 5000,
        "fuel_type": "",
        "body_type": "",
        "engine_type": "",
        "purpose": "",
        "preference": ""
    }

# 입력 완료 상태 체크 세션
if "input_completed" not in st.session_state:
    st.session_state.input_completed = {
        "budget": False,
        "fuel": False,
        "body": False,
        "purpose": False,
        "preference": False
    }

# 추천 차량 세션
if "recommended_cars" not in st.session_state:
    st.session_state.recommended_cars = []

# 페이지 상태관리
if "page" not in st.session_state:
    st.session_state.page = "home"


# 차량 추천 함수 - gpt
def recommend_cars():
    if not conn or not cur:
        st.error("데이터베이스 연결이 필요합니다.")
        return []

    try:
        # 사용자 입력 가져오기
        budget_min = st.session_state.user_inputs["budget_min"]
        budget_max = st.session_state.user_inputs["budget_max"]
        fuel_type = st.session_state.user_inputs["fuel_type"]
        body_type = st.session_state.user_inputs["body_type"]

        # 쿼리 작성 - 사용자 선호도에 맞는 차량 검색
        query = """
        Select c.*, b.BRAND_NAME, e.ENGINE_NAME, bt.BODY_TYPE_NAME, ft.FUEL_TYPE_NAME
        From CAR_INFO c
        join BRAND_INFO b on c.CAR_BRAND = b.BRAND_ID
        join ENGINE_INFO e on c.CAR_ENGINE_TYPE = e.ENGINE_ID
        join BODY_TYPE_INFO bt on c.CAR_BODY_TYPE = bt.BODY_TYPE_ID
        join FUEL_TYPE_INFO ft on c.CAR_FUEL_TYPE = ft.FUEL_TYPE_ID
        where c.CAR_PRICE BETWEEN %s AND %s
        """

        params = [budget_min * 10000, budget_max * 10000]

        if fuel_type:
            query += " AND ft.FUEL_TYPE_NAME = %s"
            params.append(fuel_type)

        params = [budget_min * 10000, budget_max * 10000]  # 만원 단위를 원 단위로 변환
        # 연료 타입 필터 추가
        if fuel_type:
            query += " AND e.fuel_name = %s"
            params.append(fuel_type)

        # 바디 타입 필터 추가
        if body_type:
            query += " AND bt.body_type_name = %s"
            params.append(body_type)

        # 정렬 - 가격 기준
        query += " ORDER BY c.car_price ASC LIMIT 5"

        cur.execute(query, params)
        cars = cur.fetchall()
        return cars

    except mysql.connector.Error as e:
        st.error(f"차량 추천 쿼리 실패: {e}")
        return []


# 첫 번째 페이지(찾으러 가기)
if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차, 차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")

    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("찾으러 가기", key="start_button"):
            st.session_state.page = "balance"
        st.markdown('</div>', unsafe_allow_html=True)

## 첫 페이지 끝, 두번째는 gpt 임의 작성 후 성규님과 맞추기

# 밸런스(옵션선택) 화면
elif st.session_state.page == "balance":
    selected = option_menu(
        menu_title=None,
        options=["예산 범위", "연료 타입", "바디타입", "용도 체크", "선호도"],
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

    # 예산 범위 입력
    if selected == "예산 범위":
        st.header("예산 설정")
        st.write("예산 차량 구매 예산은 어느 정도 생각하고 계신가요?")

        min_val, max_val = st.slider(
            "구매 예산 범위 설정 (단위: 만원)",
            0, 5000, (0, 5000), step=100
        )
        st.write(f"선택한 예산: **{min_val}만원 ~ {max_val}만원**")

        # 세션 상태에 저장
        st.session_state.user_inputs["budget_min"] = min_val
        st.session_state.user_inputs["budget_max"] = max_val

        # 입력 완료 상태 업데이트 - 추가
        if st.button("저장 후 다음", key="budget_save"):
            st.session_state.input_completed["budget"] = True
            st.success("예산 범위가 저장되었습니다!")

        # 연료 타입 선택
        elif selected == "연료 타입":
            st.header("연료 타입 선택")
            if cur:
                cur.execute("SELECT FUEL_TYPE_NAME FROM FUEL_TYPE_INFO")
                fuels = [row["FUEL_TYPE_NAME"] for row in cur.fetchall()]
            else:
                fuels = ["가솔린", "디젤", "하이브리드", "전기"]

            fuel = st.selectbox("선호하는 연료 타입을 선택하세요.", fuels)
            st.write(f"선택한 연료 타입: **{fuel}**")

            # 세션 상태에 저장
            st.session_state.user_inputs["fuel_type"] = fuel

            # 입력 완료 상태 업데이트 - 추가
            st.session_state.input_completed["fuel"] = True
            st.success("연료 타입이 저장되었습니다!")


        # 바디타입 선택
        elif selected == "바디타입":
            st.header("바디타입 선택")
            if cur:
                cur.execute("select BODY_TYPE_NAME FROM BODY_TYPE_INFO")
                bodies = [row["BODY_TYPE_NAME"] for row in cur.fetchall()]
            else:
                bodies = ["승용차", "SUV", "경차"]

            body = st.selectbox("선호하는 바디타입을 선택하세요.", bodies)
            st.write(f"선택한 바디타입: **{body}**")

            # 세션 상태에 저장
            st.session_state.user_inputs["body_type"] = body

            # 입력 완료 상태 업데이트 - 추가
            if st.button("저장 후 다음", key="body_save"):
                st.session_state.input_completed["body"] = True
                st.success("바디타입이 저장되었습니다!")

    # 용도 체크
    elif selected == "용도 체크":
        st.header("차량 사용 용도 체크")
        purpose = st.radio("주 사용 용도를 선택하세요.", ["출퇴근", "여행/나들이", "업무용", "주말 드라이브"], horizontal=True)
        st.write(f"선택한 용도: **{purpose}**")

        # 세션 상태에 저장
        st.session_state.user_inputs["purpose"] = purpose

        # 입력 완료 상태 업데이트 - 추가
        if st.button("저장 후 다음", key="purpose_save"):
            st.session_state.input_completed["purpose"] = True
            st.success("사용 용도가 저장되었습니다!")

    # 선호도 체크
    elif selected == "선호도":
        st.header("중요하게 생각하는 항목을 순서대로 3개 선택해주세요")
        st.write("[랭킹] 1~3 순위")

        options = ["연비(최저)", "가격(최저)", "평점(네이버 평점 기준)", "차체크기", "성능"]

        # 1순위 선택
        first = st.selectbox("1순위", options, key="rank1")
        # 2순위 선택 (1순위에서 고른 항목은 제외)
        second = st.selectbox("2순위", [o for o in options if o != first], key="rank2")
        # 3순위 선택 (1,2순위에서 고른 항목은 제외)
        third = st.selectbox("3순위", [o for o in options if o not in [first, second]], key="rank3")

        st.write(f"1순위: {first}, 2순위: {second}, 3순위: {third}")

        # 세션에 저장
        st.session_state.user_inputs["preference"] = [first, second, third]
        st.session_state.input_completed["preference"] = True

        # 입력 완료 상태 업데이트 - 추가
        st.session_state.input_completed["preference"] = True

        # 모든 항목 완료여부 확인
        all_completed = all(st.session_state.input_completed.values())

        if st.button("추천 차량 보기", disabled=not all_completed):
            # 차량 추천 로직 실행
            recommended_cars = recommend_cars()
            st.session_state.recommended_cars = recommended_cars
            st.session_state.page = "recommendation"
            st.rerun()  # 페이지 새로고침

        # 모든 항목이 완료되지 않았으면 안내 메시지 표시
        if not all_completed:
            incomplete_items = [item for item, completed in st.session_state.input_completed.items() if not completed]
            st.warning(f"다음 항목을 완료해주세요: {', '.join(incomplete_items)}")

#두번째 페이지 끝, 세번째 페이지

# 추천 결과 페이지
elif st.session_state.page == "recommendation":
    st.markdown(
        """
        <style>
        body {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1>나의 첫 차는?</h1>", unsafe_allow_html=True)

    # 추천 차량 목록이 있는지 확인
    if st.session_state.recommended_cars:
        # 추천 차량 표시
        for idx, car in enumerate(st.session_state.recommended_cars):
            with st.container():
                st.markdown(f'<div class="car-info-container">', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 2])

                with col1:
                    # 차량 이미지가 있으면 표시, 없으면 기본 이미지
                    if 'car_img_url' in car and car['car_img_url']:
                        st.image(car['car_img_url'], width=300)
                    else:
                        st.image("대체이미지주소", width=300)

                with col2:
                    # 차량 정보 헤더
                    st.markdown(f'<div class="car-info-header">{car["brand_name"]} {car["car_full_name"]}</div>',
                                unsafe_allow_html=True)

                    # 기본 정보 표시
                    st.markdown('<div class="car-specs">', unsafe_allow_html=True)

                    # 가격 정보
                    price_in_million = car['car_price'] / 10000  # 원 단위에서 만원 단위로 변환
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">가격:</span> {price_in_million:,.1f}만원</div>',
                        unsafe_allow_html=True)

                    # 연료 타입
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">연료:</span> {car["fuel_type_name"]}</div>',
                        unsafe_allow_html=True)

                    # 엔진 타입
                    st.markdown(
                        f'<div class="spec-item"><span class="spec-label">엔진:</span> {car["engine_name"]}</div>',
                        unsafe_allow_html=True)

                    # 연비
                    if 'car_fuel_efficiency' in car:
                        st.markdown(
                            f'<div class="spec-item"><span class="spec-label">연비:</span> {car["car_fuel_efficiency"]}km/L</div>',
                            unsafe_allow_html=True)

                    # 출력 (마력/토크)
                    if 'car_horsepower' in car:
                        st.markdown(
                            f'<div class="spec-item"><span class="spec-label">출력:</span> {car["car_horsepower"]}hp</div>',
                            unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # 상세 정보 버튼
                    if st.button(f"상세 정보 보기", key=f"detail_{idx}"):
                        st.session_state.selected_car = car
                        st.session_state.page = "car_detail"
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

        # 새로운 추천 받기 버튼
        if st.button("같은 조건에 다른 모델 추천 받기"):
            st.session_state.page = "balance"
            st.rerun()
    else:
        st.warning("추천 차량이 없습니다. 새로운 조건으로 다시 시도해보세요.")
        if st.button("다시 설정하기"):
            st.session_state.page = "balance"
            st.rerun()






