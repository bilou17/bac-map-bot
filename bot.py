import os
import time
from threading import Thread
import telebot
from telebot import types
from flask import Flask

TOKEN = "8595028279:AAGlsrY5HpwrvDFXIMRXksyrjcowwPCa-J8"
bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = "https://lustrous-raindrop-86f3e6.netlify.app"

# 1. إنشاء سيرفر ويب وهمي لمنع موقع Render من إدخال البوت في وضع النوم
app = Flask("")


@app.route("/")
def home():
  return "BacMapDz Bot is running 24/7!"


def run_web():
  # تشغيل السيرفر على المنفذ المطلوب
  app.run(host="0.0.0.0", port=8080)


def keep_alive():
  t = Thread(target=run_web)
  t.start()


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_name = message.from_user.first_name

  welcome_text = (
      f"أهلاً بك يا **{user_name}** في بوت **Bac Map** 🎓\n\n"
      "🌍 **الخريطة التفاعلية للبكالوريا:**\n"
      "اضغط على الزر أدناه لفتح الخريطة والتحديات مباشرة داخل التلغرام!"
  )

  markup = types.InlineKeyboardMarkup(row_width=1)

  # زر فتح الخريطة داخل التلغرام
  web_app_info = types.WebAppInfo(WEB_APP_URL)
  btn_webapp = types.InlineKeyboardButton(
      "🌍 فتح الخريطة والتحديات", web_app=web_app_info
  )

  markup.add(btn_webapp)
  bot.send_message(
      message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown"
  )


# 2. تشغيل البوت مع حماية تلقائية ضد انقطاع الإنترنت أو أخطاء الـ Timeout
def start_bot():
  while True:
    try:
      print("البوت يعمل بنجاح ويستقبل الرسائل...")
      bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
      print(f"حدث خطأ في الاتصال: {e}")
      print("جاري إعادة المحاولة خلال 5 ثوانٍ...")
      time.sleep(5)


if __name__ == "__main__":
  # تشغيل السيرفر الوهمي في الخلفية
  keep_alive()
  # تشغيل البوت
  start_bot()
