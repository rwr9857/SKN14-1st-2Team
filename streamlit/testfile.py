import streamlit as st
from streamlit_option_menu import option_menu
import base64
import os
from dotenv import load_dotenv

# --- 환경변수 로드 (.env 파일에 DB 정보 저장) ---
load_dotenv()


# --- 배경 이미지 설정 함수 (Base64) ---
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


# --- 스타일 설정 (폰트 등) ---
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

# --- 배경 이미지 적용 ---
set_background('../docs/background.png')

# --- 로고 삽입 ---
st.image("../docs/logo.png", width=150)

# --- 사용자 입력 데이터 세션 상태 초기화 ---
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {
        "budget_min": 0,
        "budget_max": 5000,
        "purpose": "",
        "preference": []
    }

# --- 입력 완료 상태 체크 세션 ---
if "input_completed" not in st.session_state:
    st.session_state.input_completed = {
        "budget": False,
        "purpose": False,
        "preference": False
    }

# --- 추천 차량 세션 ---
if "recommended_cars" not in st.session_state:
    st.session_state.recommended_cars = []

# --- 페이지 상태관리 ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- 메인화면 ---
if st.session_state.page == "home":
    st.markdown("<h1>당신의 첫 차, 차근차근 함께 찾아요</h1>", unsafe_allow_html=True)
    st.write("나에게 맞는 첫 차를 3분 만에 찾아드립니다.")

    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("찾으러 가기", key="start_button"):
            st.session_state.page = "balance"
        st.markdown('</div>', unsafe_allow_html=True)

# --- 밸런스(설문) 화면 ---
elif st.session_state.page == "balance":
    selected = option_menu(
        menu_title=None,
        options=["예산 범위", "용도 체크", "선호도"],
        icons=["cash-coin", "clipboard-check", "heart"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F8B94A"},
            "icon": {"color": "#444", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px"},
            "nav-link-selected": {"background-color": "#FFCC66"},
        }
    )

    # --- 예산 범위 입력 ---
    if selected == "예산 범위":
        st.header("예산 설정")
        st.write("차량 구매 예산은 어느 정도 생각하고 계신가요?")

        min_val, max_val = st.slider(
            "구매 예산 범위 설정 (단위: 만원)",
            0, 5000, (0, 5000), step=100
        )
        st.write(f"선택한 예산: **{min_val}만원 ~ {max_val}만원**")

        # 세션 상태에 저장
        st.session_state.user_inputs["budget_min"] = min_val
        st.session_state.user_inputs["budget_max"] = max_val

        # 입력 완료 상태 업데이트
        st.session_state.input_completed["budget"] = True
        st.success("예산 범위가 저장되었습니다!")

    # --- 용도 체크 ---
    elif selected == "용도 체크":
        st.header("차량 사용 용도 체크")
        purpose = st.radio("주 사용 용도를 선택하세요.", ["출퇴근", "여행/나들이", "업무용", "주말 드라이브"], horizontal=True)
        st.write(f"선택한 용도: **{purpose}**")

        # 세션 상태에 저장
        st.session_state.user_inputs["purpose"] = purpose

        # 입력 완료 상태 업데이트
        st.session_state.input_completed["purpose"] = True
        st.success("사용 용도가 저장되었습니다!")

    # --- 선호도 ---
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

    # 모든 항목 완료여부 확인
    all_completed = all(st.session_state.input_completed.values())

    if all_completed:
        st.success("모든 항목이 완료되었습니다!")

    if st.button("추천 차량 보기", disabled=not all_completed):
        st.session_state.page = "recommendation"
        st.rerun()

    # 모든 항목이 완료되지 않았으면 안내 메시지 표시
    if not all_completed:
        incomplete_items = [item for item, completed in st.session_state.input_completed.items() if not completed]
        st.warning(f"다음 항목을 완료해주세요: {', '.join(incomplete_items)}")

# --- 추천 결과 페이지 ---
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


