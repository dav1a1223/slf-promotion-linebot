from flask import Flask, request, abort
from simi_extract import CandReplyer
import os
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
cand_replyer = CandReplyer()

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN',''))
    handler = WebhookHandler(os.environ.get('CHANNEL_SECRET',''))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=cand_replyer.reply(event.message.text)))


if __name__ == "__main__":
    app.run()