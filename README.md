
# Huddle Cost Bot

A Slack app that estimates the cost of huddles based on:
- number of participants
- duration
- average hourly rate

## Environment Variables (set in Render)
- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `AVG_HOURLY_RATE` (default = 80)

## Deploy on Render
1. Push this repo to GitHub
2. Go to [Render.com](https://render.com)
3. Create a new **Web Service**
4. Connect to this repo
5. Use:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:flask_app`
6. Add environment variables (your Slack credentials)
7. Copy your Render URL (e.g. `https://huddle-cost.onrender.com`)
8. In Slack app settings → Event Subscriptions → set:
