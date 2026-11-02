import os
import json
import time
import urllib.parse
import urllib.request

# Переменные задаются в настройках хостинга
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_БОТА")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "your_admin").lstrip("@")

# Текст можно менять. Демо-пометка должна оставаться понятной.
OFFER_TEXT = (
    "🎁 ДЕМО-ОФФЕР НА ПОДАРОК\n\n"
    "Это демонстрация интерфейса.\n"
    "Реальной передачи подарка и выплаты звёзд здесь НЕ происходит.\n\n"
    "Подарок: {gift}\n"
    "Получатель: {recipient}"
)

API = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def telegram(method, data=None):
    payload = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(API + method, data=payload)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def send_message(chat_id, text, keyboard=None):
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard, ensure_ascii=False)
    return telegram("sendMessage", data)


def handle(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text.startswith("/start"):
        send_message(
            chat_id,
            "Бот демонстрационных офферов запущен.\n\n"
            "Команда:\n/offer <подарок> <получатель>"
        )
        return

    if text.startswith("/id"):
        send_message(chat_id, f"Ваш Telegram ID: {message['from']['id']}")
        return

    if text.startswith("/offer"):
        parts = text.split(maxsplit=2)
        gift = parts[1] if len(parts) > 1 else "не указан"
        recipient = parts[2] if len(parts) > 2 else "не указан"

        keyboard = {
            "inline_keyboard": [[{
                "text": "Связаться с администратором",
                "url": f"https://t.me/{ADMIN_USERNAME}"
            }]]
        }
        send_message(
            chat_id,
            OFFER_TEXT.format(gift=gift, recipient=recipient),
            keyboard
        )
        return

    send_message(chat_id, "Используй команду: /offer <подарок> <получатель>")


def main():
    if not BOT_TOKEN or BOT_TOKEN == "ВСТАВЬ_ТОКЕН_БОТА":
        raise RuntimeError("Не задана переменная BOT_TOKEN")

    offset = 0
    while True:
        try:
            result = telegram("getUpdates", {
                "timeout": 50,
                "offset": offset
            })
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                if "message" in update:
                    handle(update["message"])
        except Exception as error:
            print("Ошибка:", error, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
