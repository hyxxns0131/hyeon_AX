import streamlit as st


def render_japan_page():
    # 1. 일본풍 클래식 쪽빛 & 화이트 스타일링
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F7F8FA;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1B2A4A !important;
        }
        [data-testid="stSidebar"] * {
            color: #F8BBD0 !important;
        }

        .main-title {
            color: #1B2A4A;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #E57373;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #1B2A4A;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .card-box h4 {
            color: #1B2A4A;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2. 타이틀
    st.markdown('<h1 class="main-title">🇯🇵 일본 (Japan)</h1>', unsafe_allow_html=True)

    # 3. 본문 설명
    japan_description = """
### ⛩️ 정갈한 미식과 고즈넉한 풍경, 과거와 현재가 깃든 여정

일본은 섬세한 디테일과 장인정신, 온천 문화와 현대적인 서브컬처가 공존하는 여행지입니다.
초고층 빌딩 숲 도쿄부터 천년 고도 교토의 사찰, 그리고 겨울의 설국 홋카이도까지 사계절 내내 다채로운 감성을 선사합니다.

---

#### 🌟 **여행 전문가 강력 추천 대표 관광 코스**
1. **메트로폴리스 & 쇼핑 (도쿄)**: 시부야 스크램블, 긴자 쇼핑거리, 아사쿠사 센소지, 신주쿠 야경
2. **천년의 역사와 전통 (교토 & 나라)**: 붉은 도리이가 늘어선 후시미 이나리 신사, 기요미즈데라(청수사), 나라 사슴공원
3. **미식의 천국 (오사카 & 후쿠오카)**: 도톤보리 글리코상, 하카타 라멘 골목, 야타이(포장마차) 야간 투어
4. **대자연과 온천 휴양 (홋카이도 & 유후인)**: 후라노 라벤더 밭, 삿포로 눈축제, 전통 료칸 가이세키 요리 체험

---

#### 💡 **일본 여행 필수 체크 포인트**
- **입국 사전 등록**: 비짓재팬웹(Visit Japan Web)을 통해 검역 및 세관 신고 QR코드를 미리 발급받으면 공항 입국이 빠릅니다.
- **교통 패스 활용**: 이동 경로에 맞춰 JR 패스나 지역 지하철 패스(스이카/이코카 모바일 등록 가능)를 준비하세요.
- **동전 지갑 준비**: 카드 결제가 확대되었지만 소규모 로컬 식당이나 자판기 이용을 위해 소액 현금/동전 지갑이 필수입니다.
"""
    st.markdown(japan_description)
    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 사이트 방문 버튼
    st.link_button(
        label="🇯🇵 일본정부관광국(JNTO) 공식 사이트 방문",
        url="https://www.japan.travel/ko/kr/",
        use_container_width=True,
    )

    # 5. 지역별 추천 가이드 (탭)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 지역별 추천 가이드")

    tab1, tab2, tab3 = st.tabs(["🏯 고도·전통 사찰", "🍜 식도락·도시 탐방", "♨️ 온천·설경 힐링"])

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>교토 & 나라 (Kyoto & Nara)</h4>
                <p>대나무 숲 아라시야마와 천년 고찰을 거닐며 전통 말차 한 잔과 함께 일본 고유의 여백의 미를 느껴보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>도쿄 & 오사카 (Tokyo & Osaka)</h4>
                <p>화려한 도심의 랜드마크 전망대부터 골목길 숨은 이자카야와 스시 오마카세까지 오감을 만족시키는 도시 여행입니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>홋카이도 & 큐슈 (Hokkaido & Kyushu)</h4>
                <p>겨울 설경 속 노천 온천욕을 즐기거나, 따뜻한 벳푸·유후인 온천 마을에서 료칸 힐링을 누려보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="일본 여행 포털 - Japan Tourism",
        page_icon="🇯🇵",
        layout="wide",
    )
    render_japan_page()