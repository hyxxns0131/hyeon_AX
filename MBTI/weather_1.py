# 날씨 API 실습
# OpenWeatherMap 현재 날씨 API로 특정 도시의 날씨를 가져와 출력한다.
# 사전준비 OpenWeatherMap회원 가입 후 API발급
# pip install requests python-dotenv
#.env 파일을 생성하고 이곳에 OPENWEATHER_API_KEY 발급 받은 _API_키
#.env.example OPENWEATHER_API_KEY=your_key
#.env.example 받아서 .env로 이름 바꾸고 자기 API를 채운다.


import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv("../.env")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

st.set_page_config(page_title="국가별 날씨 & 환율", page_icon="🌤️", layout="wide")

COUNTRY_CITY_MAP = {
    "대한민국 🇰🇷": {"서울": "Seoul", "부산": "Busan", "제주": "Jeju"},
    "호주 🇦🇺": {"시드니": "Sydney", "멜버른": "Melbourne", "브리즈번": "Brisbane"},
    "일본 🇯🇵": {"도쿄": "Tokyo", "오사카": "Osaka", "후쿠오카": "Fukuoka"},
    "미국 🇺🇸": {"뉴욕": "New York", "로스앤젤레스": "Los Angeles"},
    "영국 🇬🇧": {"런던": "London", "캠브리지": "Cambridge"},
    "프랑스 🇫🇷": {"파리": "Paris", "니스": "Nice"},
    "독일 🇩🇪": {"베를린": "Berlin", "뮌헨": "Munich"}
}

CURRENCY_MAP = {
    "대한민국 🇰🇷": {"code": "KRW", "symbol": "₩", "name": "대한민국 원"},
    "호주 🇦🇺": {"code": "AUD", "symbol": "A$", "name": "호주 달러"},
    "일본 🇯🇵": {"code": "JPY", "symbol": "¥", "name": "일본 엔"},
    "미국 🇺🇸": {"code": "USD", "symbol": "$", "name": "미국 달러"},
    "영국 🇬🇧": {"code": "GBP", "symbol": "£", "name": "영국 파운드"},
    "프랑스 🇫🇷": {"code": "EUR", "symbol": "€", "name": "유로"},
    "독일 🇩🇪": {"code": "EUR", "symbol": "€", "name": "유로"}
}

@st.cache_data(ttl=1800)
def get_all_rates(api_key):
    if not api_key:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("result") == "success":
                rates = data["conversion_rates"]
                usd_to_krw = rates.get("KRW", 1340.0)
                krw_table = {}
                for curr, rate in rates.items():
                    if rate > 0:
                        krw_table[curr] = usd_to_krw / rate
                return krw_table
    except Exception:
        pass
    return None

def get_fashion_lookbook(temp):
    if temp >= 28:
        return "시원한 썸머 룩 🩴", "린넨 셔츠, 슬리브리스, 버뮤다 팬츠, 스트랩 샌들"
    elif 20 <= temp < 28:
        return "산뜻한 캐주얼 룩 👕", "반팔 티셔츠, 얇은 셔츠, 슬랙스, 코튼 팬츠"
    elif 15 <= temp < 20:
        return "포근한 간절기 가디건 룩 🧶", "가디건, 루즈핏 맨투맨, 와이드 팬츠, 로퍼"
    elif 10 <= temp < 15:
        return "클래식 트렌치 & 자켓 룩 🧥", "트렌치코트, 블레이저, 니트웨어, 데님"
    else:
        return "따뜻한 윈터 패딩 룩 🧣", "헤비 아우터, 울 코트, 캐시미어 머플러, 방한 부츠"

# 귀엽고 둥글둥글한 UI 스타일 정의
st.html("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* { font-family: 'Pretendard', sans-serif; }

.stApp {
    background-color: #f8fafc;
}

/* Streamlit 내장 border 컨테이너를 둥글고 세련되게 커스텀 */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px !important;
    background-color: #ffffff !important;
    border: 1px solid #edf2f7 !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03) !important;
    padding: 16px 20px !important;
    margin-bottom: 16px;
}

