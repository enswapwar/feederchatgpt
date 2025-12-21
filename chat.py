from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import requests
from prompt import SYSTEM_PROMPT

app = Flask(__name__)
CORS(app)

last_title = None
last_reply = None

@app.route("/")
def index():
    return "feeder backend alive"

# --------------------
# RSS受信（A用）
# --------------------
@app.route("/process_rss", methods=["POST"])
def process_rss():
    global last_title, last_reply

    data = request.get_json()
    if not data or "rss" not in data:
        return jsonify({"error": "no rss"}), 400

    rss = data["rss"]

    items = re.findall(r"<item>(.*?)</item>", rss, re.DOTALL)
    if not items:
        return jsonify({"error": "no item"}), 400

    latest = items[0]
    title = re.search(r"<title>(.*?)</title>", latest, re.DOTALL)
    if not title:
        return jsonify({"error": "no title"}), 400

    text = title.group(1)

    if text == last_title:
        return jsonify({"status": "same"})

    last_title = text

    # @chatgpt が含まれるときだけ反応
    if "@chatgpt" in text.lower():
        last_reply = ask_llm(text)

    return jsonify({"status": "ok"})

# --------------------
# B用：返答取得
# --------------------
@app.route("/reply", methods=["GET"])
def reply():
    if not last_reply:
        return jsonify({"reply": None})

    r = last_reply
    last_reply = None
    return jsonify({"reply": r})


# --------------------
# ChatGPT API
# --------------------
def ask_llm(text):
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
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
        json=payload
    )
    return r.json()["choices"][0]["message"]["content"]
