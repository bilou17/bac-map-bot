import os
import time
from datetime import datetime
from threading import Thread
import telebot
from telebot import types
from flask import Flask

TOKEN = "8595028279:AAGlsrY5HpwrvDFXIMRXksyrjcowwPCa-J8"
bot = telebot.TeleBot(TOKEN)

# 1. معرف حسابك الشخصي ليصلك إشعار بالزوار الجدد
ADMIN_ID = 2052554632

# 2. معلومات القناة للإشتراك الإجباري
CHANNEL_USERNAME = "@billupfollowerst"
CHANNEL_LINK = "https://t.me/billupfollowerst"
APK_POST_LINK = "https://t.me/billupfollowerst/3"  # رابط منشور التطبيق داخل القناة

WEB_APP_URL = "https://starlit-piroshki-5591a1.netlify.app"

# سيرفر Flask لمنع وضع النوم على Render
app = Flask("")

@app.route("/")
def home():
    return "BacMapDz Bot is running 24/7!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# دالة التحقق من اشتراك المستخدم في القناة
def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"خطأ في فحص الاشتراك (تأكد من رفع البوت أدمن في القناة): {e}")
        return False

# دالة إرسال إشعار للآدمين عند دخول مستخدم جديد
def notify_admin(user):
    if ADMIN_ID != 0:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            username = f"@{user.username}" if user.username else "لا يوجد"
            msg = (
                "🔔 **زائر جديد للبوت!**\n\n"
                f"👤 **الاسم:** {user.first_name} {user.last_name or ''}\n"
                f"🏷 **اليوزر:** {username}\n"
                f"🆔 **الـ ID:** `{user.id}`\n"
                f"⏰ **الوقت:** {now}"
            )
            bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"فشل إرسال إشعار للآدمين: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    
    # إرسال إشعار لك عن الزائر
    notify_admin(user)

    # 🛑 فحص الاشتراك الإجباري
    if not is_user_subscribed(user.id):
        welcome_text = (
            f"أهلاً بك يا **{user.first_name}** في بوت **Bac Map** 🎓\n\n"
            "⚠️ **عذراً، يجب عليك الاشتراك في القناة الرسمية أولاً لاستخدام البوت ويمكنك تحميل التطبيق من القناة!**\n\n"
            "اشترك في القناة ثم اضغط على زر **«تحقق من الاشتراك 🔄»**"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_channel = types.InlineKeyboardButton("📢 اشترك في القناة الآن", url=CHANNEL_LINK)
        btn_check = types.InlineKeyboardButton("🔄 تحقق من الاشتراك", callback_data="check_sub")
        markup.add(btn_channel, btn_check)
        
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")
        return

    # إذا كان مشتركاً بالفعل، تظهر له القائمة الرئيسية
    show_main_menu(message.chat.id, user.first_name)

# دالة عرض القائمة الرئيسية
def show_main_menu(chat_id, first_name):
    welcome_text = (
        f"أهلاً بك يا **{first_name}** في بوت **Bac Map** 🎓\n\n"
        "🌍 **الخريطة التفاعلية للبكالوريا:**\n"
        "يمكنك استخدام الخريطة مباشرة داخل التلغرام أو تحميل تطبيق الأندرويد ليعمل معك بدون إنترنت!"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    web_app_info = types.WebAppInfo(WEB_APP_URL)
    btn_webapp = types.InlineKeyboardButton("🌍 فتح الخريطة والتحديات", web_app=web_app_info)
    btn_app_link = types.InlineKeyboardButton("📲 تحميل تطبيق BacMap (APK)", url=APK_POST_LINK)
    
    markup.add(btn_webapp, btn_app_link)
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# زر إعادة التحقق من الاشتراك
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription_callback(call):
    if is_user_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق، مرحباً بك!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id, call.from_user.first_name)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد!", show_alert=True)

# تشغيل البوت
def start_bot():
    while True:
        try:
            print("البوت يعمل بنجاح ويستقبل الرسائل...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"حدث خطأ في الاتصال: {e}")
            time.sleep(5)

if __name__ == "__main__":
    keep_alive()
    start_bot()
