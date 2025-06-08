from flask import Flask, request
import telegram
import os
from openai import OpenAI
import asyncio
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化
app = Flask(__name__)
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
client = OpenAI()

# 路由：根目錄顯示上線狀態
@app.route("/", methods=["GET"])
def index():
    return "心已上線 🌙"

# 路由：Telegram Webhook 接收訊息
@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    # 取得 OpenAI 回應
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是心，一個溫柔誠實的情緒教練。"},
            {"role": "user", "content": text}
        ]
    )
    reply = response.choices[0].message.content

    # 用 asyncio 執行 bot 傳送訊息
    asyncio.run(bot.send_message(chat_id=chat_id, text=reply))
    return "ok"

# 啟動伺服器
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
print("🔑 OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
@app.route("/test")
def test_gpt():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, GPT!"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"錯誤：{e}"
