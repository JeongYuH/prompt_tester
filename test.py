import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from utils import read_file, get_current_time
import os
import json

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("프롬프트 테스트 도구")

# 사용자 입력
user_query = st.text_area("프롬프트를 입력하세요:", height=200)
max_tokens = st.slider("최대 토큰 수:", min_value=50, max_value=500, value=200, step=50)

# 파일에서 프롬프트 읽기
prompt = read_file(f"{os.getcwd()}/prompt_tester/prompt/upgrade_query.md")
prompt = prompt.replace("{nowDateTime}", get_current_time())

if st.button("테스트"):
    if user_query:
        try:
            # 함수 정의 수정
            functions = [
                {
                    "name": "process_user_query",
                    "description": "사용자 쿼리를 처리하고 일정 정보를 추출합니다.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "schedules": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "date": {
                                            "type": "string",
                                            "description": "일정 날짜 및 기간"
                                        },
                                        "time": {
                                            "type": "string",
                                            "description": "일정 시간"
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "일정 설명"
                                        },
                                        "alarm": {
                                            "type": "string",
                                            "description": "알람 설정"
                                        }
                                    },
                                    "required": ["date", "time", "description"]
                                }
                            }
                        },
                        "required": ["schedules"]
                    }
                }
            ]

            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_query}
                ],
                functions=functions,
                function_call={"name": "process_user_query"},
                max_tokens=max_tokens
            )
            
            # 함수 호출 결과 추출
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "process_user_query":
                result = json.loads(function_call.arguments)
                st.subheader("AI 응답:")
                for schedule in result["schedules"]:
                    st.write(f"날짜: {schedule['date']}")
                    st.write(f"시간: {schedule['time']}")
                    st.write(f"설명: {schedule['description']}")
                    if 'alarm' in schedule:
                        st.write(f"알람: {schedule['alarm']}")
                    st.write("---")
            else:
                st.warning("예상치 못한 응답 형식입니다.")

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
    else:
        st.warning("프롬프트를 입력해주세요.")

st.sidebar.markdown("### 사용 방법")
st.sidebar.markdown("1. 프롬프트를 입력하세요.")
st.sidebar.markdown("2. 최대 토큰 수를 조정하세요.")
st.sidebar.markdown("3. '테스트' 버튼을 클릭하세요.")