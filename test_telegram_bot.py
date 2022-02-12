import telebot

# 5226042274:AAHgeq4GlMuOweHCP29FZsshQGzID3O7gKQ
# bot = telebot.TeleBot("5226042274:AAHgeq4GlMuOweHCP29FZsshQGzID3O7gKQ", parse_mode=None)
#
#
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
#
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#
#
# bot.infinity_polling()


bot = telebot.TeleBot("5226042274:AAHgeq4GlMuOweHCP29FZsshQGzID3O7gKQ")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Hello':
        bot.reply_to(message, 'Hello Bot Creator!')
        #     bot.reply_to(message, message.text)
    elif message.text == 'Hi':
        bot.reply_to(message, 'Hi again, The indians bot creator!')


bot.infinity_polling()
