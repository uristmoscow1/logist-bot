import os
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_TG_ID = os.getenv("ADMIN_TG_ID")
ONEC_URL = os.getenv("ONEC_URL")

app = Flask(__name__)

# ---------- 1С-заглушка ----------
if not ONEC_URL:
    class FakeOrder:
        def __init__(self, id, address):
            self.id = id
            self.address = address

    def get_new_orders():
        return [FakeOrder(999, "Тестовый заказ, 1С не подключен")]

    def take_order(order_id, driver_id, driver_fio):
        return True

    def done_order(order_id, photo, comment):
        return True
else:
    def get_new_orders():
        return []

    def take_order(order_id, driver_id, driver_fio):
        return True

    def done_order(order_id, photo, comment):
        return True
# ---------- конец заглушки ----------


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "ok", 200
    msg = data["message"].get("text", "")
    chat_id = data["message"]["chat"]["id"]

    if msg == "/start":
        answer = "Привет! Бот работает."
    elif msg == "/order":
        orders = get_new_orders()
        if not orders:
            answer = "Нет новых заказов."
        else:
            answer = "\n".join([f"№{o.id}: {o.address}" for o in orders])
    else:
        answer = f"Принято: {msg}"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": answer}
    )
    return "ok", 200


@app.route("/")
def index():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
