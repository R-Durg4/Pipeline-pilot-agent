from flask import Flask, render_template, request
from analyzer import analyze_log

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html", log_text="", result=None)

@app.post("/analyze")
def analyze():
    log_text = request.form.get("log_text", "")[:20000]
    result = analyze_log(log_text)
    return render_template("index.html", log_text=log_text, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
