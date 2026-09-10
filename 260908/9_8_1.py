# raw_trade_data.csv 파일 활용
# HS 코드가 85로 시작하는 (반도체류) + 국가명 미국 또는 베트남 + 수출금액 0 보다 큰 수(실제 수출 실적이 있는) 행만
# 다중 조건으로 필터링 한 뒤, 수출금액 상위 10건을 화면에 보여주고 report.csv 로 저장
# streamlit 사용 streamlit run 9_8_1.py

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="무역 데이터 분석 대시보드", layout="wide")

st.title("📊 반도체류(HS 85) 대미·대베트남 수출 상위 10건 분석")

# 여러 경로에서 raw_trade_data.csv 파일을 유연하게 탐색합니다.
possible_paths = [
    "raw_trade_data.csv",
    os.path.join("common", "raw_trade_data.csv"),
    os.path.join("..", "common", "raw_trade_data.csv"),
    os.path.join(os.path.dirname(__file__), "raw_trade_data.csv"),
    os.path.join(os.path.dirname(__file__), "..", "common", "raw_trade_data.csv")
]

file_path = None
for path in possible_paths:
    if os.path.exists(path):
        file_path = path
        break

if file_path is None:
    st.error("파일을 찾을 수 없습니다. `raw_trade_data.csv` 경로를 확인해 주세요.")
else:
    # 1. CSV 데이터 로드 (인코딩 문제 방지를 위해 utf-8 / cp949 대응)
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 2. 다중 조건 필터링
    # - HS 코드를 문자열로 변환 후 '85'로 시작하는 행
    # - 국가명이 '미국' 또는 '베트남'
    # - 수출금액이 0보다 큰 행
    # 컬럼 매핑 (대소문자 및 한글/영문 매핑 지원으로 대소문자 불일치 버그 예방)
    hs_col = next((c for c in df.columns if c.lower() in ["hs_code", "hs코드", "hscode"]), "HS_CODE")
    country_col = next((c for c in df.columns if c.lower() in ["국가명", "국가", "country"]), "국가명")
    export_col = next((c for c in df.columns if c.lower() in ["수출금액", "수출액", "export_amount"]), "수출금액")

    cond_hs = df[hs_col].astype(str).str.startswith("85")
    cond_country = df[country_col].isin(["미국", "베트남"])
    cond_amount = pd.to_numeric(df[export_col], errors="coerce") > 0

    filtered_df = df[cond_hs & cond_country & cond_amount].copy()

    # 3. 수출금액 기준 내림차순 정렬 및 상위 10건 추출
    top10_df = (
        filtered_df.sort_values(by=export_col, ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    # 4. report.csv 로 로컬 저장 (스크립트 폴더 내 저장하여 절대/상대 경로 실행 호환, Excel 호환 utf-8-sig)
    report_filename = os.path.join(os.path.dirname(__file__), "report.csv")
    top10_df.to_csv(report_filename, index=False, encoding="utf-8-sig")

    # 5. Streamlit 화면 출력
    st.success(f"필터링 완료: 총 {len(top10_df)}건이 추출되어 `{os.path.basename(report_filename)}`에 저장되었습니다.")
    
    st.subheader("📋 수출금액 상위 10건 내역")
    st.dataframe(top10_df, use_container_width=True)

    # 브라우저 다운로드 버튼 제공 (선택 기능)
    csv_data = top10_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="📥 report.csv 다운로드",
        data=csv_data,
        file_name="report.csv",
        mime="text/csv",
    )