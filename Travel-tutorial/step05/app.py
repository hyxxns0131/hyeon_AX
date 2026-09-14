import streamlit as st


def render_korea_page():
    # 1. 한국 전통 단청 & 모던 K-Culture 스타일링
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F8F9FA;
        }
        
        [data-testid="stSidebar"] {
            background-color: #0B2B5C !important;
        }
        [data-testid="stSidebar"] * {
            color: #F4D03F !important;
        }

        .main-title {
            color: #0B2B5C;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #C0392B;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #0B2B5C;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .card-box h4 {
            color: #0B2B5C;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2. 타이틀
    st.markdown('<h1 class="main-title">🇰🇷 대한민국 (Republic of Korea)</h1>', unsafe_allow_html=True)

    # 3. 본문 설명
    korea_description = """
### 🌸 찬란한 5천 년 역사와 글로벌 K-Culture가 살아 숨 쉬는 곳

대한민국은 유구한 궁궐 문화와 첨단 IT 인프라, 사계절의 뚜렷한 자연경관이 완벽한 조화를 이루는 역동적인 여행지입니다.
서울의 고궁과 빌딩 숲, 천혜의 자연을 품은 제주도, 활기찬 항구도시 부산까지 다채로운 매력을 경험할 수 있습니다.

---

#### 🌟 **여행 전문가 강력 추천 대표 관광 코스**
1. **역사 & 도심 라이프 (서울)**: 경복궁, 북촌한옥마을, 성수동 카페거리, DDP(동대문디자인플라자)
2. **해양 & 낭만 (부산 & 강릉)**: 해운대 블루라인파크, 자갈치시장, 강릉 안목해변 커피거리
3. **유네스코 세계자연유산 (제주도)**: 성산일출봉, 만장굴, 한라산 영실코스, 올레길 트레킹
4. **전통 미식 & 예술 (전주 & 경주)**: 전주 한옥마을 비빔밥 탐방, 경주 대릉원 및 첨성대 야경 투어

---

#### 💡 **대한민국 여행 필수 체크 포인트**
- **대중교통 이용**: 전국 호환 교통카드(T-money, 캐시비) 또는 기후동행카드를 준비하면 지하철과 버스를 자유롭게 환승할 수 있습니다.
- **배달 & 디지털 편의**: 세계 최고 수준의 초고속 무료 Wi-Fi와 편리한 모바일 지도 앱(네이버 지도, 카카오맵)을 활용하세요.
- **최적의 여행 시기**: 벚꽃이 만개하는 봄(4월~5월)과 단풍이 물드는 가을(10월~11월)이 야외 활동에 가장 쾌적합니다.
"""
    st.markdown(korea_description)
    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 사이트 방문 버튼
    st.link_button(
        label="🇰🇷 대한민국 구석구석 공식 포털 방문",
        url="https://korean.visitkorea.or.kr",
        use_container_width=True,
    )

    # 5. 지역별 추천 가이드 (탭)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 테마별 추천 가이드")

    tab1, tab2, tab3 = st.tabs(["🏯 궁궐 & K-Culture", "🌊 푸른 바다 & 미식", "🌿 힐링 자연 & 웰니스"])

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>서울 & 수도권 (Seoul & Incheon)</h4>
                <p>낮에는 600년 역사의 경복궁과 창덕궁 후원을 산책하고, 밤에는 홍대·성수동의 트렌디한 팝업스토어와 K-POP 문화를 즐겨보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>부산 & 동해안 (Busan & Gangneung)</h4>
                <p>끝없이 펼쳐진 에메랄드빛 동해안 바다를 따라 신선한 제철 해산물과 바다 전망 카페거리 투어를 만끽할 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>제주 & 남해안 (Jeju & Namhae)</h4>
                <p>도심을 벗어나 피톤치드 가득한 사려니숲길을 걷고, 제주의 청정 바다와 올레길에서 진정한 쉼을 찾아보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="글로벌 여행 포털 - 대한민국",
        page_icon="🇰🇷",
        layout="wide",
    )
    render_korea_page()