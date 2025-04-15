
import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    # Google Drive 파일 ID
    file_id = "1qLhjML-02cLN6ZU2WU9-bmQ1yNQPmjRo"  # ← 당신의 ID로 바꿔주세요
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # CSV 다운로드 후 데이터프레임으로 변환
    response = requests.get(url)
    csv_raw = StringIO(response.text)
    df = pd.read_csv(csv_raw)
    return df

df = load_data()

st.title("🔍 RMF → ATT&CK → CVE → CCE 검색 앱 (콤보박스 + 시각화 포함)")
st.markdown("RMF ID, CVE, CCE, ATT&CK ID를 선택 또는 검색어 입력으로 조회하고 시각화합니다.")

search_mode = st.radio("🔎 검색 방식 선택", ["직접 검색어 입력", "RMF ID 콤보박스 선택"])
search_term = ""

if search_mode == "직접 검색어 입력":
    search_term = st.text_input("검색어 입력 (예: AC-3, CCE-12345-6, T1087, CVE-2021-1234 등)")
elif search_mode == "RMF ID 콤보박스 선택":
    rmf_ids = sorted(df['RMF ID'].dropna().unique())
    selected_rmf = st.selectbox("📂 RMF ID 선택", rmf_ids)
    search_term = selected_rmf

available_fields = ['RMF ID', 'ATT&CK ID', 'CVE ID', 'CCE ID', 'RMF 설명', 'CVE 설명']
selected_fields = st.multiselect("🔧 검색 범위 선택", available_fields, default=available_fields)

if search_term and selected_fields:
    with st.spinner("검색 중입니다..."):
        filtered = df[df[selected_fields].apply(
            lambda x: x.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.success(f"🔎 총 {len(filtered)}개의 결과가 검색되었습니다.")
        st.dataframe(filtered)

        if 'RMF ID' in filtered.columns:
            rmf_counts = filtered['RMF ID'].value_counts().head(10)
            st.subheader("📊 검색 결과 내 상위 RMF ID별 빈도")
            fig, ax = plt.subplots(figsize=(10, 4))
            rmf_counts.plot(kind='bar', ax=ax)
            ax.set_ylabel("연결된 항목 수")
            ax.set_xlabel("RMF ID")
            st.pyplot(fig)
else:
    st.info("검색어를 입력하거나 RMF ID를 선택하고, 검색 범위를 지정하세요.")
