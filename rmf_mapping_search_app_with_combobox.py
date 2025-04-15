
import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

@st.cache_data(ttl=3600)
def load_data():
    file_id = "YOUR_GOOGLE_DRIVE_FILE_ID"  # 🔁 여기를 사용자 파일 ID로 변경
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    csv_raw = StringIO(response.text)
    df = pd.read_csv(csv_raw)
    return df

df = load_data()

st.title("⚡ 빠른 RMF → ATT&CK → CVE → CCE 검색 앱")
st.markdown("최적화된 속도로 RMF 기반 보안 매핑을 검색할 수 있습니다.")
st.write("📋 현재 CSV 컬럼 목록:", df.columns.tolist())

# 단일 검색 대상 선택 (속도 향상)
available_fields = ['RMF ID', 'ATT&CK ID', 'CVE ID', 'CCE ID', 'RMF 설명', 'CVE 설명']
selected_field = st.selectbox("🔧 검색할 항목 선택 (속도 향상)", available_fields)

# 검색어 입력
search_term = st.text_input("🔍 검색어 입력 (예: AC-2, CCE-12345-6, T1087 등)")

# 시각화 여부 선택
show_chart = st.checkbox("📊 결과 차트 표시", value=False)

# 검색 실행
if search_term and selected_field:
    with st.spinner("검색 중입니다..."):
        filtered = df[df[selected_field].astype(str).str.contains(search_term, case=False)]
        row_count = len(filtered)
        if row_count > 1000:
            st.warning("⚠️ 결과가 많아 상위 1000개만 표시됩니다.")
            filtered = filtered.head(1000)
        st.success(f"🔎 {row_count}개의 결과가 검색되었습니다.")
        st.dataframe(filtered)

        if show_chart and 'RMF ID' in filtered.columns:
            rmf_counts = filtered['RMF ID'].value_counts().head(10)
            st.subheader("📊 상위 RMF ID별 빈도")
            fig, ax = plt.subplots(figsize=(10, 4))
            rmf_counts.plot(kind='bar', ax=ax)
            ax.set_ylabel("연결된 항목 수")
            ax.set_xlabel("RMF ID")
            st.pyplot(fig)
else:
    st.info("검색어와 항목을 선택하세요.")
