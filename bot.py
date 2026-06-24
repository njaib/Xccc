import telebot
from playwright.sync_api import sync_playwright
import os
import threading
from flask import Flask


# =====================
# تنظیمات
# =====================

BOT_TOKEN = "8743115028:AAGWYA2yp_vtNRKA14A9t53_Z5uAoapN-8g"

WEBSITE_URL = "https://khorasantelecom.co/transactions/receipts?tab=all"


bot = telebot.TeleBot(BOT_TOKEN)


# =====================
# Flask برای Render
# =====================

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot Running"


# =====================
# گرفتن اسکرین شات
# =====================

def take_screenshot():

    image = "website.png"

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width":1280,
                "height":1200
            }
        )


        page.goto(
            WEBSITE_URL,
            wait_until="networkidle"
        )


        page.screenshot(
            path=image,
            full_page=True
        )


        browser.close()


    return image



# =====================
# تلگرام
# =====================


@bot.message_handler(commands=["start"])
def start(message):

    user_id = message.chat.id


    bot.send_message(
        user_id,
        "⏳ در حال باز کردن سایت و گرفتن تصویر..."
    )


    try:

        img = take_screenshot()


        with open(img,"rb") as photo:

            bot.send_photo(
                user_id,
                photo,
                caption="📸 تصویر سایت"
            )


        os.remove(img)


    except Exception as e:


        bot.send_message(
            user_id,
            f"خطا:\n{e}"
        )



# =====================
# اجرا
# =====================


def run_bot():

    bot.infinity_polling()


if __name__ == "__main__":


    threading.Thread(
        target=run_bot
    ).start()


    port=int(
        os.environ.get(
            "PORT",
            10000
        )
    )


    app.run(
        host="0.0.0.0",
        port=port
    )