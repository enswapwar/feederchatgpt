from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "feeder backend alive"

# -------------------------
# RSSを受け取って解析するAPI
# -------------------------
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    if not data or "rss" not in data:
        return jsonify({"error": "no rss"}), 400

    rss_raw = data["rss"]

    # 今はデバッグ用にRSSをそのまま返す
    # 後で解析ロジックを入れる
    return jsonify({
        "status": "ok",
        "length": len(rss_raw),
        "sample": rss_raw[:200]  # 先頭200文字だけ確認用
    })
