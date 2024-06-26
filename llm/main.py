import os
import sys
import uuid
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from dotenv import load_dotenv
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
import re



load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")
PROJECT_NAME=os.getenv("PROJECT_NAME")


def get_translation_from_language_to_english(text: str) -> str:
  """
  This function takes a user question and uses Gemini to answer it 
  in the context of Moroccan elections.

  Args:
      text: The user's text as a string.

  Returns:
      The answer generated by Gemini as a string.
  """

  # Specify the Gemini model and API key
  llm = ChatGoogleGenerativeAI(
      model=MODEL_NAME, google_api_key=GEMINI_API_KEY, project=PROJECT_NAME
  )
  text = text.replace(".",",")
  # Craft the prompt template for Gemini
  prompt = f"Translate ALL the following text to English: {text} , Translate ALL text please !"

  # Call Gemini to generate the answer
  result = llm.invoke(prompt)

  # Extract the answer from the response (assuming it's the first sentence)
  answer = result.content.split(".")[0].strip()  # Might need adjustment based on output format

  return answer

if __name__=="__main__":
    resume_text="“النص إلى صوت” هي طريقة تحويل الكتابة (في سبيل المثال في صيغة وورد أو بي دي أف) الى صوت وكأنه قرأها أحد من أهل اللغة. ويستخدم برنامج قراءة أصوات الكمبيوتر لجعل النص صوتًا. Narakeet هو موقع تحويل النص الى صوت عربي ويقدم لكم إمكانية استخدام مركبات صوتية تبدو طبيعية وتشبه الأصوات البشرية."
    print(get_translation_from_language_to_english(resume_text))