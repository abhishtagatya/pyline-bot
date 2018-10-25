import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('JgAUp2xUHTYAQUlAT+w2llgEHM3/koPdgEihrdmZPQGQCte0B92nuk9v4CJwyDxLggV53unbqvzVzl/Nk7fSw5Ydv9Bty15NWZBMGGjaYMXczoqUTZhOTvG4T5QGyPN9bs7nDX3pbKCtVoDLEYengwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9af0032122cd7403a00a834fb71bc40f')


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    text = (event.message.text).lower()
    text_argument = text.split()
    
    def Look_Level(level = []):
        global check_level
        check_level = []
        
        for i in check_level:
            try:
                int(i)
                check_level.append(int(i))
            except:
                pass
        
        # cek kalau user milih lebih dari 1 level
        if len(check_level) != 1:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Upps! It's good if you learn one by one.\nPlease select 1 Level only. :)"))
        
        # cek kalau user tidak milih level di range 1-6 
        elif check_level[0] not in range(1,7):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Wa! Sorry, we don't have Level {}\n".format(check_level[0])),
            TextSendMessage(text="Please choose from Level 1-7 only."))        
        
        # cek pilihan level nya udah sesuai
        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Here we go!"))
        
    
    if "level" in text:
        Look_Level(text_argument)


if __name__ == "__main__":
    app.run
