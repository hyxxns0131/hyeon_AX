import streamlit as st
import os
import base64
import time

# 페이지 설정
st.set_page_config(
    page_title="무역 직무 MBTI 테스트",
    page_icon="🚢",
    layout="centered"
)

# -------------------------------------------------------------
# [폰트 설정] 로컬 폰트 로드
# -------------------------------------------------------------
def get_custom_font_css():
    possible_paths = [
        r"C:\Users\user\hyeon_AX\MBTI\font2",
        r"C:\Users\user\hyeon_AX\MBTI\font2.ttf",
        r"C:\Users\user\hyeon_AX\MBTI\font2.otf",
        r"C:\Users\user\hyeon_AX\MBTI\font2.woff",
        r"C:\Users\user\hyeon_AX\MBTI\font2.woff2",
        "font2",
        "font2.ttf"
    ]
    
    font_path = None
    for path in possible_paths:
        if os.path.exists(path) and os.path.isfile(path):
            font_path = path
            break

    if font_path:
        with open(font_path, "rb") as f:
            font_data = f.read()
        b64_font = base64.b64encode(font_data).decode("utf-8")
        return f"""
        @font-face {{
            font-family: 'CustomFont';
            src: url(data:font/truetype;charset=utf-8;base64,{b64_font}) format('truetype');
            font-weight: normal;
            font-style: normal;
        }}
        html, body, [class*="css"], .stMarkdown, p, button, input, label, h1, h2, h3, h4, span, div {{
            font-family: 'CustomFont', sans-serif !important;
        }}
        """
    else:
        return """
        html, body, [class*="css"], .stMarkdown, p, button, input, label, h1, h2, h3, h4, span, div {
            font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif !important;
        }
        """

