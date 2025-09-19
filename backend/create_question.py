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
    
    system_prompt = """
    あなたはセキュリティ教育用の問題生成システムです。
受講者は後でこの問題を解き、脆弱性検知スキルを評価されます。

必ず次のルールを守ってください：
- 出力は **純粋なJSON配列文字列**（Markdownコードブロックなし）で返すこと。
- 配列の各要素は以下5項目を必ず含むこと:
  - "level"（1〜5の整数）
  - "language"（使用言語）
  - "source code"（実行可能なプログラムのコードブロッックのmarkdown形式の文字列。```言語\\n...\\n``` 形式）
  - "answer"（脆弱な箇所を具体的に。）
  - "explanation"（原因・攻撃可能性・影響・修正方針を簡潔に）
- "source code" は **おおよそ20行前後（±5行以内）**、かつ**実行可能**な小さなプログラムにすること。
- 一見正常に動くが、どこかにセキュリティ上の問題を潜ませること。
- 脆弱性なし問題を混ぜてもよい（その場合は "answer": "なし" とする）。
- 必ず **有効なJSON** を返し、余計なテキストを一切含めないこと。
"""
    user_prompt = f"""
レベル1〜5をそれぞれ1問ずつ生成してください。
すべての問題の "language" は "{language}" に統一してください。
    """
    questions = chat_with_gpt(system_prompt, user_prompt)
    return questions


def evaluate_result(evaluation_request):
    #　プロンプトが確定次第追加
    system_prompt = """
あなたはセキュリティ教育用の自動採点器です。

入力:
- envaluation_request: 出題時のJSON配列（各要素は "level","language","source code","answer","explanation" を含む）とユーザの回答（"user_answer","user_explanation" を含む）を結合したJSON配列文字列。

採点:
- 各問題のスコア = 位置特定(0〜1)*0.6 + 理由説明(0〜1)*0.4
- 難易度の重み: L1=1.0, L2=1.2, L3=1.4, L4=1.6, L5=1.8
- 最終スコアは100点満点換算
- グレード: 0–39 Beginner, 40–64 Practitioner, 65–84 Advanced, 85–100 Expert

評価の留意点:
- 同義表現は減点しない（例：「テンプレートインジェクション」vs「未エスケープ出力によるXSS」）。
- カテゴリ混同（SQLiをXSSと記述など）は理由説明を大きく減点。
- 「脆弱性なし」の問題に対して脆弱だと主張した場合はスコアを低く（合理的懸念の具体指摘があれば最大0.2まで部分点）。

出力:
- **純粋なJSON** で以下の形式のみを返す（余計なテキスト・Markdown禁止）：
  {
    "total_score": <0〜100の整数>,
    "grade": "Beginner"|"Practitioner"|"Advanced"|"Expert",
    "per_item": [
      {
        "index": <0始まりの整数>,
        "level": "<文字列>",           // FastAPI側スキーマに合わせて文字列で返すこと
        "position_score": <0〜1>,
        "reason_score": <0〜1>,
        "weighted_score": <数値>,
        "feedback": "<短い講評>"
      }
    ],
    "summary": "<全体講評>"
  }
"""
    user_prompt = f"""
evaluation_request:
{evaluation_request}    
    """    
    eval = chat_with_gpt(system_prompt, user_prompt)

    return eval
