import streamlit as st
import pandas as pd
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="예제 3 - 문서 요약 앱", page_icon="📄")

# --------------- 사이드바 (설정 & 요약 옵션) ---------------
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="sk- 로 시작하는 OpenAI API Key를 입력하세요.")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0, help="사용할 모델을 선택하세요.")
    
    st.divider()
    
    st.header("요약 옵션")
    summary_length = st.radio(
        "요약 길이",
        ["짧게 (3줄)", "보통 (5~7줄)", "자세히 (bullet point)"],
        index=0
    )
    
    summary_style = st.selectbox(
        "요약 스타일",
        ["일반", "친절하게", "비즈니스 보고서풍", "초등학생도 이해하기 쉽게"],
        index=0
    )

# -------------------- 메인 화면 --------------------
st.title("📄 예제 3: 파일 업로드 문서 요약 앱")
st.caption("텍스트 파일이나 CSV 파일을 업로드하면 OpenAI API가 원하는 스타일로 요약해줍니다.")

# 1. 파일 업로드 (csv, txt, md 지원)
uploaded_file = st.file_uploader("요약할 파일(CSV, TXT)을 업로드하세요", type=["csv", "txt", "md"])

if uploaded_file is not None:
    file_contents = ""
    file_type = uploaded_file.name.split(".")[-1].lower()

    # 파일 확장자에 따른 처리
    if file_type == "csv":
        try:
            df = pd.read_csv(uploaded_file)
            file_contents = df.to_csv(index=False)
            
            st.subheader("업로드한 문서 미리보기")
            with st.expander("CSV 데이터 테이블 미리보기", expanded=True):
                st.dataframe(df.head(10))  # 상위 10개 행 표시
        except Exception as e:
            st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    else:
        # TXT / MD 파일 처리
        file_contents = uploaded_file.read().decode("utf-8")
        st.subheader("업로드한 문서 미리보기")
        with st.expander("원문 (앞부분)", expanded=True):
            st.text_area("파일 내용", value=file_contents, height=150, disabled=True, label_visibility="collapsed")

    # 2. 요약하기 버튼
    if file_contents:
        if st.button("요약하기", type="primary"):
            if not api_key:
                st.warning("사이드바에 OpenAI API Key를 먼저 입력해주세요.")
            else:
                try:
                    client = OpenAI(api_key=api_key)
                    
                    # 프롬프트 구성
                    system_prompt = f"""
                    너는 전문 문서 및 데이터 요약 AI이다.
                    제시된 파일의 핵심 내용을 분석하고 다음 조건에 맞춰 요약해라:
                    - 요약 길이: {summary_length}
                    - 요약 스타일: {summary_style}
                    """
                    
                    with st.spinner("파일을 읽고 요약하는 중입니다..."):
                        response = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": f"다음 내용을 요약해줘:\n\n{file_contents}"}
                            ]
                        )
                    
                    # 요약 결과 출력
                    summary_result = response.choices[0].message.content
                    st.subheader("📝 요약 결과")
                    st.success("요약이 완료되었습니다!")
                    st.markdown(summary_result)
                    
                    st.divider()
                    
                    # 토큰 사용량 정보
                    usage = response.usage
                    st.subheader("📊 사용한 토큰 정보")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("입력 토큰", f"{usage.prompt_tokens} 개")
                    col2.metric("출력 토큰", f"{usage.completion_tokens} 개")
                    col3.metric("총 토큰", f"{usage.total_tokens} 개")

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")