from transport.AbstractTransport import AbstractTransport
import requests
from flask import Flask, request
from Router import Router
import json


class Facebook(AbstractTransport):
    verify_token = None

    access_token = None

    access_point_root = None

    def __init__(self, app: Flask, router: Router, access_token: str, verify_token: str, access_point_root: str):
        self.app = app
        self.access_token = access_token
        self.verify_token = verify_token
        self.access_point_root = access_point_root
        self.router = router
        self.init_app()

    def init_app(self):
        self.app.add_url_rule('/', self.access_point_root, self.webhook, methods=['POST'])
        self.app.add_url_rule('/', self.access_point_root, self.verify, methods=['GET'])
        self.app.add_url_rule('/', self.access_point_root, self.webhook, methods=['POST'])
        self.app.add_url_rule('/', self.access_point_root, self.webhook, methods=['POST'])

    def webhook(self):
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        self.send_message(sender_id, self.get_reply_message(sender_id, self.get_message_text(messaging_event)))

        return "ok", 200

    def send_message(self, recipient_id, message_text):
        params = {
            "access_token": self.access_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    def get_message_text(self, messaging_event: dict):
        message = ''
        try:
            message = messaging_event["message"]["text"].lower()
        except KeyError:
            pass
        return message
