import os
import streamlit as st
import requests
from dotenv import load_dotenv

# ----------------------------------------------------
# 0. 환경 변수 로드
# ----------------------------------------------------
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

st.set_page_config(
    page_title="모여봐요 여행의 숲",
    page_icon="🏝️",
    layout="wide"
)

if "calc_target" not in st.session_state:
    st.session_state.calc_target = "USD"


# ----------------------------------------------------
# 1. 국내 주요 명소 한 줄 소개 딕셔너리
# ----------------------------------------------------
DOMESTIC_SPOT_DESCRIPTIONS = {
    "강남역": "최신 트렌드와 쇼핑, 활기찬 야경과 맛집이 24시간 잠들지 않는 서울의 대표 번화가입니다.",
    "선릉과정릉": "도심 속 푸른 숲길을 걸으며 조선 왕릉의 고즈넉한 정취와 휴식을 즐길 수 있는 유네스코 세계문화유산입니다.",
    "경복궁": "조선 왕조 제일의 법궁으로, 웅장한 근정전과 연못 위의 경회루가 사계절 내내 아름다운 역사의 중심지입니다.",
    "N서울타워": "남산 정상에서 360도 파노라마로 서울 전경과 낭만적인 석양, 화려한 야경을 한눈에 담을 수 있는 서울의 랜드마크입니다.",
    "롯데월드타워": "국내 최고층 전망대 서울스카이와 아쿠아리움, 쇼핑몰이 한곳에 모인 럭셔리 복합 문화 명소입니다.",
    "북촌한옥마을": "실제 주민들이 살아가는 조선 시대 양반 가옥 골목으로, 고풍스러운 한옥 처마와 남산 뷰가 어우러진 사진 명소입니다.",
    "동대문디자인플라자(DDP)": "자하 하디드의 유려한 곡선 건축물로 전시, 패션쇼, 미래지향적 야경 산책을 만끽할 수 있는 디자인 성지입니다.",
    "명동성당": "한국 천주교의 상징이자 붉은 벽돌의 웅장한 고딕 양식 건축미를 감상할 수 있는 도심 속 평화로운 성소입니다.",
    "창덕궁": "자연 지형을 그대로 살린 한국 전통 정원의 정수 '후원(비원)'을 품은 가장 한국적인 궁궐입니다.",
    "여의도 한강공원": "시원한 강바람을 맞으며 피크닉과 한강 라면, 자전거 라이딩과 유람선을 즐기기 가장 좋은 쉼터입니다.",
    "국립중앙박물관": "반가사유상을 비롯한 수만 점의 국보급 유물과 아름다운 야외 거울못 정원을 무료로 둘러볼 수 있는 문화 명소입니다."
}


