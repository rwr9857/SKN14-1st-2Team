import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from io import BytesIO

# --- 세션 상태 초기화 ---
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
        'selected_menu': "기본 정보"
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# --- 페이지 설정 ---
st.set_page_config(page_title="차근차근", layout="wide")

# --- 스타일 설정 (배경 색) ---
st.markdown(
    """
    <style>
        body { background-color: #FFF5D7; }   
        .main { background-color: #FFF5D7; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 이미지 base64 변환 ---
def get_image_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

logo_path = "차근차근_로고_(1).png"  # 로고 파일명
img_base64 = get_image_base64(logo_path)

# --- 로고 버튼 (클릭시 기본정보로 이동) ---  todo 로고와 버튼 문제 해결
st.markdown(
    f"""
    <a href="?page=기본 정보" target="_self" style="position: fixed; top: 20px; left: 20px; z-index: 100;">
        <img src="data:image/png;base64,{img_base64}" width="120">
    </a>
    """,
    unsafe_allow_html=True
)

# --- URL 파라미터 읽기 ---
query_params = st.query_params
if "page" in query_params:
    st.session_state.selected_menu = query_params["page"]

# --- 메뉴 (Option Menu) ---
selected = option_menu(
    menu_title=None,
    options=["기본 정보", "예산 범위", "연료 타입", "바디타입", "선호도"],
    icons=["info-circle", "cash-coin", "ev-station", "car-front-fill", "heart"],
    orientation="horizontal",
    default_index=["기본 정보", "예산 범위", "연료 타입", "바디타입", "선호도"].index(st.session_state.selected_menu),
    styles={
        "container": {"padding": "0!important", "background-color": "#F8B94A"},
        "icon": {"color": "#444", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px"},
        "nav-link-selected": {"background-color": "#FFCC66"},
    },
    key="selected_menu"
)

# --- 페이지별 내용 ---
if selected == "기본 정보":
    st.header("기본 정보")
    st.session_state.age = st.number_input("나이(세)", 20, 40, st.session_state.age)
    st.session_state.gender = st.radio(
        "성별",
        ["남", "여"],
        horizontal=True,
        index=["남", "여"].index(st.session_state.gender) if st.session_state.gender else 0
    )
    st.session_state.purpose = st.selectbox(
        "주 사용 용도",
        ["출퇴근", "여행/나들이", "업무용", "주말 드라이브"],
        index=["출퇴근", "여행/나들이", "업무용", "주말 드라이브"].index(st.session_state.purpose) if st.session_state.purpose else 0
    )

elif selected == "예산 범위":
    st.header("차량 구매 예산")
    col1, col2 = st.columns([1,1.3])
    with col1:
        st.image("예산_아이콘.png", width=100)  # 예산 아이콘 필요
    with col2:
        st.session_state.min_val, st.session_state.max_val = st.slider(
            "구매 예산 범위 설정 (단위: 만 원)", 1000, 5000, (st.session_state.min_val, st.session_state.max_val), step=1000
        )

elif selected == "연료 타입":
    st.header("연료 타입 선택")
    st.session_state.engine_type = st.radio(
        "원하는 연료 타입을 선택하세요",
        ["디젤", "가솔린", "하이브리드", "전기"],
        horizontal=True,
        index=["디젤", "가솔린", "하이브리드", "전기"].index(st.session_state.engine_type) if st.session_state.engine_type else 0
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

    first_priority = st.selectbox(
        "🏆 1순위",
        options=preference_options,
        index=preference_options.index(st.session_state.first) if st.session_state.first in preference_options else 0,
        key="first_priority_select"
    )

    second_options = [opt for opt in preference_options if opt != first_priority]
    second_priority = st.selectbox(
        "🥈 2순위",
        options=second_options,
        index=second_options.index(st.session_state.second) if st.session_state.second in second_options else 0,
        key="second_priority_select"
    )

    third_options = [opt for opt in second_options if opt != second_priority]
    third_priority = st.selectbox(
        "🥉 3순위",
        options=third_options,
        index=third_options.index(st.session_state.third) if st.session_state.third in third_options else 0,
        key="third_priority_select"
    )

    st.session_state.first = first_priority
    st.session_state.second = second_priority
    st.session_state.third = third_priority

    st.write("#### 🔎 선택한 중요도 순위")
    st.write(f"1순위: **{st.session_state.first}**")
    st.write(f"2순위: **{st.session_state.second}**")
    st.write(f"3순위: **{st.session_state.third}**")

# --- 모든 항목 완료시 차량 추천 버튼 ---
required_fields = [
    st.session_state.age,
    st.session_state.gender,
    st.session_state.purpose,
    st.session_state.min_val,
    st.session_state.max_val,
    st.session_state.engine_type,
    st.session_state.body_type,
    st.session_state.first,
    st.session_state.second,
    st.session_state.third
]

with st.container():
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        if st.button("차량 추천받기"):
            if all(required_fields):
                st.success("✅ 다음 페이지로 이동합니다!")
                # TODO: 다음 단계 이동 로직 추가
            else:
                st.error("⚠️ 모든 값을 입력 후 버튼을 눌러주세요.")
