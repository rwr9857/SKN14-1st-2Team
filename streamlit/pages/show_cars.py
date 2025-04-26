import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()


# db 초기화 함수
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


# DB 연결
conn = init_db()
cur = conn.cursor(dictionary=True) if conn else None


# 페이지별 차량 정보 가져오는 함수
def get_cars_by_page(page: int, page_size: int = 8):
    offset = (page - 1) * page_size
    query = """
        SELECT * FROM car_info
        LIMIT %s OFFSET %s
    """

    conn = init_db()
    if conn is None:
        return []

    cars = []
    try:
        cur = conn.cursor(dictionary=True)  # 딕셔너리 형태로 반환
        cur.execute(query, (page_size, offset))
        rows = cur.fetchall()

        for row in rows:
            # 필드 수가 부족하면 빈 값으로 채움
            if len(row) < 10:
                row = {**row, **{f"field_{i+1}": "" for i in range(len(row), 10)}}
            cars.append(row)  # 딕셔너리 형태로 반환
    except mysql.connector.Error as e:
        st.error(f"쿼리 실행 실패: {e}")
    finally:
        conn.close()

    return cars


# 페이지 설정
st.set_page_config(
    # page_title="차근차근", layout="centered", initial_sidebar_state="collapsed"
    page_title="차근차근",
)

st.sidebar.title("메뉴")

st.sidebar.button("차량 정보 조회")
st.sidebar.button("통계 정보")
st.sidebar.button("리뷰와 평점")

# 상단 로고와 제목
st.markdown(
    "<h1 style='text-align: center; color: #005f4b;'>차근차근</h1>",
    unsafe_allow_html=True,
)
st.markdown("##", unsafe_allow_html=True)

# 페이지네이션 상태
if "pagenation" not in st.session_state:
    st.session_state.pagenation = 1  # 기본 페이지는 1로 설정
else:
    st.session_state.pagenation = int(st.session_state.pagenation)


# 페이지 버튼 콜백
def set_pagenation(p):
    # 페이지를 설정하고 새로 고침
    st.session_state.pagenation = p
    st.rerun()  # 페이지 새로고침


# 필터 드롭다운
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    st.selectbox("외형", ["전체", "경차", "승용차", "SUV", "기타"])
with col2:
    st.selectbox("가격", ["전체", "TEST", "TEST", "TEST"])
with col3:
    st.selectbox("차종", ["전체", "TEST", "TEST", "TEST"])
with col4:
    st.selectbox("연비", ["전체", "TEST", "TEST", "TEST"])
with col5:
    st.selectbox("유종", ["전체", "가솔린", "디젤", "하이브리드", "전기"])

st.markdown("---")

# 차량 목록 가져오기
cars_from_db = get_cars_by_page(st.session_state.pagenation)

# 더미 이미지
dummy_image_url = (
    "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png"
)

# 차량 카드 표시
if cars_from_db:
    for i in range(0, len(cars_from_db), 4):  # 4개씩 카드로 나누기
        card_row = cars_from_db[i : i + 4]  # 한 줄에 4개의 카드
        cols = st.columns(4)  # 4개의 열 생성
        for idx, car in enumerate(card_row):
            with cols[idx]:  # 각 열에 카드 표시
                st.image(dummy_image_url, use_container_width=True)  # 더미 이미지
                st.markdown(f"**{car['CAR_FULL_NAME']}**")
                st.markdown(f"{car['CAR_PRICE']}만원")
else:
    st.write("차량 정보가 없습니다.")

# 페이지네이션 버튼
st.markdown("### ")
pagination_cols = st.columns(5)
for i in range(5):
    with pagination_cols[i]:
        if st.button(str(i + 1)):
            set_pagenation(i + 1)
