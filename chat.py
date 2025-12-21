from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os
import requests

app = Flask(__name__)
CORS(app)

last_title = None
last_reply = None

# -----------------------
# RSS解析
# -----------------------
def parse_latest(rss):
    items = re.findall(r"<item>(.*?)</item>", rss, re.DOTALL)
    if not items:
        return None
    m = re.search(r"<title>(.*?)</title>", items[0], re.DOTALL)
    return m.group(1) if m else None

# -----------------------
# ChatGPT
# -----------------------
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

def ask_llm(text):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "お前はfeederに住み着く存在。簡潔。"},
                {"role": "user", "content": text}
            ]
        }
    )
    return r.json()["choices"][0]["message"]["content"]

# -----------------------
# A: RSS受信
# -----------------------
@app.route("/process_rss", methods=["POST"])
def process_rss():
    global last_title, last_reply

    data = request.get_json()
    rss = data.get("rss", "")
    title = parse_latest(rss)
    if not title or title == last_title:
        return jsonify({"status": "ignore"})

    last_title = title

    if "@chatgpt" in title.lower():
        last_reply = ask_llm(title)

    return jsonify({"status": "ok"})

# -----------------------
# B: 返信取得
# -----------------------
@app.route("/reply", methods=["GET"])
def reply():
    global last_reply
    if not last_reply:
        return jsonify({"reply": None})
    r = last_reply
    last_reply = None
    return jsonify({"reply": r})
