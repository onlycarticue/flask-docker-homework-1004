from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, request, render_template_string

app = Flask(__name__)
LOG_FILE = Path("/app/logs/log.txt")
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Message board</title><style>
body{font:16px system-ui,sans-serif;background:#f4f6f8;margin:0;padding:3rem 1rem;color:#17202a}
.card{max-width:620px;margin:auto;background:white;padding:2rem;border-radius:14px;box-shadow:0 8px 30px #0001}
textarea{box-sizing:border-box;width:100%;min-height:150px;padding:12px;font:inherit;border:1px solid #ccd3dc;border-radius:8px}
button{margin-top:12px;background:#1769aa;color:#fff;border:0;border-radius:8px;padding:10px 18px;font:inherit;cursor:pointer}
.result{margin-top:20px;padding:12px;background:#edf7ed;border-radius:8px;white-space:pre-wrap}
</style></head><body><main class="card"><h1>Send a message</h1>
<form method="post"><label for="message">Your message</label><p><textarea id="message" name="message" required maxlength="5000" placeholder="Type your message here...">{{ message }}</textarea></p><button type="submit">Send</button></form>
{% if response %}<section class="result" role="status"><strong>{{ response }}</strong><br>{{ saved }}</section>{% endif %}
</main></body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    response = saved = ""
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with LOG_FILE.open("a", encoding="utf-8") as log:
                log.write(f"{datetime.now(timezone.utc).isoformat()}\t{message}\n")
            response = f"Server received: {message}"
            saved = "Message saved to log.txt."
        else:
            response = "Please enter a message."
    return render_template_string(PAGE, message=message, response=response, saved=saved)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
