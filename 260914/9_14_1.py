import os
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

# 현재 파일 기준 상위 폴더의 .env 파일 정확히 지정
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / ".env"

load_dotenv(ENV_PATH)
# REST API 키 환경변수명으로 변경
KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")

st.set_page_config(layout="wide")
st.title("서울 주요 명소 지도 (Kakao Map)")

# 키 로딩 상태 화면에 직접 표시
if not KAKAO_KEY:
    st.error(f"❌ .env 파일을 찾지 못했거나 KAKAO_REST_API_KEY가 비어 있습니다. 탐색 경로: {ENV_PATH}")
    st.stop()
else:
    st.success(f"🔑 REST API 키 로드 성공 (앞 6자리): {KAKAO_KEY[:6]}******")

places = [
    {"name": "남산서울타워", "lat": 37.551169, "lng": 126.988227},
    {"name": "경복궁", "lat": 37.579617, "lng": 126.977041},
    {"name": "석촌호수", "lat": 37.509134, "lng": 127.103318},
    {"name": "강남역", "lat": 37.497952, "lng": 127.027619}
]

center_lat = places[1]["lat"]
center_lng = places[1]["lng"]
places_json = json.dumps(places, ensure_ascii=False)

# 주의: 카카오 JS SDK는 JavaScript 키 전용입니다.
# REST API 키 입력 시 백엔드 인증 오류(카카오 도메인 불일치 등)가 발생할 수 있습니다.
kakao_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; }}
        #map {{ width: 100%; height: 550px; background-color: #f0f0f0; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var script = document.createElement('script');
        script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_KEY}&autoload=false";
        document.head.appendChild(script);

        script.onload = function() {{
            kakao.maps.load(function() {{
                var mapContainer = document.getElementById('map');
                var mapOptions = {{
                    center: new kakao.maps.LatLng({center_lat}, {center_lng}),
                    level: 8
                }};
                var map = new kakao.maps.Map(mapContainer, mapOptions);

                var data = {places_json};
                data.forEach(function(item) {{
                    var markerPosition = new kakao.maps.LatLng(item.lat, item.lng);
                    var marker = new kakao.maps.Marker({{
                        position: markerPosition,
                        map: map
                    }});

                    var infowindow = new kakao.maps.InfoWindow({{
                        content: '<div style="padding:5px;font-size:12px;text-align:center;">' + item.name + '</div>'
                    }});
                    infowindow.open(map, marker);
                }});
            }});
        }};
    </script>
</body>
</html>
"""

components.html(kakao_html, height=580)