from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# 前回の最新タイトルを保持（メモリ上）
last_title = None

@app.route("/")
def index():
    return "feeder backend alive"

# -----------------------
# RSS解析
# -----------------------
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

# -----------------------
# 受信API (feeder→POST)
# RSS と feed_id / content の両方に対応
# -----------------------
@app.route("/process", methods=["POST"])
def process():
    global last_title

    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    # -----------------------
    # RSS解析部分
    # -----------------------
    if "rss" in data:
        rss_raw = data["rss"]
        parsed = parse_rss(rss_raw)

        if not parsed:
            return jsonify({"error": "no items found"}), 400

        current_title = parsed["title"]

        # 前回と同じなら無視
        if last_title == current_title:
            return jsonify({
                "status": "same",
                "ignore": True
            })

        # 違う → 更新
        last_title = current_title

        return jsonify({
            "status": "ok",
            "latest": parsed
        })

    # -----------------------
    # フィード投稿内容（feed_id / content）
    # logs に表示させるため追加
    # -----------------------
    feed_id = data.get("feed_id")
    content = data.get("content")

    print("========== FEED RECEIVED ==========")
    print(f"FEED ID: {feed_id}")
    print(f"CONTENT: {content}")
    print("===================================")

    return jsonify({
        "status": "ok",
        "received_id": feed_id,
        "received_content": content
    })
