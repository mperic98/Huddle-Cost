import os
import time
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Environment variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
AVG_HOURLY_RATE = float(os.environ.get("AVG_HOURLY_RATE", 80))

# Initialize Slack app
bolt_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Store huddle data (in-memory)
huddles = {}

# Endpoint for Slack events (slash commands)
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Slash command: /huddle-cost start
@bolt_app.command("/huddle-cost")
def handle_huddle_command(ack, body, respond):
    ack()  # Acknowledge immediately

    user_id = body["user_id"]
    text = body.get("text", "").strip().lower()

    if text == "start":
        huddles[user_id] = time.time()
        respond(f"📞 Huddle started for <@{user_id}>.")
    elif text == "end":
        start_time = huddles.pop(user_id, None)
        if not start_time:
            respond("⚠️ No huddle found. Start one with `/huddle-cost start`.")
            return
        duration_hours = (time.time() - start_time) / 3600
        cost = duration_hours * AVG_HOURLY_RATE
        respond(
            f"💰 Huddle ended!\n"
            f"🕒 Duration: {duration_hours:.2f} hours\n"
            f"💵 Estimated Cost: ${cost:.2f}"
        )
    else:
        respond("Usage: `/huddle-cost start` or `/huddle-cost end`")

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
