from google import genai
from dotenv import load_dotenv
import os
GEMINI_API_KEY = "API키 넣는곳;P"

client = genai.Client(
    api_key=GEMINI_API_KEY
)
def analyze(text):

  prompt = f"""
너는 감정 분석 AI이다.

반드시 아래 JSON형식으로만 답해.

{{
"reply":"",
"emotion":"",
"confidence":0.0
}}
사용자 입력:
{text}
"""
  response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = prompt
  )
  return response.text
while True:
    text = input("나 : ")

    if text == "exit":
        break

    print("AI :", analyze(text))