# ----------------------------------------------------
# 2. 해외 여행지 데이터베이스 (도시별 매력 설명 desc 추가)
# ----------------------------------------------------
GLOBAL_DESTINATIONS = {
    "일본 🇯🇵": {
        "currency": "JPY",
        "currency_symbol": "¥",
        "flight_base": 350000,
        "cities": {
            "도쿄 (Tokyo)": {
                "lat": 35.6762, "lon": 139.6503,
                "desc": "초현대적인 마천루와 애니메이션·패션의 성지이면서, 골목마다 에도 시대의 전통과 다채로운 미식이 공존하는 아시아 최대 메가시티입니다.",
                "spots": ["시부야 스크램블 스퀘어 & 하치코", "센소지 & 아사쿠사 거리", "도쿄 타워 & 롯폰기 힐즈", "신주쿠 교엔 & 오모이데요코초"],
                "restaurants": [
                    {"name": "이치란 라멘 시부야점", "cat": "돈코츠 라멘", "desc": "독서실 칸막이에서 즐기는 커스텀 돈코츠 라멘", "url": "https://www.google.com/maps/search/Ichiran+Shibuya"},
                    {"name": "미도리 스시 긴자점", "cat": "정통 스시", "desc": "가성비 넘치는 고품질 제철 생선 초밥 전문점", "url": "https://www.google.com/maps/search/Midori+Sushi+Ginza"},
                    {"name": "모토무라 규카츠 신주쿠", "cat": "소고기 카츠", "desc": "개인 화로에 직접 구워 먹는 부드러운 규카츠", "url": "https://www.google.com/maps/search/Motomura+Gyukatsu+Shinjuku"}
                ]
            },
            "오사카 (Osaka)": {
                "lat": 34.6937, "lon": 135.5023,
                "desc": "'먹다가 망한다'는 말이 있을 정도로 식도락 문화가 발달한 활기찬 항구 도시로, 화려한 네온사인과 친근한 매력이 넘치는 여행지입니다.",
                "spots": ["도톤보리 글리코상", "오사카성 천수각", "유니버설 스튜디오 재팬 (USJ)", "우메다 공중정원 전망대"],
                "restaurants": [
                    {"name": "쿠시카츠 다루마 도톤보리", "cat": "꼬치 튀김", "desc": "바삭하고 얇은 튀김옷의 원조 쿠시카츠 전문점", "url": "https://www.google.com/maps/search/Kushikatsu+Daruma+Dotonbori"},
                    {"name": "치보 오코노미야키", "cat": "철판요리", "desc": "두툼한 반죽과 풍성한 토핑의 대표 오코노미야키", "url": "https://www.google.com/maps/search/Chibo+Dotonbori"},
                    {"name": "우오신 스시 우메다", "cat": "대왕 초밥", "desc": "압도적인 네타 크기를 자랑하는 오사카 인기 스시집", "url": "https://www.google.com/maps/search/Uoshin+Sushi+Umeda"}
                ]
            },
            "후쿠오카 (Fukuoka)": {
                "lat": 33.5904, "lon": 130.4017,
                "desc": "한국에서 가장 가까운 일본 규슈의 관문으로, 진한 돈코츠 라멘과 밤거리의 낭만적인 포장마차(야타이), 아기자기한 쇼핑이 매력적인 도시입니다.",
                "spots": ["하카타 캐널시티", "오호리 공원 & 후쿠오카 성터", "모모치 해변 & 후쿠오카 타워", "나카스 포장마차(야타이) 거리"],
                "restaurants": [
                    {"name": "신신라멘 하카타 텐진", "cat": "하카타 돈코츠", "desc": "잡내 없이 진하고 구수한 하카타 3대 라멘", "url": "https://www.google.com/maps/search/Hakata+Shin-Shin+Tenjin"},
                    {"name": "키와미야 함바그 하카타점", "cat": "철판 함바그", "desc": "달궈진 스톤에 직접 구워먹는 육즙 가득 소고기 함바그", "url": "https://www.google.com/maps/search/Kiwamiya+Hakata"},
                    {"name": "원조 하카타 멘타이쥬", "cat": "명란 덮밥", "desc": "특제 다시마 다시 소스를 곁들인 후쿠오카 최고급 명란 요리", "url": "https://www.google.com/maps/search/Ganso+Hakata+Mentaiju"}
                ]
            },
            "교토 (Kyoto)": {
                "lat": 35.0116, "lon": 135.7681,
                "desc": "천년 동안 일본의 수도였던 곳으로, 수천 개의 사찰과 붉은 신사 기둥, 울창한 대나무 숲길이 고즈넉한 일본의 고전미를 전해줍니다.",
                "spots": ["후시미 이나리 신사(천개의 토리이)", "기요미즈데라(청수사)", "아라시야마 대나무숲(치쿠린)", "킨카쿠지(금각사)"],
                "restaurants": [
                    {"name": "히노데 우동", "cat": "카레 우동", "desc": "철학의 길 근처에서 즐기는 깊고 매콤달콤한 명품 카레우동", "url": "https://www.google.com/maps/search/Hinode+Udon+Kyoto"},
                    {"name": "규카츠 교토카츠규 가와라마치", "cat": "정통 규카츠", "desc": "얇고 바삭한 튀김옷과 부드러운 와규의 조화", "url": "https://www.google.com/maps/search/Kyoto+Katsugyu+Kawaramachi"},
                    {"name": "아라비카 커피 아라시야마(% Arabica)", "cat": "스페셜티 커피", "desc": "도게츠교 강변 뷰를 감상하며 마시는 교토 대표 라떼", "url": "https://www.google.com/maps/search/Arabica+Kyoto+Arashiyama"}
                ]
            }
        }
    },
    "영국 🇬🇧": {
        "currency": "GBP",
        "currency_symbol": "£",
        "flight_base": 1300000,
        "cities": {
            "런던 (London)": {
                "lat": 51.5074, "lon": -0.1278,
                "desc": "웅장한 고딕 건축의 빅벤부터 웨스트엔드 뮤지컬, 세계적인 무료 박물관들이 즐비한 세계 문화와 예술의 수도입니다.",
                "spots": ["빅벤 & 국회의사당", "타워 브리지 & 런던탑", "대영박물관 (영국박물관)", "버킹엄 궁전 근위병 교대식"],
                "restaurants": [
                    {"name": "Poppie's Fish & Chips", "cat": "피시 앤 칩스", "desc": "바삭하고 담백한 대구살을 튀겨낸 영국 대표 음식", "url": "https://www.google.com/maps/search/Poppies+Fish+and+Chips+Soho"},
                    {"name": "Dishoom Covent Garden", "cat": "모던 인도 요리", "desc": "런던 현지인들도 줄 서서 먹는 최고 평점의 인도 요리", "url": "https://www.google.com/maps/search/Dishoom+Covent+Garden"},
                    {"name": "Flat Iron Soho", "cat": "스테이크", "desc": "착한 가격에 만나는 미니 도끼 칼 스테이크 맛집", "url": "https://www.google.com/maps/search/Flat+Iron+Soho"}
                ]
            },
            "케임브리지 (Cambridge)": {
                "lat": 52.2053, "lon": 0.1218,
                "desc": "뉴턴과 튜링의 발자취가 서린 유서 깊은 대학 도시로, 캠강을 따라 나룻배를 타는 낭만적인 펀팅(Punting) 투어가 백미입니다.",
                "spots": ["킹스 칼리지 & 예배당", "캠강 펀팅(Punting) 보트 투어", "수학의 다리(퀸즈 칼리지)", "피츠윌리엄 박물관 & 시내 마켓"],
                "restaurants": [
                    {"name": "Fitzbillies (피츠빌리스)", "cat": "첼시 번 & 티룸", "desc": "1920년부터 사랑받아 온 달콤하고 쫀득한 원조 첼시 번 명소", "url": "https://www.google.com/maps/search/Fitzbillies+Cambridge"},
                    {"name": "The Eagle (디 이글)", "cat": "전통 영국 펍", "desc": "1667년 개업, DNA 이중나선 발견 선언과 역사적 RAF 낙서가 남은 펍", "url": "https://www.google.com/maps/search/The+Eagle+Cambridge"},
                    {"name": "Aroma Cafe & Kitchen", "cat": "브런치 & 카페", "desc": "캠강 산책 후 즐기기 좋은 정갈한 잉글리시 브런치와 커피", "url": "https://www.google.com/maps/search/Aroma+Cafe+Cambridge"}
                ]
            },
            "에든버러 (Edinburgh)": {
                "lat": 55.9533, "lon": -3.1883,
                "desc": "절벽 위에 우뚝 솟은 고성과 중세풍 화강암 거리가 마치 판타지 소설 속으로 들어온 듯 신비롭고 고풍스러운 스코틀랜드의 심장입니다.",
                "spots": ["에든버러 성", "로열 마일 거리", "칼튼 힐 전망대", "아서스 시트(사자 언덕)"],
                "restaurants": [
                    {"name": "The Witchery by the Castle", "cat": "스코티시 파인다이닝", "desc": "고딕 양식의 신비로운 인테리어와 스코틀랜드 전통 요리", "url": "https://www.google.com/maps/search/The+Witchery+by+the+Castle"},
                    {"name": "Oink Victoria Street", "cat": "통돼지 바베큐 롤", "desc": "바삭한 껍질과 부드러운 고기가 가득한 가성비 샌드위치", "url": "https://www.google.com/maps/search/Oink+Victoria+Street+Edinburgh"},
                    {"name": "The Elephant House", "cat": "해리포터 성지 카페", "desc": "J.K. 롤링이 해리포터를 집필했던 유서 깊은 카페", "url": "https://www.google.com/maps/search/The+Elephant+House+Edinburgh"}
                ]
            },
            "맨체스터 (Manchester)": {
                "lat": 53.4808, "lon": -2.2426,
                "desc": "세계 축구 팬들의 성지이자 산업혁명의 발상지로, 붉은 벽돌 창고를 개조한 힙한 펍과 인디 음악 씬이 살아 숨 쉬는 활력 넘치는 도시입니다.",
                "spots": ["올드 트래포드(맨유 홈구장)", "에티하드 스타디움(맨시티 구장)", "존 라이랜즈 도서관", "국립 축구 박물관"],
                "restaurants": [
                    {"name": "Hawksmoor Manchester", "cat": "영국식 스테이크", "desc": "빅토리아 시대 법원을 개조한 최고급 영국 스테이크하우스", "url": "https://www.google.com/maps/search/Hawksmoor+Manchester"},
                    {"name": "Rudy's Neapolitan Pizza", "cat": "화덕 피자", "desc": "세계적인 피자 순위에 꼽히는 맨체스터 안코츠 명소", "url": "https://www.google.com/maps/search/Rudys+Pizza+Manchester"},
                    {"name": "Federal Cafe & Bar", "cat": "호주식 브런치", "desc": "촉촉한 프렌치 토스트와 플랫 화이트가 훌륭한 브런치 카페", "url": "https://www.google.com/maps/search/Federal+Cafe+Manchester"}
                ]
            }
        }
    },
    "중국 🇨🇳": {
        "currency": "CNY",
        "currency_symbol": "¥",
        "flight_base": 360000,
        "cities": {
            "베이징 (Beijing)": {
                "lat": 39.9042, "lon": 116.4074,
                "desc": "자금성과 만리장성 등 대륙의 압도적인 황실 역사 유적과 현대 예술 지구가 공존하는 중국 3천 년 역사의 중심지입니다.",
                "spots": ["자금성(고궁박물원)", "만리장성(팔달령)", "이화원(황실 정원)", "천안문 광장 & 싼리툰"],
                "restaurants": [
                    {"name": "취안쥐더(전취덕) 베이징덕 본점", "cat": "베이징 카오야", "desc": "150년 전통 바삭한 껍질과 촉촉한 속살의 북경오리", "url": "https://www.google.com/maps/search/Quanjude+Beijing"},
                    {"name": "하이디라오 왕푸징점", "cat": "사천 훠궈", "desc": "최고급 서비스와 신선한 재료로 즐기는 정통 훠궈", "url": "https://www.google.com/maps/search/Haidilao+Wangfujing+Beijing"},
                    {"name": "다동 카오야(Da Dong)", "cat": "모던 중식 & 오리", "desc": "기름기를 쏙 뺀 바삭한 크리스피 북경오리 전문점", "url": "https://www.google.com/maps/search/Da+Dong+Roast+Duck+Beijing"}
                ]
            },
            "상하이 (Shanghai)": {
                "lat": 31.2304, "lon": 121.4737,
                "desc": "황푸강을 사이에 두고 유럽풍 고전 건축의 와이탄과 미래도시 같은 화려한 스카이라인이 드라마틱하게 마주하는 트렌디한 국제도시입니다.",
                "spots": ["와이탄 유럽풍 거리 & 야경", "동방명주 & 상하이 타워", "예원(전통 명나라 정원)", "신천지 카페거리 & 대한민국 임시정부 청사"],
                "restaurants": [
                    {"name": "자자탕바오(Jia Jia Tang Bao)", "cat": "샤오롱바오", "desc": "진한 게살 육즙이 터지는 상하이 최고 인기 딤섬", "url": "https://www.google.com/maps/search/Jia+Jia+Tang+Bao+Shanghai"},
                    {"name": "그랜드 마더(Grand Mother)", "cat": "상하이 가정식", "desc": "달콤짭조름한 동파육(홍샤오로우)과 마파두부 맛집", "url": "https://www.google.com/maps/search/Grand+Mother+Restaurant+Shanghai"},
                    {"name": "로스트 헤븐(Lost Heaven)", "cat": "운남 요리", "desc": "와이탄 근처 이국적인 분위기와 맛있는 운남 퓨전 요리", "url": "https://www.google.com/maps/search/Lost+Heaven+on+the+Bund"}
                ]
            },
            "칭다오 (Qingdao)": {
                "lat": 36.0671, "lon": 120.3826,
                "desc": "붉은 지붕과 푸른 바다가 어우러져 '동양의 작은 유럽'이라 불리며, 신선한 해산물 바지락 볶음과 시원한 칭다오 생맥주를 즐기기 완벽한 휴양지입니다.",
                "spots": ["칭다오 맥주 박물관", "잔교(팔각정 바다 부두)", "5.4 광장 & 야경 분수", "신호산 공원(붉은 지붕 독일풍 전경)"],
                "restaurants": [
                    {"name": "해주처(바지락 요리)", "cat": "해산물 포차", "desc": "매콤한 바지락 볶음과 갓 뽑아낸 생 칭다오 맥주 한 잔", "url": "https://www.google.com/maps/search/Qingdao+Seafood+Clams"},
                    {"name": "춘화루(Chun He Lou)", "cat": "산둥 요리", "desc": "백년 역사를 지닌 바삭한 탕수육과 향탑만두 명가", "url": "https://www.google.com/maps/search/Chun+He+Lou+Qingdao"},
                    {"name": "피차이위안 꼬치거리", "cat": "로컬 길거리 음식", "desc": "오징어 꼬치, 양꼬치를 비롯한 칭다오 대표 야시장", "url": "https://www.google.com/maps/search/Pichai+Yuan+Qingdao"}
                ]
            }
        }
    },
    "프랑스 🇫🇷": {
        "currency": "EUR",
        "currency_symbol": "€",
        "flight_base": 1250000,
        "cities": {
            "파리 (Paris)": {
                "lat": 48.8566, "lon": 2.3522,
                "desc": "센강을 따라 에펠탑과 루브르가 펼쳐지는 낭만의 도시로, 미식과 예술, 패션의 향기가 가득해 전 세계 여행자들의 버킷리스트로 꼽힙니다.",
                "spots": ["에펠탑 & 샹드마르스 공원", "루브르 박물관", "몽마르트르 언덕 & 사크레쾨르 대성당", "오르세 미술관 & 센강 유람선"],
                "restaurants": [
                    {"name": "Le Relais de l'Entrecôte", "cat": "스테이크", "desc": "특제 소스를 얹은 바베큐 스테이크와 무한 감자튀김", "url": "https://www.google.com/maps/search/Le+Relais+de+l'Entrecote+Paris"},
                    {"name": "Bouillon Chartier", "cat": "전통 프렌치", "desc": "100년 전통의 유서 깊은 파리지앵 가성비 비스트로", "url": "https://www.google.com/maps/search/Bouillon+Chartier+Paris"},
                    {"name": "Café de Flore", "cat": "프랑스 카페", "desc": "생제르맹 거리를 대표하는 유서 깊은 감성 노천 카페", "url": "https://www.google.com/maps/search/Cafe+de+Flore+Paris"}
                ]
            },
            "니스 (Nice)": {
                "lat": 43.7102, "lon": 7.2620,
                "desc": "눈부신 에메랄드빛 코트다쥐르 지중해 바다와 붉은 구시가지 골목, 온화한 햇살이 일 년 내내 반겨주는 프랑스 남부 최고의 휴양 도시입니다.",
                "spots": ["프롬나드 데 장글레(영국인 산책로)", "캐슬 힐(니스 파노라마 전망대)", "니스 구시가지(살레야 광장 시장)", "마티스 미술관"],
                "restaurants": [
                    {"name": "Chez René Socca", "cat": "니스 전통 간식", "desc": "병아리콩 전(소카)과 다양한 지중해 핑거푸드", "url": "https://www.google.com/maps/search/Chez+Rene+Socca+Nice"},
                    {"name": "La Voglia", "cat": "지중해 해산물", "desc": "살레야 시장 근처 푸짐한 해산물 파스타와 화덕 피자", "url": "https://www.google.com/maps/search/La+Voglia+Nice"},
                    {"name": "Fenocchio Glacier", "cat": "수제 젤라또", "desc": "100가지 독특한 풍미를 자랑하는 니스 원조 젤라또", "url": "https://www.google.com/maps/search/Fenocchio+Glacier+Nice"}
                ]
            },
            "리옹 (Lyon)": {
                "lat": 45.7640, "lon": 4.8357,
                "desc": "프랑스 미식의 수도로 불리며, 유네스코 구시가지 골목 비외 리옹과 전통 식당 '부숑(Bouchon)'에서 프랑스 진짜 손맛을 경험할 수 있습니다.",
                "spots": ["푸르비에르 노트르담 대성당", "리옹 구시가지(비외 리옹)", "벨쿠르 광장", "폴 보퀴즈 전통 미식 시장"],
                "restaurants": [
                    {"name": "Le Bouchon des Filles", "cat": "부숑 전통식", "desc": "미식의 도시 리옹 정통 가정식 코스 요리", "url": "https://www.google.com/maps/search/Le+Bouchon+des+Filles+Lyon"},
                    {"name": "Brasserie Georges", "cat": "전통 브라세리", "desc": "1836년 문을 연 웅장한 아르데코 양식의 비스트로", "url": "https://www.google.com/maps/search/Brasserie+Georges+Lyon"},
                    {"name": "Boulangerie Saint Paul", "cat": "베이커리", "desc": "붉은 프랄린을 넣은 리옹 명물 브리오슈 타르트", "url": "https://www.google.com/maps/search/Boulangerie+Saint+Paul+Lyon"}
                ]
            }
        }
    },
    "베트남 🇻🇳": {
        "currency": "VND",
        "currency_symbol": "₫",
        "flight_base": 380000,
        "cities": {
            "다낭 (Da Nang)": {
                "lat": 16.0544, "lon": 108.2022,
                "desc": "끝없이 펼쳐진 미케 비치와 가성비 좋은 고급 풀빌라, 신비로운 바나힐과 유등 띄우는 호이안 야경까지 완벽한 힐링 휴양지입니다.",
                "spots": ["미케 비치 해변", "바나힐 골든 브릿지", "오행산 (마블 마운틴)", "호이안 올드타운 야경 투어"],
                "restaurants": [
                    {"name": "냐벱 스아 (Nha Bep Xua)", "cat": "베트남 가정식", "desc": "반쎄오, 분짜, 모닝글로리가 맛있는 깔끔한 식당", "url": "https://www.google.com/maps/search/Nha+Bep+Xua+Da+Nang"},
                    {"name": "목 해산물 식당 (Moc Seafood)", "cat": "해산물 BBQ", "desc": "크레이피시와 버터 갈릭 새우를 착한 가격에 즐기는 곳", "url": "https://www.google.com/maps/search/Moc+Seafood+Da+Nang"},
                    {"name": "콩카페 1호점 (Cong Caphe)", "cat": "코코넛 커피", "desc": "한강변을 바라보며 마시는 달콤한 코코넛 스무디 커피", "url": "https://www.google.com/maps/search/Cong+Caphe+Da+Nang"}
                ]
            },
            "하노이 (Hanoi)": {
                "lat": 21.0285, "lon": 105.8542,
                "desc": "호안끼엠 호수 주변의 활기찬 오토바이 물결과 기찻길 마을, 달콤한 에그 커피와 정통 쌀국수가 여행자를 매료시키는 베트남의 수도입니다.",
                "spots": ["호안끼엠 호수 & 응옥선 사당", "하노이 기찻길 마을", "성 요셉 대성당", "하롱베이 크루즈 당일/1박 투어"],
                "restaurants": [
                    {"name": "분짜 흐엉리엔(오바마 분짜)", "cat": "숯불 분짜", "desc": "오바마 대통령이 방문해 극찬한 숯불 돼지고기 쌀국수", "url": "https://www.google.com/maps/search/Bun+Cha+Huong+Lien+Hanoi"},
                    {"name": "포텐 리꿕수(Pho 10)", "cat": "소고기 쌀국수", "desc": "미쉐린 빕구르망에 선정된 깊은 소고기 육수 쌀국수", "url": "https://www.google.com/maps/search/Pho+10+Ly+Quoc+Su+Hanoi"},
                    {"name": "카페 지앙(Cafe Giang)", "cat": "원조 에그 커피", "desc": "1946년부터 이어져 온 부드럽고 달콤한 커스터드 에그커피", "url": "https://www.google.com/maps/search/Cafe+Giang+Hanoi"}
                ]
            },
            "호치민 (Ho Chi Minh)": {
                "lat": 10.8231, "lon": 106.6297,
                "desc": "프랑스 식민지 시절의 우아한 건축물과 현대적인 루프탑 바, 카페 아파트먼트 등 젊고 역동적인 에너지가 넘치는 베트남의 경제 중심지입니다.",
                "spots": ["노트르담 대성당 & 중앙 우체국", "통일궁(독립궁)", "벤탄 시장 & 카페 아파트먼트", "사이공 스카이덱(비텍스코)"],
                "restaurants": [
                    {"name": "꽌넴(Quan Nem)", "cat": "게살 넴 & 분짜", "desc": "CNN에 소개된 바삭한 통게살 스프링롤 넴 맛집", "url": "https://www.google.com/maps/search/Quan+Nem+Ho+Chi+Minh"},
                    {"name": "피자 4피스(Pizza 4P's)", "cat": "화덕 피자 & 부라타 치즈", "desc": "수제 부라타 치즈와 퓨전 화덕피자로 유명한 베트남 최고 레스토랑", "url": "https://www.google.com/maps/search/Pizza+4Ps+Ben+Thanh"},
                    {"name": "반미 홍호아(Banh Mi Hong Hoa)", "cat": "바삭 반미", "desc": "갓 구운 바게트에 고기와 파테를 듬뿍 넣은 국민 반미", "url": "https://www.google.com/maps/search/Banh+Mi+Hong+Hoa+Ho+Chi+Minh"}
                ]
            }
        }
    },
    "미국 🇺🇸": {
        "currency": "USD",
        "currency_symbol": "$",
        "flight_base": 1450000,
        "cities": {
            "뉴욕 (New York)": {
                "lat": 40.7128, "lon": -74.0060,
                "desc": "타임스퀘어의 번쩍이는 전광판, 브로드웨이 뮤지컬, 센트럴 파크와 미술관들이 뿜어내는 잠들지 않는 전 세계 문화와 트렌드의 심장입니다.",
                "spots": ["타임스퀘어 & 브로드웨이", "센트럴 파크 산책", "자유의 여신상 페리", "엠파이어 스테이트 빌딩 & 록펠러 탑"],
                "restaurants": [
                    {"name": "Peter Luger Steak House", "cat": "드라이에이징 스테이크", "desc": "브루클린에서 이어져 온 백년 전통 포터하우스 스테이크", "url": "https://www.google.com/maps/search/Peter+Luger+Steak+House+Brooklyn"},
                    {"name": "Joe's Pizza", "cat": "뉴욕 조각 피자", "desc": "그리니치 빌리지의 클래식 바삭 치즈 슬라이스 피자", "url": "https://www.google.com/maps/search/Joes+Pizza+Carmine+St"},
                    {"name": "Katz's Delicatessen", "cat": "파스트라미 샌드위치", "desc": "훈제 소고기를 아낌없이 채워 넣은 뉴욕 소울 푸드", "url": "https://www.google.com/maps/search/Katzs+Delicatessen"}
                ]
            },
            "로스앤젤레스 (Los Angeles)": {
                "lat": 34.0522, "lon": -118.2437,
                "desc": "눈부신 캘리포니아 햇살과 산타모니카 해변, 할리우드 영화 산업의 꿈과 유니버설 스튜디오의 즐거움이 가득한 서부 최대의 엔터테인먼트 도시입니다.",
                "spots": ["할리우드 명예의 거리 & 사인", "산타모니카 피어 해변", "그리피스 천문대 야경", "유니버설 스튜디오 할리우드"],
                "restaurants": [
                    {"name": "인앤아웃 버거 할리우드", "cat": "캘리포니아 버거", "desc": "신선한 패티와 애니멀 스타일 감자튀김의 서부 대표 버거", "url": "https://www.google.com/maps/search/In-N-Out+Burger+Sunset+Blvd"},
                    {"name": "보테가 루이(Bottega Louie)", "cat": "이탈리안 & 디저트", "desc": "다운타운 명물 대리석 인테리어와 화려한 마카롱 타르트", "url": "https://www.google.com/maps/search/Bottega+Louie+Los+Angeles"},
                    {"name": "핑크스 핫도그(Pink's Hot Dogs)", "cat": "클래식 칠리독", "desc": "1939년부터 할리우드 스타들이 즐겨 찾던 칠리 치즈 핫도그", "url": "https://www.google.com/maps/search/Pinks+Hot+Dogs+LA"}
                ]
            },
            "샌프란시스코 (San Francisco)": {
                "lat": 37.7749, "lon": -122.4194,
                "desc": "붉은 금문교와 언덕길을 오르는 클래식 케이블카, 피어 39의 물개들과 신선한 사워도우 조개스프가 낭만을 더하는 항구 도시입니다.",
                "spots": ["금문교(골든게이트 브리지)", "피셔맨스 워프 & 피어 39 바다사자", "롬바드 꽃길 거리", "알카트라즈 섬 감옥 투어"],
                "restaurants": [
                    {"name": "보딘 베이커리(Boudin Bakery)", "cat": "클램 차우더", "desc": "새콤한 사워도우 브레드 볼에 담아주는 진한 조개 스프", "url": "https://www.google.com/maps/search/Boudin+Bakery+Fishermans+Wharf"},
                    {"name": "슈퍼두퍼 버거 유니온스퀘어", "cat": "오가닉 수제버거", "desc": "갈릭 프라이와 달콤한 밀크셰이크가 일품인 샌프란 명물", "url": "https://www.google.com/maps/search/Super+Duper+Burgers+Union+Square"},
                    {"name": "타르틴 베이커리(Tartine Bakery)", "cat": "장인 크루아상", "desc": "미국 3대 베이커리로 꼽히는 향긋한 컨트리 브레드와 페이스트리", "url": "https://www.google.com/maps/search/Tartine+Bakery+San+Francisco"}
                ]
            }
        }
    },
    "스위스 🇨🇭": {
        "currency": "CHF",
        "currency_symbol": "CHF",
        "flight_base": 1400000,
        "cities": {
            "인터라켄 (Interlaken)": {
                "lat": 46.6863, "lon": 7.8632,
                "desc": "알프스의 두 호수 사이에 자리 잡은 천혜의 마을로, 융프라우요흐와 그린델발트로 향하는 산악 액티비티의 베이스캠프입니다.",
                "spots": ["융프라우요흐 유럽의 지붕", "그린델발트 피르스트 액티비티", "하더쿨름 전망대", "브리엔츠 호수 유람선"],
                "restaurants": [
                    {"name": "Restaurant Taverne", "cat": "치즈 퐁듀 & 뢰스티", "desc": "스위스 전통 알프스 치즈 퐁듀와 바삭한 감자 뢰스티", "url": "https://www.google.com/maps/search/Restaurant+Taverne+Interlaken"},
                    {"name": "Bebbis Restaurant", "cat": "스위스 전통식", "desc": "활기찬 분위기에서 라이브 음악과 즐기는 미트 퐁듀", "url": "https://www.google.com/maps/search/Bebbis+Restaurant+Interlaken"},
                    {"name": "Velo Cafe", "cat": "브런치 & 커피", "desc": "인터라켄 중심가에서 즐기는 신선한 베이글과 커피", "url": "https://www.google.com/maps/search/Velo+Cafe+Interlaken"}
                ]
            },
            "취리히 (Zurich)": {
                "lat": 47.3769, "lon": 8.5417,
                "desc": "청정한 호수와 리마트강을 끼고 있는 스위스 최대 도시로, 세계 최고의 삶의 질과 고급 쇼핑, 예술 갤러리가 조화를 이루는 곳입니다.",
                "spots": ["취리히 호수 산책로", "반호프슈트라세 명품거리", "그로스뮌스터 대성당", "린덴호프 언덕 전망"],
                "restaurants": [
                    {"name": "Zeughauskeller", "cat": "취리히 정통식", "desc": "15세기 무기고를 개조한 곳에서 맛보는 취리히식 송아지 요리", "url": "https://www.google.com/maps/search/Zeughauskeller+Zurich"},
                    {"name": "Sprungli", "cat": "스위스 초콜릿 카페", "desc": "미니 마카롱 '룩셈부르겔리'와 핫초콜릿의 본산", "url": "https://www.google.com/maps/search/Sprungli+Paradeplatz+Zurich"},
                    {"name": "Rheinfelder Bierhalle", "cat": "비어가든 & 뢰스티", "desc": "푸짐한 소시지와 바삭한 뢰스티를 맥주와 즐기는 로컬 식당", "url": "https://www.google.com/maps/search/Rheinfelder+Bierhalle+Zurich"}
                ]
            },
            "루체른 (Luzern)": {
                "lat": 47.0502, "lon": 8.3093,
                "desc": "꽃으로 장식된 지붕 덮인 중세 목조다리 카펠교와 백조가 노니는 호수, 필라투스산이 한 폭의 엽서 같은 그림을 완성하는 낭만 도시입니다.",
                "spots": ["카펠교(유럽 최고 목조다리)", "빈사의 사자상", "필라투스/리기산 산악열차", "루체른 호수 유람선"],
                "restaurants": [
                    {"name": "Wirtshaus Galliker", "cat": "스위스 전통 가정식", "desc": "100년 넘는 전통을 간직한 루체른식 파이(Chugelipastete)", "url": "https://www.google.com/maps/search/Wirtshaus+Galliker+Luzern"},
                    {"name": "Old Swiss House", "cat": "테이블 사이드 슈니첼", "desc": "손님 테이블 앞에서 버터에 직접 구워주는 명물 슈니첼", "url": "https://www.google.com/maps/search/Old+Swiss+House+Luzern"},
                    {"name": "Bachmann", "cat": "초콜릿 베이커리", "desc": "흐르는 초콜릿 벽과 신선한 프랄린을 만나는 루체른 대표 제과점", "url": "https://www.google.com/maps/search/Confiserie+Bachmann+Luzern"}
                ]
            }
        }
    },
    "헝가리 🇭🇺": {
        "currency": "HUF",
        "currency_symbol": "Ft",
        "flight_base": 1150000,
        "cities": {
            "부다페스트 (Budapest)": {
                "lat": 47.4979, "lon": 19.0402,
                "desc": "도나우강의 진주라 불리며, 황금빛 국회의사당 야경과 노천 세체니 온천, 앤틱한 궁전 카페에서 동유럽의 고혹적인 매력을 느낄 수 있습니다.",
                "spots": ["국회의사당 야경 & 다뉴브강 크루즈", "어부의 요새 & 마차시 성당", "세체니 온천", "부다 왕궁 & 세체니 다리"],
                "restaurants": [
                    {"name": "Menza Étterem", "cat": "굴라쉬 & 헝가리식", "desc": "레트로 모던한 감성에서 맛보는 깊고 얼큰한 소고기 굴라쉬", "url": "https://www.google.com/maps/search/Menza+Etterem+Budapest"},
                    {"name": "Comme Chez Soi", "cat": "이탈리안 & 헝가리안", "desc": "푸아그라 요리와 해산물 파스타로 유명한 친절한 맛집", "url": "https://www.google.com/maps/search/Comme+Chez+Soi+Budapest"},
                    {"name": "New York Café", "cat": "궁전풍 카페", "desc": "세상에서 가장 아름다운 카페로 꼽히는 화려한 궁전 카페", "url": "https://www.google.com/maps/search/New+York+Cafe+Budapest"}
                ]
            },
            "데브레첸 (Debrecen)": {
                "lat": 47.5316, "lon": 21.6273,
                "desc": "헝가리 제2의 도시로, 웅장한 대형 개혁교회와 대초원 호르토바지의 야생마, 푸른 나기에르되 숲속 온천이 여유를 선사합니다.",
                "spots": ["데브레첸 대개혁 교회", "호르토바지 국립공원 초원", "데리 박물관", "나기에르되 공원 & 온천"],
                "restaurants": [
                    {"name": "Csokonai Restaurant", "cat": "전통 헝가리안", "desc": "데브레첸 소시지와 오리 다리 구이가 유명한 클래식 식당", "url": "https://www.google.com/maps/search/Csokonai+Restaurant+Debrecen"},
                    {"name": "IKON Restaurant", "cat": "모던 파인다이닝", "desc": "로컬 식재료를 현대적으로 재해석한 헝가리 동부 최고 맛집", "url": "https://www.google.com/maps/search/IKON+Restaurant+Debrecen"},
                    {"name": "Vintage World Cafe", "cat": "디저트 브런치", "desc": "꽃과 앤틱 가구로 꾸며진 사진 찍기 좋은 예쁜 베이커리 카페", "url": "https://www.google.com/maps/search/Vintage+World+Debrecen"}
                ]
            },
            "세게드 (Szeged)": {
                "lat": 46.2530, "lon": 20.1414,
                "desc": "일조량이 가장 풍부해 '햇살의 도시'라 불리며, 파프리카의 본고장답게 얼큰한 생선 어탕 헐라슬레와 아름다운 돔 성당이 유명합니다.",
                "spots": ["세게드 서약 교회(둠 성당)", "시나고그(화려한 유대교 회당)", "티서 강변 산책로", "모라 페렌츠 박물관"],
                "restaurants": [
                    {"name": "Kiskőrössy Halászcsárda", "cat": "헐라슬레(어탕)", "desc": "세게드 명물 파프리카 민물 매운탕 헐라슬레 원조 맛집", "url": "https://www.google.com/maps/search/Kiskorossy+Halaszcsarda+Szeged"},
                    {"name": "Propeller Söröző", "cat": "수제 맥주 & 학센", "desc": "바삭한 족발 요리와 신선한 헝가리 로컬 생맥주", "url": "https://www.google.com/maps/search/Propeller+Szeged"},
                    {"name": "A Cappella Cukrászda", "cat": "도보스 토르테", "desc": "돔 광장 앞에서 카라멜 케이크를 맛보는 유서 깊은 제과점", "url": "https://www.google.com/maps/search/A+Cappella+Cukraszda+Szeged"}
                ]
            }
        }
    }
}


