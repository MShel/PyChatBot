import json
from urllib import request

import requests
from flask import Flask
from flask_restful import Resource

from Router import Router
from transport.AbstractTransport import AbstractTransport


class Telegram(AbstractTransport):
    verify_token = None

    token = 'test'

    access_point_root = None

    ENDPOINTS_TO_ADD = ["/"]

    MESSAGES_URL = "https://api.telegram.org/{}/{}"

    def __init__(self, router: Router, token: str, access_point_root: str):
        self.token = token
        self.access_point_root = access_point_root
        self.router = router
        self.send_message(1, "12312131")

    def get_end_points_to_add(self):
        return self.ENDPOINTS_TO_ADD

    def send_message(self, recipient_id: int, message_text: str):
        data = json.dumps({
            "chat_id":
                recipient_id
            ,
            "text":
                message_text

        })

        requests.post(self.MESSAGES_URL.format(self.token, "sendMessage"), data = data)

    def get_help_message(self):
        return "wkjenfkjwenfkw"


class TelegramEndPoint(Resource):
    telega = None

    app = None

    methods = ['GET', 'POST']

    def __init__(self, transport: Telegram, app: Flask):
        self.telega = transport
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
                            messageGenerator = self.telega.get_reply_message(sender_id,
                                                                             messaging_event["message"]["text"].lower())
                            for message in messageGenerator:
                                self.telega.send_message(sender_id, message)
            except KeyError:
                if sender_id:
                    self.telega.send_message(sender_id, "This facebook action is not supported yet")
        return self.app.make_response("ok")

    def get_privacy(self):
        self.app.send_static_file('privacy.html')

    def verify(self) -> tuple:
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == self.telega.verify_token:
                return "Verification token mismatch", 403

            return self.app.make_response(request.args["hub.challenge"])

        return "We Got to FB transport!", 200
