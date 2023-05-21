from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
import pytesseract
from PIL import Image
import io
import requests

app = Flask(__name__)

import os

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # Here you can define how to handle text messages
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    image = Image.open(io.BytesIO(message_content.content))

    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(image)

    # Use GPT-4 to generate an explanation
    explanation = generate_explanation(text)  # This function needs to be implemented

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=explanation))

def generate_explanation(text):
    # This function should use GPT-4 to generate an explanation based on the text
    # For now, we'll just return the text
    return text

if __name__ == "__main__":
    app.run()
