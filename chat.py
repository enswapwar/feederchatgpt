# ---------------------------
# chat.py
# feeder の最新タイトルを受け取り
# OpenAI API に投げて返答を返す骨組み
# ---------------------------

import requests
import os

# ---------------------------
# 環境変数から OpenAI API キー取得
# Render 側で OPENAI_API_KEY をセットしておく必要あり
# ---------------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    print("ERROR: OPENAI_API_KEY が環境変数に存在しない。Render に設定しろ。")
    raise SystemExit

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def ask_llm(text):
    """Feeder の最新タイトルを LLM に投げて返答を生成する"""

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "お前は x-feeder に住み着いた住民として振る舞う。"
                    "返信は一言～数行の短いチャット文にしろ。"
                    "語尾やキャラは自由。"
                )
            },
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(OPENAI_API_URL, headers=headers, json=payload)

    try:
        res = r.json()
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        print("LLM ERROR:", e)
        print("RAW RESPONSE:", r.text)
        return None


# ==================================================
# feeder へ投稿する（POST Feed）
# ==================================================
FEEDER_POST_URL = "https://www1.x-feeder.info/xxxx/post_feed.php"
# ↑ お前の部屋 ID に合わせて書き換えろ

def post_to_feeder(response_text):
    """生成された文章を feeder に投稿する"""

    payload = {
        "post": response_text,
        "submit": "submit"
    }

    r = requests.post(FEEDER_POST_URL, data=payload)
    return r.status_code


# ==================================================
# テスト実行（Render Log で確認できる）
# ==================================================
if __name__ == "__main__":
    print("=== chat.py TEST RUN ===")
    test_msg = "テストメッセージ"
    print("Input:", test_msg)

    rep = ask_llm(test_msg)
    print("LLM response:", rep)

    if rep:
        print("Post status:", post_to_feeder(rep))
