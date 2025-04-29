import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import base64
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
        .close-button-container {
            position: absolute;
            top: 1rem;
            right: 1rem;
            z-index: 999999;
        }
        .close-button {
            width: 32px;
            height: 32px;
            background-color: #02584B;
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
            padding: 0;
            line-height: 1;
            text-decoration: none;
        }
        .close-button:hover {
            background-color: #036b5f;
            text-decoration: none;
            color: white;
        }
        .option-menu {
            background-color: #F8B94A;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .option-menu-item {
            color: #333;
        }
        .option-menu-item:hover {
            color: #EEB437;
        }
        .option-menu-item.active {
            color: #EEB437;
            font-weight: bold;
        }
        .section-title {
            color: #EEB437;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
            font-size: 20px;
        }
        .option-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 10px 0;
        }
        .option-button {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .option-button:hover {
            background-color: #FFF9E6;
            border-color: #EEB437;
        }
        .option-button.selected {
            background-color: #FFF9E6;
            border-color: #EEB437;
            color: #EEB437;
            font-weight: bold;
        }
        .stButton button {
            background-color: #EEB437;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            width: 100%; 
        }
        
        .st-emotion-cache-ocsh0s {
            min-height: 0rem;
        }
        .st-emotion-cache-180ybpv {
            flex : 1;
        }
        
        .st-emotion-cache-10c9vv9 {
            display: flex;
            background-color: #F6C248;
            width: 30px;
            height: 30px;
            justify-content: center;
            align-items: center;
            border-radius: 50%;
        }
       
        
        .st-emotion-cache-16tyu1 a {
            color: WHITE !important;
            text-decoration: none !important;
        }
        .stButton button:hover {
            background-color: #d69c2e;
        }
        .stProgress > div > div {
            background-color: #EEB437;
        }
        .sidebar-content {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .car-card {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #EEB437;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .car-title-container {
            padding: 0 50px;
            width: 100%;
        }
        .car-title {
            color: white;
            font-weight: bold;
            text-align: center;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            padding: 0.5rem 1rem;
            background-color: #EEB437;
            display: block;
        }
        .st-emotion-cache-16tyu1 h3 {
            padding: 0.2rem 0px 0.2rem;
            width: 100%;
            display: flex;
            justify-content: center;
        }
        .car-info {
            color: #333;
            margin-bottom: 5px;
        }
        
        .car-subtitle {
            font-size: 1.8rem;
            color: #02584B;
            margin-bottom: 2rem;
            background-color: #f8d66d;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            display: inline-block;
        }
        .car-image {
            text-align: center;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 70px;
        }
        .car-image img {
            max-width: 100%;
            height: auto;
        }
        .st-emotion-cache-u0yi3i {
            gap:0 !important;
        }
        
        .car-specs {
            width: 100%;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-top: 2rem;
        }
        .spec-item {
            display: flex;
            align-items: center;
            gap: 0.1rem;
    
            color: #333;
            padding: 0.5rem;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .spec-label {
            color: #666;
            min-width: 80px;
        }
        .navigation-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
        }
        .navigation-button {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #02584B;
        }
        .car-info-right {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            padding: 1rem;
        }
        .stButton>button {
            background-color: transparent !important;
            border: none !important;
            color: black !important;
            font-weight: 900 !important;
            font-size: 24px !important;
            padding: 0 !important;
            box-shadow: none !important;
        }
        .stButton>button:hover {
            background-color: transparent !important;
            color: #333333 !important;
        }
        </style>
        
        <div class="close-button-container">
            <a href="fourth_page" class="close-button">×</a>
        </div>
    """, unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(page_title="차근차근 - 추천 결과", layout="wide")
set_custom_styles()

# 로고 표시
st.image("../../docs/차근차근 로고.png", width=180)

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
        'selected_car_id': None,
        'recommendations_saved': False  # 추천 결과 저장 여부를 추적하는 플래그 추가
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

team_session()

# 추천 차량 가져오기
def get_filtered_cars():
    try:
        # 선호도에 따른 정렬 컬럼 매핑
        preference_columns = {
            "연비 (최저)": ("car_fuel_efficiency", "ASC"),
            "가격 (최저)": ("car_price", "ASC"),
            "평점 (네이버 평점 기준)": ("cri.avg_score", "DESC"),
            "차체 크기 (실내 공간 기준 = 축거/전장*100)": ("car_size", "DESC"),
            "성능 (출력-최저)": ("car_horsepower", "DESC")
        }

        # 필터 조건 동적 생성
        filters = []
        params = []

        # 예산
        filters.append("ci.car_price BETWEEN %s AND %s")
        params.extend([st.session_state.min_val, st.session_state.max_val])

        # 바디타입
        if st.session_state.body_type and st.session_state.body_type != "전체":
            filters.append("bti.body_type_category = %s")
            params.append(st.session_state.body_type)

        # 연료타입
        if st.session_state.fuel_type and st.session_state.fuel_type != "전체":
            filters.append("fi.fuel_type_name = %s")
            params.append(st.session_state.fuel_type)

        where_clause = " AND ".join(filters)

        # 정렬 기준 설정
        order_clauses = []
        for pref in [st.session_state.first, st.session_state.second, st.session_state.third]:
            if pref in preference_columns:
                col, direction = preference_columns[pref]
                order_clauses.append(f"{col} {direction}")

        order_by = ", ".join(order_clauses) if order_clauses else "ci.car_price ASC"

        query = f"""
            SELECT DISTINCT
                ci.car_id,
                bi.brand_name,
                ci.car_full_name, 
                ci.car_price, 
                ci.car_img_url, 
                ci.car_fuel_efficiency, 
                ci.car_horsepower,
                ci.car_engine_type,
                fi.fuel_type_name,
                bti.body_type_category,
                COALESCE(cri.avg_score, 0) as avg_score,
                ci.car_size
            FROM teamdb.CAR_INFO ci
            JOIN teamdb.BRAND_INFO bi 
                ON ci.car_brand = bi.brand_id 
            JOIN teamdb.BODY_TYPE_INFO bti 
                ON ci.car_body_type = bti.body_name 
            JOIN teamdb.FUEL_TYPE_INFO fi
                ON ci.car_fuel_type = fi.fuel_type_id
            LEFT JOIN teamdb.CAR_REVIEW_INFO cri
                ON ci.car_full_name = cri.car_name
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT 3
        """

        conn = team_db()
        if conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(query, tuple(params))
            cars = cur.fetchall()
            conn.close()
            return cars

    except mysql.connector.Error as e:
        st.error(f"차량 추천 쿼리 실패: {e}")
        return []

# 추천 결과 저장
def save_recommendation(user_id, car_details):
    try:
        conn = team_db()
        if conn:
            cur = conn.cursor()

            # recommendation 테이블에 저장
            insert_recommendation_query = """
            INSERT INTO teamdb.car_recommendation_info
            (user_id, car_id)
            VALUES (%s, %s)
            """

            for car in car_details:
                recommendation_values = (
                    user_id,
                    car["car_id"]
                )
                cur.execute(insert_recommendation_query, recommendation_values)

            conn.commit()
            conn.close()
            return True

    except mysql.connector.Error as e:
        st.error(f"추천 결과 저장 실패: {e}")
        return False

# 메인 컨텐츠
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # 추천 차량 가져오기
    recommended_cars = get_filtered_cars()

    # 추천 결과 저장 (세션에 user_id가 있고, 아직 저장되지 않은 경우에만)
    if 'user_id' in st.session_state and recommended_cars and not st.session_state.recommendations_saved:
        if save_recommendation(st.session_state.user_id, recommended_cars):
            st.session_state.recommendations_saved = True  # 저장 성공 시 플래그 설정

    # 현재 표시할 차량 인덱스 관리
    if 'current_car_index' not in st.session_state:
        st.session_state.current_car_index = 0

    # 추천 차량 표시
    if recommended_cars:
        current_car = recommended_cars[st.session_state.current_car_index]


        # 이미지와 정보를 컬럼으로 나누기
        col1, col2 = st.columns([1, 1])

        # 왼쪽 컬럼 - 이미지
        with col1:
            st.markdown('<div class="car-image">', unsafe_allow_html=True)
            if current_car['car_img_url'] and current_car['car_img_url'].strip().startswith("http"):
                st.image(current_car['car_img_url'].strip(), width=500)
            else:
                st.image("../../docs/대체이미지.png", width=500)
            st.markdown('</div>', unsafe_allow_html=True)

        # 오른쪽 컬럼 - 정보
        with col2:
            st.markdown('<div class="car-info-right">', unsafe_allow_html=True)
            # 제목
            st.markdown('<h4 class="section-title">나의 신차는</h4>', unsafe_allow_html=True)
            # 차량 이름
            st.markdown(f'''
                <div class="car-title-container">
                    <h3 class="car-title">{current_car["car_full_name"]}</h3>
                </div>
            ''', unsafe_allow_html=True)

            # 기본 정보
            st.markdown('<div class="car-specs">', unsafe_allow_html=True)

            # 가격 정보
            price_in_million = current_car["car_price"]
            try:
                price_in_million = float(price_in_million)
                price_range = f"{price_in_million:,.0f}~{price_in_million*1.2:,.0f}만원"
            except (ValueError, TypeError):
                price_range = "가격 정보 없음"

            st.markdown(f'<div class="spec-item"><span class="spec-label">가격</span>{price_range}</div>', unsafe_allow_html=True)

            # 연료 정보
            st.markdown(f'<div class="spec-item"><span class="spec-label">연료</span>{current_car["fuel_type_name"]}</div>', unsafe_allow_html=True)

            # 엔진 정보
            if current_car["car_engine_type"]:
                st.markdown(f'<div class="spec-item"><span class="spec-label">엔진</span>{current_car["car_engine_type"]}</div>', unsafe_allow_html=True)

            # 연비 정보
            if 'car_fuel_efficiency' in current_car:
                st.markdown(f'<div class="spec-item"><span class="spec-label">연비</span>{current_car["car_fuel_efficiency"]}km/ℓ</div>', unsafe_allow_html=True)

            # 출력 정보
            if 'car_horsepower' in current_car:
                st.markdown(f'<div class="spec-item"><span class="spec-label">출력</span>{current_car["car_horsepower"]}hp</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 네비게이션 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("←", key="prev", use_container_width=False):
                st.session_state.current_car_index = (st.session_state.current_car_index - 1) % len(recommended_cars)
                st.rerun()
        with col2:
            st.markdown(f'<div style="text-align: center; font-weight: bold;">같은 조건의 다른모델 추천받기 ({st.session_state.current_car_index + 1}/{len(recommended_cars)})</div>', unsafe_allow_html=True)
        with col3:
            if st.button("→", key="next", use_container_width=False):
                st.session_state.current_car_index = (st.session_state.current_car_index + 1) % len(recommended_cars)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("조건에 맞는 차량이 없습니다. 다른 조건으로 다시 시도해보세요.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 저작권 표시
st.markdown("""
    <div class="copyright">
    Copyright 2025. Chageun. All rights reserved.
    </div>
""", unsafe_allow_html=True)