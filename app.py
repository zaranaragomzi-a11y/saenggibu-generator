import streamlit as st
import openai
from prompt import BASE_PROMPT
from utils import extract_text_from_pdf
import os

st.set_page_config(page_title="세특 생성기", layout="wide")
st.title("📘 세특 초안 자동 생성기")

# 🔑 OpenAI Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 1. 파일 업로드
uploaded_file = st.file_uploader(
    "보고서 파일 업로드 (PDF)", type=["pdf"]
)

# 2. 옵션
subject = st.selectbox("과목", ["화학", "물리", "생명과학", "지구과학", "기타"])
byte_limit = st.selectbox("글자 수 제한", [100, 200, 300])

# 3. 추가 프롬프트
extra_prompt = st.text_area(
    "추가 요청사항 (선택)",
    placeholder="예: 탐구 과정 중심으로, 진로 연계 강조"
)

# 4. 실행
if st.button("세특 생성"):
    if not uploaded_file:
        st.warning("파일을 업로드하세요.")
    else:
        with st.spinner("분석 중..."):
            text = extract_text_from_pdf(uploaded_file)

            final_prompt = f"""
{BASE_PROMPT.format(subject=subject, byte_limit=byte_limit)}

[추가 요청사항]
{extra_prompt}

[학생 보고서 내용]
{text}
"""

            response = openai.ChatCompletion.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": final_prompt}],
                temperature=0.3
            )

            result = response.choices[0].message.content
            st.subheader("📄 생성된 세특")
            st.text_area("", result, height=200)
