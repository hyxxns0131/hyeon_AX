import streamlit as st

# 1. 페이지 레이아웃 및 기본 설정
st.set_page_config(
    page_title="미국 여행 포털 - USA Tourism", page_icon="🇺🇸", layout="wide"
)

# 2. 아메리칸 스타일(미국 국기 & 메트로폴리탄) CSS 스타일링
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@700;900&family=Noto+Sans+KR:wght@300;400;700&display=swap');

    /* 1. 전체 배경: 딥 네이비 블루 */
    .stApp {
        background-color: #0A192F;
        color: #E6F1FF;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 사이드바 스타일링 (자유의 여신상 청동색/골드 포인트) */
    [data-testid="stSidebar"] {
        background-color: #020C1B !important;
        border-right: 1px solid #1E2D4A;
    }
    [data-testid="stSidebar"] * {
        color: #FFD700 !important;
    }

    /* 2. 미국 히어로 헤더 박스 (네이비 & 딥 레드 포인트) */
    .usa-frame {
        background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 50%, #B91C1C 100%);
        border: 2px solid #FFD700;
        padding: 35px 20px;
        text-align: center;
        border-radius: 8px;
        margin: 10px 0 25px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }

    .usa-frame h1 {
        color: #FFFFFF !important;
        font-family: 'Merriweather', serif;
        font-weight: 900 !important;
        font-size: 2.4rem !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }

    /* 3. 상단 별 패턴 바 */
    .star-bar {
        text-align: center;
        letter-spacing: 8px;
        font-size: 18px;
        color: #FFD700;
        margin-bottom: 10px;
    }

    /* 4. 카드 박스 디자인 */
    .card-box {
        background-color: #112240;
        border: 1px solid #233554;
        border-left: 5px solid #B91C1C;
        padding: 22px;
        border-radius: 6px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .card-box h4 {
        color: #FFD700 !important;
        font-family: 'Merriweather', serif;
        margin-top: 0;
    }
    .card-box p {
        color: #8892B0 !important;
        margin-bottom: 0;
    }

    /* 5. 탭(Tabs) 스타일 지정 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    /* 기본 탭 */
    .stTabs [data-baseweb="tab"] {
        background-color: #112240 !important;
        border: 1px solid #233554 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 10px 20px !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #8892B0 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    /* 선택된 활성 탭 (배경: 버건디 레드, 글자: 흰색) */
    .stTabs [aria-selected="true"] {
        background-color: #B91C1C !important;
        border: 1px solid #EF4444 !important;
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

# 1. 상단 미국 상징 별 패턴
st.markdown('<div class="star-bar">★ ★ ★ ★ ★</div>', unsafe_allow_html=True)

# 2. 메인 헤더 타이틀
st.markdown(
    """
    <div class="usa-frame">
        <h1>🗽 UNITED STATES OF AMERICA<br>미국 여행 포털</h1>
    </div>
""",
    unsafe_allow_html=True,
)

# 3. 레이아웃 분할 (좌: 자유의 여신상 이미지 / 우: 주요 개요 및 추천 코스)
col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.image(
        "https://images.unsplash.com/photo-1605130284535-11dd9eedc58a?q=80&w=1000&auto=format&fit=crop",
        caption="🗽 자유의 여신상 (Statue of Liberty, New York)",
        use_container_width=True,
    )

with col2:
    st.write(
        """
### 🦅 기회의 땅, 압도적인 기상의 대륙 여행

미국은 세계 경제와 문화의 중심지인 대도시부터 세계 자연유산으로 지정된 거대한 국립공원까지 끊임없는 경이로움을 선사하는 나라입니다.
태평양과 대서양을 아우르는 넓은 영토에서 다채로운 문화와 미식, 그리고 최첨단 엔터테인먼트를 경험해 보세요.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **화려한 도심 & 문화 (뉴욕 & 워싱턴 D.C.)**: 타임스퀘어, 브로드웨이 뮤지컬, 센트럴파크 및 박물관 탐방
2. **미서부 대자연 로드트립 (그랜드 캐니언 & 요세미티)**: 대륙의 기상을 느끼는 광활한 국립공원과 66번 국도 드라이브
3. **태양과 엔터테인먼트 (LA & 라스베이거스)**: 할리우드 유니버설 스튜디오, 베니스 비치, 화려한 야경의 도시
4. **낙원의 섬 휴양 (하와이)**: 와이키키 해변, 화산 국립공원, 완벽한 해양 스포츠와 힐링
"""
    )

st.markdown("<br>", unsafe_allow_html=True)

# 4. 필수 체크포인트 & 버튼 섹션
st.markdown(
    """
#### 💡 **미국 여행 필수 체크 포인트**
- **ESTA(전자허가제) 신청**: 출국 최소 72시간 전 반드시 공식 ESTA 홈페이지에서 비자 면제 승인을 받으세요.
- **팁(Tip) 문화**: 레스토랑 이용 시 보통 식대 금액의 15%~20% 정도를 팁으로 지불하는 것이 일반적입니다.
- **넓은 시차 및 이동**: 미 대륙 내에서도 4개의 시차가 존재하므로 주간 이동 시 시차 계산이 필수적입니다.
"""
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. 공식 사이트 방문 버튼
st.link_button("🇺🇸 미국 공식 관광청 Visit The USA 방문", "https://www.visittheusa.com")


# ----------------------------------------------------
# 추가 인터랙티브 팁 섹션
# ----------------------------------------------------
st.markdown("<br><hr style='border-color: #233554;'>", unsafe_allow_html=True)
st.subheader("✈️ 전문가의 권역별 추천 가이드")

tab1, tab2, tab3 = st.tabs(["🏙️ 미동부 (East Coast)", "🌴 미서부 (West Coast)", "🌋 하와이 & 괌 (Islands)"])

with tab1:
    st.markdown(
        """
        <div class="card-box">
            <h4>뉴욕 & 보스턴 (New York & Boston)</h4>
            <p>세계 문화와 금융의 중심지 뉴욕의 마천루를 감상하고, 고풍스러운 대학 도시 보스턴에서 미국 역사의 발자취를 따라가보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        """
        <div class="card-box">
            <h4>샌프란시스코 & 로스앤젤레스 (San Francisco & LA)</h4>
            <p>금문교의 낭만이 있는 샌프란시스코, 영화와 예술의 도시 LA, 그리고 환상적인 태평양 해안 도로(PCH) 드라이브를 즐기세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        """
        <div class="card-box">
            <h4>오아후 & 마우이 (Oahu & Maui)</h4>
            <p>에메랄드빛 바다에서의 서핑과 천혜의 자연 풍경, 쇼핑과 휴양이 완벽하게 결합된 세계 최고의 휴양지입니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )