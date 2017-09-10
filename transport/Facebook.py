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
        #self.app.add_url_rule('/', self.access_point_root, self.verify, methods=['GET'])
        self.app.add_url_rule('/','index', lambda :'hola', methods=['GET'])
        #self.app.add_url_rule('/', self.access_point_root, self.webhook, methods=['POST'])

    def webhook(self) -> tuple:
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        messageGenerator = self.get_reply_message(sender_id, messaging_event["message"]["text"].lower())
                        for message in messageGenerator:
                            self.send_message(sender_id, message)

        return "ok", 200

    def privacy(self):
        print(test)
        return self.app.send_static_file('privacy.html')

    def verify(self) -> tuple:
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == facebook_token:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200

        return "We Goy to FB transport!", 200

    def send_message(self, recipient_id: int, message_text: int):
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
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
