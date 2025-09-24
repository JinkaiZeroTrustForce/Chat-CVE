from flask import Flask, render_template, request
import requests,jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("start.html")

@app.route("/sendLang", methods=["POST"])
def sendLang():#バックにurlで送る
        language = request.form.get("language")
        
        url="http://localhost:5000/receive"#仮、5173
        #url="http://localhost:3000/generate_question" #バック送信URL
        params = {"language": language}
        #print(params)
    
        #response = requests.post(url, params=params)
        return render_template("/input.html")#画面遷移


@app.route("/receive", methods=["GET","POST"])#sendのあと向こうがreceiveに送ってくるはずなので受け取ってinput.html表示
def receive():
    #data = request.get_json()
    #------------------------------------------------------------------------------------------------
    data= {
    "level": 1,
    "language": "php",
    "source code": "```php\n<?php\nif ($_SERVER['REQUEST_METHOD'] === 'POST') {\n    $username = $_POST['username'];\n    $password = $_POST['password'];\n    if ($username === 'admin' && $password === 'pass123') {\n        echo \"Welcome admin!\";\n    } else {\n        echo \"Invalid credentials.\";\n    }\n}\n?>\n<form method=\"post\">\n  Username: <input name=\"username\"><br>\n  Password: <input name=\"password\" type=\"password\"><br>\n  <input type=\"submit\" value=\"Login\">\n</form>\n```",
    "answer": "$password === 'pass123'",
    "explanation": "パスワードがコード内にハードコードされており、ソースコード漏洩やリバースエンジニアリングによって簡単に特定される。環境変数や安全な認証システムを利用すべき。"}
    
    level = data.get("level")
    question = data.get("source code")
    answer = data.get("answer")
    explanation = data.get("explanation")
    #------------------------------------回答と説明をansewerに送信------------------------------------------------------------
    url="http://localhost:5000/answer"
    
    params = {"answer": answer,"explanation": explanation}
    response = requests.post(url, params=params)#answerに送信

    return render_template("/input.html",level=level,question=question)

@app.route("/input", methods=["GET","POST"])
def input():#入力された情報をバックに送る、

    input1 = request.form['where']
    input2 = request.form['why']

    if(input1 and input2):
        url="http://localhost:5000/debug"
        #url="http://localhost:3000/generate_question" #バック送信URL

        params = {"where": input1,"why":input2}
        response = requests.post(url, params=params)#jsonで送りたいよね
    return render_template("/answer.html",where=input1, why=input2)#デバッグ用だからいらん
    #return ""#本来はこれ


@app.route("/debug", methods=["GET","POST"])#デバッグ用
def debug():


    return ""

@app.route("/answer", methods=["GET","POST"])#回答、
def answer():


    return ""


if __name__ == "__main__":
     app.run(debug=True)
                                  