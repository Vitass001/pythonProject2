import random
import telebot
from telebot import types


token = '2084950457:AAFHmbs-Sn6H3plEe0bh0A2YZ1kr7G04YVA'

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])

def first(message):

    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.add('Так')
    bot.send_photo(message.chat.id, open('hi.jpg', 'rb'))
    send = bot.send_message(message.chat.id,'Привіт🦖Я динозавр Dinorrr, який живе у IT світі👾' \
               '\nПропоную тобі пройти Дііінотест на знання англійської🏴' \
               '\n󠁧󠁢󠁥󠁮󠁧󠁿Ти зі мною?⬇️', reply_markup=keyboard)
    bot.register_next_step_handler(send,main_func)


def main_func(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                        row_width=2)
    button1 = types.KeyboardButton(text='Test')
    buttons.add(button1)
    bot.send_photo(message.chat.id, open('CELECT.jpg', 'rb'))
    button_from_user = bot.send_message(message.chat.id,text = 'Вибирай тест ☺️',
                                        reply_markup=buttons)
    bot.register_next_step_handler(button_from_user, func_after_main)


def func_after_main(message):
    if message.text == 'Test':
        func_for_test(message)


def func_for_test(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                        row_width=2)
    button3 = types.KeyboardButton(text='Start')
    buttons.add(button3)
    button_from_user = bot.send_message(message.chat.id, text='Цей тест розраховнаий на 10 хв\n Стартуємо!',
                                        reply_markup=buttons)
    bot.register_next_step_handler(button_from_user, func_start_test)


def func_start_test(message):
    if message.text == 'Start':
        bot.send_photo(message.chat.id, open('lets_s.jpg', 'rb'))
        func_test(message)


def func_test(message):
    global dct
    global keys
    global num
    global cor_ans
    cor_ans = 0
    dct = {}
    with open('answer.txt', 'r', encoding="utf-8") as file:
        q = 0
        for i in file.readlines():
            lst = i.strip().split('*')
            dct[lst[0]] = lst[1].strip('[]').split(",")
            q = q + 1
            if q == 30:
                break
    num = 1
    keys = list(dct.keys())
    func_for_random(message)


def func_for_random(message):
    global qes
    qes = random.choice(keys)
    if num == 20:
        bot.send_photo(message.chat.id, open('end.jpg', 'rb'))
        bot.send_message(message.chat.id, text='Ви пройшли тест!')
        print('Ви пройшли тест')
        func_the_end(message)
    else:
        func_start(message)


def func_start(message):
    global num
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    button1 = types.KeyboardButton(text=f'{dct[qes][0]}')
    button2 = types.KeyboardButton(text=f'{dct[qes][1]}')
    button3 = types.KeyboardButton(text=f'{dct[qes][2]}')
    buttons.add(button1, button2, button3)
    button_from_user = bot.send_message(message.chat.id, f'{num}){qes}',reply_markup=buttons)
    num = num + 1
    bot.register_next_step_handler(button_from_user,func_for_perevirka)

def func_for_perevirka(message):
    keyboard = types.ReplyKeyboardMarkup(False)
    global cor_ans
    if message.text == dct[qes][3]:
        cor_ans  = cor_ans + 1
        bot.send_photo(message.chat.id, open('TRUE.jpg', 'rb'))
        bot.send_message(message.chat.id, text=f'Відповіть {dct[qes][3]} правильна! ✅')
        func_for_random(message)
    else:
        bot.send_photo(message.chat.id, open('ERROR.jpg', 'rb'))
        bot.send_message(message.chat.id, text=f'Відповіть {message.text} неправильна! ❌\n'
                                               f'Правильна відповідь: {dct[qes][3]}')
        func_for_random(message)

def func_the_end(message):
    if cor_ans < 5:
        lvl = 'A1'
    elif cor_ans >= 5 and cor_ans <= 9:
        lvl = 'A2'
    elif cor_ans >= 10 and cor_ans <= 14:
        lvl = 'B1'
    elif cor_ans >= 15 and cor_ans <= 19:
        lvl = 'B2'
    elif cor_ans == 20:
        lvl = 'C1'
    bot.send_message(message.chat.id, text=f'\nПравильних відповідей: {cor_ans} з {num}\n'
                                           f'Ваш рівень: {lvl}')
    main_func(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
    