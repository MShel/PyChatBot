from transport.AbstractTransport import AbstractTransport
import requests
from flask import Flask, request
from Router import Router
import json
from flask_restful import Resource

class Facebook(AbstractTransport):
    verify_token = None

    access_token = 'test'

    access_point_root = None

    ENDPOINTS_TO_ADD = ["/", "/privacy", "/webhook"]

    MESSAGES_URL = "https://graph.facebook.com/v2.6/me/messages"

    def __init__(self, router: Router, access_token: str, verify_token: str, access_point_root: str):
        self.access_token = access_token
        self.verify_token = verify_token
        self.access_point_root = access_point_root
        self.router = router

    def get_end_points_to_add(self):
        return self.ENDPOINTS_TO_ADD

    def send_message(self, recipient_id: int, message_text: str):
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
        requests.post(self.MESSAGES_URL, params=params, headers=headers, data=data)

class FacebookEndPoint(Resource):

    fb = None

    app = None

    methods = ['GET', 'POST']

    def __init__(self, transport: Facebook, app: Flask):
        self.fb = transport
        self.app = app

    def get(self):
        if 'privacy' in request.path:
            return self.app.send_static_file('privacy.html')
        return self.verify()

    def post(self):
        data = request.get_json(force=True)
        print(data)
        return self.webhook(data)

    def webhook(self, data) -> tuple:
        sender_id = None
        if data["object"] == "page":
            try:
                for entry in data["entry"]:
                    for messaging_event in entry["messaging"]:
                        if messaging_event.get("message"):
                            sender_id = messaging_event["sender"]["id"]
                            messageGenerator = self.fb.get_reply_message(sender_id, messaging_event["message"]["text"].lower())
                            for message in messageGenerator:
                                self.fb.send_message(sender_id, message)
            except KeyError:
                if sender_id:
                    self.fb.send_message(sender_id, "This facebook action is not supported yet")
        return self.app.make_response("ok")

    def get_privacy(self):
        self.app.send_static_file('privacy.html')

    def verify(self) -> tuple:
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == self.fb.verify_token:
                return "Verification token mismatch", 403

            return self.app.make_response(request.args["hub.challenge"])

        return "We Got to FB transport!", 200