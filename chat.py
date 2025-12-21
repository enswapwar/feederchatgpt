from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import datetime

app = Flask(__name__)
CORS(app)

# 最後に返信した pubDate
last_replied_time = None

# 一時的に保持する返信
pending_reply = None


@app.route("/")
def index():
    return "feederchatgpt alive"


def parse_rss(rss_text):
    items = re.findall(r"<item>(.*?)</item>", rss_text, re.DOTALL)
    if not items:
        return None

    latest = items[0]

    title_match = re.search(r"<title>(.*?)</title>", latest, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    date_match = re.search(r"<pubDate>(.*?)</pubDate>", latest, re.DOTALL)
    pubdate_raw = date_match.group(1).strip() if date_match else ""

    try:
        pubdate = datetime.datetime.strptime(
            pubdate_raw, "%a, %d %b %Y %H:%M:%S %z"
        )
    except Exception:
        pubdate = None

    return {
        "title": title,
        "pubdate": pubdate,
        "pubdate_raw": pubdate_raw
    }


def fake_chatgpt_reply(text):
    # 本来は OpenAI API を叩く
    return f"ChatGPT応答: {text}"


@app.route("/process_rss", methods=["POST"])
def process_rss():
    global last_replied_time, pending_reply

    data = request.get_json()
    if not data or "rss" not in data:
        return jsonify({"error": "no rss"}), 400

    parsed = parse_rss(data["rss"])
    if not parsed or not parsed["pubdate"]:
        return jsonify({"error": "parse failed"}), 400

    item_time = parsed["pubdate"]

    # すでに返信済み or 古い
    if last_replied_time and item_time <= last_replied_time:
        return jsonify({"status": "ignored"})

    # @chatgpt が含まれていないなら無視
    if "@chatgpt" not in parsed["title"].lower():
        return jsonify({"status": "no_mention"})

    reply = fake_chatgpt_reply(parsed["title"])

    pending_reply = reply
    last_replied_time = item_time

    return jsonify({
        "status": "reply",
        "reply": reply
    })


@app.route("/reply", methods=["GET"])
def get_reply():
    global pending_reply

    if not pending_reply:
        return jsonify({})

    r = pending_reply
    pending_reply = None  # 取り出したら即消す

    return jsonify({"reply": r})
