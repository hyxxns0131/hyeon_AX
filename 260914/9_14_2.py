import http.server
import json
import os
import socketserver
import threading
import urllib.parse
import webbrowser
from pathlib import Path

import requests
from dotenv import load_dotenv

# 1. 상위 폴더의 .env 파일 경로 지정 및 환경 변수 로드
parent_dir = Path(__file__).resolve().parent.parent
env_path = parent_dir / ".env"
load_dotenv(dotenv_path=env_path)

KAKAO_API_KEY = os.getenv("KAKAO_REST_API_KEY")

if not KAKAO_API_KEY:
    raise ValueError(f".env 파일에서 KAKAO_REST_API_KEY를 찾을 수 없습니다. 경로: {env_path}")

PORT = 8765

# 2. 브라우저에 띄울 HTML (내 위치 표시 + 검색창 + 검색 버튼 + 카카오 길찾기/상세보기 연동)
HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>내 위치 중심 지도 및 검색</title>
    <!-- 오픈소스 지도 라이브러리 Leaflet (REST API 키만으로 지도 렌더링 가능) -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif; }}
        body {{ display: flex; flex-direction: column; height: 100vh; overflow: hidden; }}
        header {{
            display: flex;
            gap: 10px;
            padding: 12px 16px;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            z-index: 1000;
        }}
        input[type="text"] {{
            flex: 1;
            padding: 10px 14px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 15px;
            outline: none;
        }}
        input[type="text"]:focus {{
            border-color: #ffe812;
            box-shadow: 0 0 0 2px rgba(255, 232, 18, 0.35);
        }}
        .btn {{
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.15s;
        }}
        .btn-search {{
            background: #fee500;
            color: #191919;
        }}
        .btn-search:hover {{
            background: #ebd100;
        }}
        .btn-location {{
            background: #f1f3f5;
            color: #495057;
        }}
        .btn-location:hover {{
            background: #e9ecef;
        }}
        #container {{
            flex: 1;
            display: flex;
            position: relative;
        }}
        #sidebar {{
            width: 330px;
            background: #ffffff;
            border-right: 1px solid #eee;
            overflow-y: auto;
            display: none;
            z-index: 500;
        }}
        #sidebar.active {{
            display: block;
        }}
        .item {{
            padding: 14px 16px;
            border-bottom: 1px solid #f1f3f5;
            cursor: pointer;
            transition: background 0.15s;
        }}
        .item:hover {{
            background: #f8f9fa;
        }}
        .item-name {{
            font-weight: bold;
            font-size: 15px;
            color: #212529;
            margin-bottom: 4px;
        }}
        .item-addr {{
            font-size: 13px;
            color: #6c757d;
        }}
        #map {{
            flex: 1;
            height: 100%;
        }}
        .info-status {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.78);
            color: #fff;
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 12px;
        }}
    </style>