# -------------------------------------------------------------
# 스타일 적용 (선택지 글자 크기 안정적 확대 & 파스텔 하늘색)
# -------------------------------------------------------------
st.markdown(f"""
    <style>
    {get_custom_font_css()}

    /* 전체 배경 */
    .stApp {{
        background-color: #F0F6FA;
    }}
    
    /* 타이틀 영역 */
    .title-text {{
        font-size: 2.1rem;
        font-weight: 800;
        text-align: center;
        color: #1A365D;
        margin-bottom: 6px;
    }}
    .sub-text {{
        font-size: 1.05rem;
        text-align: center;
        color: #2B6CB0;
        margin-bottom: 20px;
    }}

    /* 시작 화면 카드 */
    .intro-card {{
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 32px 24px;
        border: 2px solid #BEE3F8;
        box-shadow: 0 4px 18px rgba(43, 108, 176, 0.07);
        text-align: center;
        margin: 10px 0 24px 0;
    }}
    .intro-icon {{
        font-size: 3.2rem;
        margin-bottom: 10px;
    }}
    .intro-title {{
        font-size: 1.5rem;
        font-weight: bold;
        color: #1A365D;
        margin-bottom: 14px;
        word-break: keep-all;
    }}
    .intro-desc {{
        font-size: 1.05rem;
        color: #4A5568;
        line-height: 1.8;
        word-break: keep-all;
        margin-bottom: 18px;
    }}
    .intro-info-box {{
        background-color: #F7FAFC;
        border-radius: 12px;
        padding: 14px;
        border: 1px dashed #63B3ED;
        text-align: left;
        font-size: 0.95rem;
        color: #2B6CB0;
        line-height: 1.6;
    }}
    
    /* 질문 카드 스타일 (1.42rem) */
    .question-box {{
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px 22px;
        border: 1.5px solid #CBD5E0;
        box-shadow: 0 4px 14px rgba(43, 108, 176, 0.05);
        margin: 14px 0 20px 0;
    }}
    .question-text {{
        font-size: 1.42rem;
        font-weight: 800;
        color: #1A202C;
        line-height: 1.55;
        word-break: keep-all;
    }}

    /* 🔍 [핵심 수정] st.button 내부 텍스트를 질문보다 살짝 작게 (1.22rem) 안정적 확대 */
    div.choice-btn-wrap > div.stButton > button {{
        background-color: #FFFFFF !important;
        border: 2px solid #CBD5E0 !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        text-align: left !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 80px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
        transition: all 0.15s ease-in-out !important;
        width: 100% !important;
    }}
    
    div.choice-btn-wrap > div.stButton > button p,
    div.choice-btn-wrap > div.stButton > button span,
    div.choice-btn-wrap > div.stButton > button div {{
        font-size: 1.22rem !important;
        font-weight: 600 !important;
        color: #2D3748 !important;
        line-height: 1.65 !important;
        word-break: keep-all !important;
        text-align: left !important;
    }}

    div.choice-btn-wrap > div.stButton > button:hover {{
        background-color: #EBF8FF !important;
        border-color: #3182CE !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(49, 130, 206, 0.16) !important;
    }}
    div.choice-btn-wrap > div.stButton > button:hover p,
    div.choice-btn-wrap > div.stButton > button:hover span {{
        color: #1A365D !important;
    }}

    /* 하단 보조 버튼 (이전 / 처음으로) */
    div.nav-btn-wrap > div.stButton > button {{
        background-color: #3182CE !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 20px !important;
    }}
    div.nav-btn-wrap > div.stButton > button p,
    div.nav-btn-wrap > div.stButton > button span {{
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
    }}
    div.nav-btn-wrap > div.stButton > button:hover {{
        background-color: #2B6CB0 !important;
    }}

    /* 🥁 로딩 애니메이션 */
    @keyframes drum-beat {{
        0% {{ transform: scale(1) rotate(0deg); }}
        25% {{ transform: scale(1.08) rotate(-4deg); }}
        50% {{ transform: scale(0.96) rotate(0deg); }}
        75% {{ transform: scale(1.08) rotate(4deg); }}
        100% {{ transform: scale(1) rotate(0deg); }}
    }}
    @keyframes drum-stick {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(10px); }}
    }}
    .loading-container {{
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 40px 20px;
        border: 2px dashed #63B3ED;
        text-align: center;
        margin: 30px 0;
    }}
    .drummer-animals {{
        font-size: 4rem;
        display: inline-block;
        animation: drum-beat 0.55s infinite ease-in-out;
    }}
    .drum-sticks {{
        font-size: 2.8rem;
        animation: drum-stick 0.28s infinite alternate ease-in-out;
    }}
    .loading-title {{
        font-size: 1.45rem;
        font-weight: 800;
        color: #1A365D;
        margin-top: 14px;
    }}
    .loading-sub {{
        font-size: 1.05rem;
        color: #3182CE;
        font-weight: 600;
        margin-top: 6px;
    }}

    /* 🐾 직무 캐릭터 카드 스타일 */
    .character-card {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F7FD 100%);
        border-radius: 20px;
        padding: 24px 20px;
        border: 2px solid #90CDF4;
        box-shadow: 0 6px 18px rgba(49, 130, 206, 0.12);
        text-align: center;
        margin: 15px 0 20px 0;
    }}
    .character-avatar {{
        font-size: 4.5rem;
        line-height: 1;
        margin-bottom: 8px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }}
    .character-badge {{
        display: inline-block;
        background-color: #3182CE;
        color: #FFFFFF;
        font-size: 0.88rem;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 8px;
    }}
    .character-name {{
        font-size: 1.55rem;
        font-weight: 800;
        color: #1A365D;
        margin-bottom: 6px;
    }}
    .character-slogan {{
        font-size: 1.02rem;
        font-weight: 600;
        color: #2B6CB0;
        margin-bottom: 12px;
        font-style: italic;
    }}
    .character-item-tag {{
        display: inline-block;
        background-color: #FFFFFF;
        border: 1px solid #CBD5E0;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 0.9rem;
        color: #4A5568;
        margin: 2px 4px;
    }}

    /* 결과 박스 */
    .result-box {{
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 24px 20px;
        border: 2px solid #63B3ED;
        box-shadow: 0 4px 16px rgba(43, 108, 176, 0.08);
        margin-top: 10px;
    }}
    .result-header {{
        text-align: center;
        font-size: 1.1rem;
        color: #2B6CB0;
        font-weight: bold;
    }}
    .job-title {{
        font-size: 1.55rem;
        font-weight: 800;
        color: #1A365D;
        text-align: center;
        margin: 10px 0 14px 0;
        word-break: keep-all;
    }}

    /* 강점 배지 */
    .badge-container {{
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 18px;
        flex-wrap: wrap;
    }}
    .badge {{
        background-color: #EBF8FF;
        color: #2B6CB0;
        border: 1px solid #90CDF4;
        padding: 6px 12px;
        border-radius: 18px;
        font-size: 0.92rem;
        font-weight: bold;
    }}

    /* 해설 박스 */
    .desc-box {{
        background-color: #F7FAFC;
        border-radius: 12px;
        padding: 16px 18px;
        border-left: 5px solid #3182CE;
        margin-bottom: 10px;
    }}
    .desc-item {{
        font-size: 1rem;
        line-height: 1.7;
        color: #2D3748;
        margin-bottom: 8px;
        word-break: keep-all;
    }}

    /* 실무 가이드 박스 */
    .practical-box {{
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 22px 20px;
        border: 1px solid #BEE3F8;
        box-shadow: 0 2px 10px rgba(43, 108, 176, 0.04);
        margin-top: 14px;
        margin-bottom: 20px;
    }}
    .practical-section-title {{
        font-size: 1.12rem;
        font-weight: 800;
        color: #1A365D;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .practical-routine {{
        background-color: #F0F6FA;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 14px;
        font-size: 0.96rem;
        line-height: 1.65;
        color: #2C5282;
    }}
    .practical-point {{
        font-size: 0.97rem;
        line-height: 1.7;
        color: #4A5568;
        margin-bottom: 6px;
        word-break: keep-all;
    }}

    /* 순위 카드 */
    .rank-card {{
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .rank-title {{
        font-size: 1.02rem;
        font-weight: 700;
        color: #1A202C;
    }}
    .rank-score {{
        font-size: 0.95rem;
        color: #2B6CB0;
        font-weight: 700;
    }}

    /* 모바일 반응형 */
    @media (max-width: 640px) {{
        .title-text {{
            font-size: 1.65rem !important;
            margin-bottom: 4px;
        }}
        .sub-text {{
            font-size: 0.92rem !important;
            margin-bottom: 16px;
        }}
        .question-text {{
            font-size: 1.22rem !important;
        }}
        div.choice-btn-wrap > div.stButton > button p,
        div.choice-btn-wrap > div.stButton > button span,
        div.choice-btn-wrap > div.stButton > button div {{
            font-size: 1.12rem !important;
            line-height: 1.6 !important;
        }}
        div.choice-btn-wrap > div.stButton > button {{
            padding: 15px 14px !important;
            min-height: 72px !important;
        }}
        .character-avatar {{
            font-size: 3.8rem !important;
        }}
        .character-name {{
            font-size: 1.35rem !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 질문 데이터 (20문항)[cite: 1]
# -------------------------------------------------------------
questions = [
    # E vs I (1~5)
    {"q": "Q1. 새로운 해외 바이어와의 첫 화상 미팅이 잡혔을 때 내 모습은? 🤝", "type": "EI", "A": "직접 대화하며 친밀감을 형성하고 분위기를 주도하는 것이 기대된다.", "B": "미리 준비할 스크립트와 질문 리스트부터 꼼꼼히 정리하고 준비한다."},
    {"q": "Q2. 대규모 국제 무역 박람회(Exhibition)에 참가했을 때 나는? 🎪", "type": "EI", "A": "부스를 적극적으로 돌아다니며 명함을 주고받고 먼저 인사를 건넨다.", "B": "우리 부스에 직접 찾아오는 관심 바이어 응대에 깊이 있게 집중한다."},
    {"q": "Q3. 해외 거래처와 계약 진행 중 작은 오해가 발생했을 때 선호하는 방식은? 📞", "type": "EI", "A": "바로 메신저 콜이나 화상 통화를 걸어 직접 대화로 신속히 푼다.", "B": "관련 근거 자료와 사실관계를 서면 메일로 명확하게 정리해 전달한다."},
    {"q": "Q4. 새로운 타깃 국가의 시장 조사를 진행할 때 나의 업무 스타일은? 👥", "type": "EI", "A": "팀원들과 회의를 진행하며 대화를 통해 아이디어를 확장해 나간다.", "B": "혼자 조용히 통계 데이터와 산업 분석 리포트를 정독하며 맥락을 짚는다."},
    {"q": "Q5. 일주일간의 빡빡했던 해외 출장이 끝난 후 주말에 나는? ✈️", "type": "EI", "A": "지인들을 만나 출장 에피소드를 공유하며 활력을 채운다.", "B": "집에서 온전히 나만의 시간을 가지며 에너지를 충전한다."},

    # S vs N (6~10)
    {"q": "Q6. 새로운 수출 품목의 관세율과 HS CODE를 확인할 때 나는? 🏷️", "type": "SN", "A": "품목 분류 규정집과 실제 제품 스펙을 항목별로 꼼꼼히 대조한다.", "B": "이 제품이 글로벌 시장에서 어떤 새로운 가치와 파급력을 가질지 상상한다."},
    {"q": "Q7. 무역 실적 보고서를 작성할 때 더 눈이 가는 영역은? 📊", "type": "SN", "A": "월별 선적 수량, 통관 단가, 실질 영업이익 등 구체적인 데이터 수치", "B": "향후 3개년 글로벌 통상 트렌드와 새로운 권역별 성장 가능성"},
    {"q": "Q8. 해외 신규 물류 운송 루트를 설정해야 할 때 우선순위는? 🗺️", "type": "SN", "A": "기존에 검증된 선사와 정기 항로가 주는 안정성과 신뢰도", "B": "복합 운송이나 새로운 환적 거점 등 효율을 높일 수 있는 대안 모색"},
    {"q": "Q9. 시장 조사 중 바이어 트렌드를 분석할 때 더 집중하는 것은? 🛍️", "type": "SN", "A": "현재 시장에서 가장 잘 팔리는 베스트셀러의 규격과 가격 구조", "B": "향후 시즌을 이끌 새로운 소비자 라이프스타일과 감성 트렌드"},
    {"q": "Q10. 신용장(L/C)이나 선적 서류를 검토할 때 내 스타일은? 📄", "type": "SN", "A": "서류의 철자 하나, 수치 오차 하나까지 철저하게 대조한다.", "B": "전체적인 계약 구조와 납기 프로세스의 흐름을 먼저 확인한다."},

    # T vs F (11~15)
    {"q": "Q11. 바이어가 무리한 단가 인하(Discount)를 요청할 때 내 반응은? 💸", "type": "TF", "A": "원가 마진율과 손익분기점 데이터를 바탕으로 냉정하고 명확하게 기준을 제시한다.", "B": "바이어의 현지 상황과 고충을 경청하며 장기적 협력을 고려한 절충안을 모색한다."},
    {"q": "Q12. 운송 도중 물품 파손 클레임이 발생했을 때 먼저 머릿속에 떠오르는 것은? ⚠️", "type": "TF", "A": "인코텀즈 조건과 운송 구간별 책임 소재, 보험 처리 절차", "B": "예상치 못한 문제로 곤란해졌을 바이어와 파트너사의 입장"},
    {"q": "Q13. 함께 일하는 해외 로컬 에이전트를 평가할 때 가장 중요한 기준은? ⭐", "type": "TF", "A": "정확한 마감 일정 준수율과 계약 달성 실적", "B": "원활한 소통 의지와 상호 신뢰, 협력적인 태도"},
    {"q": "Q14. 팀원이 선적 서류 작성 중 실수를 했을 때 나의 첫 피드백은? 📋", "type": "TF", "A": "어디서 실수가 발생했는지 경로를 파악하고 재발 방지 가이드를 정리한다.", "B": "당황했을 팀원을 먼저 안심시키고 함께 수습 방안을 찾아본다."},
    {"q": "Q15. 계약이 최종 성사되었을 때 가장 큰 보람을 느끼는 지점은? 🏆", "type": "TF", "A": "협상을 통해 회사에 유리한 조건과 높은 이익률을 확보했을 때", "B": "파트너사와 깊은 신뢰를 구축하며 좋은 관계를 맺었다는 확신이 들 때"},

    # J vs P (16~20)
    {"q": "Q16. 수출 선적 일정을 관리할 때 내 업무 방식은? 🚢", "type": "JP", "A": "생산, 통관, 서류 마감 일정을 캘린더에 일 단위로 체계화해 둔다.", "B": "주요 납기 마감일을 중심에 두고 상황 변화에 맞춰 유연하게 조율한다."},
    {"q": "Q17. 현지 항만 사정으로 선박 출항이 갑작스럽게 지연된다면? 🚨", "type": "JP", "A": "미리 마련해 둔 플랜 B 대안 매뉴얼에 따라 즉시 후속 작업을 진행한다.", "B": "변화한 현장 상황을 실시간으로 파악하며 가장 기민한 대안을 선택한다."},
    {"q": "Q18. 하루 무역 업무를 시작하기 전 나의 모습은? ☕", "type": "JP", "A": "오늘 완료해야 할 작업 목록을 우선순위별로 정리하고 착수한다.", "B": "도착한 해외 메일들을 확인하며 당장 시급한 이슈부터 순서대로 처리한다."},
    {"q": "Q19. 해외 출장 일정을 계획할 때 선호하는 방식은? 🧳", "type": "JP", "A": "미팅 시간, 동선, 이동 교통편까지 사전에 빈틈없이 구성해 둔다.", "B": "필수 미팅 시간만 확정해 두고 현지 상황에 맞춰 유동적으로 이동한다."},
    {"q": "Q20. 업무 파일 및 무역 서류 폴더를 관리할 때 스타일은? 📂", "type": "JP", "A": "연도별, 바이어별, 프로젝트별로 명확한 규칙을 정해 체계적으로 분류한다.", "B": "기본 폴더에 보관하되 필요한 파일은 검색 기능을 활용해 빠르게 찾아낸다."}
]

# -------------------------------------------------------------
# 6대 무역 직무 데이터[cite: 1]
# -------------------------------------------------------------
trade_jobs = {
    "해외영업": {
        "title": "글로벌 무대를 누비는 무역 개척자, [해외영업]",
        "icon": "🌍💼",
        "character": {
            "avatar": "🦁✈️",
            "name": "글로벌 골드사자 '레오'",
            "badge": "패기만만 개척형",
            "slogan": "\"전 세계 바이어와 악수하고 계약서를 성사시키는 글로벌 네고왕!\"",
            "items": ["여권 & 항공권", "비즈니스 명함첩", "영업 실적 그래프"]
        },
        "keywords": ["글로벌 네고력", "신시장 개척", "커뮤니케이션"],
        "explanations": [
            "새로운 국가의 잠재 바이어를 발굴하고 가격 및 계약 조건을 능숙하게 주도하는 무역의 최전선 역할입니다.",
            "문화적 차이를 뛰어넘는 소통 능력과 상대방의 니즈를 빠르게 포착하는 비즈니스 센스가 가장 강력한 무기입니다.",
            "목표 지향적인 마인드셋으로 매출을 견인하며 글로벌 파트너십을 확장해 나가는 데 최고의 성취감을 느낍니다."
        ],
        "certs": ["국제무역사 1급", "무역영어 1급", "TOEIC Speaking / OPIc (AL 이상)"],
        "ideal_weights": {"E": 4, "I": 1, "S": 2, "N": 3, "T": 3, "F": 2, "J": 3, "P": 2},
        "daily_routine": "오전에는 밤사이 시차로 인해 인입된 해외 바이어 메일 회신 및 견적서(Quotation) 발송을 진행하고, 오후에는 수주 계약 조건 네고 화상 미팅 및 해외 전시회 부스 참가 준비를 수행합니다.",
        "practical_points": [
            "<b>신규 판로 개척:</b> B2B 플랫폼(알리바바, 링크드인 등)과 글로벌 박람회를 통해 타깃 국가의 잠재 바이어 DB를 구축하고 콜드 메일을 성사시킵니다.",
            "<b>가격 네고 및 계약 체결:</b> 제조원가와 국제운임, 목표 마진율을 정밀히 계산한 인코텀즈 견적을 산출하고 바이어와의 가격 줄다리기에서 유리한 고지를 점합니다.",
            "<b>납기 및 사후 관리:</b> 생산 일정 및 선적 현황을 공유하며 바이어와의 라포(신뢰 관계)를 다져 1회성 거래를 장기 반복 오더로 연결합니다."
        ]
    },
    "무역사무/수출입관리": {
        "title": "빈틈없는 프로세스의 중심, [무역사무 / 수출입관리]",
        "icon": "📑🚢",
        "character": {
            "avatar": "🦫📑",
            "name": "철두철미 비버 '비비'",
            "badge": "완벽주의 서류왕",
            "slogan": "\"글자 하나, 숫자 하나 틀림없이 안전 통관을 책임지는 수호자!\"",
            "items": ["돋보기", "신용장(L/C) 철", "날짜 스탬프"]
        },
        "keywords": ["선적 서류 정밀검토", "통관 프로세스 준수", "리스크 방어"],
        "explanations": [
            "신용장(L/C), B/L, 송장 등 복잡한 무역 서류를 단 하나의 오차도 없이 꼼꼼하게 관리하는 무역의 든든한 백본입니다.",
            "원산지 증명 및 국가별 수출입 통관 규정을 철저히 준수하여 회사의 행정적·재정적 리스크를 완벽하게 차단합니다.",
            "선적 및 통관의 전체 일정을 체계적인 루틴으로 관리하여 물류 지연 없이 안전한 수출입을 보장합니다."
        ],
        "certs": ["국제무역사 1급", "원산지관리사", "무역영어 1급"],
        "ideal_weights": {"E": 1, "I": 4, "S": 4, "N": 1, "T": 3, "F": 2, "J": 5, "P": 0},
        "daily_routine": "오전에는 선적 서류(Invoice, P/L) 작성 및 관세사 통관 신고 접수를 진행하고, 오후에는 입고 컨테이너 검수, 신용장(L/C) 조건 불일치(Discrepancy) 확인 및 외환 대금 결제를 마감합니다.",
        "practical_points": [
            "<b>무결점 선적 서류 작성:</b> 상업송장(C/I), 포장명세서(P/L), 원산지증명서(C/O)의 수량·금액·중량을 오차 없이 작성하여 통관 보류를 사전 차단합니다.",
            "<b>신용장 및 대금 결제 방어:</b> L/C 원본 조항과 선하증권(B/L) 상의 철자 하나까지 대조하여 은행 매입 거절 및 하자 수수료 리스크를 완벽히 방어합니다.",
            "<b>수출입 행정 스케줄 컨트롤:</b> 관세청 유니패스(UNI-PASS)를 실시간 모니터링하여 수출입 면허를 제때 발급받고 납기 마감일을 엄수합니다."
        ]
    },
    "글로벌 소싱/바잉 MD": {
        "title": "트렌드를 발굴하는 제품 큐레이터, [글로벌 소싱 / 바잉 MD]",
        "icon": "🛍️✨",
        "character": {
            "avatar": "🦊🛍️",
            "name": "트렌드세터 사막여우 '루루'",
            "badge": "감각만점 큐레이터",
            "slogan": "\"전 세계 핫한 보물을 발굴해 최고의 가성비로 소싱하는 안목 천재!\"",
            "items": ["소싱 샘플 키트", "팬톤 컬러칩", "원가 계산기"]
        },
        "keywords": ["소비자 트렌드 포착", "원가 최적화", "샘플링 감각"],
        "explanations": [
            "글로벌 시장의 최신 트렌드를 기민하게 읽고 국내외 시장에서 통할 경쟁력 있는 상품과 원부자재를 찾아냅니다.",
            "공급사와의 단가 협상과 품질 검수를 주도하며 합리적인 원가 구조와 높은 상품성을 동시에 확보합니다.",
            "단순한 가격 비교를 넘어 제품의 스토리와 심미적 가치를 발견하고 브랜딩과 연결 짓는 감각이 뛰어납니다."
        ],
        "certs": ["유통관리사 2급", "CPIM(생산재고관리사)", "무역영어 1급"],
        "ideal_weights": {"E": 3, "I": 2, "S": 2, "N": 4, "T": 2, "F": 3, "J": 1, "P": 4},
        "daily_routine": "오전에는 글로벌 트렌드 플랫폼 리서치 및 경쟁사 소싱 제품 벤치마킹을 실시하고, 오후에는 해외 공장 샘플 검수, MOQ(최소주문수량) 네고 및 패키지 개발 회의를 진행합니다.",
        "practical_points": [
            "<b>해외 공급처 발굴(Sourcing):</b> 원가 경쟁력을 갖춘 해외 현지 OEM/ODM 공장을 직접 발굴하고 신뢰할 수 있는 소싱 라인을 확보합니다.",
            "<b>원가 및 MOQ 줄다리기:</b> 생산 수량에 따른 단계별 단가 절충안을 설계하고 수입 부대비용(관세, 내륙운송비)을 포함한 착지 원가를 계산합니다.",
            "<b>샘플 테스팅 & 퀄리티 컨트롤:</b> 입고된 시제품의 내구성, 성분 인증, 패키지 완성도를 까다롭게 점검하여 제품 결함과 반품 리스크를 최소화합니다."
        ]
    },
    "포워딩/국제물류": {
        "title": "지구촌 물류의 해결사, [국제물류 / 포워딩]",
        "icon": "⚓🚚",
        "character": {
            "avatar": "🐬⚓",
            "name": "오션캡틴 돌고래 '포키'",
            "badge": "순발력 만렙 항해사",
            "slogan": "\"폭풍우도 물류 적체도 뚫고 화물을 제시간에 배송하는 해결사!\"",
            "items": ["선박/항공 트래커", "글로벌 타임존 시계", "무전기"]
        },
        "keywords": ["운송 루트 최적화", "돌발상황 순발력", "운임 네고"],
        "explanations": [
            "해상 및 항공 운송 경로를 효율적으로 설계하고 화물이 목적지까지 가장 빠르고 경제적으로 도착하도록 조율합니다.",
            "항만 파업, 기상 악화, 운송 지연 등 물류 현장의 돌발 변수에도 흔들림 없이 대체 솔루션을 찾아내는 순발력이 강점입니다.",
            "선사 및 해외 파트너와의 긴밀한 네트워크를 활용하여 실시간 운송 현황을 기민하게 트래킹하고 해결합니다."
        ],
        "certs": ["물류관리사", "보세사", "국제무역사 1급"],
        "ideal_weights": {"E": 3, "I": 2, "S": 3, "N": 2, "T": 4, "F": 1, "J": 2, "P": 4},
        "daily_routine": "오전에는 선사/항공사 선복(Space) 부킹 현황 확인 및 선적 화물 추적을 수행하고, 오후에는 화주 견적 문의 대응, 운임 네고 및 항만 창고 입출고 이슈를 조율합니다.",
        "practical_points": [
            "<b>최적 복합 운송 설계:</b> 화물의 납기 마감과 예산에 맞춰 해상 FCL/LCL, 항공 특송, 복합운송 등 가장 경제적이고 빠른 항로를 제안합니다.",
            "<b>선복(Space) 확보 및 운임 협상:</b> 성수기 물류 대란 상황에서도 선사/항공사와의 유대관계를 발휘해 긴급 컨테이너 스페이스를 확보합니다.",
            "<b>물류 현장 트러블슈팅:</b> 적체된 터미널 환적 지연, 세관 검사 지정 등 돌발 변수 발생 시 즉각적인 대체 루트 가동으로 화주 피해를 막아냅니다."
        ]
    },
    "관세사/통관·FTA 컨설턴트": {
        "title": "무역 규정과 법률의 마스터, [관세사 / FTA·통관 컨설턴트]",
        "icon": "⚖️📜",
        "character": {
            "avatar": "🦉⚖️",
            "name": "지혜로운 부엉이 '아서'",
            "badge": "법률 마스터 전략가",
            "slogan": "\"복잡한 관세법과 품목분류 규정 속에서 절세의 길을 밝히는 현자!\"",
            "items": ["관세율표 해설서", "판례집", "법봉"]
        },
        "keywords": ["HS CODE 품목분류", "FTA 특혜세율 분석", "무역 법률 자문"],
        "explanations": [
            "수출입 물품의 정확한 품목분류(HS CODE)와 과세가격 평가를 통해 통관 리스크를 합법적으로 최소화합니다.",
            "복잡한 FTA 원산지 결정기준을 판정하고 체계적인 원산지 증명 컨설팅으로 실질적인 절세 혜택을 창출합니다.",
            "통상 관련 법률 지식과 엄격한 논리적 근거를 토대로 세관 조사 대응 및 통관 적법성을 전문적으로 입증합니다."
        ],
        "certs": ["관세사(전문자격)", "원산지관리사", "보세사"],
        "ideal_weights": {"E": 1, "I": 4, "S": 4, "N": 1, "T": 5, "F": 0, "J": 4, "P": 1},
        "daily_routine": "오전에는 세관 수입신고서 검토 및 수입요건 확인(식품위생법, 전파법 등)을 진행하고, 오후에는 기업 FTA 사후검증 대응 자료 작성 및 품목분류 유권해석 자문을 수행합니다.",
        "practical_points": [
            "<b>HS CODE 정밀 매핑:</b> 애매한 신기술·복합 제품의 도면과 스펙을 분석해 가장 유리하면서도 법적 하자가 없는 10자리 세번을 확정합니다.",
            "<b>FTA 원산지 검증 및 절세:</b> 원재료 내역(BOM)을 토대로 세번변경기준(CTC) 및 부가가치기준(RVC)을 판정해 관세를 0%까지 낮추는 절세 컨설팅을 제공합니다.",
            "<b>통관 리스크 감정 및 법률 방어:</b> 관세청 세무조사나 품목분류 이의제기 시 법적 판례와 국제관세기구(WCO) 사례를 근거로 화주를 변호합니다."
        ]
    },
    "무역 데이터 분석/전략 기획": {
        "title": "데이터로 통상 흐름을 읽는 전략가, [무역 데이터 분석 / 사업기획]",
        "icon": "📊💡",
        "character": {
            "avatar": "🐱💻",
            "name": "스마트 캣 '네오'",
            "badge": "데이터 브레인 분석가",
            "slogan": "\"무역 통계와 환율 데이터 속에서 미래 시장의 패턴을 읽어냅니다!\"",
            "items": ["데이터 대시보드", "듀얼 모니터", "파이썬 스크립트"]
        },
        "keywords": ["통상 통계 모델링", "글로벌 환율/지표 분석", "신시장 전략 설계"],
        "explanations": [
            "전 세계 관세율, 수출입 통계, 환율 추이 등 방대한 정량 데이터를 정밀하게 가공하여 거시 통상 흐름을 읽어냅니다.",
            "데이터 기반 인사이트를 바탕으로 유망 수출 타깃 국가를 선정하고 리스크를 최소화하는 진출 전략을 기획합니다.",
            "복잡한 글로벌 통상 이슈를 논리적인 리포트와 시각화 지표로 전환하여 경영진의 전략적 의사결정을 돕습니다."
        ],
        "certs": ["ADsP(데이터분석준전문가)", "SQLD", "국제무역사 1급"],
        "ideal_weights": {"E": 1, "I": 4, "S": 2, "N": 4, "T": 5, "F": 0, "J": 3, "P": 2},
        "daily_routine": "오전에는 관세청 무역통계(K-stat), UN Comtrade 데이터 정제 및 이상치 탐지를 진행하고, 오후에는 품목별 글로벌 가격 지수 대시보드 구축 및 신규 권역 진출 전략 보고서를 작성합니다.",
        "practical_points": [
            "<b>정량 데이터 파이프라인 구축:</b> 글로벌 수출입 원자재 시세, 물류 운임 지수(SCFI 등), 환율 변동성을 파이썬/SQL로 수집·가공하여 인사이트를 도출합니다.",
            "<b>글로벌 권역별 수요 예측:</b> 국가별 수입 물량 증감 추이를 모델링하여 향후 6개월~1년 내 수요가 급증할 이머징 마켓을 발굴합니다.",
            "<b>데이터 시각화 및 경영 자문:</b> 복잡한 통상 지표를 직관적인 대시보드(BI 툴)로 구현해 경영진이 적기 수출 가격과 타이밍을 잡도록 지원합니다."
        ]
    }
}

def calculate_job_rankings(user_scores):
    job_scores = []
    for job_key, job_info in trade_jobs.items():
        weights = job_info["ideal_weights"]
        score = 0
        max_possible = 0
        for dim, user_val in user_scores.items():
            score += user_val * weights.get(dim, 1)
            max_possible += 5 * weights.get(dim, 1)
        match_percentage = int((score / max_possible) * 100)
        job_scores.append((job_key, match_percentage, job_info))
    job_scores.sort(key=lambda x: x[1], reverse=True)
    return job_scores

# -------------------------------------------------------------
# 선택지 클릭 시 즉시 다음 단계로 이동하는 헬퍼 함수
# -------------------------------------------------------------
def choose_and_proceed(choice_text):
    cur = st.session_state.current_q
    st.session_state.user_answers[cur] = choice_text
    
    if cur < len(questions) - 1:
        st.session_state.current_q += 1
        st.session_state.stage = "test"
    else:
        st.session_state.stage = "loading"
    st.rerun()

# 세션 상태 관리
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * len(questions)

# -------------------------------------------------------------
# [화면 1] 시작 화면
# -------------------------------------------------------------
if st.session_state.stage == "intro":
    st.markdown("<div class='title-text'>🚢 무역 직무 성향 MBTI 테스트 📝</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>나의 업무 스타일과 가장 잘 어울리는 무역 직무를 찾아보세요!</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='intro-card'>
            <div class='intro-icon'>🚢🗺️✈️</div>
            <div class='intro-title'>글로벌 통상 무대에서 나는 어떤 전문가일까요?</div>
            <div class='intro-desc'>
                해외영업, 무역사무, 바잉MD, 포워딩, 관세사, 무역데이터 분석까지!<br>
                무역 실무 상황을 반영한 <b>20가지 질문</b>을 통해 나의 성향 지표를 분석하고,<br>
                나의 <b>시그니처 무역 캐릭터 페르소나</b>와 추천 자격증, TOP 3 랭킹을 확인해보세요.
            </div>
            <div class='intro-info-box'>
                ⏱️ <b>소요 시간:</b> 약 2~3분 내외 (답변 클릭 시 자동 진행)<br>
                📝 <b>문항 수:</b> 총 20문항 (한 문제씩 진행)<br>
                💡 정답이 없으니 평소 나의 자연스러운 스타일에 가깝게 골라주세요!
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='nav-btn-wrap'>", unsafe_allow_html=True)
    if st.button("🚀 테스트 시작하기", use_container_width=True):
        st.session_state.stage = "test"
        st.session_state.current_q = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# [화면 2] 질문 진행 화면 (안정적인 고유 키 버튼 기반 원클릭 이동)
# -------------------------------------------------------------
elif st.session_state.stage == "test":
    cur_idx = st.session_state.current_q
    total_q = len(questions)

    st.markdown("<div class='title-text'>🚢 무역 직무 성향 MBTI 테스트 📝</div>", unsafe_allow_html=True)

    progress_val = cur_idx / total_q
    st.progress(progress_val)
    st.markdown(
        f"<p style='text-align: right; font-weight: 600; color: #2B6CB0; font-size: 0.98rem; margin-top: -6px;'>"
        f"진행 상황: {cur_idx + 1} / {total_q} 문항"
        f"</p>",
        unsafe_allow_html=True
    )

    q_data = questions[cur_idx]

    # 질문 박스 (1.42rem)
    st.markdown(f"""
        <div class='question-box'>
            <div class='question-text'>{q_data['q']}</div>
        </div>
    """, unsafe_allow_html=True)

    # 🎯 [핵심] 고유 키를 부여한 st.button으로 멈춤 없는 즉시 넘김 보장
    st.markdown("<div class='choice-btn-wrap'>", unsafe_allow_html=True)
    
    if st.button(f"A.  {q_data['A']}", key=f"btn_step_A_{cur_idx}", use_container_width=True):
        choose_and_proceed(q_data["A"])

    if st.button(f"B.  {q_data['B']}", key=f"btn_step_B_{cur_idx}", use_container_width=True):
        choose_and_proceed(q_data["B"])
        
    st.markdown("</div>", unsafe_allow_html=True)

    # ⬅️ 하단 네비게이션
    st.write("")
    st.markdown("<div class='nav-btn-wrap'>", unsafe_allow_html=True)
    c_prev, _ = st.columns([1, 1])
    with c_prev:
        if cur_idx > 0:
            if st.button("⬅️ 이전 문제", key=f"btn_prev_nav_{cur_idx}", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()
        else:
            if st.button("🏠 처음으로", key="btn_home_nav", use_container_width=True):
                st.session_state.stage = "intro"
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# [화면 3] 북 치는 동물 애니메이션
# -------------------------------------------------------------
elif st.session_state.stage == "loading":
    st.markdown("<div class='title-text'>🚢 무역 직무 성향 MBTI 테스트 📝</div>", unsafe_allow_html=True)
    st.progress(1.0)
    
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
            <div class='loading-container'>
                <div class='drummer-animals'>🐱🥁🐶</div>
                <div class='drum-sticks'>🥢 🎶 🥁</div>
                <div class='loading-title'>두구두구두구...! 결과 분석 중이에요!</div>
                <div class='loading-sub'>귀여운 친구들이 북을 치며 당신의 캐릭터를 소환하고 있어요 ✨</div>
            </div>
        """, unsafe_allow_html=True)
    
    time.sleep(2.0)
    st.session_state.stage = "result"
    st.rerun()

