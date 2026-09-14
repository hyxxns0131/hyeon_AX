import streamlit as st


def render_usa_page():
    # 1. 아메리칸 클래식 네이비 & 레드 스타일링
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F8FAFC;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1A365D !important;
        }
        [data-testid="stSidebar"] * {
            color: #93C5FD !important;
        }

        .main-title {
            color: #1A365D;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #DC2626;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #1A365D;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .card-box h4 {
            color: #1A365D;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2. 타이틀
    st.markdown('<h1 class="main-title">🇺🇸 미국 (United States of America)</h1>', unsafe_allow_html=True)

    # 3. 본문 설명
    usa_description = """
### 🗽 자유와 기회의 땅, 압도적인 대륙 스케일을 만나는 여행

미국은 세계 경제와 대중문화의 중심지이자 경이로운 국립공원들을 품고 있는 광활한 나라입니다.
잠들지 않는 뉴욕의 빌딩 숲부터 캘리포니아의 푸른 해변, 붉은 암석이 빚어낸 그랜드 캐니언까지 끝없는 모험이 펼쳐집니다.

---

#### 🌟 **여행 전문가 강력 추천 대표 관광 코스**
1. **세계의 심장 (뉴욕 & 워싱턴 D.C.)**: 맨해튼 타임스스퀘어, 센트럴파크, 자유의 여신상, 스미스소니언 박물관
2. **서부 해안 & 엔터테인먼트 (LA & 샌프란시스코)**: 할리우드 거리, 산타모니카 해변, 금문교, 실리콘밸리 투어
3. **대자연의 경이로움 (미서부 그랜드 서클)**: 그랜드 캐니언, 자이언 캐니언, 앤텔로프 캐니언, 모뉴먼트 밸리
4. **천상의 휴양지 (하와이)**: 오아후 와이키키 해변, 마우이 할레아칼라 일출, 카우아이 원시림 탐방

---

#### 💡 **미국 여행 필수 체크 포인트**
- **ESTA(전자여행허가) 발급**: 무비자 입국을 위해 출국 최소 72시간 전 공식 웹사이트에서 ESTA 승인을 완료해야 합니다.
- **팁(Tip) 문화**: 레스토랑, 택시, 호텔 서비스 이용 시 결제 금액의 18%~22% 수준의 팁을 포함하는 것이 일반적입니다.
- **렌터카 & 로드트립**: 광활한 대륙 특성상 도심 외곽 및 국립공원 여행 시 국제운전면허증과 렌터카 준비가 필수적입니다.
"""
    st.markdown(usa_description)
    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 사이트 방문 버튼
    st.link_button(
        label="🇺🇸 GoUSA 미국관광청 공식 사이트 방문",
        url="https://www.gousa.or.kr/",
        use_container_width=True,
    )

    # 5. 지역별 추천 가이드 (탭)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 지역별 추천 가이드")

    tab1, tab2, tab3 = st.tabs(["🏙 동부 메트로폴리스", "🚗 서부 로드트립·캐니언", "🌺 하와이·남부 휴양"])

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>뉴욕 & 보스턴 (New York & Boston)</h4>
                <p>브로드웨이 뮤지컬 관람과 세계 3대 미술관 탐방, 역사 깊은 아이비리그 명문 대학가를 거닐어보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>라스베이거스 & 그랜드 서클 (Las Vegas & Grand Circle)</h4>
                <p>화려한 불야성의 도시를 지나 수억 년 세월이 빚어낸 붉은 협곡들을 달리는 일생일대의 로드트립을 즐길 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>하와이 & 마이애미 (Hawaii & Miami)</h4>
                <p>에메랄드빛 태평양 파도에서 서핑을 즐기고, 야자수 아래 여유로운 트로피컬 휴양을 만끽하세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="미국 여행 포털 - GoUSA",
        page_icon="🇺🇸",
        layout="wide",
    )
    render_usa_page()