# -----------------------
# ChatGPTに投げる関数（骨組み）
# -----------------------
import requests

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_KEY = "YOUR_OPENAI_KEY"

def ask_llm(text):
    # feed内容をLLMにぶん投げる
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "お前はfeederに住み着く住民としてふるまえ。"},
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    res = r.json()

    # LLMの返答本文だけ抽出
    return res["choices"][0]["message"]["content"]


# -----------------------
# feederへ投稿する関数（骨組み）
# -----------------------
FEEDER_POST_URL = "https://www1.x-feeder.info/xxxx/post_feed.php"  # ←お前の環境に合わせて

def post_to_feeder(response_text):
    payload = {
        "post": response_text,
        "submit": "submit"
    }

    r = requests.post(FEEDER_POST_URL, data=payload)
    return r.status_code
