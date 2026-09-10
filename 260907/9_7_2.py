"""
k-pop 아이돌데이터셋 기초 탐색
pandas head/tail/shape/info/columns를 사용해서 데이터 화면 에 순서대로 보여주는 streamlit 앱이다.
실행방법 streamlit run 9_7_2.py
"""
# 내가 한 것
import io
import pandas as pd
import streamlit as st


CSV_PATH = "kpopidol.csv"

st.title("💃K-POP IDOL 데이터셋 기초 탐색🕺")
st.caption("pandas의 head/tail/info/columns로 데이터셋 기본 정보를 확인합니다.")

uploade_file = st. file_uploader("kpopidol_csv 파일을 직접 업로드 할 수 있습니다.(선택사항)", type="csv")

if uploade_file is not None : 
    df = pd.read_csv(uploade_file)
else :
    try :

        df = pd.read_csv(CSV_PATH)

    except FileNotFoundError :
        st.error("❌파일을 찾을 수 없습니다.")
        st.info("같은 경로에 파일을 업로드 하거나 csv파일을 폴더에 넣고 새로고침 하세요.")
        df = None 


if df is not None : 
    st.subheader("1) head() : 데이터의 앞 부분 5개 행 미리보기")
    st.dataframe(df.head(), use_container_width=True) # 기본행 5개

    st.subheader("2) tail() : 데이터의 앞 부분 5개 행 미리보기")
    st.dataframe(df.tail(), use_container_width=True) # 기본행 5개

    st.subheader("3) shape() : 행 개수, 열 개수")
    col1, col2 = st.columns(2)
    with col1 : 
        st.metric("행 개수", f"{df.shape[0]}개")
    with col2 : 
        st.metric("열 개수", f"{df.shape[1]}개")

    st.subheader("4) columns : 전체 열 (컬럼) 이름 목록")

    st.write(list(df.columns))

    st.subheader("5) info() : 각 열의 자료형과 결측치(NaN) 여부 요약")


    info_df = pd.DataFrame({
        "타입" : df.dtypes,
        "결측치 아닌 개수" : df.notna().sum(),
        "결측치 개수" : df.isna().sum(),
    })
    st.dataframe(info_df, use_container_width=True)