import streamlit as st

# 1. 페이지 레이아웃 및 기본 설정
st.set_page_config(
    page_title="한국 여행 포털 - Korea Tourism", page_icon="🇰🇷", layout="wide"
)

# 2. 가독성을 완벽하게 보정한 다크 앤티크 전통 CSS 스타일링
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;700&display=swap');

    /* 1. 전체 배경: 깊은 다크 네이비 */
    .stApp {
        background-color: #0E0B25;
        color: #E2DFD8;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #080618 !important;
        border-right: 1px solid #D4AF37;
    }
    [data-testid="stSidebar"] * {
        color: #E6C687 !important;
    }

    /* 2. 메인 액자 프레임 (가독성 보정) */
    .traditional-frame {
        background-color: #F3E5C8 !important; /* 연한 한지 바탕 */
        border: 4px solid #B8860B;
        outline: 2px solid #8B6508;
        outline-offset: -8px;
        padding: 35px 20px;
        text-align: center;
        border-radius: 4px;
        margin: 20px 0 30px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        position: relative;
    }

    /* 액자 내부 모든 텍스트의 색상을 강제로 진한 먹색/브라운으로 고정 */
    .traditional-frame, 
    .traditional-frame h1, 
    .traditional-frame p, 
    .traditional-frame span {
        color: #1A1A1A !important;
        font-family: 'Gowun Batang', serif;
    }

    .main-title {
        font-weight: 700 !important;
        font-size: 2.3rem !important;
        margin: 0 !important;
        letter-spacing: -1px;
        line-height: 1.4;
    }

    /* 액자 네 모서리 십자 문양 */
    .traditional-frame::before, .traditional-frame::after {
        content: "┼";
        position: absolute;
        color: #8B6508 !important;
        font-size: 20px;
        font-weight: bold;
    }
    .traditional-frame::before { top: 3px; left: 8px; }
    .traditional-frame::after { top: 3px; right: 8px; }

    /* 3. 상/하단 문양 아이콘 바 */
    .pattern-bar {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin: 15px 0;
        font-size: 24px;
    }

    /* 4. 전통 카드 박스 */
    .card-box {
        background-color: #1A153A;
        border: 1px solid #D4AF37;
        border-left: 5px solid #C02A2A;
        padding: 22px;
        border-radius: 6px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .card-box h4 {
        color: #F3E5C8 !important;
        font-family: 'Gowun Batang', serif;
        margin-top: 0;
    }
    .card-box p {
        color: #D1CDC0 !important;
        margin-bottom: 0;
    }

    /* 5. 탭(Tabs) 디자인 및 가독성 전면 수정 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    /* 선택되지 않은 기본 탭 */
    .stTabs [data-baseweb="tab"] {
        background-color: #181335 !important;
        border: 1px solid #8B6508 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 10px 20px !important;
    }
    
    /* 선택되지 않은 탭의 글자색 (밝은 골드빛) */
    .stTabs [data-baseweb="tab"] p {
        color: #E6C687 !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }

    /* 선택된 활성 탭 (배경: 황금색, 글자: 진한 버건디/블랙) */
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        border: 1px solid #FFD700 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #3A0505 !important;
        font-weight: 800 !important;
    }

    /* 6. 하단 전통 물결 무늬 */
    .wave-pattern {
        width: 100%;
        height: 80px;
        background-image: repeating-radial-gradient(
            circle at 50% 100%,
            transparent 0,
            transparent 15px,
            #B8860B 16px,
            #B8860B 17px,
            transparent 18px,
            transparent 30px
        );
        background-size: 60px 40px;
        opacity: 0.25;
        margin-top: 40px;
        border-top: 1px solid #D4AF37;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 메인 화면 구성
# ----------------------------------------------------

# 1. 상단 전통 문양 바
st.markdown(
    """
    <div class="pattern-bar">
        <span style="color: #FF4D4D;">💮</span>
        <span style="color: #FFD700;">☸</span>
        <span style="color: #4D94FF;">🏵</span>
        <span style="color: #E6C687;">❂</span>
        <span style="color: #FF69B4;">🌺</span>
    </div>
""",
    unsafe_allow_html=True,
)

# 2. 메인 액자 타이틀 (글자색 또렷하게 보정)
st.markdown(
    """
    <div class="traditional-frame">
        <h1 class="main-title">한국의 미를 보여주는<br>🇰🇷 대한민국 여행 포털</h1>
    </div>
""",
    unsafe_allow_html=True,
)

# 3. 하단 대칭 문양 바
st.markdown(
    """
    <div class="pattern-bar" style="font-size: 18px; margin-bottom: 30px;">
        <span style="color: #FF69B4;">🌺</span>
        <span style="color: #E6C687;">❂</span>
        <span style="color: #4D94FF;">🏵</span>
        <span style="color: #FFD700;">☸</span>
        <span style="color: #FF4D4D;">💮</span>
    </div>
""",
    unsafe_allow_html=True,
)

# 4. 본문 콘텐츠
st.write(
    """
### 🐯 반만년의 유구한 전통과 K-컬처의 매력이 공존하는 나라

대한민국은 고즈넉한 궁궐과 유서 깊은 사찰부터 세계 트렌드를 이끄는 K-팝, K-드라마, 초현대적 도심까지 완벽하게 어우러진 다채로운 매력의 여행지입니다.
사계절의 변화가 뚜렷하여 계절마다 전혀 다른 풍경을 선물하며, 편리한 대중교통과 치안으로 편안한 여정을 제공합니다.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **K-컬처 & 전통의 조화 (서울)**: 경복궁 한복 체험부터 명동·성수동 쇼핑, N서울타워에서 바라보는 화려한 도심 야경
2. **해양 도시 & 미식 탐방 (부산)**: 해운대·광안리 바다, 감천문화마을, 신선한 해산물과 돼지국밥 식도락 여행
3. **유네스코 세계자연유산 (제주도)**: 성산일출봉, 만장굴, 한라산 등 청정 대자연과 여유로운 드라이브 코스
4. **천년 고도의 숨결 (경주)**: 불국사, 석굴암, 첨성대 및 아름다운 야경을 자랑하는 동궁과 월지 탐방

---

#### 💡 **한국 여행 필수 체크 포인트**
- **편리한 대중교통**: T-money(티머니) 교통카드 하나로 전국 지하철, 버스, 택시를 손쉽게 이용하세요.
- **24시간 K-푸드 & 배달**: 치맥(치킨+맥주)부터 밤늦게까지 즐길 수 있는 야식 문화가 발달해 있습니다.
- **최적의 여행 시기**: 봄(3월~5월)의 벚꽃 시즌과 가을(9월~11월)의 단풍 시즌은 가장 아름다운 풍경을 자랑합니다.
"""
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. 공식 사이트 방문 버튼
st.link_button("🇰🇷 대한민국 공식 관광 사이트 VisitKorea 방문", "https://korean.visitkorea.or.kr")

# 6. 추가 인터랙티브 팁 섹션 (가독성 보정된 탭)
st.markdown("<br><hr style='border-color: #D4AF37;'>", unsafe_allow_html=True)
st.subheader("✈️ 전문가의 지역별 추천 가이드")

tab1, tab2, tab3 = st.tabs(["🏯 전통·역사", "🌊 대자연·휴양", "🛍️ K-컬처·쇼핑"])

with tab1:
    st.markdown(
        """
        <div class="card-box">
            <h4>경주 & 안동 (Gyeongju & Andong)</h4>
            <p>신라 천년의 역사가 숨 쉬는 경주와 조선시대 선비 정신 및 하회탈춤 전통을 간직한 안동에서 고풍스러운 한국의 미를 경험해보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        """
        <div class="card-box">
            <h4>제주 & 강원 (Jeju & Gangwon)</h4>
            <p>에메랄드빛 바다와 오름이 펼쳐진 제주도, 웅장한 설악산과 탁 트인 동해 바다를 품은 강원도에서 완벽한 힐링을 선사합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        """
        <div class="card-box">
            <h4>서울 & 부산 (Seoul & Busan)</h4>
            <p>K-POP, 뷰티, 패션의 성지인 서울과 트렌디한 해변 라이프스타일, 화려한 야경을 자랑하는 부산에서 역동적인 한국을 느껴보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 7. 하단 전통 물결 무늬
st.markdown('<div class="wave-pattern"></div>', unsafe_allow_html=True)