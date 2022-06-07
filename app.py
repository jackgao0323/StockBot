import os
from datetime import datetime

from flask import Flask, abort, request

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re

from stock_list import stock

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

line_bot_api.push_message(os.environ.get("USER_ID"), TextSendMessage(text='你可以開始了'))

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('包子',message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('包子臭臭'))

    # Send To Line
    # reply = TextSendMessage(text=f"{get_message}")
    reply = TextSendMessage(text=f"蝦蝦搞好帥")
    line_bot_api.reply_message(event.reply_token, reply)