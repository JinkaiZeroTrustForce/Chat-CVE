from flask import Flask, request, jsonify,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("/input.html")

@app.route("/receive", methods=["GET"])
def receive():
    data = request.get_json()
    language = data.get("language")
    
    print("受信:", language)
    return jsonify({"status": "ok", "received": language})

if __name__ == "__main__":
    app.run(port=5001, debug=True)