# ----------------------------------------------------
# 3. 국내 지역구별 동물 주민 캐릭터 매칭
# ----------------------------------------------------
def get_district_villager(address):
    default_villager = {
        "name": "애플 🐹", "title": "동네 골목 탐험대장", "icon": "🍎",
        "comment": "골목골목 숨은 예쁜 카페와 맛있는 간식거리가 가득한 동네예요!",
        "theme_color": "#ff6b6b", "bg_color": "#ffe3e3"
    }
    if not address:
        return default_villager
    if any(k in address for k in ["강남구", "서초구", "송파구"]):
        return {
            "name": "너굴 사장 🦝", "title": "트렌디 번화가 총괄 대표", "icon": "💰",
            "comment": "높은 빌딩과 세련된 명소가 가득한 핫플레이스입니다! 알찬 쇼핑을 즐겨보세요!",
            "theme_color": "#f39c12", "bg_color": "#fef5e7"
        }
    elif any(k in address for k in ["종로구", "중구", "용산구"]):
        return {
            "name": "여울 🐶", "title": "서울 명소 수석 안내원", "icon": "🌸",
            "comment": "고궁과 남산타워처럼 유서 깊은 아름다움을 간직한 서울의 심장부예요!",
            "theme_color": "#27ae60", "bg_color": "#eafaf1"
        }
    elif any(k in address for k in ["마포구", "서대문구", "영등포구", "은평구"]):
        return {
            "name": "쭈니 🐿️", "title": "트렌드 & 카페 셀럽", "icon": "☕",
            "comment": "감성적인 인디 음악과 개성 넘치는 편집숍이 흐르는 낭만적인 지역이지, 차차!",
            "theme_color": "#2980b9", "bg_color": "#ebf5fb"
        }
    elif any(k in address for k in ["성동구", "광진구", "강동구", "동대문구"]):
        return {
            "name": "사이다 🐱", "title": "피크닉 & 힐링 가이드", "icon": "🌿",
            "comment": "서울숲과 푸른 강바람을 맞으며 산책하기 참 좋은 평화로운 곳이에요, 퐁퐁~",
            "theme_color": "#16a085", "bg_color": "#e8f8f5"
        }
    return default_villager


