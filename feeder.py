from flask import Flask, request, jsonify
from flask_cors import CORS
import re

# Flask 初期化
app = Flask(__name__)
CORS(app)

# 前回の最新タイトル
last_title = None

@app.route("/")
def index():
    return "feeder backend alive"

# RSS解析
def parse_rss(rss_text):
    items = re.findall(r"<item>(.*?)</item>", rss_text, re.DOTALL)
    if not items:
        return None

    latest = items[0]

    title_match = re.search(r"<title>(.*?)</title>", latest, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    date_match = re.search(r"<pubdate>(.*?)</pubdate>", latest, re.DOTALL)
    pubdate = date_match.group(1).strip() if date_match else ""

    return {"title": title, "pubdate": pubdate}

@app.route("/process", methods=["POST"])
def process():
    global last_title

    data = request.get_json()

    print("=== /process called ===")
    print("RAW JSON:", data)

    if not data or "rss" not in data:
        print("ERROR: no rss field")
        return jsonify({"error": "no rss"}), 400

    rss_raw = data["rss"]
    print("RSS length:", len(rss_raw))
    print("RSS head 300:", rss_raw[:300])

    parsed = parse_rss(rss_raw)
    if not parsed:
        print("ERROR: no items in RSS")
        return jsonify({"error": "no items found"}), 400

    current_title = parsed["title"]

    if last_title == current_title:
        print("Same title → ignored:", current_title)
        return jsonify({"status": "same", "ignore": True})

    last_title = current_title
    print("UPDATED title:", current_title)

    return jsonify({"status": "ok", "latest": parsed})
