# 인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩("utf_8_sig", "cp949", "euc_kr") 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실 등급별 생존율 막대그래프 생성 후 그림으로 저장  chart.png
# 실행 streamlit run 9_7_4.py

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager as fm

st.title("인코딩 자동 감지 + 한글 폰트 막대 그래프(Titanic 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실 등급별 생존율을 표로 확인합니다.")

CSV_PATH = os.path.join(os.path.dirname(__file__), "Titanic_cleaned.csv")
FONT_PATH = os.path.join(os.path.dirname(__file__), "font1.ttf")

def read_csv_with_auto_encoding(file_path):
    encodings = ["utf_8_sig", "cp949", "euc_kr"]
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            # 어떤 인코딩으로 읽었는지 화면에 알림 추가
            st.success(f"'{enc}' 인코딩으로 파일을 성공적으로 읽었습니다.")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise e
    raise ValueError(f"모든 인코딩({encodings})으로 파일을 읽는 데 실패했습니다: {file_path}")

# 한글 폰트 설정
if os.path.exists(FONT_PATH):
    font_name = fm.FontProperties(fname=FONT_PATH).get_name()
    plt.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False
else:
    st.warning(f"폰트 파일을 찾을 수 없습니다: {FONT_PATH}")

# 데이터 로드 및 표 생성
try:
    df = read_csv_with_auto_encoding(CSV_PATH)
    
    # 객실 등급별 생존율 계산 및 표 형태로 준비
    if 'Pclass' in df.columns and 'Survived' in df.columns:
        # 소수점 첫째 자리까지만 표시되도록 .round(1) 추가
        survival_rate = (df.groupby('Pclass')['Survived'].mean() * 100).round(1)
        
        # Series를 보기 좋은 DataFrame으로 변환
        survival_df = survival_rate.reset_index()
        survival_df.columns = ['객실 등급 (Pclass)', '생존율 (%)']
        
        st.subheader("📊 객실 등급별 생존율 요약 표")
        # 표(DataFrame)로 화면에 출력
        st.dataframe(survival_df, use_container_width=True)
        
        # 원본 데이터 확인용 미리보기 (선택사항)
        with st.expander("원본 데이터 상위 5행 보기"):
            st.dataframe(df.head())
            
    else:
        st.error("CSV 파일에 'Pclass' 또는 'Survived' 컬럼이 존재하지 않습니다.")
        st.dataframe(df.head())
        
except Exception as e:
    st.error(f"파일 읽기 오류: {e}")

# 차트그리기 - 교수님 (수정된 부분)
st.markdown("---")
st.subheader("3) 객실등급별 생존율 막대그래프")
try:
    font_prop = fm.FontProperties(fname=FONT_PATH)
    fm.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"]=font_prop.get_name()
    st.write("font1.ttf 폰트를 적용했습니다.")
except FileNotFoundError:
    st.warning("폰트 파일을 찾을 수 없습니다.")

pclass_survival_rate = df.groupby('Pclass')['Survived'].mean()
fig, ax = plt.subplots(figsize=(8,5))
(pclass_survival_rate * 100).plot(kind="bar", color="blue", ax=ax)
ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실등급(Pclass)")
ax.set_ylabel("생존율(%)")

st.pyplot(fig)

output_png = os.path.join(os.path.dirname(__file__),"chart.png")
fig.savefig(output_png)
