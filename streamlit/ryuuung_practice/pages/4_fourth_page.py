import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
import altair as alt

# 환경변수 로드
load_dotenv()

def get_star_rating(score):
    """
    10점 만점을 5개의 별로 변환
    ★ : 채워진 별
    ☆ : 빈 별
    """
    max_stars = 5
    stars_score = (score / 10) * 5  # 10점 만점을 5점 만점으로 변환
    full_stars = int(stars_score)  # 온전한 별의 개수
    empty_stars = max_stars - full_stars  # 빈 별의 개수
    
    return "★" * full_stars + "☆" * empty_stars

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
        .car-title {
            color: #02584B;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            padding-top: 20px;
            border-bottom: 2px solid #F6C248;
        }
        .review-stats {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        .review-metric {
            font-size: 18px;
            font-weight: bold;
            color: #F6C248;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .star-rating {
            color: #F6C248;
            font-size: 20px;
            letter-spacing: 2px;
        }
        .star-empty {
            color: #ddd;
        }
        .participant-count {
            color: #666;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .graph-container {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .review-button {
            margin-top: 10px;
        }
        .review-button button {
            background-color: #F6C248 !important;
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            font-size: 14px !important;
        }
        .review-button button:hover {
            background-color: #e5b43c !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }
        .comment-section {
            margin-top: 20px;
            padding: 20px;
       
            border-radius: 10px;
        }
        .comment-card {
            background-color: white;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 3px solid #F6C248;
        }
        .comment-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            color: #666;
            font-size: 14px;
        }
        .comment-content {
            color: #333;
            line-height: 1.5;
        }
        .graph-title {
            font-size: 16px;
            font-weight: bold;
            color: #02584B;
            margin-bottom: 10px;
            text-align: center;
        }
        .rating-box {
            background-color: white;
            padding: 10px;
            padding-left: 40px;
            border-radius: 8px;
            text-align: center;
            max-width: 200px;
            margin-bottom: 20px;
        }
        .average-score {
            font-size: 36px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .participant-count {
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }
        .rating-description {
            color: #666;
            font-size: 13px;
            line-height: 1.4;
            text-align: center;
        }
        .star-rating {
            color: #F6C248;
            font-size: 24px;
            letter-spacing: 2px;
            margin: 10px 0;
        }
        .car-image-container {
            width: 100%;
            max-height: 250px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .car-image-container img {
            width: 100%;
            height: auto;
            object-fit: contain;
            vertical-align: middle;
        }
        .st-emotion-cache-16tyu1 h2 {
            font-size: 1.5rem;
        }
        .image-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        .review-button {
            margin-top: 0 !important;
        }
        .review-button button {
            background-color: #F6C248 !important;
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            font-size: 14px !important;
            width: 100% !important;
        }
        .review-button button:hover {
            background-color: #e5b43c !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }
        .age-group-container {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .car-rank {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }
        .rank-label {
            font-weight: bold;
            color: #02584B;
            min-width: 30px;
        }
        .car-info {
            flex-grow: 1;
        }
        .age-title {
            color: #02584B;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #F6C248;
        }
        .car-rank-container {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin-top: 15px;
        }
        .car-rank {
            flex: 1;
            text-align: center;
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-image {
            width: 100%;
            height: 150px;
            object-fit: contain;
            margin-top: 10px;
        }
        .age-column {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            height: 100%;
        }
        .car-rank {
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .rank-label {
            font-weight: bold;
            color: #02584B;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .car-info {
            margin: 10px 0;
            text-align: center;
        }
        .car-image {
            width: 100%;
            height: 150px;
            object-fit: contain;
            margin-top: 10px;
        }
        .age-title {
            color: #02584B;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #F6C248;
            text-align: center;
        }
        .age-row {
            background-color: #EDF3F9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .age-label {
            color: #02584B;
            font-size: 28px;
            font-weight: bold;
            margin-right: 30px;
            min-width: 80px;
        }
        .cars-container {
            display: flex;
            align-items: center;
            gap: 30px;
        }
        .car-list {
            display: flex;
            gap: 30px;
            flex-grow: 1;
        }
        .car-item {
            flex: 1;
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: relative;
        }
        .car-image {
            width: 100%;
            height: 120px;
            object-fit: contain;
            margin-bottom: 10px;
        }
        .car-rank {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #F6C248;
            color: white;
            padding: 3px 15px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
  
        .car-name {
            font-weight: bold;
            color: #333;
            margin: 10px 0 5px 0;
            font-size: 15px;
        }
        .car-count {
            color: #666;
            font-size: 13px;
        }
        .rank-divider {
            width: 30px;
            height: 2px;
            background-color: #ddd;
            margin: 0 10px;
        }
        .age-stats-container {
            background-color: #EDF3F9;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding-top: 20px;
        }
        .st-emotion-cache-16tyu1 h3 {
            font-size: 1.2rem;
            padding: 2rem 0px 1rem;
        }
        
        p, ol, ul, dl {
        
        }
        
        .age-group-title {
            color: #02584B;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .car-card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: relative;
            min-height: 280px;
            display: flex;
            flex-direction: column;
        }
        .car-rank-badge {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #F6C248;
            color: white;
            padding: 3px 15px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-image {
            width: 100%;
            height: 120px;
            object-fit: contain;
            margin: 10px 0;
        }
        .car-title {
            font-weight: bold;
            color: #333;
            margin: 10px 0 5px 0;
            font-size: 15px;
            text-align: center;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .car-count {
            color: #666;
            font-size: 13px;
            text-align: center;
        }
        .gender-stats-table {
            font-size: 14px;
            margin-top: 15px;
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
        SELECT DISTINCT
            ci.nickname,
            ci.comment_avg_score,
            ci.comment_text,
            ci.created_at
        FROM (
            SELECT 
                nickname,
                comment_avg_score,
                comment_text,
                created_at,
                review_id,
                ROW_NUMBER() OVER (
                    PARTITION BY nickname, comment_text
                    ORDER BY created_at DESC
                ) as rn
            FROM teamdb.comment_info
        ) ci
        JOIN teamdb.car_review_info cri ON cri.review_id = ci.review_id
        WHERE cri.car_name = %s AND ci.rn = 1
        ORDER BY ci.created_at DESC
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
        SELECT DISTINCT
            cri.car_name,
            cri.avg_score,
            cri.survey_people_count,
            cri.graph_info,
            bi.brand_name,
            bti.body_type_category,
            ci.car_price
        FROM teamdb.car_review_info cri
        JOIN (
            SELECT car_full_name, car_brand, car_body_type, car_price
            FROM teamdb.car_info
            GROUP BY car_full_name, car_brand, car_body_type, car_price
        ) ci ON cri.car_name = ci.car_full_name
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
            
            # 차량 제목
            st.markdown(f'<div class="car-title">{car_name} ({review["brand_name"]})</div>', unsafe_allow_html=True)
            
            # 리뷰 통계와 그래프
            col1, col2, col3 = st.columns([1, 1, 1.5])
            
            # 자동차 이미지 (왼쪽)
            with col1:
                # 자동차 이미지 URL 가져오기
                conn = team_db()
                car_img_url = None
                if conn:
                    try:
                        cur = conn.cursor(dictionary=True)
                        cur.execute("SELECT car_img_url FROM teamdb.CAR_INFO WHERE car_full_name = %s LIMIT 1", (car_name,))
                        result = cur.fetchone()
                        if result:
                            car_img_url = result['car_img_url']
                    finally:
                        conn.close()

                st.markdown('''
                    <style>
                    .car-image-container {
                        width: 100%;
                        max-height: 250px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        overflow: hidden;
                        border-radius: 8px;
                        margin-bottom: 10px;
                    }
                    .car-image-container img {
                        width: 100%;
                        height: auto;
                        object-fit: contain;
                        vertical-align: middle;
                    }
                    .image-wrapper {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: flex-start;
                        background-color: white;
                        border-radius: 8px;
                        padding: 20px;
                        margin-top: 20px;
                    }
                    div[data-testid="stButton"] {
                        width: 100%;
                        margin-top: 0 !important;
                    }
                    div[data-testid="stButton"] button {
                        background-color: #F6C248 !important;
                        color: white !important;
                        padding: 8px 16px !important;
                        border-radius: 8px !important;
                        border: none !important;
                        font-weight: bold !important;
                        transition: all 0.3s ease !important;
                        font-size: 14px !important;
                        width: 100% !important;
                    }
                    div[data-testid="stButton"] button:hover {
                        background-color: #e5b43c !important;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
                    }
                    </style>
                ''', unsafe_allow_html=True)

                # 이미지와 버튼을 포함하는 컨테이너
                with st.container():
                    if car_img_url and car_img_url.strip().startswith("http"):
                        st.markdown(f'''
                            <div class="image-wrapper">
                                <div class="car-image-container">
                                    <img src="{car_img_url.strip()}" alt="{car_name}">
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="image-wrapper">
                                <div class="car-image-container">
                                    <img src="../../docs/대체이미지.png" alt="대체 이미지">
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    # 리뷰 버튼
                    if st.button("댓글 확인하러가기", key=f"review_btn_{i}"):
                        st.session_state[f"show_reviews_{car_name}"] = not st.session_state.get(f"show_reviews_{car_name}", False)
                        st.rerun()
            
            # 평점 정보 (중앙)
            with col2:
                avg_score = review["avg_score"]
                stars = get_star_rating(avg_score)
                st.markdown(f'''
                    <div class="rating-box">
                        <div class="average-score">{avg_score:.1f}</div>
                        <div class="participant-count">{review["survey_people_count"]}명 참여</div>
                        <div class="rating-description">
                            이 모델을 소유한<br>
                            오너들이 마이카에 등록한<br>
                            본인차의 평가점수입니다
                        </div>
                        <div class="star-rating">{stars}</div>
                    </div>
                ''', unsafe_allow_html=True)
            
            # 그래프 (오른쪽)
            with col3:
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

                if graph_labels and graph_scores:
                    # 레이더 차트를 위해 첫번째 값을 마지막에 한번 더 추가 (차트를 닫기 위해)
                    graph_labels.append(graph_labels[0])
                    graph_scores.append(graph_scores[0])
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=graph_scores,
                        theta=graph_labels,
                        fill='toself',
                        fillcolor='rgba(246, 194, 72, 0.3)',
                        line=dict(color='#F6C248', width=2),
                        hovertemplate='%{theta}: %{r:.1f}점<extra></extra>'
                    ))

                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 10],
                                showline=False,
                                gridcolor='#f0f0f0',
                                tickformat='.1f'
                            ),
                            angularaxis=dict(
                                gridcolor='#f0f0f0'
                            ),
                            bgcolor='white'
                        ),
                        title={
                            'text': '상세 평가',
                            'y': 0.95,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'size': 16, 'color': '#02584B'}
                        },
                        showlegend=False,
                        margin=dict(l=20, r=20, t=40, b=20),
                        height=250,
                        width=300
                    )

                    st.plotly_chart(fig, use_container_width=False, config={'displayModeBar': False})

            # 댓글 섹션
            if st.session_state.get(f"show_reviews_{car_name}", False):
                st.markdown('<div class="comment-section">', unsafe_allow_html=True)
                comments = get_comments_by_car(car_name)
                if comments:
                    st.markdown("#### 사용자 댓글")
                    for comment in comments:
                        st.markdown(f'''
                            <div class="comment-card">
                                <div class="comment-header">
                                    <span><strong>{comment['nickname']}</strong> ({comment['comment_avg_score']}⭐️)</span>
                                    <span>{comment['created_at']}</span>
                                </div>
                                <div class="comment-content">
                                    {comment['comment_text']}
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.info("아직 댓글이 없습니다.")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
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
    st.header("🚗 통계 정보")

    def load_statistics():
        conn = team_db()
        if conn is None:
            return pd.DataFrame()
        try:
            query = """
                SELECT
                    u.user_age,
                    u.user_gender,
                    j.job_name,
                    c.car_full_name
                FROM teamdb.car_recommendation_info r
                JOIN teamdb.user_info u ON r.user_id = u.user_id
                JOIN teamdb.car_info c ON r.car_id = c.car_id
                LEFT JOIN teamdb.job_type_info j ON u.user_job = j.job_id
            """
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            st.error(f"통계 데이터 불러오기 실패: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

    stats_df = load_statistics()

    if stats_df.empty:
        st.info("아직 추천받은 기록이 없습니다.")
    else:
        ### 연령별 통계
        st.subheader("📊 연령대별 선호 차량 분석")
        
        # 연령대 그룹핑
        stats_df['age_group'] = pd.cut(
            stats_df['user_age'],
            bins=[0, 29, 39, 49, 100],
            labels=['20대', '30대', '40대', '50대 이상']
        )

        # 연령대별 데이터를 한 번에 처리
        age_groups = ['20대', '30대', '40대']
        
        # 3개의 열 생성
        cols = st.columns(3)
        
        for idx, age in enumerate(age_groups):
            with cols[idx]:
                age_data = stats_df[stats_df['age_group'] == age]
                if not age_data.empty:
                    st.markdown(f'''
                        <div class="age-stats-container">
                            <div class="age-group-title">{age}</div>
                            <div style="display: flex; flex-direction: column; gap: 15px;">
                    ''', unsafe_allow_html=True)
                    
                    # 상위 3개 차량 추출
                    top_cars = (
                        age_data.groupby('car_full_name')
                        .size()
                        .reset_index(name='count')
                        .sort_values('count', ascending=False)
                        .head(3)
                    )

                    for rank, (_, car) in enumerate(top_cars.iterrows(), 1):
                        # 차량 이미지 URL 가져오기
                        conn = team_db()
                        car_img_url = None
                        if conn:
                            try:
                                cur = conn.cursor(dictionary=True)
                                cur.execute(
                                    "SELECT car_img_url FROM teamdb.CAR_INFO WHERE car_full_name = %s LIMIT 1",
                                    (car['car_full_name'],)
                                )
                                result = cur.fetchone()
                                if result:
                                    car_img_url = result['car_img_url']
                            finally:
                                conn.close()

                        st.markdown(f'''
                            <div class="car-card">
                                <div class="car-rank-badge">
                                    {rank}위
                                </div>
                                <img src="{car_img_url.strip() if car_img_url and car_img_url.strip().startswith('http') else '../../docs/대체이미지.png'}" 
                                     class="car-image">
                                <div class="car-title">
                                    {car['car_full_name']}
                                </div>
                                <div class="car-count">
                                    추천 수: {car['count']}건
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)

                    st.markdown('''
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

        ### 성별별 통계
        st.subheader("📊 성별별 선호 차량")

        # 성별 데이터를 한 번에 처리하기 위한 컬럼 생성
        gender_cols = st.columns(2)
        
        genders = stats_df['user_gender'].dropna().unique()
        for idx, gender in enumerate(genders):
            with gender_cols[idx]:
                gender_data = stats_df[stats_df['user_gender'] == gender]
                if not gender_data.empty:
                    top_cars = (
                        gender_data.groupby('car_full_name')
                        .size()
                        .reset_index(name='count')
                        .sort_values('count', ascending=False)
                        .head(5)
                    )

                    st.markdown(f"#### {gender}")
                    chart = alt.Chart(top_cars).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta('count:Q', title='추천 수'),
                        color=alt.Color('car_full_name:N', title='차량명',
                                      scale=alt.Scale(scheme='category20')),  # 색상 스키마 추가
                        tooltip=['car_full_name:N', 'count:Q']
                    ).properties(
                        width=300,
                        height=300,
                        title=f"{gender} 선호 차량 TOP 5"
                    )
                    st.altair_chart(chart, use_container_width=True)

                    # 상세 데이터 테이블 추가
                    st.markdown("""
                        <style>
                        .gender-stats-table {
                            font-size: 14px;
                            margin-top: 15px;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="gender-stats-table">', unsafe_allow_html=True)
                    for idx, row in top_cars.iterrows():
                        st.markdown(f"**{idx+1}위**: {row['car_full_name']} ({row['count']}건)")
                    st.markdown('</div>', unsafe_allow_html=True)

        ### 직업별 통계
        st.subheader("📊 직업별 선호 차량")

        # 데이터 준비
        jobs_order = ['대학생', '사무직', 'IT/개발', '서비스직', '생산직', '기타']

        job_car = (
            stats_df.groupby(['job_name', 'car_full_name'])
            .size()
            .reset_index(name='count')
        )

        top3_job_car = (
            job_car.sort_values(['job_name', 'count'], ascending=[True, False])
            .groupby('job_name')
            .head(3)
        )

        # 직업명 순서 고정
        top3_job_car['job_name'] = pd.Categorical(top3_job_car['job_name'], categories=jobs_order, ordered=True)
        top3_job_car = top3_job_car.sort_values(['job_name'])

        # offset 생성
        offset_list = []
        offset_counter = 0
        for job in jobs_order:
            count = top3_job_car[top3_job_car['job_name'] == job].shape[0]
            offset_list.extend([offset_counter + i for i in range(count)])
            offset_counter += count + 4  # 간격

        top3_job_car['offset'] = offset_list

        # 직업명 레이블용 데이터
        job_labels = top3_job_car.groupby('job_name').first().reset_index()[['job_name', 'offset']]

        # Altair 시각화
        labels_chart = alt.Chart(job_labels).mark_text(
            align='right',
            baseline='middle',
            dx=-5,
            fontSize=13,
            fontWeight='bold'
        ).encode(
            y=alt.Y('offset:O', axis=None),
            text='job_name:N'
        ).properties(width=100)

        bars = alt.Chart(top3_job_car).mark_bar(size=16).encode(
            y=alt.Y('offset:O', axis=None),
            x=alt.X('count:Q', title='추천 수'),
            color=alt.Color('car_full_name:N', legend=None),
            tooltip=[
                alt.Tooltip('job_name:N', title='직업'),
                alt.Tooltip('car_full_name:N', title='차량'),
                alt.Tooltip('count:Q', title='추천 수')
            ]
        ).properties(width=600)

        text_car = alt.Chart(top3_job_car).mark_text(
            align='left',
            baseline='middle',
            dx=5,
            fontSize=11
        ).encode(
            y='offset:O',
            x='count:Q',
            text='car_full_name:N'
        )

        full_chart = alt.hconcat(labels_chart, bars + text_car).resolve_scale(y='shared')
        st.altair_chart(full_chart, use_container_width=True)

# 저작권 표시
st.markdown("""
    <div class="copyright">
    Copyright 2025. Chageun. All rights reserved.
    </div>
""", unsafe_allow_html=True) 