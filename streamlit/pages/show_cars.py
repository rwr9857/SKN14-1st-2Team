import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

def init_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET", "utf8mb4"),
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"DB 연결 실패: {e}")
        return None

# --- 필터용 고유값 조회 함수 ---
def get_distinct_values(query):
    conn = init_db()
    if conn is None:
        return []
    try:
        cur = conn.cursor()
        cur.execute(query)
        return [row[0] for row in cur.fetchall() if row[0] is not None]
    finally:
        conn.close()

body_types = ["전체"] + get_distinct_values("SELECT BODY_TYPE_NAME FROM teamdb.BODY_TYPE_INFO")
fuel_types = ["전체"] + get_distinct_values("SELECT FUEL_TYPE_NAME FROM teamdb.FUEL_TYPE_INFO")
model_types = ["전체"] + get_distinct_values("SELECT MODEL_TYPE_NAME FROM teamdb.MODEL_TYPE_INFO")


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

# --- 로고 및 타이틀 ---
try:
    logo_image = Image.open("차근차근 로고.png")
    st.image(logo_image, width=100)
except FileNotFoundError:
    st.error("로고 이미지를 찾을 수 없습니다.")


# --- 차량 정보 조회 페이지 ---
if st.session_state.page == "차량 정보 조회":
    # --- 필터 드롭다운 ---
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        selected_body = st.selectbox("외형", body_types)
    with col2:
        selected_price = st.selectbox("가격", ["전체", "1000만원대", "2000만원대", "3000만원대", "4000만원 이상"])
    with col3:
        selected_model = st.selectbox("차종", model_types)
    with col4:
        selected_eff = st.selectbox("연비", ["전체", "10이하", "10~15", "15이상"])
    with col5:
        selected_fuel = st.selectbox("유종", fuel_types)

    st.markdown("---")

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

    def get_min_efficiency(selected):
        if selected == "10이하":
            return 0
        elif selected == "10~15":
            return 10
        elif selected == "15이상":
            return 15
        return None

    # --- make_query 함수 ---
    def make_query(price_range=None, min_efficiency=None, body_type=None, model_type=None, fuel_type=None, limit=8, offset=0):
        query = """
        SELECT
            c.CAR_ID,
            c.CAR_FULL_NAME,
            b.BRAND_NAME,
            m.MODEL_TYPE_NAME,
            bt.BODY_TYPE_NAME,
            f.FUEL_TYPE_NAME,
            c.CAR_PRICE,
            c.CAR_FUEL_EFFICIENCY,
            c.CAR_IMG_URL
        FROM teamdb.CAR_INFO c
        JOIN teamdb.BRAND_INFO b ON c.CAR_BRAND = b.BRAND_ID
        JOIN teamdb.MODEL_TYPE_INFO m ON c.CAR_MODEL = m.MODEL_TYPE_ID
        JOIN teamdb.BODY_TYPE_INFO bt ON c.CAR_BODY_TYPE = bt.BODY_TYPE_ID
        JOIN teamdb.FUEL_TYPE_INFO f ON c.CAR_FUEL_TYPE = f.FUEL_TYPE_ID
        WHERE 1=1
        """
        if price_range:
            query += f" AND c.CAR_PRICE BETWEEN {price_range[0]} AND {price_range[1]}"
        if min_efficiency is not None:
            query += f" AND c.CAR_FUEL_EFFICIENCY >= {min_efficiency}"
        if body_type and body_type != "전체":
            query += f" AND bt.BODY_TYPE_NAME = '{body_type}'"
        if model_type and model_type != "전체":
            query += f" AND m.MODEL_TYPE_NAME = '{model_type}'"
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
        model_type=selected_model if selected_model != "전체" else None,
        fuel_type=selected_fuel if selected_fuel != "전체" else None,
        limit=page_size,
        offset=offset
    )

    conn = init_db()
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
            card_row = cars_from_db[i : i + 4]
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
    else:
        st.write("차량 정보가 없습니다.")

    # --- 페이지네이션 버튼 ---
    st.markdown("### ")
    pagination_cols = st.columns(5)
    for i in range(5):
        with pagination_cols[i]:
            if st.button(str(i + 1)):
                set_pagenation(i + 1)

# --- 리뷰와 평점 페이지(추후 구현) ---
elif st.session_state.page == "리뷰와 평점":
    st.header("차량 리뷰 및 평점")
    st.info("차량별 리뷰 및 평점 데이터는 추후 제공될 예정입니다.")
    # 추후: 차량 리스트, 각 차량별 리뷰/평점 표시

# --- 통계 정보 페이지(예시) ---
elif st.session_state.page == "통계 정보":
    st.header("통계 정보")
    st.info("통계 기능은 추후 제공될 예정입니다.")


