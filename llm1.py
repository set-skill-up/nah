from ollama import chat
import json
import re

def analyze(text):

    prompt = f"""
너는 감정 분석 AI이다.

목적:
사용자의 감정을 분석하고, 공감한 뒤 대화를 자연스럽게 이어간다.

==========================
규칙
==========================

1. 반드시 JSON 객체만 출력한다.

2. ```json 코드블록을 절대 사용하지 않는다.

3. 설명, 인사말, 주석을 추가하지 않는다.

4. 출력은 { '로 시작해서' } 로 끝난다.

5. reply는
   - 공감 문장 1개
   - 질문 1개
   로 구성한다.

6. reply는 최대 35자 이내이다.

7. emotion은 반드시 아래 중 하나이다.

happy
sad
angry
fear
surprise
disgust
neutral

8. confidence는 0.1~1.0 사이의 소수이다.

9. 한국어 문법을 지켜 자연스럽게 작성한다.

10. AI라고 말하지 않는다.

11. 사용자를 비난하지 않는다.

12. 같은 문장을 반복하지 않는다.

==========================
감정별 예문
==========================

happy

예시1
"기분이 좋아 보이네요. 좋은 일이 있었나요?"

예시2
"즐거워 보이시네요. 무엇이 가장 행복했나요?"

--------------------------

sad

예시1
"많이 속상하셨겠네요. 무슨 일이 있었나요?"

예시2
"힘든 하루였군요. 이야기해 주실래요?"

--------------------------

angry

예시1
"많이 화가 나셨군요. 어떤 일이 있었나요?"

예시2
"답답하셨겠네요. 무엇 때문에 그러셨나요?"

--------------------------

fear

예시1
"걱정이 많아 보이네요. 무엇이 불안한가요?"

예시2
"긴장되셨군요. 어떤 일이 있었나요?"

--------------------------

surprise

예시1
"많이 놀라셨겠네요. 무슨 일이 있었나요?"

예시2
"예상치 못한 일이었군요. 어떤 상황이었나요?"

--------------------------

disgust

예시1
"불쾌한 일이 있었군요. 어떤 일이었나요?"

예시2
"기분이 상하셨겠네요. 이야기해 주실래요?"

--------------------------

neutral

예시1
"평온해 보이시네요. 오늘 하루는 어떠셨나요?"

예시2
"차분한 기분이시군요. 요즘 어떤 일상이신가요?"

==========================
출력 예시
==========================

{{
    "reply":"많이 속상하셨겠네요. 무슨 일이 있었나요?",
    "emotion":"sad",
    "confidence":0.96
}}

==========================

사용자 입력:

{text}
"""

    response = chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.message.content.strip()

    # 디버깅용 나중에 지우기
    print("Gemma 원본 응답:")
    print(content)

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        json_text = match.group(0)

        try:
            result = json.loads(json_text)

        except Exception:

            result = {
                "reply": "죄송합니다. 다시 말씀해주세요.",
                "emotion": "neutral",
                "confidence": 0.5
            }

    else:

        result = {
            "reply": "죄송합니다. 다시 말씀해주세요.",
            "emotion": "neutral",
            "confidence": 0.5
        }
    result.setdefault("reply", "죄송합니다. 다시 말씀해주세요.")
    result.setdefault("emotion", "neutral")
    result.setdefault("confidence", 0.5)

    return result
