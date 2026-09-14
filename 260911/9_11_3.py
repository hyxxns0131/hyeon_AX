# 대화 기록을 기억하는 멀티턴 챗봇
# st.session_state에 대화 기록을 저장해서, 이전 대화 맥락을 기억하는 챗봇
# st.chat_message / st.chat_input 같은 Streamlit의 채팅 전용 위젯을 사용합니다.
# stream=True 옵션으로 답변이 실시간으로 타이핑되듯 출력됩니다.
# streamlit run 9_11_3.py

# 시스템 메세지를 사용자가 설정 하도록
# 대화기록 초기화 버튼


import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="나의 첫번째 챗봇", page_icon="🪅")
st.title("멀티턴 대화 챗봇 🪅")
st.caption("대화 맥락을 기억하고 실시간 스트리밍으로 답변하는 Streamlit 챗봇입니다.")

# ----------------- 사이드바 설정 -----------------
with st.sidebar:
    st.header("설정")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="sk- 로 시작하는 OpenAI API Key를 입력하세요."
    )
    
    model = st.selectbox(
        "모델 선택",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
        help="사용할 OpenAI 모델을 선택하세요."
    )
    
    # 사용자 정의 시스템 메시지
    system_prompt = st.text_area(
        "시스템 메시지 설정",
        value="너는 친절하고 유능한 인공지능 비서야.",
        help="챗봇의 역할이나 페르소나를 설정할 수 있습니다."
    )
    
    st.markdown("[API 키 발급받기](https://platform.openai.com/api-keys)")
    st.divider()
    
    # 대화 기록 초기화 버튼
    if st.button("대화 내용 초기화", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------------- 세션 상태 초기화 -----------------
# 이전 대화 기록을 기억하기 위한 st.session_state 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------- 이전 대화 출력 -----------------
# 페이지가 다시 로드되어도 기존 메시지를 계속 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------- 채팅 입력 및 처리 -----------------
if prompt := st.chat_input("메시지를 입력해 주세요..."):
    # API 키 체크
    if not api_key:
        st.error("사이드바에 OpenAI API Key를 입력해주세요!")
        st.stop()

    # 1. 사용자 메시지 화면 표시 및 세션 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. OpenAI API 요청 메시지 구성 (시스템 메시지 + 이전 대화 기록)
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # 3. 챗봇 답변 화면 표시 (스트리밍)
    with st.chat_message("assistant"):
        try:
            client = OpenAI(api_key=api_key)
            
            # API 호출 (stream=True 적용)
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                stream=True
            )
            
            # 실시간 타이핑 효과로 응답 출력
            response_content = st.write_stream(stream)
            
            # 4. 챗봇 답변을 세션에 저장
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")