from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os
import requests

app = Flask(__name__)
CORS(app)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

SYSTEM_PROMPT = """
お前はfeederに住み着く存在。
無茶なことはするな、お前がfeederから消える。
簡潔。
自分をchatGPTだと名乗れ。
"""

last_handled_title = None

# -----------------------
# RSS解析
# -----------------------
def parse_latest_item(rss):
    items = re.findall(r"<item>(.*?)</item>", rss, re.DOTALL)
    if not items:
        return None

    latest = items[0]

    title = re.search(r"<title>(.*?)</title>", latest, re.DOTALL)
    title = title.group(1) if title else ""

    return title.strip()

# -----------------------
# ChatGPT呼び出し
# -----------------------
def ask_gpt(text):
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=20
    )

    res = r.json()
    return res["choices"][0]["message"]["content"]

# -----------------------
# RSS受信API
# -----------------------
@app.route("/process_rss", methods=["POST"])
def process_rss():
    global last_handled_title

    data = request.get_json()
    rss = data.get("rss", "")

    title = parse_latest_item(rss)
    if not title:
        return jsonify({"status": "no_item"})

    if title == last_handled_title:
        return jsonify({"status": "same"})

    last_handled_title = title

    # @chatgpt が含まれていなければ無視
    if "@chatgpt" not in title.lower():
        return jsonify({"status": "no_call"})

    reply = ask_gpt(title)

    return jsonify({
        "status": "reply",
        "reply": reply
    })
