import os
import telebot
from flask import Flask

# تشغيل سيرفر وهمي لكي يظل موقع Render مشغلاً للبوت بدون توقف
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

# التوكن الخاص ببوتك
API_TOKEN = '9259122635:AAH713kXaZmQHepu7wxgPYOQeAh8cXxTTBk'
bot = telebot.TeleBot(API_TOKEN)

# 🛑 قائمة الكلمات المحظورة الشاملة
BAD_WORDS = [
    # عبارات أرسلتها أنت ومزيجاتها
    'كسمك', 'كسم أمك', 'كسم أبوك', 'ابن المتناكة', 'ابن الشرموطة', 'ابن الوسخة', 
    'يا ابن المتناكة', 'يا ابن الشرموطة', 'متناك', 'متناك في الطيز', 'نيكك', 'هنيكك', 
    'هنيك أمك', 'هنيكك في الطيز', 'زبي في كسك', 'زبي في طيزك', 'شرموطة', 'قحبة', 
    'لبوة', 'عرص', 'خول', 'ديوث', 'منيك', 'كس أمك', 'طيزك', 'زب أمك', 'زب أبوك', 
    'نيك أمك', 'نيكك نيك', 'يا خرا', 'يا خرة', 'يا ابن الخرا', 'يا وسخ', 'يا نجس', 
    'يا قذر', 'يا كلب', 'يا ابن الكلب', 'يا حيوان', 'يا حمار', 'يا تيس', 'يا ابن التيس', 
    'كسمك يا عرص', 'كسمك يا خول', 'كسمك يا شرموطة', 'ابن المتناكة يا ديوث', 
    'يا متناك يا عرص', 'هنيكك نيك يا خول', 'زبي في بقك', 'زبي في طيزك يا شرموطة',
    
    # عبارات وكلمات إضافية للحماية
    'خاص', 'تعالي خاص', 'وادلعها', 'نسهر', 'منيوك', 'كس', 'زب', 'طيز', 'يا خول', 'يا معرص', 'نتناك'
]

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    if message.text:
        # تنظيف النص وفحصه
        text = message.text.strip().lower()
        
        # التحقق إذا كان النص يحتوي على أي كلمة محظورة
        if any(word in text for word in BAD_WORDS):
            try:
                # حذف الرسالة فوراً
                bot.delete_message(message.chat.id, message.message_id)
                
                # إرسال تحذير للعضو (يمكنك مسح هذا السطر إذا كنت تريد الحذف بصمت)
                bot.send_message(message.chat.id, f"⚠️ عذراً @{message.from_user.username}، الكلمات المزعجة أو البذيئة ممنوعة هنا!")
            except Exception as e:
                print(f"Error: {e}")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    from threading import Thread
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
