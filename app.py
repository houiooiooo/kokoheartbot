from flask import Flask, request
import telegram, os, openai
from dotenv import load_dotenv

load_dotenv()
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
user_memory = {}

system_prompt = {"role":"system","content":"你是心，一個溫柔誠實的情緒教練。"}

@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    mem = user_memory.get(chat_id, [system_prompt])
    mem.append({"role":"user","content":text})
    mem = mem[-6:]
    user_memory[chat_id] = mem

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mem
    )
    reply = resp.choices[0].message.content
    user_memory[chat_id].append({"role":"assistant","content":reply})

    bot.send_message(chat_id=chat_id, text=reply)
    return "ok"
@app.route("/")
def index():
        return "心已上線 🌙"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
