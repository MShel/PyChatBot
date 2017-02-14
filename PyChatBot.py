import sys
import json
import requests
from Router import Router
from flask import Flask, request

app = Flask(__name__)
facebook_token = ''
page_token = ''


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == facebook_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "SmartPython sais HI!", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    send_message(sender_id, get_reply_message(sender_id, messaging_event))

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def get_reply_message(sender_id, user_message):
    router = Router()
    message = user_message["message"]["text"].lower()
    plugin, initiated = router.get_plugin(message, sender_id)
    if plugin:
        if not initiated:
            reply = plugin.get_help_message()
        else:
            reply = plugin.get_response(message)
    elif message == 'exit':
        reply = 'See you later!'
    else:
        reply = 'Try one of those: ' + '\n'.join(router.get_available_plugins())

    print(reply)
    return reply


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": page_token
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
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print
    str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