# -------------------------------------------------------------
# [화면 4] 최종 결과 화면
# -------------------------------------------------------------
elif st.session_state.stage == "result":
    st.markdown("<div class='title-text'>🚢 무역 직무 성향 MBTI 테스트 📝</div>", unsafe_allow_html=True)
    st.progress(1.0)
    st.markdown("<p style='text-align: right; font-weight: 600; color: #1A365D;'>진행 완료: 20 / 20 문항</p>", unsafe_allow_html=True)

    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for i, ans in enumerate(st.session_state.user_answers):
        q_type = questions[i]["type"]
        if ans == questions[i]["A"]:
            scores[q_type[0]] += 1
        else:
            scores[q_type[1]] += 1

    mbti_result = (
        ("E" if scores["E"] >= scores["I"] else "I") +
        ("S" if scores["S"] >= scores["N"] else "N") +
        ("T" if scores["T"] >= scores["F"] else "F") +
        ("J" if scores["J"] >= scores["P"] else "P")
    )

    ranked_jobs = calculate_job_rankings(scores)
    top_job_key, top_score, top_job_data = ranked_jobs[0]
    char_info = top_job_data["character"]

    # 1. 🐾 캐릭터 페르소나 카드
    st.markdown(f"""
        <div class='character-card'>
            <div class='character-avatar'>{char_info['avatar']}</div>
            <div class='character-badge'>{char_info['badge']}</div>
            <div class='character-name'>{char_info['name']}</div>
            <div class='character-slogan'>{char_info['slogan']}</div>
            <div style='margin-top: 10px;'>
                <span style='font-size: 0.9rem; color: #718096; font-weight: 600;'>🎒 시그니처 아이템:</span><br>
                <span class='character-item-tag'>✨ {char_info['items'][0]}</span>
                <span class='character-item-tag'>✨ {char_info['items'][1]}</span>
                <span class='character-item-tag'>✨ {char_info['items'][2]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. 메인 직무 분석 & 3줄 해설
    st.markdown(f"""
        <div class='result-box'>
            <div class='result-header'>🎉 분석 성향: <b>{mbti_result}</b></div>
            <div class='job-title'>{top_job_data['icon']} 1위 추천: {top_job_data['title']}</div>
            <div class='badge-container'>
                <span class='badge'>🏷️ {top_job_data['keywords'][0]}</span>
                <span class='badge'>🏷️ {top_job_data['keywords'][1]}</span>
                <span class='badge'>🏷️ {top_job_data['keywords'][2]}</span>
            </div>
            <div class='desc-box'>
                <div class='desc-item'><b>1. 업무 특성:</b> {top_job_data['explanations'][0]}</div>
                <div class='desc-item'><b>2. 강점 발휘:</b> {top_job_data['explanations'][1]}</div>
                <div class='desc-item'><b>3. 성장 방향:</b> {top_job_data['explanations'][2]}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. 🏢 회사에서의 실제 업무 및 역량 적용 가이드
    st.write("")
    st.markdown(f"""
        <div class='practical-box'>
            <div class='practical-section-title'>🏢 회사 현업에서는 정확히 어떤 일을 하나요?</div>
            <div class='practical-routine'>
                <b>📌 하루 실무 루틴 요약:</b><br>{top_job_data['daily_routine']}
            </div>
            <div class='practical-section-title' style='margin-top: 14px;'>💡 나의 강점 역량을 실무에 적용하는 방법</div>
            <div class='practical-point'>• {top_job_data['practical_points'][0]}</div>
            <div class='practical-point'>• {top_job_data['practical_points'][1]}</div>
            <div class='practical-point'>• {top_job_data['practical_points'][2]}</div>
        </div>
    """, unsafe_allow_html=True)

    # 4. 추천 자격증 영역
    st.markdown("#### 📜 역량 강화를 위한 추천 자격증")
    c_cert1, c_cert2, c_cert3 = st.columns(3)
    with c_cert1:
        st.info(f"**{top_job_data['certs'][0]}**")
    with c_cert2:
        st.info(f"**{top_job_data['certs'][1]}**")
    with c_cert3:
        st.info(f"**{top_job_data['certs'][2]}**")

    # 5. 어울리는 무역 직무 TOP 3
    st.write("")
    st.markdown("#### 🏆 나와 잘 맞는 무역 직무 TOP 3")
    medals = ["🥇 1위", "🥈 2위", "🥉 3위"]
    for idx in range(3):
        r_name, r_pct, r_info = ranked_jobs[idx]
        st.markdown(f"""
            <div class='rank-card'>
                <span class='rank-title'>{medals[idx]} {r_info['icon']} {r_name}</span>
                <span class='rank-score'>적합도 {r_pct}%</span>
            </div>
        """, unsafe_allow_html=True)

    # 6. 세부 성향 지표
    st.write("")
    st.markdown("#### 📊 나의 4대 지표 분석 결과")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("외향성 (E) vs 내향성 (I)", f"E: {scores['E']}점 / I: {scores['I']}점")
        st.metric("실무현실 (S) vs 직관방향 (N)", f"S: {scores['S']}점 / N: {scores['N']}점")
    with c2:
        st.metric("논리판단 (T) vs 관계공감 (F)", f"T: {scores['T']}점 / F: {scores['F']}점")
        st.metric("계획체계 (J) vs 상황유연 (P)", f"J: {scores['J']}점 / P: {scores['P']}점")

    # 다시 시작하기
    st.write("")
    st.markdown("<div class='nav-btn-wrap'>", unsafe_allow_html=True)
    if st.button("🔄 처음으로 돌아가기", key="btn_restart_final", use_container_width=True):
        st.session_state.stage = "intro"
        st.session_state.current_q = 0
        st.session_state.user_answers = [None] * len(questions)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)