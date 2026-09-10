# 구구단 만들기
# 구구단을 외우자!



import streamlit as st

st.title("✨ 구구단 웹 계산기 ✨")
st.write("원하는 단을 선택하거나 입력하면 웹 페이지에 예쁘게 출력됩니다.")

dan = st.number_input("출력할 단을 입력하세요", min_value=1, max_value=9, value=2, step=1)

st.markdown(f"### 📊 [ {dan} 단 ]")

for i in range(1, 10):
    st.write(f"{dan} × {i} = **{dan * i}**")
    