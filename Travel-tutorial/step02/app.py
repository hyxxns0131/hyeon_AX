import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="세계 여행 포털", page_icon="🌍", layout="wide")

# 사이드바 메뉴 구성
menu = st.sidebar.radio("메뉴 선택", ["홈", "미국", "중국", "일본"])

# 메인 콘텐츠 구성
if menu == "홈":
    st.title("🇰🇷 대한민국 (Korea)")
    st.subheader("전통과 현대가 공존하는 다채로운 매력의 나라")
    st.write(
        """
        안녕하세요! 20년 경력의 여행 컨설턴트입니다. 
        대한민국은 사계절의 변화가 뚜렷하며, K-컬처와 첨단 도시, 그리고 풍부한 역사를 자랑합니다.
        서울의 활기찬 도시 풍경부터 제주도의 청정 자연까지 특별한 여행을 경험해 보세요.
        """
    )
    st.info("💡 추천 여행지: 서울 경복궁, 제주도 성산일출봉, 부산 해운대")

elif menu == "미국":
    st.title("🇺🇸 미국 (USA)")
    st.subheader("광활한 대자연과 세계 문화의 중심지")
    st.write(
        """
        동부의 역사적인 도시부터 서부의 압도적인 국립공원까지! 
        뉴욕의 타임스퀘어, 그랜드 캐니언의 장엄함, 그리고 로스앤젤레스의 여유로움을 만나보세요.
        """
    )
    st.link_button("🇺🇸 미국 공식 관광청 방문하기", "https://www.gousa.or.kr/")

elif menu == "중국":
    st.title("🇨🇳 중국 (China)")
    st.subheader("웅장한 역사와 광활한 대륙의 숨결")
    st.write(
        """
        수천 년의 역사를 간직한 만리장성과 자금성, 그리고 비현실적인 풍경의 장가계와 장강삼협까지. 
        대륙의 거대한 스케일과 깊이 있는 문화유산을 체험하실 수 있습니다.
        """
    )
    st.link_button("🇨🇳 중국 공식 관광청 방문하기", "http://www.cnto.or.kr/")

elif menu == "일본":
    st.title("🇯🇵 일본 (Japan)")
    st.subheader("온천, 식도락, 그리고 세심한 모시의 나라")
    st.write(
        """
        가까운 거리로 언제든 떠나기 좋은 인기 여행지입니다. 
        도쿄의 최첨단 거리, 교토의 고즈넉한 전통 사찰, 그리고 오사카의 미식 여행과 각지의 유명 온천을 즐겨보세요.
        """
    )
    st.link_button("🇯🇵 일본 공식 관광청(JNTO) 방문하기", "https://www.japan.travel/ko/kr/")