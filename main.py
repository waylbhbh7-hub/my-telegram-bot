import os
import telebot
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

API_TOKEN = '9259122635:AAH713kXaZmQHepu7wxgPYOQeAh8cXxTTBk'
bot = telebot.TeleBot(API_TOKEN)

# قائمة الكلمات المفردة لتسهيل الفحص الذكي
BAD_WORDS = [
    'كسمك', 'كسم', 'أمك', 'امك', 'أبوك', 'ابوك', 'المتناكة', 'المتناكه', 'الشرموطة', 'الشرموطه', 'الوسخة', 'الوسخه',
    'متناك', 'نيكك', 'هنيكك', 'انيكك', 'نيك', 'شرموطة', 'شرموطه', 'قحبة', 'قحبه', 'لبوة', 'لبوه', 'عرص', 'خول', 
    'ديوث', 'منيك', 'طيزك', 'طيز', 'زب', 'خرا', 'خرة', 'خره', 'وسخ', 'نجس', 'قذر', 'كلب', 'حيوان', 'حمار', 'تيس',
    'خاص', 'وادلعها', 'نسهر', 'منيوك', 'كس', 'يا خول', 'يا معرص', 'نتناك', 'خخخ'
]

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    if message.text:
        # تقسيم النص إلى كلمات منفصلة للفحص الدقيق
        message_words = message.text.strip().split()
        
        for word in message_words:
            # تنظيف الكلمة من العلامات الزائدة وفحصها
            clean_word = word.strip(".,!@#$%" * "()_+={}[]|\\:;\"'<>,.?/~`").lower()
            
            if clean_word in BAD_WORDS:
                try:
                    # حذف الرسالة فوراً
                    bot.delete_message(message.chat.id, message.message_id)
                    # إرسال تحذير
                    bot.send_message(message.chat.id, f"⚠️ عذراً @{message.from_user.username}، الكلمات البذيئة ممنوعة هنا!")
                    break # التوقف بعد الحذف
                except Exception as e:
                    print(f"Error: {e}")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    from threading import Thread
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
