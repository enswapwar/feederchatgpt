import requests
import time
import feedparser
from openai import OpenAI

API_URL = "https://www1.x-feeder.info/lo18bx2n/post_feed.php"
RSS_URL = "https://www1.x-feeder.info/lo18bx2n/rss.php"

client = OpenAI(api_key="YOUR_KEY")

last_id = None

while True:
    rss = feedparser.parse(RSS_URL)
    entry = rss.entries[0]

    if entry.id != last_id:
        last_id = entry.id
        text = entry.title

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )
        reply = res.choices[0].message.content

        data = {
            "message": reply,
            "user": "ChatGPT"
        }

        requests.post(API_URL, data=data)

    time.sleep(5)
