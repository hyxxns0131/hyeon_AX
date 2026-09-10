import streamlit as st
import pandas as pd
import requests
import base64
import os
import random
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------------
# 1. 상위 폴더의 .env 및 환경변수 로드
# -------------------------------------------------------------
current_dir = Path(__file__).resolve().parent
parent_env_path = current_dir.parent / ".env"

if parent_env_path.exists():
    load_dotenv(dotenv_path=parent_env_path)
else:
    load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# -------------------------------------------------------------
# 2. 페이지 설정
# -------------------------------------------------------------
st.set_page_config(
    page_title="싸이월드 ▷미니홈피",
    page_icon="🧡",
    layout="wide"
)

# -------------------------------------------------------------
# 3. DOSGothic 폰트 로드 & 싸이월드 미니홈피 CSS
# -------------------------------------------------------------
FONT_DIR = r"C:\Users\user\hyeon_AX\exchange"

def get_font_base64(directory, font_base_name="DOSGothic"):
    extensions = [".ttf", ".otf", ".woff", ".woff2"]
    for ext in extensions:
        font_path = os.path.join(directory, font_base_name + ext)
        if os.path.exists(font_path):
            with open(font_path, "rb") as f:
                data = f.read()
            font_format = "truetype" if ext in [".ttf", ".otf"] else ext.replace(".", "")
            return base64.b64encode(data).decode(), font_format
            
    direct_path = os.path.join(directory, font_base_name)
    if os.path.exists(direct_path):
        with open(direct_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode(), "truetype"
    return None, None

font_b64, font_format = get_font_base64(FONT_DIR, "DOSGothic")

font_face_css = ""
if font_b64:
    font_face_css = f"""
    @font-face {{
        font-family: 'DOSGothic';
        src: url(data:font/{font_format};base64,{font_b64}) format('{font_format}');
        font-weight: normal;
        font-style: normal;
    }}
    html, body, [class*="css"], .stMarkdown, .stSelectbox, .stNumberInput, .stButton, div, span, p, input, select {{
        font-family: 'DOSGothic', monospace, 'Gulim', sans-serif !important;
    }}
    """

st.markdown(f"""
<style>
{font_face_css}

/* 기본 여백 조정 */
.block-container {{
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}}

/* 전체 윈도우 배경 (그레이톤) */
.stApp {{
    background-color: #A3B8CC;
}}

/* 윈도우 익스플로러 창 스타일 */
.win-window {{
    background-color: #ECE9D8;
    border: 3px solid #0055EA;
    border-radius: 6px 6px 0 0;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    margin-bottom: 8px;
}}

.win-titlebar {{
    background: linear-gradient(to right, #0058EE, #3B93FF);
    color: white;
    padding: 3px 8px;
    font-size: 13px;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.win-buttons {{
    font-family: 'Courier New', monospace;
    font-weight: bold;
}}

/* 싸이월드 가죽 다이어리 커버 */
.cy-diary-wrapper {{
    background-color: #27B1BF;
    border: 3px solid #16808B;
    border-radius: 16px;
    padding: 14px 14px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.15);
}}

/* 상단 흰색 점선 플레이어 바 (요청하신 부분!) */
.cy-top-player {{
    background-color: #FFFFFF;
    border: 2px dashed #16808B;
    border-radius: 16px;
    padding: 8px 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
}}

.player-left {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.play-badge {{
    background: #FF5E00;
    color: white;
    font-size: 11px;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.5px;
    animation: blink 1.2s infinite ease-in-out;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.6; }}
}}

.song-title {{
    font-size: 13px;
    font-weight: bold;
    color: #1E3A5F;
}}

.player-controls {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: #444;
}}

.equalizer {{
    display: inline-flex;
    align-items: flex-end;
    gap: 2px;
    height: 12px;
}}
.eq-bar {{
    width: 3px;
    background-color: #FF5E00;
    border-radius: 1px;
    animation: eq-bounce 0.8s infinite ease-in-out;
}}
.eq-bar:nth-child(1) {{ height: 40%; animation-delay: 0.1s; }}
.eq-bar:nth-child(2) {{ height: 80%; animation-delay: 0.3s; }}
.eq-bar:nth-child(3) {{ height: 60%; animation-delay: 0.2s; }}
.eq-bar:nth-child(4) {{ height: 100%; animation-delay: 0.4s; }}

@keyframes eq-bounce {{
    0%, 100% {{ height: 30%; }}
    50% {{ height: 100%; }}
}}

.progress-track {{
    width: 100px;
    height: 6px;
    background: #E2E8F0;
    border-radius: 3px;
    position: relative;
    overflow: hidden;
}}
.progress-fill {{
    width: 45%;
    height: 100%;
    background: linear-gradient(to right, #FF8F45, #FF5E00);
}}

/* 메인 흰색 내지 */
.cy-diary-inner {{
    background-color: #FFFFFF;
    border: 2px dashed #66C5CC;
    border-radius: 12px;
    padding: 14px;
    position: relative;
}}

/* 좌측 프로필 박스 */
.profile-box {{
    background-color: #FAFAFA;
    border: 1px solid #D3DFE6;
    border-radius: 6px;
    padding: 12px;
    text-align: center;
}}

.today-stat {{
    font-size: 12px;
    color: #444;
    font-weight: bold;
    margin-bottom: 8px;
}}
.today-stat span.red {{ color: #EE2B2B; }}
.today-stat span.blue {{ color: #1B78D5; }}

.minimi-frame {{
    border: 1px solid #CCD5DB;
    background-color: #FFF;
    padding: 10px;
    border-radius: 4px;
    margin: 8px 0;
}}

.today-feel {{
    border: 1px solid #ADC2D1;
    background: #F7FAFC;
    font-size: 12px;
    padding: 3px;
    border-radius: 3px;
    color: #333;
    margin-bottom: 10px;
}}

.profile-desc {{
    font-size: 12px;
    color: #666;
    line-height: 1.5;
    text-align: left;
    padding: 8px 4px;
    border-top: 1px dotted #CCD5DB;
    border-bottom: 1px dotted #CCD5DB;
}}

/* 본문 타이틀 행 */
.cy-head-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #3399A8;
    padding-bottom: 6px;
    margin-bottom: 10px;
}}

.cy-home-title {{
    font-size: 18px;
    font-weight: bold;
    color: #0E5E6F;
}}

.cy-home-url {{
    font-size: 11px;
    color: #888;
}}

.mini-room-title {{
    font-size: 13px;
    font-weight: bold;
    color: #FF5E00;
    margin-bottom: 8px;
    border-bottom: 1px dotted #FF5E00;
    padding-bottom: 4px;
}}

/* 오렌지 버튼 */
.stButton>button {{
    background: linear-gradient(to bottom, #FF8F45 0%, #FF5900 100%) !important;
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: bold !important;
    border: 1px solid #D64600 !important;
    border-radius: 4px !important;
    padding: 5px 12px !important;
    box-shadow: 1px 1px 0px #8C2E00 !important;
    width: 100%;
}}

.stButton>button:hover {{
    background: linear-gradient(to bottom, #FFA366 0%, #FF7024 100%) !important;
}}

/* 탭 메뉴 */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: 2px solid #27B1BF;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: #27B1BF;
    color: white !important;
    border-radius: 4px 4px 0 0;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: bold;
}}
.stTabs [aria-selected="true"] {{
    background-color: #FFFFFF !important;
    color: #0E5E6F !important;
    border: 2px solid #27B1BF;
    border-bottom: 2px solid white;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. 여행 국가별 기본 데이터 (100 JPY 기준)
# -------------------------------------------------------------
COUNTRY_DATA = {
    "일본 (Tokyo / Osaka) 🇯🇵": {
        "code": "JPY",
        "unit": 100,
        "symbol": "¥",
        "default_rate_per_unit": 915.50,
        "desc": "ㄴr는 ㄱr끔.. 일본 편의점 털러 뱅기를 탄ㄷr..☆",
        "places": [
            "도쿄 시부야 스카이 (노을 보며 눈물 한 방울..)",
            "교토 아라시야마 치쿠린 (대나무 숲에서 감성 충전)",
            "오사카 도톤보리 글리코상 앞 (추억의 만세 포즈 찰칵!)"
        ],
        "food": [
            "진한 돈코츠 라멘 & 수제 교자 (이게 바로 행복이지..)",
            "입에서 살살 녹는 와규 스키야키",
            "편의점 푸딩 & 타마고 산도 (필수 코스!)"
        ],
        "tips": [
            "스이카(Suica) 교통카드 폰에 쏙 넣고 다니면 완전 간지남.",
            "동전이 많이 생기니 분리형 동전 지갑 안 챙기면 대참사!",
            "일본 택시는 문이 자동으로 열리니까 손 대지 말기 약속~"
        ],
        "caution": [
            "길빵(길거리 흡연) 절대 금지! 걸리면 벌금 물어요 ㅠ_ㅠ",
            "도쿄는 에스컬레이터 왼쪽, 오사카는 오른쪽에 서는 센스!",
            "작은 이자카야는 현금만 받는 곳이 많으니 엔화 넉넉히 챙기기."
        ],
        "slider_range": (850.0, 1050.0)
    },
    "미국 (New York / LA) 🇺🇸": {
        "code": "USD",
        "unit": 1,
        "symbol": "$",
        "default_rate_per_unit": 1338.00,
        "desc": "Broadway를 걸으며.. 뉴요커가 된 것 같은 착각 속으로..",
        "places": [
            "뉴욕 센트럴파크 (돗자리 펴고 이어폰 꽂기)",
            "LA 그리피스 천문대 (라라랜드 재현해보기)",
            "그랜드 캐니언 (대자연 앞에서 숙연해지는 하루..)"
        ],
        "food": [
            "육즙 좔좔 흐르는 뉴욕 오리지널 수제 버거",
            "두툼한 티본 스테이크 썰기",
            "서부 감성 인앤아웃 버거 & 크림치즈 베이글"
        ],
        "tips": [
            "카드가 다 돼서 현금은 진짜 비상금만 조금 있으면 OK!",
            "출국 전 ESTA 비자 발급 안 받으면 비행기 못 타요..",
            "식당에서 팁(Tip) 18~20% 주는 거 잊지 말기!"
        ],
        "caution": [
            "밤늦게 지하철이나 외진 골목 혼자 걸어다니면 위험해요!",
            "길거리에서 술병 들고 마시면 경찰 출동함.. 조심조심.",
            "렌터카 차 안에 가방 보이면 차창 깨질 수 있으니 트렁크에 넣기!"
        ],
        "slider_range": (1250.0, 1450.0)
    },
    "유럽 (Paris / Western Europe) 🇫🇷": {
        "code": "EUR",
        "unit": 1,
        "symbol": "€",
        "default_rate_per_unit": 1475.20,
        "desc": "음악과 낭만이 흐르는 센강.. 에펠탑 야경에 취해본ㄷr..★",
        "places": [
            "파리 에펠탑 화이트 점등식 (반짝일 때 소원 빌기)",
            "루브르 박물관 모나리자와 눈맞춤",
            "몽마르트르 언덕 (거리의 화가에게 초상화 부탁하기)"
        ],
        "food": [
            "갓 구워낸 버터 풍미 가득 크루아상 & 에스프레소",
            "프랑스 정통 비프 부르기뇽 & 에스카르고",
            "알록달록 달콤한 수제 마카롱"
        ],
        "tips": [
            "뮤지엄 패스 미리 예약 안 하면 하루 종일 줄만 설 수도..",
            "가게 들어갈 때 '봉주르~' 인사 한마디면 대우가 달라져요.",
            "나비고(Navigo) 교통패스로 파리 지하철 정복하기!"
        ],
        "caution": [
            "에펠탑 근처 서명단, 팔찌 강매, 소매치기 진짜 조심!",
            "가방은 꼭 앞으로 매고 핸드폰 스트랩 꽉 쥐고 다니기.",
            "유럽은 화장실도 돈 받으니까 식당 갔을 때 미리미리 다녀오기."
        ],
        "slider_range": (1350.0, 1650.0)
    },
    "베트남 (Danang / Hanoi) 🇻🇳": {
        "code": "VND",
        "unit": 100,
        "symbol": "₫",
        "default_rate_per_unit": 5.40,
        "desc": "하루 종일 쌀국수 먹고 마사지 받으며 힐링하는 지상낙원..",
        "places": [
            "다낭 미케비치 해변 (야자수 아래서 낮잠 자기)",
            "호이안 올드타운 (등불 아래서 소원배 띄우기)",
            "바나힐 골든브릿지 (구름 위의 거대한 손)"
        ],
        "food": [
            "깊고 진한 국물의 소고기 쌀국수 & 분짜",
            "바삭하고 든든한 반미(Banh Mi) 샌드위치",
            "달달한 콩카페 코코넛 스무디 커피"
        ],
        "tips": [
            "택시는 바가지 쓰지 말고 무조건 '그랩(Grab)' 부르기!",
            "한국에서 5만 원권 챙겨가서 현지 환전소 가는 게 제일 이득!",
            "돈 단위가 크니까 '0' 하나 빼고 나누기 2 하면 원화 가격!"
        ],
        "caution": [
            "오토바이 날치기 조심! 길가 쪽으로 폰 들고 서있지 말기.",
            "수돗물 절대 마시지 말고 편의점에서 생수 사마시기.",
            "도로 건널 땐 뛰지 말고 천천히 일정한 속도로 걸어가야 안 부딪힘!"
        ],
        "slider_range": (4.5, 6.5)
    }
}

# -------------------------------------------------------------
# 5. 여행 운세 데이터
# -------------------------------------------------------------
FORTUNES = {
    "JPY": [
        {"fortune": "우연히 들어간 작은 골목 식당에서 인생 라멘을 맛볼 운세..★", "item": "아날로그 필름 카메라", "color": "벚꽃 도트 핑크", "hex": "#FFB7C5"},
        {"fortune": "가챠 뽑기 한 방에 원하는 최애 캐릭터 피규어 득템 대성공!", "item": "키티 동전지갑", "color": "레몬 크림 옐로우", "hex": "#FFF3B0"},
        {"fortune": "환승도 척척, 비 한 방울 안 맞고 쾌적하게 여행할 완벽한 타이밍!", "item": "손수건", "color": "소다 블루", "hex": "#A2D2FF"}
    ],
    "USD": [
        {"fortune": "브루클린 다리 위에서 인생 미니홈피 대문 사진을 건질 운세!", "item": "레트로 선글라스", "color": "코발트 스카이", "hex": "#3A86FF"},
        {"fortune": "친절한 현지인과 유쾌한 스몰토크로 하루 종일 기분 업!", "item": "컨버스 스니커즈", "color": "빈티지 캐러멜", "hex": "#DDA15E"},
        {"fortune": "복잡한 도심 속 나만의 조용하고 아늑한 카페를 발견할 하루.", "item": "줄이어폰", "color": "세이지 올리브", "hex": "#CCD5AE"}
    ],
    "EUR": [
        {"fortune": "오후 햇살 가득한 테라스에서 듣는 버스킹에 심장이 콩닥콩닥..", "item": "가죽 다이어리", "color": "로맨틱 와인", "hex": "#A3485E"},
        {"fortune": "에펠탑 조명이 반짝이는 순간 평생 잊지 못할 낭만을 만끽할 운세!", "item": "실크 목스카프", "color": "앤틱 아이보리", "hex": "#FAF0CA"},
        {"fortune": "루브르 명작 앞에서 깊은 영감을 받아 다이어리 한 페이지를 채울 날!", "item": "베레모", "color": "빈티지 라벤더", "hex": "#BDB2FF"}
    ],
    "VND": [
        {"fortune": "시원한 마사지와 코코넛 스무디 한 잔에 피로가 사르르 녹아내려요!", "item": "라탄 미니백", "color": "망고 오렌지", "hex": "#FF9F1C"},
        {"fortune": "야시장 상인분이 기분 좋게 덤을 얹어주는 따뜻한 인심을 경험할 운세!", "item": "휴대용 손선풍기", "color": "민트 애플그린", "hex": "#2EC4B6"},
        {"fortune": "노을 지는 호이안 소원배 위에서 빈 소원이 실제로 이루어질 예감..★", "item": "밀짚 모자", "color": "살구 피치", "hex": "#FFBF69"}
    ]
}

# -------------------------------------------------------------
# 6. 실시간 환율 조회 함수
# -------------------------------------------------------------
@st.cache_data(ttl=600)
def fetch_current_rate(currency_code, unit, default_rate):
    if not EXCHANGE_API_KEY:
        return default_rate, "오프라인 모드"
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/KRW"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            data = res.json()
            if data.get("result") == "success":
                rates = data.get("conversion_rates", {})
                if currency_code in rates:
                    krw_per_1_foreign = 1.0 / rates[currency_code]
                    rate_per_unit = round(krw_per_1_foreign * unit, 2)
                    return rate_per_unit, "실시간 연동 성공"
    except Exception:
        pass
    return default_rate, "대체 환율 적용"

# -------------------------------------------------------------
# 7. 상단 윈도우 익스플로러 창틀 바
# -------------------------------------------------------------
st.markdown("""
<div class="win-window">
    <div class="win-titlebar">
        <span>싸이월드 ▷미니홈피 - Microsoft Internet Explorer</span>
        <span class="win-buttons">_ □ ✕</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 8. 싸이월드 가죽 다이어리 바인더 & 상단 BGM 플레이어 (흰색 바 영역)
# -------------------------------------------------------------
st.markdown('<div class="cy-diary-wrapper">', unsafe_allow_html=True)

# 바로 이 부분이 첨부해주신 이미지의 흰색 점선 바 영역입니다!
st.markdown("""
<div class="cy-top-player">
    <div class="player-left">
        <span class="play-badge">▶ PLAYING</span>
        <span class="song-title">♪ 프리스타일 - 수취인불명 (feat. 희영)</span>
        <div class="equalizer">
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
        </div>
    </div>
    <div class="player-controls">
        <div class="progress-track"><div class="progress-fill"></div></div>
        <span><b>01:42</b> / 04:15</span>
        <span style="cursor:pointer; color:#FF5E00; font-weight:bold;">[가사보기]</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 다이어리 내부 흰색 종이 내지 시작
st.markdown('<div class="cy-diary-inner">', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2.7], gap="medium")

# --- 좌측 프로필 패널 ---
with col_left:
    st.markdown("""
    <div class="profile-box">
        <div class="today-stat">
            TODAY <span class="red">28375</span> | TOTAL <span class="blue">28388</span>
        </div>
        <div class="minimi-frame">
            <div style="font-size: 42px; margin-bottom: 4px;">🎒✈️</div>
            <div style="font-size: 11px; color:#555; font-weight:bold;">[방랑자 미니미]</div>
        </div>
        <div class="today-feel">
            <b>TODAY IS..</b> <span style="color:#FF5E00;">♬ 설레임</span>
        </div>
        <div class="profile-desc">
            세상은 넓고<br>
            가고 싶은 곳은 많다..<br>
            환율아 내려가라..★<br><br>
            <b>홈주인</b> 여행자
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.selectbox("★ 나의 1촌 목록 파도타기", ["일촌 파도타기▼", "철수네 미니홈피", "유리 다이어리", "맹구 돌수집 갤러리"], index=0)

# --- 우측 메인 콘텐츠 패널 ---
with col_right:
    st.markdown("""
    <div class="cy-head-row">
        <div class="cy-home-title">여행자님의 미니홈피</div>
        <div class="cy-home-url">http://www.cyworld.com/travel_love</div>
    </div>
    """, unsafe_allow_html=True)

    # 탭 메뉴
    tab_home, tab_diary, tab_photo, tab_guest = st.tabs([
        "홈 (환율/계산기)",
        "다이어리 (꿀팁)",
        "사진첩 (명소&맛집)",
        "방명록 (주의사항)"
    ])

    # 1. 홈 탭 (환율 계산기 + 운세 + 일촌 메일 알림)
    with tab_home:
        st.markdown('<div class="mini-room-title">Mini Room : 실시간 환율 & 환전소</div>', unsafe_allow_html=True)
        
        selected_country = st.selectbox(
            "목적지 선택하기 (나라를 골라줘!)",
            options=list(COUNTRY_DATA.keys()),
            index=0
        )
        country_info = COUNTRY_DATA[selected_country]

        current_unit_rate, status_msg = fetch_current_rate(
            country_info['code'], 
            country_info['unit'], 
            country_info['default_rate_per_unit']
        )
        unit_display = f"{country_info['unit']:,} {country_info['code']}"

        c_rate1, c_rate2 = st.columns([1, 1])
        with c_rate1:
            st.metric(
                label=f"현재 기준 환율 ({unit_display})",
                value=f"{current_unit_rate:,.2f} 원",
                help=f"연동 상태: {status_msg}"
            )
        with c_rate2:
            st.info(f"💭 {country_info['desc']}")

        calc_tab1, calc_tab2 = st.tabs(["외화 ➔ 원화 환산", "원화 ➔ 외화 환산"])
        with calc_tab1:
            f_val = st.number_input(
                f"사용할 금액 ({country_info['symbol']} {country_info['code']})",
                min_value=0.0,
                value=float(country_info['unit'] * 10),
                step=float(country_info['unit'])
            )
            total_krw = (f_val / country_info['unit']) * current_unit_rate
            st.success(f"필요한 도토리(원화): **약 {total_krw:,.0f} 원**")

        with calc_tab2:
            k_val = st.number_input("보유 중인 원화 (KRW ₩)", min_value=0, value=300000, step=50000)
            total_foreign = (k_val / current_unit_rate) * country_info['unit']
            st.success(f"바꿀 수 있는 외화: **약 {total_foreign:,.2f} {country_info['symbol']} ({country_info['code']})**")

        st.markdown("---")

        # 오늘의 여행 운세
        st.markdown('<div class="mini-room-title">포춘쿠키 : 오늘의 여행 운세 뽑기</div>', unsafe_allow_html=True)
        if st.button("🔮 오늘의 여행 운세 캡슐 열기"):
            country_fortunes = FORTUNES.get(country_info['code'], FORTUNES["JPY"])
            st.session_state[f"fortune_{country_info['code']}"] = random.choice(country_fortunes)

        current_fortune = st.session_state.get(f"fortune_{country_info['code']}")
        if current_fortune:
            st.markdown(f"""
            <div style="background:#FFF9E6; border:1px solid #FFDE7D; padding:10px 14px; border-radius:6px; font-size:12px; margin-top:8px;">
                <div style="color:#B36B00; font-weight:bold; margin-bottom:4px;">💌 오늘의 운세: {current_fortune['fortune']}</div>
                <div style="color:#555;">🎒 <b>행운 소품:</b> <span style="color:#FF5E00;">{current_fortune['item']}</span> | 🎨 <b>행운 색상:</b> <span style="color:{current_fortune['hex']}; font-weight:bold;">{current_fortune['color']}</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 일촌 목표 환율 메일 알림 신청
        st.markdown('<div class="mini-room-title">일촌 알리미 : 목표 환율 메일 예약</div>', unsafe_allow_html=True)
        min_val, max_val = country_info["slider_range"]
        suggested_target = round(current_unit_rate * 0.98, 1)
        suggested_target = max(min_val, min(max_val, suggested_target))

        target_rate = st.slider(
            f"목표 환율 ({unit_display} 기준, 원)",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(suggested_target),
            step=0.1
        )

        alert_cond = st.radio(
            "발송 조건",
            ["목표 환율 이하로 떨어졌을 때 (환전 대박 찬스!)", "목표 환율 이상으로 올랐을 때"],
            index=0
        )

        user_email = st.text_input("소식을 받을 이메일 주소", placeholder="cyworld_traveler@nate.com")

        if st.button("★ 일촌 메일 알림 신청하기 ★"):
            if not user_email or "@" not in user_email:
                st.error("올바른 이메일 주소를 입력해주세요!")
            else:
                if "alerts" not in st.session_state:
                    st.session_state.alerts = []
                st.session_state.alerts.append({
                    "여행지": selected_country.split()[0],
                    "기준단위": unit_display,
                    "목표환율": f"{target_rate:,.1f}원",
                    "조건": "이하" if "이하" in alert_cond else "이상",
                    "이메일": user_email
                })
                st.balloons()
                st.success(f"예약 완료! {unit_display} 환율이 {target_rate:,.1f}원에 도달하면 `{user_email}`로 알림을 보냅니다.")

        if "alerts" in st.session_state and st.session_state.alerts:
            st.markdown("##### 📋 일촌 예약 수첩")
            st.dataframe(pd.DataFrame(st.session_state.alerts), use_container_width=True)

    # 2. 다이어리 탭 (여행 꿀팁)
    with tab_diary:
        st.markdown(f'<div class="mini-room-title">Diary : {selected_country} 여행 꿀팁 일기</div>', unsafe_allow_html=True)
        for idx, t in enumerate(country_info["tips"], 1):
            st.markdown(f"""
            <div style="border-bottom: 1px dotted #B8D3DD; padding: 8px 0; font-size: 13px;">
                <b>Day {idx}.</b> {t}
            </div>
            """, unsafe_allow_html=True)

    # 3. 사진첩 탭 (명소 & 맛집)
    with tab_photo:
        st.markdown(f'<div class="mini-room-title">Photo : {selected_country} 스크랩 명소 & 맛집</div>', unsafe_allow_html=True)
        st.markdown("##### 📍 꼭 가봐야 할 명소")
        for p in country_info["places"]:
            st.write(f"- 📷 **{p}**")
        
        st.markdown("---")
        st.markdown("##### 🍴 감동의 로컬 맛집")
        for f in country_info["food"]:
            st.write(f"- ☕ **{f}**")

    # 4. 방명록 탭 (주의사항)
    with tab_guest:
        st.markdown(f'<div class="mini-room-title">Guest Book : 안전 여행을 위한 일촌들의 당부글</div>', unsafe_allow_html=True)
        for c in country_info["caution"]:
            st.markdown(f"""
            <div style="background-color: #F8F9FA; border: 1px solid #E2E8F0; padding: 10px; border-radius: 4px; margin-bottom: 8px; font-size: 13px;">
                🚨 <b>주의사항:</b> {c}
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)