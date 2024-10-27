import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from utils import get_current_time
import os
import json

# .env 파일에서 환경 변수 로드
# load_dotenv()
openai_api_key = st.secrets["OPENAI_API_KEY"]



# OpenAI 클라이언트 초기화
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=openai_api_key)

st.title("프롬프트 테스트 도구")

# 사이드바에 설정 추가
with st.sidebar:
    st.markdown("### 설정")
    max_tokens = st.slider("최대 토큰 수:", min_value=50, max_value=500, value=200, step=50)
    repeat_count = st.number_input("반복 횟수:", min_value=1, max_value=100, value=1, step=1)
    temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    top_p = st.slider("Top P:", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    model = st.selectbox("LLM 모델:", ["gpt-4o", "gpt-4o-mini"])

# 시스템 프롬프트 입력
system_prompt = st.text_area("시스템 프롬프트를 입력하세요:", height=200)
system_prompt = system_prompt.replace("{nowDateTime}", get_current_time())

# 사용자 입력
user_query = st.text_area("프롬프트를 입력하세요:", height=200)

if st.button("테스트"):
    if user_query and system_prompt:
        try:
            results = []
            for i in range(repeat_count):
                st.subheader(f"반복 {i+1}")
                # OpenAI API 호출
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
                
                # 응답 출력
                result = response.choices[0].message.content
                st.write(result)
                st.write("---")  # 각 반복 사이에 구분선 추가
                
                # 결과를 리스트에 추가
                results.append({
                    "iteration": i+1,
                    "result": result
                })

            # JSON 다운로드 링크 추가
            json_results = json.dumps(results, ensure_ascii=False, indent=2)
            st.download_button(
                label="JSON으로 결과 다운로드",
                data=json_results,
                file_name="test_results.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
    else:
        st.warning("프롬프트와 시스템 프롬프트를 모두 입력해주세요.")
