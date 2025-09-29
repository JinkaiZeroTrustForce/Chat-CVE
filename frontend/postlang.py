from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

global_questions = []
global_index = 0
user_answers = []

@app.route("/")
def index():
    return render_template("start.html")

@app.route("/sendLang", methods=["POST"])
def sendLang():
    global global_questions, global_index, user_answers
    language = request.form.get("language")
    url = "http://localhost:5173/generate_question"
    params = {"language": language}
    response = requests.post(url, params=params)
    global_questions = response.json()
    global_index = 0
    user_answers = []
    # 最初の問題へ進む（GETで）
    return redirect(url_for('next_question'))

@app.route("/next_question", methods=["GET"])
def next_question():
    global global_questions, global_index
    if global_index >= len(global_questions):
        return redirect(url_for('log'))
    res = global_questions[global_index]
    level = res.get("level")
    question = res.get("source_code", "")
    # 回答前なので answer/explanation なし
    return render_template(
        "/input.html",
        level=level, question=question,
        answer="", explanation="", 
        show_answer=False, 
        total_score="", feeback=""
    )

@app.route("/input", methods=["GET", "POST"])
def input():
    global global_questions, global_index, user_answers

    if request.method == "POST":
        # 回答情報取得
        input1 = request.form.get('where')
        input2 = request.form.get('why')
        level = request.form.get("level")
        question = request.form.get("question")

        # 現在の問題取得＆保存
        res = global_questions[global_index]
        answer = res.get("answer", "")
        explanation = res.get("explanation", "")

        user_answers.append({
            "where": input1, "why": input2,
            "level": level, "question": question
        })

        global_index += 1

        # 模範解答の表示＋「次へ」ボタン
        return render_template(
            "/input.html",
            level=level, question=question,
            answer=answer, explanation=explanation,
            show_answer=True, total_score="", feeback=""
        )
    # GETの場合は次の問題へ
    return redirect(url_for('next_question'))

@app.route("/log", methods=["GET"])
def log():
    global user_answers
    return render_template("/log.html", user_answers=user_answers)

if __name__ == "__main__":
    app.run(debug=True)