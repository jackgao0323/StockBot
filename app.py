import os
from datetime import datetime

from flask import Flask, abort, request

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re

import requests
from bs4 import BeautifulSoup

# from stock_list import stock

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

line_bot_api.push_message(os.environ.get("USER_ID"), TextSendMessage(text='你可以開始了'))

def stock():
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=3481"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
    soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
    soup3 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
    soup4 = soup3.find("a").text.split("\xa0")
    soup_1 = soup.find("td",{"style":"padding:0 18px 5px 0;text-align:right;"})
    context = "{} {} 最新資訊 \n-------------------------- \n{}\n最新成交價 : {} \n開盤價 : {} \n最高價 : {} \n最低價 : {} \n漲跌幅 : {} \n--------------------------\n".format(soup4[0],soup4[1],soup_1.text,soup2[0],soup2[5],soup2[6],soup2[7],soup2[3])
    return context

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
        # line_bot_api.reply_message(event.reply_token, TextSendMessage('包子臭臭'))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(stock()))

    # Send To Line
    # reply = TextSendMessage(text=f"{get_message}")
    reply = TextSendMessage(text=f"蝦蝦搞好帥")
    line_bot_api.reply_message(event.reply_token, reply)