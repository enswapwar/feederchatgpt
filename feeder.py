from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)  # ブラウザからのアクセスを許可

@app.route("/rss", methods=["POST"])
def rss():
    data = request.get_json()
    if not data or "rss" not in data:
        return jsonify({"ok": False, "error": "RSSなし"})
    
    rss_xml = data["rss"]

    # XML解析
    try:
        root = ET.fromstring(rss_xml)
        latest_title = root.find("./channel/item/title").text
    except Exception as e:
        return jsonify({"ok": False, "error": f"XML解析失敗: {e}"})
    
    # 必要に応じて加工・保存できる
    return jsonify({"ok": True, "latest_title": latest_title})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
