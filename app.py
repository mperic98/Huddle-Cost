import os
import time
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Environment variables from Render
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
AVG_HOURLY_RATE = float(os.environ.get("AVG_HOURLY_RATE", 80))

# Initialize Slack app
bolt_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Store huddle data (in-memory; use DB if you want persistence)
huddles = {}

# Endpoint Slack will call
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@bolt_app.event("call_started")
def on_huddle_start(event, say):
    call_id = event["call"]["id"]
    participants = event["call"]["participants"]
    huddles[call_id] = {
        "start_time": time.time(),
        "participants": participants
    }
    say(f"📞 Huddle started with {len(participants)} participants.")

@bolt_app.event("call_ended")
def on_huddle_end(event, say):
    call_id = event["call"]["id"]
    info = huddles.pop(call_id, None)
    if not info:
        return
    duration_hours = (time.time() - info["start_time"]) / 3600
    num_participants = len(info["participants"])
    cost = num_participants * duration_hours * AVG_HOURLY_RATE
    say(
        f"💰 Huddle ended!\n"
        f"👥 Participants: {num_participants}\n"
        f"🕒 Duration: {duration_hours:.2f} hours\n"
        f"💵 Estimated Cost: ${cost:.2f}"
    )

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)

