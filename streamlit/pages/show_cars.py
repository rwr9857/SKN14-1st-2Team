import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()


def team_db():
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

# --- 로고 및 타이틀 ---
try:
    logo_image = Image.open("차근차근 로고.png")
    st.image(logo_image, width=100)
except FileNotFoundError:
    st.error("로고 이미지를 찾을 수 없습니다.")


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
        FROM comment_info ci
        JOIN car_review_info cri ON cri.review_id = ci.review_id
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


# --- 차량 정보 조회 페이지 ---
if st.session_state.page == "차량 정보 조회":
    # --- 필터 드롭다운 ---
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        selected_body = st.selectbox("외형", body_types)
    with col2:
        selected_price = st.selectbox("가격", ["전체", "1000만원대", "2000만원대", "3000만원대", "4000만원 이상"])
    with col3:
        selected_eff = st.selectbox("연비", ["전체", "10이하", "10~15", "15이상"])
    with col4:
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
        JOIN teamdb.BRAND_INFO b ON c.brand_id = b.BRAND_ID
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

    else:
        st.write("차량 정보가 없습니다.")

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

    reviews = get_review_summary()

    # 리뷰 페이지네이션 상태
    if "review_pagenation" not in st.session_state:
        st.session_state.review_pagenation = 1


    def set_review_pagenation(p):
        st.session_state.review_pagenation = p
        st.rerun()


    # 페이지네이션 설정
    review_page_size = 4  # 한 페이지에 보여줄 리뷰 수
    total_reviews = len(reviews)
    total_review_pages = (total_reviews + review_page_size - 1) // review_page_size if total_reviews > 0 else 1

    # 현재 페이지에 표시할 리뷰 계산
    start_idx = (st.session_state.review_pagenation - 1) * review_page_size
    end_idx = start_idx + review_page_size
    current_reviews = reviews[start_idx:end_idx] if reviews else []

    if reviews:
        # 현재 페이지의 리뷰만 표시
        for i, review in enumerate(current_reviews):
            cols = st.columns(1)  # 1열만
            with cols[0]:
                st.markdown(f"### {review['car_name']}")
                st.metric("평균 평점", f"{review['avg_score']:.1f} ⭐️")
                st.write(f"설문 참여 인원: {review['survey_people_count']}명")

                # 그래프
                graph_data = {}
                for line in review['graph_info'].split(','):
                    parts = line.strip().split('\n')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        try:
                            graph_data[key] = float(value)
                        except ValueError:
                            continue

                if graph_data:
                    st.bar_chart(graph_data)

                # 댓글 보기 상태 관리
                if f"show_comments_{review['car_name']}" not in st.session_state:
                    st.session_state[f"show_comments_{review['car_name']}"] = False

                # 댓글 보기 버튼
                if st.button(f"{review['car_name']} 댓글 보기", key=f"review_comment_{i}"):
                    st.session_state[f"show_comments_{review['car_name']}"] = not st.session_state[
                        f"show_comments_{review['car_name']}"]
                    st.rerun()

                # 댓글 표시
                if st.session_state[f"show_comments_{review['car_name']}"]:
                    comments = get_comments_by_car(review['car_name'])
                    if comments:
                        for comment in comments:
                            st.markdown(
                                f"**{comment['nickname']}** ({comment['comment_avg_score']}⭐️) - {comment['created_at']}")
                            st.write(comment['comment_text'])
                            st.markdown("---")
                    else:
                        st.write("댓글이 없습니다.")
    else:
        st.info("리뷰 정보가 없습니다.")

    # --- 리뷰 페이지네이션 표시 ---
    if total_reviews > 0:
        review_page_block = 5
        current_block = (st.session_state.review_pagenation - 1) // review_page_block
        start_page = current_block * review_page_block + 1
        end_page = min(start_page + review_page_block - 1, total_review_pages)

        st.markdown("### ")
        pagination_cols = st.columns(review_page_block + 2)  # 이전, 페이지번호들, 다음

        # '이전' 버튼
        if start_page > 1:
            with pagination_cols[0]:
                if st.button("이전", key="review_prev_btn"):
                    set_review_pagenation(start_page - 1)
        else:
            pagination_cols[0].markdown("&nbsp;")

        # 페이지 번호 버튼들
        for idx, p in enumerate(range(start_page, end_page + 1)):
            with pagination_cols[idx + 1]:
                # 현재 페이지 강조 또는 버튼 생성
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
