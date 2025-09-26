import telebot
from model import get_class
import os

bot = telebot.TeleBot("TOKIT")
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f'Привет! Я бот {bot.get_me().first_name}!')
    
@bot.message_handler(content_types=['photo'])
def photo(message):
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        print(file_info)
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        res = get_class("./models/keras_model.h5", "./models/labels.txt", file_name)
        name = res[0].replace("\n", "").lower()
        proc = int(res[1] * 100)
        bot.reply_to(message, f'На изображении {name} с вероятностью {proc}%')
        os.remove(f"./{file_name}")
    else:
        bot.reply_to(message, 'Вы забыли отправить изображение!')

bot.polling()
