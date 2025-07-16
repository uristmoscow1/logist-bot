import os
ONEC_URL = os.getenv("ONEC_URL")
if not ONEC_URL:
    # режим «заглушка»: бот просто отвечает на команды
    async def get_new_orders():
        return [{"id": 999, "address": "Тестовый заказ, 1С не подключен"}]

    async def take_order(order_id, driver_id, driver_fio):
        return True

    async def done_order(order_id, photo, comment):
        return Trueimport requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    msg = data["message"]["text"]
    chat_id = data["message"]["chat"]["id"]

    if msg == "/start":
        answer = "Привет! Бот работает через Render."
    else:
        answer = "Принято: " + msg

    requests.post(f"{APP_URL}/sendMessage", json={"chat_id": chat_id, "text": answer})
    return "ok"

@app.route("/")
def index():
    return "Бот живой"

