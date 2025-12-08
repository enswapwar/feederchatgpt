@app.route("/process", methods=["POST"])
def process():
    global last_title

    data = request.get_json()

    # ---- デバッグログ ----
    print("=== /process called ===")
    print("RAW JSON:", data)
    # -----------------------

    if not data or "rss" not in data:
        print("ERROR: no rss field")
        return jsonify({"error": "no rss"}), 400

    rss_raw = data["rss"]

    # ---- デバッグログ ----
    print("RSS length:", len(rss_raw))
    print("RSS head 300:", rss_raw[:300])
    # -----------------------

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
