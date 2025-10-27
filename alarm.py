webhook_url = "https://default198a7beeda9f4c9b8252cbbf624578.12.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/20ae22760c074f0786db0f573a37782c/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=i9g0RfoQrYCQyGbcsUOnzxsSAFgwogRygzFA5Ss5228"
import requests, datetime as dt


card = {
    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [
        {"type": "TextBlock", "text": "Automated Update", "weight": "Bolder", "size": "Medium"},
        {"type": "TextBlock", "text": f"Hello from Python! Sent at {dt.datetime.utcnow().isoformat()}Z", "wrap": True}
    ],
    "actions": [
        {"type": "Action.OpenUrl", "title": "Open Dashboard", "url": "https://example.com"}
    ]
}

payload = {
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card
        }
    ]
}

r = requests.post(webhook_url, json=payload, timeout=10)

if 200 <= r.status_code < 300:
    print(f"Queued by Teams (HTTP {r.status_code}).")
else:
    print(f"Failed ({r.status_code}): {r.text}")
    r.raise_for_status()
