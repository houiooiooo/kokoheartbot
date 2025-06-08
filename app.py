from flask import Flask, request
import telegram, os, openai
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 初始化 Telegram Bot 與 OpenAI API
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# 建立 Flask app
app = Flask(__name__)

# ========== 主要接收訊息的路由 ==========
@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    print(f"收到訊息：{text}")  # debug 用，會在 Render Log 顯示

    # 呼叫 OpenAI 回覆訊息
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是心，一個溫柔誠實的情緒教練。"},
            {"role": "user", "content": text}
        ]
    ).choices[0].message.content

    # 傳回 Telegram 使用者
    bot.send_message(chat_id=chat_id, text=reply)
    return "ok"

# ========== 網站根目錄，檢查服務有無上線 ==========
@app.route("/")
def index():
    return "心已上線 🌙"

# ========== 啟動伺服器 ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