# ----------------------------------------------------
# 4. 모동숲 테마 CSS
# ----------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Gaegu:wght@400;700&display=swap');

    .stMarkdown, p, h1, h2, h3, h4, span:not([class*="stSlider"]), label, button {
        font-family: 'Jua', 'Gaegu', cursive, sans-serif;
    }

    [data-testid="stIconMaterial"], .material-symbols-rounded, .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    [data-testid="stSidebarCollapsedControl"] button {
        background-color: #56cfe1 !important;
        border: 3px solid #0096c7 !important;
        border-radius: 16px !important;
        box-shadow: 0 3px 0 #0077b6 !important;
        padding: 4px 12px !important;
        height: auto !important;
        min-width: 44px !important;
    }

    [data-testid="stSidebarCollapsedControl"] button span,
    [data-testid="stSidebarCollapsedControl"] button svg {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"] button::after {
        content: ">>" !important;
        font-family: 'Jua', sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
        display: inline-block !important;
        line-height: 1 !important;
    }

    .stApp {
        background-color: #f6f3e7;
        background-image: 
            radial-gradient(#b2e2d8 18%, transparent 19%),
            radial-gradient(#d5f1e8 18%, transparent 19%);
        background-size: 54px 54px;
        background-position: 0 0, 27px 27px;
    }

    [data-testid="stSidebar"] {
        background-color: #f7eed7 !important;
        border-right: 5px solid #d5bc96 !important;
    }

    .wood-signboard {
        background: linear-gradient(180deg, #fce0a2 0%, #ebb969 100%);
        border: 7px solid #8d5629;
        box-shadow: 0 8px 0 #573111, 0 12px 20px rgba(0,0,0,0.15);
        border-radius: 40px;
        padding: 18px 30px;
        text-align: center;
        margin: 15px 0 25px 0;
    }

    .wood-title {
        font-size: 2.3rem;
        color: #5a320f;
        text-shadow: 2px 2px 0px #fff4cf;
        letter-spacing: 1px;
    }

    .wood-subtitle {
        font-size: 1.15rem;
        color: #7a491c;
        margin-top: 4px;
    }

    /* 도시 소개 카드 (신규 추가 스타일) */
    .city-intro-box {
        background: #ffffff;
        border: 4px solid #48bfe3;
        border-radius: 24px;
        padding: 18px 24px;
        margin: 15px 0 20px 0;
        box-shadow: 0 6px 0 #0096c7;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .city-intro-badge {
        background-color: #e0fbfb;
        color: #0077b6;
        font-size: 1.05rem;
        font-weight: bold;
        padding: 6px 14px;
        border-radius: 14px;
        white-space: nowrap;
    }

    .city-intro-text {
        font-size: 1.12rem;
        color: #2b3a4a;
        line-height: 1.6;
    }

    .villager-banner {
        border-radius: 20px;
        padding: 14px 20px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 15px;
        border: 3px solid;
    }

    .villager-avatar {
        font-size: 2.2rem;
        background: #ffffff;
        border-radius: 50%;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }

    .detail-card {
        background-color: #ffffff;
        border-radius: 28px;
        border: 5px solid #64dfdf;
        padding: 24px;
        box-shadow: 0 7px 0 #48bfe3;
        height: 100%;
        box-sizing: border-box;
    }

    .place-main-title {
        font-size: 1.7rem;
        color: #0077b6;
        font-weight: bold;
        margin-bottom: 6px;
    }

    .place-badge {
        display: inline-block;
        background-color: #e0fbfb;
        color: #0096c7;
        font-size: 0.95rem;
        padding: 4px 14px;
        border-radius: 16px;
        border: 2px solid #80ed99;
        margin-bottom: 16px;
    }

    .info-line {
        font-size: 1.05rem;
        color: #4a3e35;
        line-height: 1.8;
    }

    .exchange-highlight-box {
        background: #f0fdf4;
        border: 3px solid #86efac;
        border-radius: 18px;
        padding: 14px 18px;
        margin: 12px 0;
        box-shadow: 0 3px 0 #4ade80;
    }

    .exchange-big-val {
        font-size: 1.45rem;
        font-weight: bold;
        color: #15803d;
        display: block;
        margin-bottom: 4px;
    }

    .kakao-map-btn {
        display: inline-block;
        background: linear-gradient(180deg, #fee500 0%, #f9d423 100%);
        color: #3c1e1e !important;
        font-weight: bold;
        text-decoration: none;
        padding: 10px 22px;
        border-radius: 18px;
        border: 2px solid #d4af37;
        box-shadow: 0 4px 0 #b38600;
        margin-top: 15px;
        font-size: 1.05rem;
    }

    .weather-card {
        background-color: #ffffff;
        border-radius: 28px;
        border: 5px solid #ffb703;
        padding: 24px;
        box-shadow: 0 7px 0 #fb8500;
        height: 100%;
        box-sizing: border-box;
    }

    .outfit-box {
        background-color: #fff9db;
        border-radius: 18px;
        border: 3px dashed #f4a261;
        padding: 14px 18px;
        margin-top: 14px;
        color: #6b3e11;
        line-height: 1.6;
    }

    .restaurant-card {
        background-color: #ffffff;
        border-radius: 22px;
        border: 4px solid #ff9f1c;
        padding: 18px;
        box-shadow: 0 5px 0 #e76f51;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .restaurant-title {
        font-size: 1.25rem;
        color: #d9480f;
        font-weight: bold;
        margin-bottom: 4px;
    }

    .restaurant-dist {
        display: inline-block;
        background-color: #ffe8cc;
        color: #d9480f;
        font-size: 0.85rem;
        padding: 2px 8px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-weight: bold;
    }

    .stImage img {
        border-radius: 24px !important;
        border: 5px solid #57cc99 !important;
        box-shadow: 0 6px 0 #38a3a5 !important;
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# 5. 공통 유틸 및 API 함수
# ----------------------------------------------------
def get_outfit_recommendation(temp, weather_id):
    rain_snow = ""
    if 200 <= weather_id < 600:
        rain_snow = " ☔ 비가 올 수 있으니 나뭇잎 우산을 챙기세요!"
    elif 600 <= weather_id < 700:
        rain_snow = " ❄️ 눈이 올 수 있으니 방한모자를 착용하세요!"

    if temp >= 28:
        outfit = "하와이안 셔츠, 민소매, 린넨 반바지, 스트랩 샌들"
    elif 23 <= temp < 28:
        outfit = "반팔 티셔츠, 얇은 카라 셔츠, 면바지, 청바지"
    elif 20 <= temp < 23:
        outfit = "긴팔 티셔츠, 얇은 니트 가디건, 슬랙스, 청바지"
    elif 17 <= temp < 20:
        outfit = "맨투맨, 도톰한 가디건, 면바지, 긴 바지"
    elif 12 <= temp < 17:
        outfit = "자켓, 야상 점퍼, 울 가디건, 청바지"
    elif 9 <= temp < 12:
        outfit = "트렌치코트, 블루종, 니트, 기모바지"
    elif 5 <= temp < 9:
        outfit = "도톰한 코트, 가죽자켓, 히트텍, 머플러"
    else:
        outfit = "패딩 점퍼, 두꺼운 모직코트, 털장갑, 니트 목도리"
    return outfit + rain_snow

@st.cache_data(ttl=3600)
def fetch_all_exchange_rates():
    if not EXCHANGE_API_KEY:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/KRW"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("result") == "success":
            return res.get("conversion_rates", {})
    except Exception:
        pass
    return None

def get_krw_rate(rates, currency):
    if not rates or currency not in rates or rates[currency] == 0:
        return None
    return 1 / rates[currency]

def search_places(keyword):
    if not KAKAO_REST_API_KEY or not keyword:
        return []
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": keyword, "size": 15}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        return res.json().get("documents", [])
    except Exception:
        return []

def get_nearby_restaurants(lat, lon):
    if not KAKAO_REST_API_KEY:
        return []
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {
        "category_group_code": "FD6",
        "x": str(lon), "y": str(lat),
        "radius": 500, "sort": "distance", "size": 3
    }
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        return res.json().get("documents", [])
    except Exception:
        return []

def get_weather(lat, lon):
    if not OPENWEATHER_API_KEY:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat, "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric", "lang": "kr"
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        return res.json()
    except Exception:
        return None

def get_kakao_static_map(lat, lon, width=800, height=380):
    if not KAKAO_REST_API_KEY:
        return None
    url = "https://dapi.kakao.com/v2/local/staticmap/point"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {
        "w": width, "h": height, "p": f"{lon},{lat}", "level": 3,
        "markers": f"type:default|lat:{lat}|lng:{lon}"
    }
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        if res.status_code == 200:
            return res.content
    except Exception:
        pass
    return None


# ----------------------------------------------------
# 6. 왼쪽 사이드바 (실시간 환율 & 계산기)
# ----------------------------------------------------
all_rates = fetch_all_exchange_rates()

with st.sidebar:
    st.markdown("## 🧭 무인도 종합 안내소")
    st.caption("국내와 전 세계 여행을 친절히 안내합니다!")
    st.markdown("---")

    st.markdown("### 💰 너굴 환율 센터")
    with st.expander("실시간 환율 및 계산기", expanded=True):
        if all_rates:
            usd_rate = get_krw_rate(all_rates, "USD") or 1350
            jpy_rate = (get_krw_rate(all_rates, "JPY") or 9.0) * 100
            eur_rate = get_krw_rate(all_rates, "EUR") or 1450
            cny_rate = get_krw_rate(all_rates, "CNY") or 190

            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="🇺🇸 1 USD", value=f"₩{usd_rate:,.1f}")
                if st.button("USD 변환", key="btn_usd", use_container_width=True):
                    st.session_state.calc_target = "USD"
                st.metric(label="🇪🇺 1 EUR", value=f"₩{eur_rate:,.1f}")
                if st.button("EUR 변환", key="btn_eur", use_container_width=True):
                    st.session_state.calc_target = "EUR"
            with c2:
                st.metric(label="🇯🇵 100 JPY", value=f"₩{jpy_rate:,.1f}")
                if st.button("JPY 변환", key="btn_jpy", use_container_width=True):
                    st.session_state.calc_target = "JPY"
                st.metric(label="🇨🇳 1 CNY", value=f"₩{cny_rate:,.1f}")
                if st.button("CNY 변환", key="btn_cny", use_container_width=True):
                    st.session_state.calc_target = "CNY"

            target = st.session_state.calc_target
            unit_rate = get_krw_rate(all_rates, target) or 1.0

            st.markdown(f"#### 🧮 {target} 환율 계산")
            calc_mode = st.radio(
                "변환 기준",
                [f"외화({target}) ➡️ 원화(KRW)", f"원화(KRW) ➡️ 외화({target})"],
                label_visibility="collapsed"
            )

            if "외화" in calc_mode:
                default_val = 1000.0 if target == "JPY" else 100.0
                input_val = st.number_input(f"금액 ({target})", min_value=0.0, value=default_val, step=10.0)
                result_krw = input_val * unit_rate
                st.success(f"**약 {result_krw:,.0f} 원**")
            else:
                input_krw = st.number_input("금액 (원/KRW)", min_value=0, value=100000, step=10000)
                result_foreign = input_krw / unit_rate if unit_rate > 0 else 0
                st.success(f"**약 {result_foreign:,.2f} {target}**")
        else:
            st.warning("환율 정보를 불러올 수 없습니다.")


# ----------------------------------------------------
# 7. 상단 헤더 배너
# ----------------------------------------------------
banner_path = "image/dongsoop.jpg"
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)

st.markdown("""
<div class="wood-signboard">
    <div class="wood-title">🍃 모여봐요 여행의 숲 (국내 & 해외) 🏝️</div>
    <div class="wood-subtitle">너굴 안내소에서 국내 명소부터 전 세계 도시 일정·예산까지 한 번에!</div>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# 8. 국내 vs 해외 모드 탭
# ----------------------------------------------------
travel_mode = st.radio(
    "여행 모드를 선택하세요:",
    ["🇰🇷 국내 여행지 탐색", "✈️ 국외 (해외) 여행지 추천"],
    horizontal=True
)

st.markdown("---")

# ====================================================
# [A] 국내 여행지 탐색 모드
# ====================================================
if travel_mode == "🇰🇷 국내 여행지 탐색":
    st.markdown("### ✈️ 가고 싶은 국내 여행지를 검색해보세요!")

    seoul_hotspots = [
        "선택 안 함", "강남역", "선릉과정릉", "경복궁", "N서울타워",
        "롯데월드타워", "북촌한옥마을", "동대문디자인플라자(DDP)",
        "명동성당", "창덕궁", "여의도 한강공원", "국립중앙박물관"
    ]
    quick_pick = st.selectbox("서울 인기 명소 빠른 선택:", seoul_hotspots, index=0)

    # 국내 명소 한 줄 소개 박스 표시
    if quick_pick != "선택 안 함" and quick_pick in DOMESTIC_SPOT_DESCRIPTIONS:
        st.markdown(f"""
        <div class="city-intro-box">
            <div class="city-intro-badge">✨ {quick_pick} 여행 가이드</div>
            <div class="city-intro-text">{DOMESTIC_SPOT_DESCRIPTIONS[quick_pick]}</div>
        </div>
        """, unsafe_allow_html=True)

    default_query = quick_pick if quick_pick != "선택 안 함" else ""

    col_input, col_search_btn = st.columns([5, 1])
    with col_input:
        search_keyword = st.text_input(
            "국내 장소 검색",
            value=default_query,
            placeholder="떠나고 싶은 국내 장소를 입력하세요 (예: 강남역, 해운대, 성산일출봉 등)...",
            label_visibility="collapsed"
        )
    with col_search_btn:
        btn_clicked = st.button("🔍 국내 탐색", use_container_width=True)

    if search_keyword:
        places = search_places(search_keyword)
        if not places:
            st.warning(f"'{search_keyword}'에 대한 검색 결과가 없습니다.")
        else:
            st.markdown(f"#### 📍 검색된 장소 목록 ({len(places)}곳)")
            place_options = [
                f"{p['place_name']} | ({p.get('road_address_name') or p.get('address_name') or '주소 없음'})"
                for p in places
            ]
            selected_index = st.selectbox("확인하고 싶은 정확한 장소를 선택해주세요:", range(len(place_options)), format_func=lambda i: place_options[i])
            selected_place = places[selected_index]
            lat_val = float(selected_place['y'])
            lon_val = float(selected_place['x'])
            addr_str = selected_place.get('road_address_name') or selected_place.get('address_name') or '주소 없음'
            phone_str = selected_place.get('phone') if selected_place.get('phone') else '전화번호 없음'

            villager = get_district_villager(addr_str)

            st.markdown(f"""
            <div class="villager-banner" style="background-color: {villager['bg_color']}; border-color: {villager['theme_color']};">
                <div class="villager-avatar">{villager['icon']}</div>
                <div>
                    <span style="font-size:1.15rem; font-weight:bold; color:{villager['theme_color']};">
                        지역 전담 주민: {villager['name']} ({villager['title']})
                    </span><br>
                    <span style="color:#4a3e35; font-size:1.02rem;">"{villager['comment']}"</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_detail, col_weather = st.columns([1, 1])
            with col_detail:
                st.markdown(f"""
                <div class="detail-card">
                    <div class="place-main-title">📍 {selected_place['place_name']}</div>
                    <div class="place-badge">{selected_place.get('category_name', '여행/관광')}</div>
                    <div class="info-line">
                        🏠 <b>주소:</b> {addr_str}<br>
                        📞 <b>전화번호:</b> {phone_str}<br>
                        🧭 <b>좌표:</b> 위도 {lat_val:.4f}, 경도 {lon_val:.4f}
                    </div>
                    <a href="{selected_place['place_url']}" target="_blank" class="kakao-map-btn">🗺️ 카카오 맵 길찾기 바로가기</a>
                </div>
                """, unsafe_allow_html=True)

            with col_weather:
                weather_data = get_weather(lat_val, lon_val)
                if weather_data and "weather" in weather_data:
                    w_desc = weather_data["weather"][0]["description"]
                    w_temp = weather_data["main"]["temp"]
                    w_feels = weather_data["main"]["feels_like"]
                    w_humidity = weather_data["main"]["humidity"]
                    w_id = weather_data["weather"][0]["id"]
                    w_icon = weather_data["weather"][0]["icon"]
                    icon_url = f"https://openweathermap.org/img/wn/{w_icon}@2x.png"
                    recommended_outfit = get_outfit_recommendation(w_feels, w_id)

                    st.markdown(f"""
                    <div class="weather-card">
                        <div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
                            <img src="{icon_url}" width="65" height="65" />
                            <div>
                                <span style="font-size:1.5rem; font-weight:bold; color:#e76f51;">{w_temp:.1f}°C</span>
                                <span style="color:#555; font-size:1rem; margin-left:8px;">({w_desc})</span><br>
                                <span style="color:#666; font-size:0.92rem;">체감온도 {w_feels:.1f}°C | 습도 {w_humidity}%</span>
                            </div>
                        </div>
                        <div class="outfit-box">
                            <span style="font-size:1.05rem; font-weight:bold; color:#b05d15;">👒 추천 여행 코디</span><br>
                            <span>{recommended_outfit}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("실시간 날씨 정보를 가져올 수 없습니다.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🍱 근방 500m 이내 인기 맛집 BEST 3")
            restaurants = get_nearby_restaurants(lat_val, lon_val)
            if restaurants:
                r_cols = st.columns(len(restaurants))
                for i, rest in enumerate(restaurants):
                    with r_cols[i]:
                        r_name = rest['place_name']
                        r_cat = rest.get('category_name', '음식점').split('>')[-1].strip()
                        r_dist = rest.get('distance', '0')
                        r_addr = rest.get('road_address_name') or rest.get('address_name') or '주소 정보 없음'
                        r_phone = rest.get('phone') if rest.get('phone') else '전화번호 미등록'
                        r_url = rest.get('place_url', '#')

                        st.markdown(f"""
                        <div class="restaurant-card">
                            <div>
                                <div class="restaurant-title">🍽️ {r_name}</div>
                                <span class="restaurant-dist">거리: 약 {r_dist}m</span><br>
                                <span style="font-size:0.88rem; color:#888;">{r_cat}</span>
                                <div style="font-size:0.95rem; color:#4a3e35; margin-top:8px; line-height:1.5;">
                                    📍 {r_addr}<br>📞 {r_phone}
                                </div>
                            </div>
                            <a href="{r_url}" target="_blank" class="kakao-map-btn" style="margin-top:12px; padding:6px 12px; font-size:0.95rem; text-align:center;">
                                카카오맵 메뉴 보기
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("주변 500m 이내에 등록된 음식점 정보를 찾을 수 없습니다.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"#### 🗺️ **{selected_place['place_name']}** 안내 지도")
            map_bytes = get_kakao_static_map(lat_val, lon_val, width=1000, height=450)
            if map_bytes:
                st.image(map_bytes, use_container_width=True, caption=f"📍 {selected_place['place_name']} 지도 (카카오 로컬 제공)")
            else:
                st.map([{"lat": lat_val, "lon": lon_val}], zoom=15, use_container_width=True)


# ====================================================
# [B] 국외 (해외) 여행지 추천 모드
# ====================================================
else:
    st.markdown("### ✈️ 떠나고 싶은 나라와 도시를 선택해주세요!")

    col_country, col_city = st.columns([1, 1])
    with col_country:
        selected_country = st.selectbox("1. 여행할 국가 선택:", list(GLOBAL_DESTINATIONS.keys()))
    with col_city:
        city_list = list(GLOBAL_DESTINATIONS[selected_country]["cities"].keys())
        selected_city = st.selectbox("2. 도시 선택:", city_list)

    country_info = GLOBAL_DESTINATIONS[selected_country]
    city_info = country_info["cities"][selected_city]
    currency_code = country_info["currency"]
    currency_sym = country_info["currency_symbol"]

    # 1. 해외 도시 소개 카드 (신규 추가된 부분)
    st.markdown(f"""
    <div class="city-intro-box">
        <div class="city-intro-badge">🌍 {selected_city} 매력 탐구</div>
        <div class="city-intro-text">{city_info['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 해외 도시 날씨 & 환율 요약
    st.markdown(f"### ⛅ **{selected_city}** 현지 날씨 및 환율 정보")

    col_g_weather, col_g_exchange = st.columns([1, 1])

    with col_g_weather:
        g_weather = get_weather(city_info["lat"], city_info["lon"])
        if g_weather and "weather" in g_weather:
            w_desc = g_weather["weather"][0]["description"]
            w_temp = g_weather["main"]["temp"]
            w_feels = g_weather["main"]["feels_like"]
            w_humidity = g_weather["main"]["humidity"]
            w_id = g_weather["weather"][0]["id"]
            w_icon = g_weather["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{w_icon}@2x.png"
            recommended_outfit = get_outfit_recommendation(w_feels, w_id)

            st.markdown(f"""
            <div class="weather-card">
                <div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
                    <img src="{icon_url}" width="65" height="65" />
                    <div>
                        <span style="font-size:1.5rem; font-weight:bold; color:#e76f51;">{w_temp:.1f}°C</span>
                        <span style="color:#555; font-size:1rem; margin-left:8px;">({w_desc})</span><br>
                        <span style="color:#666; font-size:0.92rem;">체감온도 {w_feels:.1f}°C | 습도 {w_humidity}%</span>
                    </div>
                </div>
                <div class="outfit-box">
                    <span style="font-size:1.05rem; font-weight:bold; color:#b05d15;">👒 현지 맞춤 추천 코디</span><br>
                    <span>{recommended_outfit}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("해외 날씨 정보를 불러올 수 없습니다.")

    with col_g_exchange:
        curr_rate = get_krw_rate(all_rates, currency_code)
        
        if curr_rate:
            if currency_code == "JPY":
                rate_text = f"100 JPY = ₩{curr_rate * 100:,.1f} 원"
            elif currency_code == "VND":
                rate_text = f"100 VND = ₩{curr_rate * 100:,.2f} 원"
            elif currency_code == "HUF":
                rate_text = f"100 HUF = ₩{curr_rate * 100:,.1f} 원"
            else:
                rate_text = f"1 {currency_code} = ₩{curr_rate:,.1f} 원"
        else:
            rate_text = "환율 정보를 불러올 수 없습니다."

        st.markdown(f"""
        <div class="detail-card">
            <div class="place-main-title">💱 {selected_country} 환율 안내</div>
            <div class="place-badge">통화 코드: {currency_code} ({currency_sym})</div>
            <div class="info-line">
                <div class="exchange-highlight-box">
                    <span class="exchange-big-val">💰 현재 환율: {rate_text}</span>
                    <span style="color:#4b5563; font-size:0.92rem;">
                        ※ 사이드바의 환율 계산기에서 원하는 금액을 직접 변환할 수 있습니다.
                    </span>
                </div>
                🧭 <b>도시 중심 좌표:</b> 위도 {city_info['lat']:.4f}, 경도 {city_info['lon']:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. 필수 주요 관광지 & 대표 로컬 맛집 3곳
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 🏛️ {selected_city}에서 꼭 가봐야 할 주요 명소")
    spot_cols = st.columns(len(city_info["spots"]))
    for i, spot in enumerate(city_info["spots"]):
        with spot_cols[i]:
            st.markdown(f"""
            <div style="background:#fff; border-radius:18px; border:3px solid #64dfdf; padding:14px; text-align:center; box-shadow:0 4px 0 #48bfe3;">
                <span style="font-size:1.2rem;">📍</span><br>
                <b style="color:#0077b6; font-size:1.05rem;">{spot}</b>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 🍴 {selected_city} 현지 인기 대표 맛집 BEST 3")
    r_cols = st.columns(3)
    for i, rest in enumerate(city_info["restaurants"]):
        with r_cols[i]:
            st.markdown(f"""
            <div class="restaurant-card">
                <div>
                    <div class="restaurant-title">🍽️ {rest['name']}</div>
                    <span class="restaurant-dist">{rest['cat']}</span>
                    <div style="font-size:0.95rem; color:#4a3e35; margin-top:8px; line-height:1.5;">
                        {rest['desc']}
                    </div>
                </div>
                <a href="{rest['url']}" target="_blank" class="kakao-map-btn" style="margin-top:12px; padding:6px 12px; font-size:0.95rem; text-align:center; background:#48bfe3; color:#fff !important; box-shadow:0 4px 0 #0077b6;">
                    구글 지도에서 위치 보기
                </a>
            </div>
            """, unsafe_allow_html=True)

    # 4. 일정표 자동 생성 및 1/N 고정비 분할 예산 계산기
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 🗓️ {selected_city} 여행 일정표 및 예산 계산기")

    col_plan_input, col_budget_view = st.columns([1, 1])

    with col_plan_input:
        st.markdown("#### 1️⃣ 여행 조건 설정")
        days_option = st.selectbox(
            "몇박 며칠 일정인가요?",
            ["2박 3일", "3박 4일", "4박 5일", "5박 6일", "6박 7일"],
            index=1
        )
        people_count = st.number_input("여행 인원수 (명)", min_value=1, max_value=20, value=2, step=1)
        
        travel_style = st.radio(
            "여행 스타일을 선택하세요:",
            ["🌱 알뜰 배낭 (가성비 중심)", "✨ 스탠다드 (일반적인 힐링)", "👑 럭셔리 (호텔 & 파인다이닝)"],
            index=1
        )

        tokens = days_option.split()
        num_nights = int(tokens[0].replace("박", ""))
        num_days = int(tokens[1].replace("일", ""))

        dest_factor = 0.55 if "베트남" in selected_country else (1.3 if "스위스" in selected_country or "영국" in selected_country else 1.0)

        if "알뜰" in travel_style:
            nightly_room_cost = 80000 * dest_factor
            daily_food_per_person = 45000 * dest_factor
            daily_shared_transport = 20000 * dest_factor
            flight_cost = int(country_info["flight_base"] * 0.9)
        elif "럭셔리" in travel_style:
            nightly_room_cost = 550000 * dest_factor
            daily_food_per_person = 220000 * dest_factor
            daily_shared_transport = 150000 * dest_factor
            flight_cost = int(country_info["flight_base"] * 1.35)
        else:
            nightly_room_cost = 200000 * dest_factor
            daily_food_per_person = 85000 * dest_factor
            daily_shared_transport = 50000 * dest_factor
            flight_cost = country_info["flight_base"]

        rooms_needed = (people_count + 1) // 2
        total_lodging_cost = nightly_room_cost * rooms_needed * num_nights
        total_shared_transport = daily_shared_transport * num_days

        shared_total = total_lodging_cost + total_shared_transport
        shared_per_person = shared_total / people_count
        personal_variable = flight_cost + (daily_food_per_person * num_days)

        cost_per_person = int(personal_variable + shared_per_person)
        total_cost = int(cost_per_person * people_count)

        foreign_per_person = cost_per_person / (curr_rate or 1.0)
        foreign_total = total_cost / (curr_rate or 1.0)

    with col_budget_view:
        st.markdown("#### 💰 1/N 고정비 분할 예상 경비 산출")

        st.markdown(f"""
        <div class="weather-card" style="border-color:#57cc99; box-shadow:0 6px 0 #38a3a5;">
            <div style="font-size:1.05rem; color:#1b4332; margin-bottom:8px;">
                👥 <b>{selected_city} | {days_option} ({people_count}명)</b><br>
                <span style="font-size:0.9rem; color:#2d6a4f;">{travel_style} 기준 (방 {rooms_needed}개 사용)</span>
            </div>
            <div style="font-size:1.45rem; font-weight:bold; color:#0077b6;">
                1인당 예상 경비: ₩{cost_per_person:,.0f} 원
            </div>
            <span style="color:#555; font-size:0.92rem;">
                (현지 통화 약 {foreign_per_person:,.0f} {currency_sym})
            </span>
            <hr style="margin:10px 0;">
            <div style="font-size:1.65rem; font-weight:bold; color:#e76f51;">
                {people_count}인 총 여행 경비: ₩{total_cost:,.0f} 원
            </div>
            <span style="color:#555; font-size:0.95rem;">
                (현지 통화 약 {foreign_total:,.0f} {currency_sym})
            </span>
            <div class="outfit-box" style="margin-top:12px; font-size:0.86rem; line-height:1.6;">
                💡 <b>예산 분할 안내:</b><br>
                총 숙소비(₩{total_lodging_cost:,.0f})와 공동 교통비(₩{total_shared_transport:,.0f})를 {people_count}명이 1/N으로 나누어 부담하므로 인원수가 많아질수록 1인당 고정비 부담이 절감됩니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. 일차별 추천 일정표 생성
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"#### 📋 {selected_city} {days_option} 맞춤 추천 일정표")

    spots = city_info["spots"]
    rests = city_info["restaurants"]

    schedule_data = []
    for day in range(1, num_days + 1):
        if day == 1:
            plan = f"공항 도착 및 숙소 체크인 ➡️ {spots[0]} 산책 및 구경 ➡️ 저녁 식사 ({rests[0]['name']})"
        elif day == num_days:
            plan = f"호텔 체크아웃 및 기념품 쇼핑 ➡️ {rests[1 % len(rests)]['name']}에서 점심 ➡️ 공항 이동 및 귀국"
        else:
            spot_idx = (day - 1) % len(spots)
            rest_idx = (day) % len(rests)
            plan = f"오전 투어 ({spots[spot_idx]}) ➡️ 점심 식사 ➡️ 오후 투어 ({spots[(spot_idx + 1) % len(spots)]}) ➡️ {rests[rest_idx]['name']} 디너 & 야경 투어"

        schedule_data.append({"일차": f"Day {day}", "상세 추천 코스 및 활동": plan})

    st.table(schedule_data)

    # 6. 도시 위치 지도 출력
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"#### 🗺️ **{selected_city}** 글로벌 지도")
    st.map([{"lat": city_info["lat"], "lon": city_info["lon"]}], zoom=12, use_container_width=True)