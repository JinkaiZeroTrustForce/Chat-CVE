from flask import Flask, render_template, request
import requests,jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("start.html")


@app.route("/send", methods=["POST"])
def send():#バックにurlで送る
        language = request.args.get("language")
        
        #url="http://localhost:5001/receive"#仮、5173
        #response = requests.post(url, language)
        return render_template("/input.html")#デバッグ用に表示しているだけ、本来はここいらん



@app.route("/receive", methods=["GET"])#sendのあと向こうがreceiveに送ってくるはずなので受け取ってinput.html表示
def receive():
    data = request.get_json()
    # {
    #"level": 1,
    #"language": "php",
    #"source code": "```php\n<?php\nif ($_SERVER['REQUEST_METHOD'] === 'POST') {\n    $username = $_POST['username'];\n    $password = $_POST['password'];\n    if ($username === 'admin' && $password === 'pass123') {\n        echo \"Welcome admin!\";\n    } else {\n        echo \"Invalid credentials.\";\n    }\n}\n?>\n<form method=\"post\">\n  Username: <input name=\"username\"><br>\n  Password: <input name=\"password\" type=\"password\"><br>\n  <input type=\"submit\" value=\"Login\">\n</form>\n```",
    #"answer": "$password === 'pass123'",
    #"explanation": "パスワードがコード内にハードコードされており、ソースコード漏洩やリバースエンジニアリングによって簡単に特定される。環境変数や安全な認証システムを利用すべき。"}
    #------------------------------------------------------------------------------------------------
    level = data.get("level")
    question = data.get("source code")

    return render_template("/input.html",level=level,question=question)



if __name__ == "__main__":
     app.run(debug=True)
                                  