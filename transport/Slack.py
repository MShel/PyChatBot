from transport.AbstractTransport import AbstractTransport
import requests
from flask import Flask, request
from Router import Router
from flask_restful import Resource


class Slack(AbstractTransport):

    verify_token = None

    access_token = 'test'

    access_point_root = None

    bot_id = None

    ENDPOINTS_TO_ADD = ["/"]

    MESSAGES_URL = "https://slack.com/api/chat.postMessage"

    def __init__(self, router: Router, verify_token: str, token: str, bot_id: str, access_point_root: str):
        self.token = token
        self.bot_id = bot_id
        self.verify_token = verify_token
        self.access_point_root = access_point_root
        self.router = router

    def get_end_points_to_add(self):
        return self.ENDPOINTS_TO_ADD

    def send_message(self, sender_id: str, message: str):

        payload = {
            'token': self.token,
            'channel': sender_id,
            'text': message,
            'as_user': True
        }

        requests.post(self.MESSAGES_URL, data=payload)


class SlackEndPoint(Resource):
    slack = None

    app = None

    methods = ['POST']

    def __init__(self, transport: Slack, app: Flask):
        self.slack = transport
        self.app = app

    def post(self):
        data = request.get_json(force=True)
        print(data)
        if data["type"] == "url_verification":
            return self.verify(data)
        elif data["type"] == "event_callback" and data["event"]["type"] == "message" and self.slack.bot_id in data["event"]["text"]:
            return self.webhook(data["event"])
        return "Nothing to see here"

    def webhook(self, data) -> tuple:
        sender_id = data["channel"]
        if "<@" in data["text"]:
            data["text"] = data["text"][data["text"].index('>')+2:]

        messageGenerator = self.slack.get_reply_message(sender_id, data["text"].lower())
        for message in messageGenerator:
            self.slack.send_message(sender_id, message)

        return self.app.make_response("ok")

    def verify(self, data):
        if data["token"] == self.slack.verify_token:
            return self.app.make_response(data["challenge"])
        return "We Got to Slack transport!", 200
