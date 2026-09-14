import streamlit as st

# 1. 페이지 레이아웃 및 기본 설정
st.set_page_config(
    page_title="일본 여행 포털 - Japan Tourism", page_icon="🇯🇵", layout="wide"
)

# 2. 일본 체리블라썸 & 도쿄타워 감성의 고급스러운 CSS 스타일링
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&family=Noto+Sans+KR:wght@300;400;700&display=swap');

    /* 1. 전체 배경: 은은한 벚꽃 핑크빛 한지 톤 */
    .stApp {
        background-color: #FCF7F8;
        color: #2B2D42;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 사이드바 스타일링 (진한 버건디/나이트 도쿄 톤) */
    [data-testid="stSidebar"] {
        background-color: #2B1E2A !important;
        border-right: 1px solid #E8A598;
    }
    [data-testid="stSidebar"] * {
        color: #FFC2D1 !important;
    }

    /* 2. 도쿄타워 & 벚꽃 헤더 박스 */
    .japan-frame {
        background: linear-gradient(135deg, #FFF0F3 0%, #FFCCD5 50%, #FFB3C1 100%);
        border: 2px solid #E63946;
        border-radius: 8px;
        padding: 35px 20px;
        text-align: center;
        margin: 10px 0 25px 0;
        box-shadow: 0 10px 25px rgba(230, 57, 70, 0.15);
        position: relative;
    }

    .japan-frame h1 {
        color: #8D0801 !important;
        font-family: 'Noto Serif KR', serif;
        font-weight: 700 !important;
        font-size: 2.3rem !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
        line-height: 1.4;
    }

    /* 3. 벚꽃 문양 바 */
    .sakura-bar {
        text-align: center;
        letter-spacing: 12px;
        font-size: 20px;
        color: #FF758F;
        margin-bottom: 10px;
    }

    /* 4. 카드 박스 디자인 (도쿄타워 레드 포인트) */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #FFCCD5;
        border-left: 5px solid #E63946;
        padding: 22px;
        border-radius: 6px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    .card-box h4 {
        color: #8D0801 !important;
        font-family: 'Noto Serif KR', serif;
        margin-top: 0;
    }
    .card-box p {
        color: #4A4E69 !important;
        margin-bottom: 0;
    }

    /* 5. 탭(Tabs) 스타일 지정 (벚꽃/도쿄타워 컬러 보정) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    /* 기본 탭 */
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border: 1px solid #FFCCD5 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 10px 20px !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #8D0801 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    /* 선택된 활성 탭 (배경: 도쿄타워 레드, 글자: 흰색) */
    .stTabs [aria-selected="true"] {
        background-color: #E63946 !important;
        border: 1px solid #D90429 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 메인 화면 구성
# ----------------------------------------------------

# 1. 상단 벚꽃 심볼 바
st.markdown('<div class="sakura-bar">🌸 🌸 🌸 🌸 🌸</div>', unsafe_allow_html=True)

# 2. 메인 헤더 타이틀
st.markdown(
    """
    <div class="japan-frame">
        <h1>🌸 낭만과 전통이 만나는 곳<br>🇯🇵 일본 여행 포털</h1>
    </div>
""",
    unsafe_allow_html=True,
)

# 3. 레이아웃 분할 (좌: 도쿄타워 & 벚꽃 이미지 / 우: 주요 개요 및 추천 코스)
col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.image(
        "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1000&auto=format&fit=crop",
        caption="🗼 도쿄타워와 감성적인 밤 풍경 (Tokyo Tower, Japan)",
        use_container_width=True,
    )

with col2:
    st.write(
        """
### ⛩️ 고즈넉한 전통과 화려한 도심이 공존하는 정취의 대륙

일본은 천년 고도의 유구한 역사와 고풍스러운 사찰, 그리고 세계 최고 수준의 첨단 도심이 완벽한 조화를 이루는 여행지입니다.
봄의 분홍빛 벚꽃부터 겨울의 하얀 눈꽃까지, 사계절 고유의 감성적인 풍경과 가이세키·라멘·스시 등 깊은 식도락을 경험해 보세요.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **트렌디 도심 & 미식 (도쿄)**: 도쿄타워 야경, 시부야 스크램블, 아사쿠사 센소지 탐방
2. **천년 고도 & 전통 문화 (교토 & 오사카)**: 금각사·청수사 산책, 도톤보리 식도락, 유니버설 스튜디오
3. **온천 힐링 & 대자연 (후쿠오카 & 유후인)**: 고즈넉한 료칸 온천 체험과 규슈 지역의 미식 기행
4. **설국 & 청정 휴양 (홋카이도/삿포로)**: 비에이 힐링 투어, 겨울 삿포로 눈축제와 라멘 거리
"""
    )

st.markdown("<br>", unsafe_allow_html=True)

# 4. 필수 체크포인트 & 버튼 섹션
st.markdown(
    """
#### 💡 **일본 여행 필수 체크 포인트**
- **Visit Japan Web 등록**: 입국 수속 및 세관 신고를 위해 출발 전 미리 등록하면 매우 빠른 입국이 가능합니다.
- **교통패스 준비**: 신칸센 및 지하철 이용 시 IC 카드(수이카/파스모) 또는 지역별 JR 패스를 미리 준비하세요.
- **온천 에티켓**: 온천 이용 시 타월을 탕 안에 넣지 않는 등 일본 고유의 온천 에티켓을 준수하는 것이 좋습니다.
"""
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. 공식 사이트 방문 버튼
st.link_button("🇯🇵 일본 정부 관광국 JNTO 공식 사이트 방문", "https://www.japan.travel/ko/kr/")


# ----------------------------------------------------
# 추가 인터랙티브 팁 섹션
# ----------------------------------------------------
st.markdown("<br><hr style='border-color: #FFCCD5;'>", unsafe_allow_html=True)
st.subheader("✈️ 전문가의 지역별 추천 가이드")

tab1, tab2, tab3 = st.tabs(["🏙️ 도쿄·관동", "🏯 Kansai·관서", "♨️ 힐링·온천"])

with tab1:
    st.markdown(
        """
        <div class="card-box">
            <h4>도쿄 & 요코하마 (Tokyo & Yokohama)</h4>
            <p>세계적인 미식의 도시이자 화려한 도쿄타워 야경, 오다이바 해변의 현대적 낭만을 느낄 수 있는 메트로폴리스입니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        """
        <div class="card-box">
            <h4>오사카 & 교토 & 나라 (Osaka & Kyoto & Nara)</h4>
            <p>맛있는 활력이 넘치는 오사카와 천년 도읍 교토의 고즈넉한 대나무 숲(아라시야마), 사슴 공원이 있는 나라를 탐방하세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        """
        <div class="card-box">
            <h4>후쿠오카 & 유후인 (Fukuoka & Yufuin)</h4>
            <p>비행시간 1시간대의 가까운 낙원! 정갈한 료칸 온천에서 즐기는 힐링과 원조 하카타 라멘 식도락 여행을 경험해 보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )