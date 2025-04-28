import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import altair as alt

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
        .car-info-container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

# 고유값 조회 함수
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

# 가격 범위 변환 함수
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

# 연비 범위 변환 함수
def get_min_efficiency(selected):
    if selected == "10이하":
        return 0
    elif selected == "10~15":
        return 10
    elif selected == "15이상":
        return 15
    return None

# 차량 검색 쿼리 생성 함수
def make_query(price_range=None, min_efficiency=None, body_type=None, fuel_type=None, limit=8, offset=0):
    query = """
    SELECT
        ci.car_full_name,
        bi.brand_name,
        bti.body_type_category,
        fi.fuel_type_name,
        ci.car_price,
        ci.car_fuel_efficiency,
        ci.car_img_url
    FROM teamdb.CAR_INFO ci
    JOIN teamdb.BRAND_INFO bi ON ci.car_brand = bi.brand_id
    JOIN teamdb.BODY_TYPE_INFO bti ON ci.car_body_type = bti.body_name
    JOIN teamdb.FUEL_TYPE_INFO fi ON ci.car_fuel_type = fi.fuel_type_id
    WHERE 1=1
    """
    if price_range:
        query += f" AND ci.car_price BETWEEN {price_range[0]} AND {price_range[1]}"
    if min_efficiency is not None:
        query += f" AND ci.car_fuel_efficiency >= {min_efficiency}"
    if body_type and body_type != "전체":
        query += f" AND bti.body_type_category = '{body_type}'"
    if fuel_type and fuel_type != "전체":
        query += f" AND fi.fuel_type_name = '{fuel_type}'"
    query += f" ORDER BY ci.car_price LIMIT {limit} OFFSET {offset}"
    return query

