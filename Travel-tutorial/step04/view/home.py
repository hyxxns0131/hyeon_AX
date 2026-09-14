import streamlit as st


def render_country_page(
    flag: str, country_name: str, country_description: str, country_url: str
):
    # 1. 한국 전통 단청 & 고풍스러운 수묵화 느낌의 CSS Styling
    st.markdown(
        """
        <style>
        /* 전체 배경을 은은하고 고즈넉한 한지/백자 느낌으로 변경 */
        .stApp {
            background-color: #F8F9FA;
        }
        
        /* 사이드바 스타일링 (전통 짙은 감청색 / 금빛 글씨) */
        [data-testid="stSidebar"] {
            background-color: #1A2B4C !important;
        }
        [data-testid="stSidebar"] * {
            color: #E2B857 !important;
        }

        /* 메인 타이틀 및 전통 단청 포인트 구분선 */
        .main-title {
            color: #1A2B4C;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #C83B3B; /* 전통 주홍/단청 레드 포인트 */
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        /* 카드/박스 디자인 (전통 감청색 포인트 바) */
        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #1A2B4C;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* 카드 박스 내 제목 색상 지정 */
        .card-box h4 {
            color: #1A2B4C;
            margin-bottom: 10px;
        }

        /* 하이라이트 텍스트 */
        .highlight {
            color: #C83B3B;
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

    # 3. 한국 본문 설명
    st.markdown(country_description)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 관광청 방문 버튼
    st.link_button(
        label=f"{flag} {country_name} 공식 관광청(VISITKOREA) 방문",
        url=country_url,
    )

    # 5. 인터랙티브 팁 섹션 (지역별 가이드)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 테마별 한국 추천 가이드")

    tab1, tab2, tab3 = st.tabs(
        ["🏯 고궁·전통", "🌊 자연·휴양", "🛍️ 현대·K-컬처"]
    )

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>서울 고궁 & 경주 (Seoul & Gyeongju)</h4>
                <p>경복궁, 창덕궁의 고즈넉한 한옥 곡선미와 신라 천년의 역사가 숨쉬는 경주에서 한국의 전통미를 느껴보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>제주도 & 강원도 (Jeju & Gangwon)</h4>
                <p>에메랄드빛 바다와 유네스코 세계자연유산의 제주, 그리고 웅장한 설악산과 탁 트인 동해안 풍경을 즐길 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>서울 성수·홍대 & 부산 (Seoul & Busan)</h4>
                <p>K-POP, 트렌디한 팝업스토어, 미식 트렌드를 이끄는 서울의 핫플레이스와 해운대 야경이 일품인 미식의 도시 부산입니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# 단독 실행 테스트용
if __name__ == "__main__":
    st.set_page_config(
        page_title="한국 여행 포털 - Visit Korea",
        page_icon="🇰🇷",
        layout="wide",
    )

    korea_description = """
### 🐅 전통과 현대가 조화롭게 어우러진 다채로운 매력의 나라

한국은 반만년의 깊은 역사와 문화유산, 그리고 세계를 사로잡은 현대 K-컬처가 완벽한 조화를 이루는 곳입니다. 
고풍스러운 한옥과 웅장한 조선 궁궐부터, 화려한 마천루와 밤낮없이 활기찬 쇼핑·미식 거리까지 다채로운 즐거움을 선사합니다.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **타임슬립 고궁 탐방 (서울)**: 경복궁 한복 체험, 북촌한옥마을, 창덕궁 후원 산책
2. **천년 역사 & 미식 탐방 (경주 & 전주)**: 신라 고도 경주의 첨성대·불국사와 전주 한옥마을의 비빔밥 미식 여행
3. **해양 휴양 & 야경 (부산 & 제주)**: 해운대 해변열차, 자갈치 시장의 싱싱한 해산물, 제주의 성산일출봉과 힐링 숲길
4. **K-컬처 & 트렌드 체험**: 성수동 팝업스토어, K-POP 성지 투어, 24시간 즐기는 야시장 미식 체험

---

#### 💡 **한국 여행 필수 체크 포인트**
- **편리한 대중교통**: T-money 카드 하나로 전국 지하철, 버스를 편리하게 이용할 수 있습니다.
- **초고속 Wi-Fi & 치안**: 전국 어디서나 빠르고 안전한 와이파이와 세계 최고 수준의 치안 환경을 자랑합니다.
- **최적의 여행 시기**: 단풍이 아름다운 가을(9월~11월)과 벚꽃이 만개하는 봄(3월~5월)이 가장 여행하기 좋습니다.
"""

    render_country_page(
        flag="🇰🇷",
        country_name="한국 (Korea)",
        country_description=korea_description,
        country_url="https://korean.visitkorea.or.kr",
    )