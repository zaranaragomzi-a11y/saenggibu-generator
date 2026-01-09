import streamlit as st
from openai import OpenAI

from prompt import BASE_PROMPT
from utils import extract_text_from_pdf


# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="세특 초안 자동 생성기",
    layout="wide"
)

st.title("📘 세특 초안 자동 생성기")
st.caption("※ AI는 초안을 생성하며, 최종 책임은 교사에게 있습니다.")


# =========================
# OpenAI Client 생성
# =========================
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================
# 입력 UI
# =========================
uploaded_file = st.file_uploader(
    "📄 보고서 파일 업로드 (PDF만 지원)",
    type=["pdf"]
)

subject = st.selectbox(
    "과목 선택",
    ["화학", "물리", "생명과학", "지구과학", "기타"]
)

byte_limit = st.selectbox(
    "글자 수 제한 (byte)",
    [500, 750, 1500]
)

extra_prompt = st.text_area(
    "✏️ 추가 요청사항 (선택)",
    placeholder="예: 탐구 과정 중심으로 정리, 진로 연계 강조"
)


# =========================
# 실행 버튼
# =========================
if st.button("🚀 세특 생성"):
    if uploaded_file is None:
        st.warning("PDF 파일을 업로드하세요.")
    else:
        with st.spinner("보고서 분석 및 세특 생성 중..."):
            # 1. PDF → 텍스트 추출
            report_text = extract_text_from_pdf(uploaded_file)

            if not report_text:
                st.error("PDF에서 텍스트를 추출하지 못했습니다.")
            else:
                # 2. 프롬프트 구성
                system_prompt = BASE_PROMPT.format(
                    subject=subject,
                    byte_limit=byte_limit
                )

                final_prompt = f"""
{system_prompt}

[추가 요청사항]
{extra_prompt if extra_prompt else "없음"}

[학생 보고서 내용]
{report_text}
"""

                # 3. OpenAI API 호출 (신버전)
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "user", "content": final_prompt}
                    ],
                    temperature=0.3
                )

                result = response.choices[0].message.content

                # 4. 출력
                st.subheader("📄 생성된 세특 초안")
                st.text_area(
                    label="",
                    value=result,
                    height=220
                )
