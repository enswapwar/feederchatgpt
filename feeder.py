from flask import Flask, request, jsonify

app = Flask(__name__)

# 動作確認用エンドポイント
@app.route("/")
def index():
    return "OK: feeder backend alive"

# RSS を受け取るエンドポイント
@app.route("/feed", methods=["POST"])
def feed():
    data = request.get_json()
    if not data or "rss" not in data:
        return jsonify({"error": "no rss"}), 400
    # ここで RSS を見て解析して必要なら送信、今はダンプだけ
    return jsonify({"status": "recv", "len": len(data["rss"])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
