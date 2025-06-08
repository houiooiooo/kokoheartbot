from flask import Flask, request
import telegram
import openai
import os

bot = telegram.Bot(token="8032536158:AAETw64tXJLwJ-a10N8Gn0-HM-MFnqX1aGk")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/8032536158:AAETw64tXJLwJ-a10N8Gn0-HM-MFnqX1aGk", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text
    print(f"收到訊息：{text}")  # debug log

    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是心，一個溫柔誠實的情緒教練。"},
            {"role": "user", "content": text}
        ]
    ).choices[0].message.content

    bot.send_message(chat_id=chat_id, text=reply)
    return "ok"

@app.route("/")
def index():
    return "心已上線 🌙"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