# 리뷰 요약 가져오기
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
        JOIN teamdb.CAR_INFO ci ON cri.car_name = ci.car_full_name
        """
        cur.execute(query)
        return cur.fetchall()
    finally:
        if conn:
            conn.close()

# 차량별 댓글 가져오기
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

# 페이지 설정
st.set_page_config(page_title="차근차근 - 차량 정보", layout="wide")
set_custom_styles()

# 로고 표시
st.image("../../docs/차근차근 로고.png", width=180)

# 사이드바 메뉴
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["차량 정보 조회", "리뷰와 평점", "통계 정보"])

# 필터 옵션 가져오기
body_types = ["전체"] + get_distinct_values(
    "SELECT DISTINCT bt.body_type_category FROM teamdb.body_type_info bt JOIN teamdb.car_info c ON bt.body_name = c.car_body_type"
)
fuel_types = ["전체"] + get_distinct_values(
    "SELECT DISTINCT f.fuel_type_name FROM teamdb.fuel_type_info f JOIN teamdb.car_info c ON f.fuel_type_id = c.car_fuel_type"
)

if page == "차량 정보 조회":
    # 필터 드롭다운
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        selected_body = st.selectbox("외형", body_types)
    with col2:
        selected_price = st.selectbox("가격", ["전체", "1000만원대", "2000만원대", "3000만원대", "4000만원 이상"])
    with col3:
        selected_eff = st.selectbox("연비", ["전체", "10이하", "10~15", "15이상"])
    with col4:
        selected_fuel = st.selectbox("유종", fuel_types)

    st.markdown("---")

    # 페이지네이션 상태
    if "pagenation" not in st.session_state:
        st.session_state.pagenation = 1

    def set_pagenation(p):
        st.session_state.pagenation = p
        st.rerun()

    # 차량 목록 가져오기
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

    # 차량 카드 표시
    if cars_from_db:
        for i in range(0, len(cars_from_db), 4):
            card_row = cars_from_db[i:i + 4]
            cols = st.columns(4)
            for idx, car in enumerate(card_row):
                with cols[idx]:
                    if car['car_img_url'] and car['car_img_url'].strip().startswith("http"):
                        st.image(car['car_img_url'].strip(), use_container_width=True)
                    else:
                        st.image("../../docs/대체이미지.png", use_container_width=True)
                    st.markdown(f"**{car['car_full_name']}**")
                    st.markdown(f"{car['car_price']}만원")
                    if st.button("세부정보", key=f"detail_{i}_{idx}"):
                        st.session_state.selected_car = car
    else:
        st.write("차량 정보가 없습니다.")

    # 세부정보 표시
    if "selected_car" in st.session_state:
        car = st.session_state.selected_car
        st.markdown("---")
        st.markdown("<h3>차량 세부정보</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            if car['car_img_url'] and car['car_img_url'].strip().startswith("http"):
                st.image(car['car_img_url'].strip(), width=300)
            else:
                st.image("../../docs/대체이미지.png", width=300)

        with col2:
            st.markdown(f"### {car.get('brand_name', '')} {car['car_full_name']}")
            st.markdown(f"**가격:** {car['car_price']}만원")
            st.markdown(f"**연료:** {car.get('fuel_type_name', '정보 없음')}")
            st.markdown(f"**차체:** {car.get('body_type_category', '정보 없음')}")
            st.markdown(f"**연비:** {car.get('car_fuel_efficiency', '정보 없음')} km/L")

    # 페이지네이션
    total_query = make_query(
        price_range=get_price_range(selected_price) if selected_price != "전체" else None,
        min_efficiency=get_min_efficiency(selected_eff) if selected_eff != "전체" else None,
        body_type=selected_body if selected_body != "전체" else None,
        fuel_type=selected_fuel if selected_fuel != "전체" else None,
        limit=1000000,
        offset=0
    )

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
    end_page = min(start_page + page_block - 1, total_pages)

    st.markdown("### ")
    pagination_cols = st.columns(page_block + 2)

    if start_page > 1:
        with pagination_cols[0]:
            if st.button("이전", key="car_page_prev"):
                set_pagenation(start_page - 1)
    else:
        pagination_cols[0].markdown("&nbsp;")

    for idx, p in enumerate(range(start_page, end_page + 1)):
        with pagination_cols[idx + 1]:
            if p == st.session_state.pagenation:
                st.markdown(f"**[{p}]**")
            else:
                if st.button(str(p), key=f"car_page_btn_{p}"):
                    set_pagenation(p)

    if end_page < total_pages:
        with pagination_cols[-1]:
            if st.button("다음", key="car_page_next"):
                set_pagenation(end_page + 1)
    else:
        pagination_cols[-1].markdown("&nbsp;")

elif page == "리뷰와 평점":
    st.header("차량 리뷰 및 평점")

    # 필터 UI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_body = st.selectbox("외형", body_types, key="review_body_filter")
    with col2:
        brand_names = ["전체"] + get_distinct_values("SELECT DISTINCT brand_name FROM teamdb.BRAND_INFO")
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

    # 리뷰 필터링
    def get_filtered_reviews():
        price_range = get_price_range(selected_price) if selected_price != "전체" else None

        query = """
        SELECT 
            cri.car_name,
            cri.avg_score,
            cri.survey_people_count,
            cri.graph_info,
            bi.brand_name,
            bti.body_type_category
        FROM teamdb.car_review_info cri
        JOIN teamdb.car_info ci ON cri.car_name = ci.car_full_name
        JOIN teamdb.brand_info bi ON ci.car_brand = bi.brand_id
        JOIN teamdb.body_type_info bti ON ci.car_body_type = bti.body_name
        WHERE 1=1
        """

        if selected_body != "전체":
            query += f" AND bti.body_type_category = '{selected_body}'"
        if selected_brand != "전체":
            query += f" AND bi.brand_name = '{selected_brand}'"
        if price_range:
            query += f" AND ci.car_price BETWEEN {price_range[0]} AND {price_range[1]}"

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
            finally:
                conn.close()
        return reviews

    reviews = get_filtered_reviews()

    # 차량명별 중복 제거
    unique_car_reviews = {}
    for review in reviews:
        car_name = review['car_name']
        if car_name not in unique_car_reviews:
            unique_car_reviews[car_name] = review
    unique_reviews = list(unique_car_reviews.values())

    # 페이지네이션 설정
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

    # 리뷰 목록 표시
    if unique_reviews:
        for i, review in enumerate(current_reviews):
            car_name = review['car_name']
            st.markdown(f"### {car_name} ({review['brand_name']})")
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

    # 페이지네이션 UI
    if total_reviews > 0:
        review_page_block = 5
        current_block = (st.session_state.review_pagenation - 1) // review_page_block
        start_page = current_block * review_page_block + 1
        end_page = min(start_page + review_page_block - 1, total_review_pages)

        st.markdown("### ")
        pagination_cols = st.columns(review_page_block + 2)

        if start_page > 1:
            with pagination_cols[0]:
                if st.button("이전", key="review_prev_btn"):
                    set_review_pagenation(start_page - 1)
        else:
            pagination_cols[0].markdown("&nbsp;")

        for idx, p in enumerate(range(start_page, end_page + 1)):
            with pagination_cols[idx + 1]:
                if p == st.session_state.review_pagenation:
                    st.markdown(f"**[{p}]**")
                else:
                    if st.button(str(p), key=f"review_page_{p}"):
                        set_review_pagenation(p)

        if end_page < total_review_pages:
            with pagination_cols[-1]:
                if st.button("다음", key="review_next_btn"):
                    set_review_pagenation(end_page + 1)
        else:
            pagination_cols[-1].markdown("&nbsp;")

elif page == "통계 정보":
    st.header("통계 정보")
    st.info("통계 기능은 추후 제공될 예정입니다.")

# 저작권 표시
st.markdown("""
    <div class="copyright">
    Copyright 2025. Chageun. All rights reserved.
    </div>
""", unsafe_allow_html=True) 