</head>
<body>

    <header>
        <input type="text" id="keyword" placeholder="장소, 주소, 상호명을 입력하세요 (예: 스타벅스, 시청)" onkeydown="if(event.key==='Enter') doSearch();">
        <button class="btn btn-search" onclick="doSearch()">검색</button>
        <button class="btn btn-location" onclick="moveToMyLocation()">내 위치</button>
    </header>

    <div id="container">
        <div id="sidebar"></div>
        <div id="map"></div>
        <div id="status" class="info-status">위치 확인 중...</div>
    </div>

    <script>
        // 기본 서울 중심 좌표
        let currentLat = 37.5665;
        let currentLng = 126.9780;
        let map;
        let userMarker = null;
        let searchMarkers = [];

        // 지도 생성
        map = L.map('map').setView([currentLat, currentLng], 15);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }}).addTo(map);

        // 1. 브라우저 GPS로 내 위치 잡기
        function moveToMyLocation() {{
            const status = document.getElementById('status');
            status.innerText = "GPS 위치 수신 중...";

            if (!navigator.geolocation) {{
                status.innerText = "현재 브라우저에서 위치 정보를 지원하지 않습니다.";
                return;
            }}

            navigator.geolocation.getCurrentPosition(
                (pos) => {{
                    currentLat = pos.coords.latitude;
                    currentLng = pos.coords.longitude;

                    map.setView([currentLat, currentLng], 15);

                    if (userMarker) map.removeLayer(userMarker);

                    userMarker = L.circleMarker([currentLat, currentLng], {{
                        radius: 8,
                        fillColor: "#0066ff",
                        color: "#ffffff",
                        weight: 3,
                        opacity: 1,
                        fillOpacity: 0.9
                    }}).addTo(map).bindPopup("<b>현재 내 위치</b>").openPopup();

                    status.innerText = "내 위치를 불러왔습니다.";
                    setTimeout(() => {{ status.innerText = ""; }}, 2500);
                }},
                (err) => {{
                    console.warn(err);
                    status.innerText = "위치 접근 권한이 없어 기본 위치(서울)로 설정됩니다.";
                    setTimeout(() => {{ status.innerText = ""; }}, 3000);
                }},
                {{ enableHighAccuracy: true, timeout: 6000 }}
            );
        }}

        // 2. 검색 버튼 클릭 시 실행 함수
        async function doSearch() {{
            const query = document.getElementById('keyword').value.trim();
            if (!query) return;

            const status = document.getElementById('status');
            const sidebar = document.getElementById('sidebar');
            status.innerText = "검색 중...";

            // 파이썬 서버 엔드포인트 호출 (내 위치 좌표 함께 전송)
            const url = `/api/search?query=${{encodeURIComponent(query)}}&lat=${{currentLat}}&lng=${{currentLng}}`;

            try {{
                const res = await fetch(url);
                const data = await res.json();
                const items = data.documents || [];

                // 이전 검색 마커 삭제
                searchMarkers.forEach(m => map.removeLayer(m));
                searchMarkers = [];
                sidebar.innerHTML = "";

                if (items.length === 0) {{
                    sidebar.innerHTML = '<div style="padding: 20px; color: #888;">검색 결과가 없습니다.</div>';
                    sidebar.classList.add('active');
                    status.innerText = "";
                    return;
                }}

                sidebar.classList.add('active');
                const bounds = [];

                items.forEach((place, i) => {{
                    const lat = parseFloat(place.y);
                    const lng = parseFloat(place.x);
                    bounds.push([lat, lng]);

                    // 마커 추가
                    const marker = L.marker([lat, lng]).addTo(map);
                    const popupContent = `
                        <div style="font-size: 13px; line-height: 1.5;">
                            <b>${{place.place_name}}</b><br>
                            ${{place.road_address_name || place.address_name}}<br>
                            <a href="${{place.place_url}}" target="_blank" style="color: #0055ff; text-decoration: underline;">카카오맵 상세/길찾기</a>
                        </div>
                    `;
                    marker.bindPopup(popupContent);
                    searchMarkers.push(marker);

                    // 좌측 목록 아이템 추가
                    const div = document.createElement('div');
                    div.className = 'item';
                    div.innerHTML = `
                        <div class="item-name">${{i + 1}}. ${{place.place_name}}</div>
                        <div class="item-addr">${{place.road_address_name || place.address_name}}</div>
                    `;
                    div.onclick = () => {{
                        map.setView([lat, lng], 17);
                        marker.openPopup();
                    }};
                    sidebar.appendChild(div);
                }});

                if (bounds.length > 0) {{
                    map.fitBounds(bounds, {{ padding: [50, 50] }});
                }}

                status.innerText = `${{items.length}}건의 결과가 표시되었습니다.`;
                setTimeout(() => {{ status.innerText = ""; }}, 2500);

            }} catch (error) {{
                console.error(error);
                status.innerText = "검색 중 오류가 발생했습니다.";
            }}
        }}

        // 페이지 시작 시 위치 잡기
        moveToMyLocation();
    </script>
</body>
</html>
"""


# 3. 파이썬 경량 HTTP 서버 핸들러
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # 메인 페이지 접속 시 HTML 반환
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
            return

        # 검색 요청 처리 (/api/search?query=...&lat=...&lng=...)
        if parsed.path == "/api/search":
            query_params = urllib.parse.parse_qs(parsed.query)
            keyword = query_params.get("query", [""])[0]
            lat = query_params.get("lat", [None])[0]
            lng = query_params.get("lng", [None])[0]

            # 카카오 키워드 장소 검색 REST API 호출
            url = "https://dapi.kakao.com/v2/local/search/keyword.json"
            headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
            params = {"query": keyword}

            # 내 위치 기준 정렬 및 반경 우선 검색
            if lat and lng:
                params["y"] = lat
                params["x"] = lng
                params["radius"] = 10000  # 10km 이내 우선
                params["sort"] = "accuracy"

            res = requests.get(url, headers=headers, params=params)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(res.content)
            return

        # 그 외 요청은 404
        self.send_response(404)
        self.end_headers()


def run_server():
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"로컬 서버 실행 중: http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    # 백그라운드 스레드에서 서버 구동
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 브라우저 실행
    webbrowser.open(f"http://localhost:{PORT}")

    print("서버가 시작되었습니다. 브라우저에서 위치 권한을 허용해주세요.")
    print("종료하려면 터미널에서 Ctrl+C를 누르세요.")

    # 메인 스레드 유지
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")