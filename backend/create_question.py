import os

import dotenv
from openai import OpenAI


def chat_with_gpt(system_prompt: str, prompt: str) -> str:
    dotenv.load_dotenv()

    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    text = (
        response.choices[0].message.content.strip()
        if response.choices[0].message.content is not None
        else ""
    )
    return text


def create_questions(language: str):
    #　プロンプトが確定次第追加
    user_prompt = ""
    system_prompt = ""
    questions = chat_with_gpt(system_prompt, user_prompt)
    return questions


def evaluate_result(evaluation_request):
    #　プロンプトが確定次第追加
    user_prompt = ""
    system_prompt = ""
    eval = chat_with_gpt(system_prompt, user_prompt)

    return eval
