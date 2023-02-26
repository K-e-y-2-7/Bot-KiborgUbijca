import os
import random
import time

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


class Greatings:
    greatings1 = {1 : 'Привіт!',
        2 : "Вітаю!",
        3 : 'Моє шанування!',
        4 : 'Здрастуйте',
        5 : 'Радий вітати!',
        6 : 'Здоровенькі були!',
        7 : 'Слава Україні!',
        8 : "Доброго здоров'я!",}

    greatings2 = {1 : 'З добрим ранком!',
        2 : 'Добрий ранок!',
        3 : 'Добрий день!',
        4 : 'День добрий!',
        5 : 'Доброго дня!',
        6 : "Добридень!",
        7 : 'Добрий вечір!',
        8 : 'Вечір добрий!',
        9 : 'Доброї ночі!'}

    def _random_greatings(self):
        '''The function return a some random greatings'''
        number = random.randint(0, 1)
        if number:
            return self.greatings1.get(random.randint(1, 8))
        else:
            named_tuple = time.localtime()  # get struct_time
            time_string = time.strftime("%H:%M:%S", named_tuple)
            if '06:00:00' <= time_string < '12:00:00':
                return self.greatings2.get(1)
            elif '12:00:00' <= time_string < '18:00:00':
                return self.greatings2.get(random.randint(2, 6))
            elif '18:00:00' <= time_string < '24:00:00':
                return self.greatings2.get(random.randint(7, 8))
            elif '24:00:00' >= time_string < '06:00:00':
                return self.greatings2.get(9)

    def get_greatings(self):
        return self._random_greatings()


base_text = ('хто ти?', 'who are you?')
def create_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Random number 🎰')
    item2 = types.KeyboardButton('How are you?')
    item3 = types.KeyboardButton('What is my name?')

    markup.add(item1, item2, item3)

    return markup

def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("I'm good.", callback_data='good')
    item2 = types.InlineKeyboardButton("I'm bad", callback_data='bad')

    markup.add(item1, item2)

    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome_kim.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = create_reply_keyboard()
    greating = Greatings()
    bot.send_message(message.chat.id, f'{greating.get_greatings()}', parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def talk(message):
    if message.chat.type == 'private':
        pass
    if message.text == 'Random number 🎰':
        bot.send_message(message.chat.id, f'Random number is:')
        bot.send_message(message.chat.id, f'🎲')
        rand = random.randint(1, 100)
        bot.send_message(message.chat.id, f'{rand}')
        if rand < 50:
            stic = open('static/kazino.webp', 'rb')
            bot.send_sticker(message.chat.id, stic)
    elif message.text == 'How are you?':
        markup = create_inline_keyboard()
        bot.send_message(message.chat.id, "I'm fine. Killing.", reply_markup=markup)
    elif message.text == 'What is my name?':
        bot.send_message(message.chat.id, f'The name of the target: {message.from_user.first_name}, {message.from_user.last_name}')
    elif message.text == 'photo':
        with open('kiborg.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    elif message.text.lower() in base_text:
        bot.send_message(message.chat.id, f"I'm kiborg ubijca")
    else:
        bot.send_message(message.chat.id, 'I dont understand you, human.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "It's great!")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "It's too sad!")

    except Exception as e:
        print(repr(e))


# Run
bot.polling(none_stop=True)