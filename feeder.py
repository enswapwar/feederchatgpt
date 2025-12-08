from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "feeder backend alive"

# -----------------------------------------------------------
# RSS文字列から <item> の title/pubdate を抽出する処理
# -----------------------------------------------------------
def parse_rss(rss_text):
    # <item>...</item> を全部抜く（DOTALLで改行含めマッチ）
    items = re.findall(r"<item>(.*?)</item>", rss_text, re.DOTALL)

    if not items:
        return None

    latest = items[0]  # 一番上＝最新

    # title
    title_match = re.search(r"<title>(.*?)</title>", latest, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    # pubdate
    date_match = re.search(r"<pubdate>(.*?)</pubdate>", latest, re.DOTALL)
    pubdate = date_match.group(1).strip() if date_match else ""

    return {
        "title": title,
        "pubdate": pubdate
    }

# -----------------------------------------------------------
# RSS受信API
# -----------------------------------------------------------
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    if not data or "rss" not in data:
        return jsonify({"error": "no rss"}), 400

    rss_raw = data["rss"]

    parsed = parse_rss(rss_raw)

    if not parsed:
        return jsonify({"error": "no items found"}), 400

    return jsonify({
        "status": "ok",
        "latest": parsed
    })
