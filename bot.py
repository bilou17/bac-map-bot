import telebot
from telebot import types

TOKEN = "8595028279:AAGlsrY5HpwrvDFXIMRXksyrjcowwPCa-J8"
bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = "https://lustrous-raindrop-86f3e6.netlify.app"

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
    btn_webapp = types.InlineKeyboardButton("🌍 فتح الخريطة والتحديات", web_app=web_app_info)
    
    markup.add(btn_webapp)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

if __name__ == '__main__':
    print("البوت يعمل بنجاح...")
    bot.polling(none_stop=True)