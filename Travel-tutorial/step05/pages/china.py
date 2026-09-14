import streamlit as st


def render_china_page():
    # 1. 중국풍 붉은빛 & 골드 포인트 고급 스타일링
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FAF5EF;
        }
        
        [data-testid="stSidebar"] {
            background-color: #8B0000 !important;
        }
        [data-testid="stSidebar"] * {
            color: #FFD700 !important;
        }

        .main-title {
            color: #B22222;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #FFD700;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #B22222;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .card-box h4 {
            color: #B22222;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2. 메인 타이틀
    st.markdown('<h1 class="main-title">🇨🇳 중국 (China)</h1>', unsafe_allow_html=True)

    # 3. 본문 설명
    china_description = """
### 🐉 웅장한 역사와 대륙의 숨결을 느끼는 여행

중국은 수천 년의 찬란한 문화유산과 초현대적 첨단 도시, 그리고 압도적인 대자연이 하나로 어우러진 대륙입니다. 
동쪽의 화려한 도시부터 서쪽의 고요한 비단길(실크로드)까지, 지역마다 각기 다른 기후와 독특한 문화적 매력을 자랑합니다.

---

#### 🌟 **여행 전문가 강력 추천 대표 관광 코스**
1. **역사 문화 탐방 (베이징)**: 만리장성, 자금성, 이화원 등 황제의 숨결이 서린 세계문화유산 탐방
2. **비현실적 대자연 (장가계 & 구채구)**: 영화 '아바타'의 배경이 된 원가계와 신비로운 에메랄드빛 호수
3. **미래 도시 & 미식 (상하이 & 청두)**: 화려한 와이탄 야경과 훠궈, 딤섬, 양꼬치, 마라탕 등 다채로운 식도락 경험
4. **역사 속 신비 (시안)**: 진시황의 불멸을 꿈꾸던 병마용갱과 옛 당나라의 수도 탐방

---

#### 💡 **중국 여행 필수 체크 포인트**
- **무비자 정책 확인**: 최신 비자 면제 정책 및 입국 요건을 출발 전 확인하세요.
- **모바일 결제 준비**: Alipay(알리페이) 또는 WeChat Pay(위챗페이)에 해외 신용카드를 미리 등록해 두면 현지 결제가 매우 편리합니다.
- **최적의 여행 시기**: 가을(9월~11월)은 날씨가 선선하고 쾌적하여 대륙 곳곳을 탐방하기에 최적입니다.
"""
    st.markdown(china_description)
    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 사이트 바로가기 버튼
    st.link_button(
        label="🇨🇳 중국 국가여유국 공식 관광 사이트 방문",
        url="https://www.travelchina.org.cn",
        use_container_width=True,
    )

    # 5. 테마별 추천 가이드 (탭)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 지역별 추천 가이드")

    tab1, tab2, tab3 = st.tabs(["🏛 역사·문화", "⛰ 대자연·풍경", "🌃 첨단·야경"])

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>베이징 & 시안 (Beijing & Xi'an)</h4>
                <p>천년 수도의 웅장함을 느끼고 싶다면 필수 코스입니다. 만리장성에 올라 대륙의 기상을 직접 체험해보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>장가계 & 구채구 (Zhangjiajie & Jiuzhaigou)</h4>
                <p>자연이 빚어낸 한 폭의 거대한 수묵화 속으로 걸어 들어가는 듯한 경이로운 비경을 선사합니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>상하이 & 홍콩 (Shanghai & Hong Kong)</h4>
                <p>동서양의 문화가 교차하는 화려한 스카이라인 야경과 트렌디한 쇼핑, 미식을 만끽할 수 있는 대표 도시입니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="중국 여행 포털 - China Tourism",
        page_icon="🇨🇳",
        layout="wide",
    )
    render_china_page()