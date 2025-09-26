from flask import Flask, render_template, request
import requests,jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("start.html")

@app.route("/sendLang", methods=["POST"])
def sendLang():#バックにurlで送る
        language = request.form.get("language")
        
        url="http://localhost:5000/receive"#仮
        #url="http://localhost:5173/generate_question" #バック送信URL
        params = {"language": language}
        #print(params)
    
        response = requests.post(url, params=params)
        return  receive()
        #return ""

@app.route("/receive", methods=["GET","POST"])#sendのあと向こうがreceiveに送ってくるはずなので受け取ってinput.html表示
def receive():
    #data = request.get_json()#jsonを受け取る
    #-------------------------------------テスト用-----------------------------------------------------------
    data= {
    "level": 1,
    "language": "php",
    "source code": "```php\n<?php\nif ($_SERVER['REQUEST_METHOD'] === 'POST') {\n    $username = $_POST['username'];\n    $password = $_POST['password'];\n    if ($username === 'admin' && $password === 'pass123') {\n        echo \"Welcome admin!\";\n    } else {\n        echo \"Invalid credentials.\";\n    }\n}\n?>\n<form method=\"post\">\n  Username: <input name=\"username\"><br>\n  Password: <input name=\"password\" type=\"password\"><br>\n  <input type=\"submit\" value=\"Login\">\n</form>\n```",
    "answer": "$password === 'pass123'",
    "explanation": "パスワードがコード内にハードコードされており、ソースコード漏洩やリバースエンジニアリングによって簡単に特定される。環境変数や安全な認証システムを利用すべき。"
    }
    
    level = data.get("level",data.get("level", ""))
    question = data.get("source code",data.get("source code", ""))
    answer = data.get("answer")
    explanation = data.get("explanation")
    #------------------------------------回答と説明をansewerに送信------------------------------------------------------------
    url="http://localhost:5000/answer"
    
    params = {"answer": answer,"explanation": explanation}
    response = requests.post(url, params=params)#answerに送信

    return render_template("/input.html",level=level,question=question)

@app.route("/input", methods=["GET","POST"])
def input():#入力された情報をバックに送る、
    level = request.form.get("level")
    question = request.form.get("question")
    input1 = request.form['where']
    input2 = request.form['why']
    #url="http://localhost:5173/generate_question" #バック送信URL
    urlLog="http://localhost:5000/log"
    #url="http://localhost:5000/debug"#デバッグ用


    if(input1 and input2):
        params = {"where": input1,"why":input2}
        paramsLog = {"level": level,"question": question,"where": input1,"why":input2}
        responseLog = requests.post(urlLog, params=paramsLog)#ログに送信
       #response = requests.post(url, params=params)#バックにjson
       
    #return render_template("/answer.html",where=input1, why=input2)#デバッグ用だからいらん

    return render_template("/input.html",level=level,question=question)


@app.route("/answer", methods=["GET","POST"])#回答、
def answer():
     #見本データ{
     #"total_score": 86,
  #"grade": "Advanced",
  #"per_item": [
# {
    #  "index": 1,
    # "level": "Easy",
    #"position_score": 0.9,
    #"reason_score": 0.8,
    #"weighted_score": 8.6,
    #"feedback": "基本的な知識は十分にありますが、説明がやや簡潔です。より具体的な根拠も述べましょう。"
#},
#--------------------------------------------------------------------------------
    data = request.get_json()#バックからスコアなどを受け取る
   
    level = request.form.get("level")
    question = request.form.get("question")
    answer = request.form.get("answer")
    explanation = request.form.get("explanation")
    point = data.get("total_score",data.get("total_score", ""))
    feeback=data.get("per_item",data.get("per_item", "")  ) 

    if(level==5):
        return render_template("/log.html")#log.htmlに問題、レベル、answer、explanation、point、feedbackとか適当に送る
    
    return render_template("/input.html",level=level,question=question,total_score=point,feeback=feeback)




@app.route("/log", methods=["GET","POST"])#回答、
def log():


    return ""

@app.route("/debug", methods=["GET","POST"])#デバッグ用、書かない
def debug():


    return ""




if __name__ == "__main__":
     app.run(debug=True)
                                  