# OpenAI + streamlit 앱
# 질문 하나 입력하면 OpenAI chat Completions API 한 번 호출
# 답변을 받아오는 가장 단순한 방법
# 대화 기록을 기억하지 않는 단발성 질문 - 답변
# streamlit run 9_11_2.py


import streamlit as st
from openai import OpenAI
st.set_page_config(page_title="나의 첫번째 챗봇", page_icon="🪅")
st.title("예제1) 나의 첫번째 챗봇")
st.caption("질문 하나 입력하면 OpenAI chat Completions API 한번 호출, 답변을 받아오는 가장 단순한 방식")

# ---------------사이드바 Api 모델--------------

with st.sidebar:
        st.header: ("설정")
        api_key = st.text_input("OpenAI API Key", type="password", help="sk- 로 시작하는 OpenAI API Key로 입력하세요.")
        model = st.selectbox("모델 선택", ["gpt-4o-mini","gpt-4.1-mini"], index=0, help='사용할 모델을 선택하세요.')
        st.markdown("[api 발급 받기](https://platform.openai.com/api-keys)")


#--------------------메인 화면-----------------

question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 환율 알려줘.")

if st.button("질문하기", type="primary"):
    if not api_key:
        st.error("OpenAI API Key를 입력하세요.")
    elif not question:
        st.error("질문을 입력하세요.")
    else:
        try:
            # OpenAI 클라이언트 초기화
            client = OpenAI(api_key=api_key)
            
            # "답변을 생각하는 중.." 로딩 스피너 적용
            with st.spinner("주인님의 질문에 답변을 생각하는 중입니다..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        # "주인님으로 시작하는 친절한 답변가" 프롬프트 설정
                        {"role": "system", "content": "너는 매우 친절하고 예의 바른 인공지능 비서야. 모든 답변은 항상 '주인님, '으로 시작해야 해."},
                        {"role": "user", "content": question}
                    ]
                )
            
            # 1. 답변 출력
            answer = response.choices[0].message.content
            st.success("답변이 완료되었습니다!")
            st.write(answer)
            
            st.divider()
            
            # 2. 토큰 사용량 표시 (비용 감 파악용)
            usage = response.usage
            st.subheader("📊 사용한 토큰 정보")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("입력 토큰 (Prompt)", f"{usage.prompt_tokens} 개")
            col2.metric("출력 토큰 (Completion)", f"{usage.completion_tokens} 개")
            col3.metric("총 토큰 (Total)", f"{usage.total_tokens} 개")

        except Exception as e:
            # 오류 메시지 출력
            st.error(f"오류가 발생했습니다: {e}")