.title-tag {
    font-size: 1.05rem;
    font-weight: 700;
    color: #334155;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.temp-text {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
}
.big-rate {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}
.sub-meta {
    font-size: 0.88rem;
    color: #64748b;
    margin-top: 4px;
}
.calc-result-badge {
    background: #ecfdf5;
    color: #059669;
    font-size: 1.05rem;
    font-weight: 700;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid #a7f3d0;
    margin-top: 14px;
}
.fashion-tip-box {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 14px;
    padding: 12px 16px;
    margin-top: 14px;
}
</style>
""")

# 타이틀 변경
st.markdown("## 🌤️ 국가별 날씨 & 환율")

c1, c2 = st.columns([1.5, 1.5])
with c1:
    selected_country = st.selectbox("🌍 국가 선택", list(COUNTRY_CITY_MAP.keys()), index=0)
with c2:
    selected_city_label = st.selectbox("🏙️ 도시 선택", list(COUNTRY_CITY_MAP[selected_country].keys()))

target_city = COUNTRY_CITY_MAP[selected_country][selected_city_label]
curr_info = CURRENCY_MAP[selected_country]

rates = get_all_rates(EXCHANGE_API_KEY)
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={target_city}&appid={API_KEY}&units=metric&lang=kr"
res = requests.get(weather_url)

if res.status_code == 200:
    w_data = res.json()
    temp = round(w_data["main"]["temp"], 1)
    feels_like = round(w_data["main"]["feels_like"], 1)
    temp_max = round(w_data["main"]["temp_max"], 1)
    temp_min = round(w_data["main"]["temp_min"], 1)
    humidity = w_data["main"]["humidity"]
    wind_speed = w_data["wind"]["speed"]
    pressure = w_data["main"]["pressure"]
    visibility = round(w_data.get("visibility", 10000) / 1000, 1)
    weather_desc = w_data["weather"][0]["description"]
    icon_code = w_data["weather"][0]["icon"]

    # 환율 로직: 한국이면 기본 달러(USD), 해외면 해당 국가 통화
    active_currency = "USD" if curr_info["code"] == "KRW" else curr_info["code"]
    active_symbol = "$" if curr_info["code"] == "KRW" else curr_info["symbol"]
    curr_rate = rates.get(active_currency, 0.0) if rates else 0.0
    usd_rate = rates.get("USD", 1340.0) if rates else 1340.0
    jpy_rate = rates.get("JPY", 9.0) if rates else 9.0

    # 1. 상단 메인 날씨 & 환율 카드
    with st.container(border=True):
        left_head, right_head = st.columns([1.5, 1])
        with left_head:
            st.html(f"""
            <div style="display:flex; align-items:center; gap:16px;">
                <img src="https://openweathermap.org/img/wn/{icon_code}@2x.png" width="70">
                <div>
                    <div class="temp-text">{temp}°C <span style="font-size:1.4rem; font-weight:600; color:#475569;">({weather_desc})</span></div>
                    <div class="sub-meta">체감 {feels_like}°C &nbsp;|&nbsp; 최고 {temp_max}°C &nbsp;|&nbsp; 최저 {temp_min}°C</div>
                </div>
            </div>
            """)
        with right_head:
            st.html(f"""
            <div style="text-align:right;">
                <div style="font-size:0.85rem; color:#64748b; font-weight:600;">1 {active_currency} 기준 원화(KRW)</div>
                <div class="big-rate">₩ {curr_rate:,.2f}</div>
                <div class="sub-meta">통화 기호: {active_symbol} &nbsp;|&nbsp; 기준: 1 USD = ₩{usd_rate:,.1f}</div>
            </div>
            """)

    # 2. 상세 날씨 지표 카드
    with st.container(border=True):
        st.markdown('<div class="title-tag">📊 상세 날씨 지표</div>', unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("습도", f"{humidity}%")
        s2.metric("풍속", f"{wind_speed} m/s")
        s3.metric("기압", f"{pressure} hPa")
        s4.metric("가시거리", f"{visibility} km")

    # 3. 하단 2분할 카드 (경비 계산기 & 글로벌 주요 통화)
    col_calc, col_global = st.columns([1.1, 1.1])

    with col_calc:
        with st.container(border=True):
            st.markdown(f'<div class="title-tag">🔢 {selected_city_label} 현지 경비 계산기</div>', unsafe_allow_html=True)
            input_val = st.number_input(
                f"현지 금액 입력 ({active_currency})",
                min_value=1.0,
                value=100.0,
                step=10.0
            )
            converted_won = input_val * curr_rate
            st.markdown(f"""
            <div class="calc-result-badge">
                👉 <b>원화 환산액:</b> ₩ {converted_won:,.0f} 원
            </div>
            """, unsafe_allow_html=True)

    with col_global:
        with st.container(border=True):
            st.markdown('<div class="title-tag">🌐 글로벌 주요 통화 참고</div>', unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            g1.metric("USD / KRW", f"₩ {usd_rate:,.2f}")
            g2.metric("100 JPY / KRW", f"₩ {(jpy_rate * 100):,.2f}")
            
            fashion_title, fashion_tip = get_fashion_lookbook(temp)
            st.markdown(f"""
            <div class="fashion-tip-box">
                <div style="font-weight:700; font-size:0.9rem; color:#0369a1;">✨ 추천 옷차림: {fashion_title}</div>
                <div style="font-size:0.85rem; color:#334155; margin-top:2px;">{fashion_tip}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.error("날씨 정보를 불러올 수 없습니다. API 키와 도시명을 확인해주세요.")