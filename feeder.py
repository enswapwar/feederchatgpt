# feeder.py
# Feeder → Render上で動く最小構成のPythonサーバ
# HTTPサーバとして動かし、GET/POSTを受けるだけの原始的入口
# ここに後でフィード書き換え処理やAPIを追加する

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # 単純に動作確認できるレスポンス
    return jsonify({"status": "ok", "msg": "feeder.py alive"})

if __name__ == "__main__":
    # RenderはPORT環境変数を自動で渡すので使う
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
