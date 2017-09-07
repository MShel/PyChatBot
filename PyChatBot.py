import sys
import json
import requests
from flask import Flask, request
import os
from storage import Redis

#TODO this whole file is bad

app = Flask(__name__, static_url_path='/static')
facebook_token = os.getenv('facebook_token')
page_token = os.getenv('page_token')

storage = Redis.RedisAdapter().get_storage()

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == facebook_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "SmartPython sais HI!", 200


@app.route('/privacy', methods=['GET'])
def privacy():
    return app.send_static_file('privacy.html')


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
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
    from Router import Router
    router = Router(storage)
    reply = 'Try one of those:\n ' + '\n'.join(router.get_available_plugins())
    try:
        message = user_message["message"]["text"].lower()
        plugin, initiated = router.get_plugin(message, sender_id)
        if plugin:
            if not initiated:
                reply = plugin.get_help_message()
            else:
                reply = plugin.get_response(message)
        elif message == 'exit':
            reply = 'See you later!'
    except KeyError:
        log(user_message)
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
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
