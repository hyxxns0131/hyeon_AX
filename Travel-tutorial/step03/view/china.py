import streamlit as st

# 1. 페이지 레이아웃 및 기본 설정
st.set_page_config(
    page_title="중국 여행 포털 - China Tourism", page_icon="🇨🇳", layout="wide"
)

# 2. 중국 관광청 느낌의 고급스러운 CSS 스타일ing
st.markdown(
    """
    <style>
    /* 전체 배경을 연한 붉은 톤/크림색의 단아한 한지 느낌으로 변경 */
    .stApp {
        background-color: #FAF5EF;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #8B0000 !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFD700 !important;
    }

    /* 제목 및 스티커 스타일링 */
    .main-title {
        color: #B22222;
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 800;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* 관광 카드/박스 디자인 */
    .card-box {
        background-color: #FFFFFF;
        border-left: 5px solid #B22222;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 하이라이트 텍스트 */
    .gold-highlight {
        color: #B22222;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 메인 화면 구성 (요청하신 양식 기반)
# ----------------------------------------------------

# 1. 타이틀
st.markdown(
    '<h1 class="main-title">🇨🇳 CN 중국 (China)</h1>', unsafe_allow_html=True
)

# 2. 중국에 대한 상세 설명 (20년 경력 여행사 베테랑 컨설턴트 픽)
st.write(
    """
### 🐉 웅장한 역사와 대륙의 숨결을 느끼는 여행

중국은 수천 년의 찬란한 문화유산과 초현대적 첨단 도시, 그리고 압도적인 대자연이 하나로 어우러진 대륙입니다. 
동쪽의 화려한 도시부터 서쪽의 고요한 비단길(실크로드)까지, 지역마다 각기 다른 기후와 독특한 문화적 매력을 자랑합니다.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **역사 문화 탐방 (베이징)**: 만리장성, 자금성, 이화원 등 황제의 숨결이 서린 세계문화유산 탐방
2. **비현실적 대자연 (장가계 & 구채구)**: 영화 '아바타'의 배경이 된 원가계와 신비로운 에메랄드빛 호수
3. **미래 도시 & 미식 (상하이 & 무등)**: 화려한 와이탄 야경과 딤섬, 양꼬치, 마라탕 등 다양한 식도락 경험
4. **역사 속 신비 (시안)**: 진시황의 불멸을 꿈꾸던 병마용갱과 옛 당나라의 옛 수도 탐방

---

#### 💡 **중국 여행 필수 체크 포인트**
- **무비자 정책**: 최신 비자 면제 환승 policy 및 입국 요건을 출발 전 확인하세요.
- **모바일 결제 준비**: Alipay(알리페이) 또는 WeChat Pay(위챗페이)에 해외 신용카드를 미리 등록하면 매우 편리합니다.
- **최적의 여행 시기**: 가을(9월~11월)은 날씨가 선선하여 대륙 곳곳을 탐방하기에 최적입니다.
"""
)

st.markdown("<br>", unsafe_allow_html=True)

# 3. 공식 사이트 방문 버튼 (요청양식 정확 적용)
st.link_button("🇨🇳 중국 공식 사이트 방문", "https://www.travelchina.org.cn")


# ----------------------------------------------------
# 추가 인터랙티브 팁 섹션 (관광청 사이트 느낌 연출)
# ----------------------------------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.subheader("✈️ 전문가의 지역별 추천 가이드")

tab1, tab2, tab3 = st.tabs(["🏛 역사·문화", "⛰ 대자연·풍경", "🌃 첨단·야경"])

with tab1:
    st.markdown(
        """
        <div class="card-box">
            <h4>베이징 & 시안 (Beijing & Xi'an)</h4>
            <p>천년 수도의 웅장함을 느끼고 싶다면 필수 코스입니다. 만리장성에 올라 대륙의 기상을 느껴보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        """
        <div class="card-box">
            <h4>장가계 & 구채구 (Zhangjiajie & Jiuzhaigou)</h4>
            <p>자연이 만든 가장 화려한 수묵화 속으로 걸어 들어가는 듯한 경이로움을 선사합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        """
        <div class="card-box">
            <h4>상하이 & 홍콩 (Shanghai & Hong Kong)</h4>
            <p>동양과 서양이 만나는 화려한 야경과 트렌디한 쇼핑, 미식을 즐길 수 있는 최고의 도시입니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )