import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="차근차근", layout="centered", initial_sidebar_state="collapsed"
)

# 상단 로고와 제목
st.markdown(
    "<h1 style='text-align: center; color: #005f4b;'>차근차근</h1>",
    unsafe_allow_html=True,
)
st.markdown("##", unsafe_allow_html=True)

# 필터 드롭다운
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    st.selectbox("외형", ["전체", "TEST", "TEST", "TEST"])
with col2:
    st.selectbox("가격", ["전체", "TEST", "TEST", "TEST"])
with col3:
    st.selectbox("차종", ["전체", "TEST", "TEST", "TEST"])
with col4:
    st.selectbox("연비", ["전체", "TEST", "TEST", "TEST"])
with col5:
    st.selectbox("유종", ["전체", "TEST", "TEST", "TEST", "TEST"])

st.markdown("---")

# 본문 레이아웃
col = st.container()

with col:
    # 차량 카드 목록 (더미 데이터)
    cars = [
        {
            "name": "2024 아반떼 N",
            "price": "4,200만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2024 아반떼",
            "price": "2,300만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2024 싼타페",
            "price": "4,500만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2024 GV60",
            "price": "6,000만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2024 아반떼 N",
            "price": "4,200만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2024 아이오닉 6",
            "price": "5,200만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2024 제네시스 G80",
            "price": "7,000만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
        {
            "name": "2025 테슬라 모델 3",
            "price": "5,800만원",
            "image": "http://file.carisyou.com/upload/2024/03/26/FILE_202403261017567070.png",
        },
    ]

    for i in range(0, len(cars), 4):
        card_row = cars[i : i + 4]
        cols = st.columns(4)
        for idx, car in enumerate(card_row):
            with cols[idx]:
                st.image(car["image"], use_container_width=True)
                st.markdown(f"**{car['name']}**")
                st.markdown(f"{car['price']}")

# 페이지네이션
st.markdown("### ")
pagination_cols = st.columns(5)
for i in range(5):
    with pagination_cols[i]:
        st.button(str(i + 1))
