import streamlit as st


def render_country_page(
    flag: str, country_name: str, country_description: str, country_url: str
):
    # 1. 일본 전통 벚꽃(사쿠라) & 차분한 딥 네이비 / 목조 톤의 CSS Styling
    st.markdown(
        """
        <style>
        /* 전체 배경을 따뜻하고 정갈한 미색/모던 린넨 느낌으로 변경 */
        .stApp {
            background-color: #FAF8F5;
        }
        
        /* 사이드바 스타일링 (차분한 일본 전통 딥 네이비 / 은은한 사쿠라 핑크 글씨) */
        [data-testid="stSidebar"] {
            background-color: #1F2A38 !important;
        }
        [data-testid="stSidebar"] * {
            color: #F3A6B2 !important;
        }

        /* 메인 타이틀 및 사쿠라 핑크 포인트 구분선 */
        .main-title {
            color: #1F2A38;
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 800;
            border-bottom: 3px solid #E07A5F; /* 테라코타/주홍 포인트 */
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        /* 카드/박스 디자인 (차분한 인디고 포인트 바) */
        .card-box {
            background-color: #FFFFFF;
            border-left: 5px solid #2B3A4A;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            margin-bottom: 20px;
        }

        /* 카드 박스 내 제목 색상 지정 */
        .card-box h4 {
            color: #1F2A38;
            margin-bottom: 10px;
        }

        /* 하이라이트 텍스트 */
        .highlight {
            color: #E07A5F;
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

    # 3. 일본 본문 설명
    st.markdown(country_description)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 공식 관광청 방문 버튼
    st.link_button(
        label=f"{flag} {country_name} 공식 정부관광국(JNTO) 방문",
        url=country_url,
    )

    # 5. 인터랙티브 팁 섹션 (지역별 가이드)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("✈️ 전문가의 테마별 일본 추천 가이드")

    tab1, tab2, tab3 = st.tabs(
        ["⛩️ 고도·전통", "🏙️ 현대·쇼핑", "♨️ 온천·자연"]
    )

    with tab1:
        st.markdown(
            """
            <div class="card-box">
                <h4>교토 & 나라 (Kyoto & Nara)</h4>
                <p>천년 고도의 기온 거리, 청수사(키요미즈데라)의 목조 건축미와 사슴들과 교감하는 나라 공원에서 일본 고유의 정취를 만나보세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class="card-box">
                <h4>도쿄 & 오사카 (Tokyo & Osaka)</h4>
                <p>트렌디한 시부야·신주쿠의 화려한 도시 전경부터 미식의 천국 오사카 도톤보리까지 다채로운 즐거움을 선사합니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            """
            <div class="card-box">
                <h4>후쿠오카 & 홋카이도 (Fukuoka & Hokkaido)</h4>
                <p>유후인·벳푸의 고즈넉한 료칸 온천 힐링과 홋카이도의 설경, 라멘 및 싱싱한 해산물 식도락을 경험할 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# 단독 실행 테스트용
if __name__ == "__main__":
    st.set_page_config(
        page_title="일본 여행 포털 - JNTO Japan",
        page_icon="🇯🇵",
        layout="wide",
    )

    japan_description = """
### 🌸 고즈넉한 전통과 화려한 현대가 공존하는 섬나라

일본은 천년의 세월을 간직한 사찰과 신사, 정갈한 료칸 온천 문화부터 트렌드를 이끄는 화려한 도심과 아기자기한 서브컬처까지 이색적인 매력이 가득한 곳입니다. 
사계절마다 변하는 수려한 자연 풍경과 디테일이 살아있는 정갈한 식도락 여행을 즐겨보세요.

---

#### 🌟 **여행사 컨설턴트 강력 추천 대표 관광 코스**
1. **천년 고도 전통 탐방 (교토 & 나라)**: 금각사, 여우신사(도리이 터널), 청수사 산책 및 전통 다도 체험
2. **미식 & 쇼핑 힐링 (도쿄 & 오사카)**: 도쿄 타워 전망대, 도톤보리 길거리 음식 탐방 및 유니버설 스튜디오
3. **온천 료칸 휴양 (후쿠오카 & 유후인)**: 정갈한 가이세키 요리와 함께 즐기는 고즈넉한 온천 힐링 라이프
4. **대자연 & 대설원 (홋카이도/삿포로)**: 삿포로 눈축제, 오타루 운하의 야경과 삿포로 맥주 박물관

---

#### 💡 **일본 여행 필수 체크 포인트**
- **교통패스 활용**: 신칸센 및 지역 패스(JR 패스, 도쿄 메트로 패스 등)를 미리 준비하면 이동 비용을 크게 절약할 수 있습니다.
- **현금 및 IC 카드**: 스이카(Suica), 파스모(Pasmo) 등 IC 카드가 매우 유용하며, 소도시 방문을 위해 약간의 현금을 준비하는 것이 좋습니다.
- **최적의 여행 시기**: 벚꽃이 만개하는 봄(3월~4월)과 단풍이 아름다운 가을(10월~11월)에 가장 인기가 높습니다.
"""

    render_country_page(
        flag="🇯🇵",
        country_name="일본 (Japan)",
        country_description=japan_description,
        country_url="https://www.japan.travel/ko/kr/",
    )