import streamlit as st


def render_country_page(
    flag: str, country_name: str, country_description: str, country_url: str
):
    # 1. 미국 성조기 & 클래식 아메리칸 감성의 블루/레드/네이비 CSS Styling
    st.markdown(
        """
        <style>
        /* 전체 배경을 화사하고 시원한 라이트 모던 크림 톤으로 변경 */
        .stApp {
            background-color: #F4F6F9;
        }
        
        /* 사이드바 스타일링 (아메리칸 클래식 딥 네이비 / 라이트 골드 글씨) */
        [data-testid="stSidebar"] {
            background-color: #0C2340 !important;
        }
        [data-testid="stSidebar"] * {
            color: #FFC72C !important;
        }

        /* 메인 타이틀 및 아메리칸 레드 포인트 구분선 */
        .main-title {
            color: #0C2340;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #C8102E; /* 성조기 레드 포인트 */
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        /* 카드/박스 디자인 (딥 블루 포인트 바) */
        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #0C2340;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* 카드 박스 내 제목 색상 지정 */
        .card-box h4 {
            color: #0C2340;
            margin-bottom: 10px;
        }

        /* 하이라이트 텍스트 */
        .highlight {
            color: #C8102E;
            font-weight: bold;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 2. 타이틀 출력
    st.markdown(
        f'<h1 class="main-title">{flag} {country_name}</h1>',
        unsafe_allow_html=True,
    )

    # 3. 미국 본문 설명
    st.markdown(country_description)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 관광청 방문 버튼
    st.link_button(
        label=f"{flag} {country_name} 공식 정부관광청(Brand USA) 방문",
        url=country_url,
    )

    # 5. 인터랙티브 팁 섹션 (지역별 가이드)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 테마별 미국 추천 가이드")

    tab1, tab2, tab3 = st.tabs(
        ["🏙️ 동부·도시", "🌴 서부·영화", "🏞️ 국립공원·자연"]
    )

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>뉴욕 & 워싱턴 D.C. (New York & Washington D.C.)</h4>
                <p>세계의 중심 타임스퀘어와 브로드웨이 뮤지컬, 자유의 여신상부터 역사와 문화가 숨쉬는 박물관 투어까지 압도적인 도시 에너지를 느껴보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>로스앤젤레스 & 샌프란시스코 (LA & San Francisco)</h4>
                <p>할리우드 유니버설 스튜디오, 산타모니카 해변의 낭만과 금문교(Golden Gate Bridge), 테슬라·구글이 위치한 실리콘밸리를 탐방해보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>그랜드 캐니언 & 옐로우스톤 (Grand Canyon & Yellowstone)</h4>
                <p>대자연의 위대함을 증명하는 그랜드 캐니언의 웅장한 협곡과 세계 최초의 국립공원 옐로우스톤의 신비로운 간헐천을 만날 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# 단독 실행 테스트용
if __name__ == "__main__":
    st.set_page_config(
        page_title="미국 여행 포털 - Visit The USA",
        page_icon="🇺🇸",
        layout="wide",
    )

    usa_description = """
### 🦅 자유와 꿈, 그리고 압도적 대자연이 펼쳐지는 곳

미국은 세계 문화와 경제의 중심지인 마천루 도시들부터 지구의 역사를 간직한 압도적인 국립공원 대자연까지, 끝없는 매력이 가득한 기회의 땅입니다. 
동부의 화려한 예술과 역사, 서부의 자유로운 해변과 영화 테마파크, 그리고 웅장한 로드트립의 낭만을 즐겨보세요.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **세계 문화 & 예술 탐방 (뉴욕)**: 센트럴 파크, 메트로폴리탄 미술관, 브로드웨이 뮤지컬 및 맨해튼 야경
2. **미 서부 엔터테인먼트 (LA & 라스베이거스)**: 할리우드 거리, 디즈니랜드, 라스베이거스 스트립의 화려한 쇼와 미식
3. **대자연 로드트립 (그랜드 캐니언 & 홀스슈 밴드)**: 헬리콥터 투어로 감상하는 대협곡과 자이언 국립공원
4. **휴양 & 힐링 (하와이)**: 와이키키 해변, 알로하 정신이 살아있는 서핑과 자생식물 및 이국적인 휴양 레저

---

#### 💡 **미국 여행 필수 체크 포인트**
- **ESTA(전자여행허가) 신청**: 입국 최소 72시간 전 공식 ESTA 홈페이지를 통해 사전 허가를 완료해야 합니다.
- **팁(Tip) 문화**: 레스토랑 이용 시 보통 15~20%의 팁을 지불하는 것이 일반적입니다.
- **넓은 영토와 시차**: 동부와 서부 간 3시간의 시차가 발생하므로 이동 동선과 비행 스케줄을 효율적으로 계획하세요.
"""

    render_country_page(
        flag="🇺🇸",
        country_name="미국 (USA)",
        country_description=usa_description,
        country_url="https://www.visittheusa.co.kr",
    )