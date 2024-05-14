import configparser
import random
import os
import time
import telebot
from telebot import types
from PIL import Image

config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(config['Telegram']['token'])


@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    btn1 = types.KeyboardButton('Далее')
    markup.add(btn1)
    bot.send_message(id, f' Привет, {message.from_user.first_name}, перед началом игры в супер крестики-нолики рекомендую ознакомиться <a href="https://telegra.ph/Super-krestiki-noliki-05-10">руководством</a>! Когда закончишь, просто нажми кнопку "Далее"',parse_mode='html',reply_markup=markup)

@bot.message_handler(commands=['leave'])
def leave(message):
        id = message.chat.id
        user = configparser.ConfigParser()
        user.read(f'users/{id}.ini')
        code = user['Lobby']['code']
        
        lobby = configparser.ConfigParser()
        lobby.read(f'lobbies/{code}.ini')
        admin = lobby['Members']['first']
        
        try:
            id2 = int(lobby["Members"]['second'])
        except KeyError:
            id2=0
        
        if id == int(admin):
            os.remove(f'lobbies/{code}.ini')
            os.remove(f'users/{id}.ini')
            bot.send_message(id, 'Лобби было удалено! Вы будете возвращенны в главное меню через пару секунд!')
            if id2>0:
                os.remove(f'users/{id2}.ini')
                bot.send_message(id2, 'Лобби было удалено! Вы будете возвращенны в главное меню через пару секунд!')
            else: None
            time.sleep(2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
            btn1 = types.KeyboardButton('Войти')
            btn2 = types.KeyboardButton('Создать')
            markup.add(btn1,btn2)
            bot.send_message(id, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
            if id2>0:
                bot.send_message(id2, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
            else: None
        else:
            os.remove(f'users/{id}.ini')
            lobby.remove_option('Members', 'second')
            second_us = lobby['Members']['second_us']
            lobby.remove_option('Members', 'second_us')
            lobby.write(open(f'lobbies/{code}.ini', 'w'))
            bot.send_message(admin, f'Игрок @{second_us} покинул ваше лобби!')
            us2 = lobby['Members']['first_us']
            bot.send_message(id, f'Ты успешно покинул лобби игрока @{us2}!')
            time.sleep(2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
            btn1 = types.KeyboardButton('Войти')
            btn2 = types.KeyboardButton('Создать')
            markup.add(btn1,btn2)
            bot.send_message(id, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
            id2 = lobby['Members']['first']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1=types.KeyboardButton('Покинуть ❌')
            btn2 = types.KeyboardButton('Начать ✅')
            markup.add(btn1)
            bot.send_message(id2, f'Лобби перезагружен успешно, код лобби: <b>{code}</b>. Введя этот код в "Войти", твой друг присоединится к твоему лобби и вы сможете начать игру!',parse_mode='html',reply_markup=markup)
    
    
@bot.message_handler()
def message(message):
    id = message.chat.id
    
    
    if message.text == 'Далее':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        btn1 = types.KeyboardButton('Войти')
        btn2 = types.KeyboardButton('Создать')
        markup.add(btn1,btn2)
        bot.send_message(id, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
    
    
    elif message.text == 'Войти':
        bot.send_message(id, 'Введи код лобби, который сообщил тебе твой друг')
    
    
    elif message.text == 'Покинуть ❌':
        user = configparser.ConfigParser()
        user.read(f'users/{id}.ini')
        code = user['Lobby']['code']
        
        lobby = configparser.ConfigParser()
        lobby.read(f'lobbies/{code}.ini')
        admin = lobby['Members']['first']
        
        try:
            id2 = int(lobby["Members"]['second'])
        except KeyError:
            id2=0
        
        if id == int(admin):
            os.remove(f'lobbies/{code}.ini')
            os.remove(f'users/{id}.ini')
            bot.send_message(id, 'Лобби было удалено! Вы будете возвращенны в главное меню через пару секунд!')
            if id2>0:
                os.remove(f'users/{id2}.ini')
                bot.send_message(id2, 'Лобби было удалено! Вы будете возвращенны в главное меню через пару секунд!')
            else: None
            time.sleep(2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
            btn1 = types.KeyboardButton('Войти')
            btn2 = types.KeyboardButton('Создать')
            markup.add(btn1,btn2)
            bot.send_message(id, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
            if id2>0:
                bot.send_message(id2, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
            else: None
        else:
            os.remove(f'users/{id}.ini')
            lobby.remove_option('Members', 'second')
            second_us = lobby['Members']['second_us']
            lobby.remove_option('Members', 'second_us')
            lobby.write(open(f'lobbies/{code}.ini', 'w'))
            bot.send_message(admin, f'Игрок @{second_us} покинул ваше лобби!')
            us2 = lobby['Members']['first_us']
            bot.send_message(id, f'Ты успешно покинул лобби игрока @{us2}!')
            time.sleep(2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
            btn1 = types.KeyboardButton('Войти')
            btn2 = types.KeyboardButton('Создать')
            markup.add(btn1,btn2)
            bot.send_message(id, 'Чтобы начать играть, нужно создать или войти в уже существующее лобби',parse_mode='html',reply_markup=markup)
            id2 = lobby['Members']['first']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1=types.KeyboardButton('Покинуть ❌')
            btn2 = types.KeyboardButton('Начать ✅')
            markup.add(btn1)
            bot.send_message(id2, f'Лобби перезагружен успешно, код лобби: <b>{code}</b>. Введя этот код в "Войти", твой друг присоединится к твоему лобби и вы сможете начать игру!',parse_mode='html',reply_markup=markup)
    
    
    elif message.text == 'Создать':
        code = random.randint(1000, 9999)
        code = str(code).zfill(4)
        
        lobby = configparser.ConfigParser()
        lobby.add_section('Members')
        lobby.set('Members', 'first', str(id))
        lobby.set('Members', 'first_us', str(message.from_user.username))
        lobby.write(open(f'lobbies/{code}.ini', 'w'))
        
        user = configparser.ConfigParser()
        user.add_section('Lobby')
        user.set('Lobby', 'code', code)
        user.write(open(f'users/{id}.ini','w'))
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1=types.KeyboardButton('Покинуть ❌')
        btn2 = types.KeyboardButton('Начать ✅')
        markup.add(btn1)
        bot.send_message(id, f'Лобби создан успешно, код лобби: <b>{code}</b>. Введя этот код в "Войти", твой друг присоединится к твоему лобби и вы сможете начать игру!',parse_mode='html',reply_markup=markup)
    
                
    else:
        text = message.text
        try:
            text = int(text)
        except ValueError:
            bot.send_message(id,'Я тебя не понимаю( Попробуй еще раз!')
            
        if os.path.exists(f'lobbies/{text}.ini'):
            lobby = configparser.ConfigParser()
            lobby.read(f'lobbies/{text}.ini')
            lobby.set('Members', 'second', str(id))
            lobby.set('Members', 'second_us', message.from_user.username)
            lobby.write(open(f'lobbies/{text}.ini', 'w'))
            
            id2=lobby['Members']['first']
            us2 = lobby['Members']['first_us']
            us = lobby['Members']['second_us']
            
            user = configparser.ConfigParser()
            user.read(f'users/{id2}.ini')
            code = user['Lobby']['code']
            
            user = configparser.ConfigParser()
            user.add_section('Lobby')
            user.set('Lobby', 'code', code)
            user.write(open(f'users/{id}.ini','w'))
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)            
            btn1=types.KeyboardButton('Покинуть ❌')
            btn2 = types.KeyboardButton('Начать ✅')
            markup.add(btn1)
            markup2.add(btn1, btn2)
            bot.send_message(id, f'Ты успешно подключился к лобби игрока @{us2}, ожидаем начала игры...',parse_mode='html',reply_markup=markup)
            bot.send_message(id2, f'К твоему лобби подключился игрок @{us}, чтобы начать игру нажми кнопку "Начать ✅"',parse_mode='html',reply_markup=markup2)
        else:
            bot.send_message(id, f'Упс! Лобби с кодом {text} не существует( Попробуй ещё раз или уточни у своего друга правильный код!')


def xo(string,a,b,c):
    x=0
    y=0
    # Открываем основное изображение
    main_image = Image.open(string)

    # Открываем изображение, которое хотим разместить
    if a==1:
        small_image = Image.open('x.png')
    elif a==2:
        small_image = Image.open('o.png')
    else:
        None
        
    
    if b==1:
        x=5
        y=5
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==2:
        x=5+150+8+4+8
        y=5
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==3:
        x=163+166+8+8
        y=5
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==4:
        x=5
        y=5+150+8+4+8
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==5:
        x=5+150+8+4+8
        y=5+150+8+4+8
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==6:
        x=163+166+8+8
        y=5+150+8+4+8
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==7:
        x=5
        y=163+166+8+8
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==8:
        x=5+150+8+4+8
        y=163+166+8+8
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
    elif b==9:
        x=163+166+8+8
        y=163+166+8+8
        if c==1:
            x=x
        elif c==2:
            x=x+51
        elif c==3:
            x=x+102
        elif c==4:
            y=y+51
        elif c==5:
            x=x+51
            y=y+51
        elif c==6:
            x=x+102
            y=y+51
        elif c==7:
            y=y+102
        elif c==8:
            x=x+51
            y=y+102
        elif c==9:
            x=x+102
            y=y+102
        
    
    # Задаем координаты, где будет размещено маленькое изображение
    position = (x, y)

    # Размещаем маленькое изображение на большом
    main_image.paste(small_image, position)

    # Сохраняем результат
    main_image.save(string)

bot.polling(none_stop=True, interval=0)