# -*- coding: utf-8 -*-
import telebot
from telebot import types
import logging 
import requests 
import ast
from db import Database
import sqlite3
 
st_lang = "ru"

text_1 = "Вы работник технической поддержки молящихся. Ваша задача отвечать на звонки молящихся и помогать им. Однако, по какой-то причине, вам стали поступать звонки из церкви. Вы приняли решение позвонить в техническую поддержку технической поддержки молящихся. \n—Что у вас там? Почему ко мне стали поступать молитвы из церкви? Этим должен заниматься “Отдел церковных молитв”, почему их перенаправляют мне?!\n—Какая-то техническая ошибка. Сейчас разберусь.\nЧерез пару минут звонок затих. Через некоторое время ко мне снова начали поступать звонки одиноко молящихся. Приняв первый, я понял, что это просто утренняя молитва и помочь я ничем не могу. Когда я ответил на второй, в меня полетел спам из всех возможных молитв. О даровании детей, о душевном спокойствии, за врагов, за все. Что именно хочет этот человек? Я отправил помощника посмотреть что там происходит. \n—Пожар. Кажется, он уже долго ждет пожарных, которые застряли на дороге. \nЯ пробудил совесть у всех водителей, которые не пропускали спасительные машины и подарил молящемуся храбрость самостоятельно спасти своего ребенка.\nПосле того, как мой помощник убедился, что все завершилось благополучно, я принял следующий звонок. \nНа этот раз не было текста молитвы, но была четкая просьба. “Господи, останови эту войну”. \nЯ-то могу остановить войну, но что там с Божьим замыслом?"
text_2 = "1. Направить молитвы в компетентный отдел, чтоб они решили вопрос, не нарушая Божьего замысла."
text_3 = "2. Ничто не может нарушить Божий замысел. На то он и Божий. Помочь молящемуся."
text_4 = "Я направил запрос в компетентный отдел и принял следующий вызов.\n—...молю Тебя, Матерь Господа нашего Иисуса Христа, да пусть Всевышний пошлет мне да моему супругу чадо. Да дарует мне Он плод чрева моего. Перемени скорбь в душе моей, да ниспошли мне радость материнства. Восславляю Тя во все дни жизни моей! Аминь!"
text_5 = "Не в моих силах остановить целую войну, но я позаботился об успешной эвакуации молящегося и его семьи. \nСледующий звонок: \n—...молю Тебя, Матерь Господа нашего Иисуса Христа, да пусть Всевышний пошлет мне да моему супругу чадо. Да дарует мне Он плод чрева моего. Перемени скорбь в душе моей, да ниспошли мне радость материнства. Восславляю Тя во все дни жизни моей! Аминь!"
text_6 = "1. Даровать дитя"
text_7 = "2. Намекнуть об усыновлении"
text_8 = "Какая милая женщина и как искренне хочет ребенка! Я позаботился, чтоб ей и ее суженному удалось зачать дитя.\nЗвонок из соседнего отдела:\n—Не создавай нам проблем! Ты хоть с судьбой ее ознакомился? Она должна была воспитать чужое дитя!"
text_9 = "Проверив судьбу женщины, я позаботился о том, чтоб вся реклама в интернете намекала ей на усыновление.\nПолучил письмо-одобрение и статус “Лучший работник технической поддержки”.\nКонец!"
text_10 = "Какая милая женщина и как искренне хочет ребенка! Я позаботился, чтоб ей и ее суженному удалось зачать дитя.\nЗвонок от начальства:\n—Серьезно? Ты доставляешь проблемы другим отделам, сам не мог решить что делать с бедолагой на войне? Теперь еще и это! Ее судьба – воспитать другого ребенка! Уволен!\nКонец!"
text_11 = "Проверив судьбу женщины, я позаботился о том, чтоб вся реклама в интернете намекала ей на усыновление.\nПозвонили из соседнего отдела:\n—Возвращаем тебе запрос от молящегося на войне. Сам разберись, у нас так дел выше крыши!"
text_12 = "Я хоть и не лучший работник, но начальство мной вполне довольно. У кого не бывает ошибок? А работа мне моя нравится.\nКонец!"

bot = telebot.TeleBot("5705495315:AAEo1whCtR2KfqWmxi1uiY51ZkpR1UovPX4")
db = Database('database.db')

logging.basicConfig( 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO, 
) 
logger = logging.getLogger(__name__) 

API_KEY = "AQVN3CW8GaV7U-DsUnvJoVUsS8cn6y7SkfA1AZMK" 

def yandex_translate_text(texts, target_language):
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    response_dict = ast.literal_eval(response.text)
    result = []
    if "translations" in response_dict:
        logger.debug(f"response_dict={response_dict}")
        result = [translation.get('text', "") for translation in response_dict['translations']]
    else:
        logger.error(f"возникла ошибка API, был возвращен ответ: {response_dict}")
    return result
 

# Команда /start
@bot.message_handler(commands=['start']) 
def start_quiz(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, st_lang)
    lang = db.check_language(message.from_user.id)
    result = yandex_translate_text("Добро пожаловать! Введите /play для начала игры, для смены языка напишите /languages. Для выбора варианта ответа введите цифру, например 1 или 2.", lang[0])
    bot.send_message(message.chat.id, result)

# Команда /continue
@bot.message_handler(commands=['continue']) 
def continue_quiz(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, st_lang)
    lang = db.check_language(message.from_user.id)
    stage = db.check_stage(message.chat.id)
    if stage[0] == '0':
        result = yandex_translate_text("Продолжить нельзя, начните игру сначала. Введите /play для начала игры.", lang[0])
        bot.send_message(message.chat.id, result)
    elif stage[0] == '1':
        quiz = text_1
        result = yandex_translate_text(quiz, lang[0])
        bot.send_message(message.chat.id, result)
        quiz = text_2
        result = yandex_translate_text(quiz, lang[0])
        bot.send_message(message.chat.id, result)
        quiz = text_3
        result = yandex_translate_text(quiz, lang[0])
        bot.send_message(message.chat.id, result)
    elif stage[0] == '11':
        result = yandex_translate_text(text_4, lang[0])
        bot.send_message(message.chat.id, result)
        result = yandex_translate_text(text_6, lang[0])
        bot.send_message(message.chat.id, result)
        result = yandex_translate_text(text_7, lang[0])
        bot.send_message(message.chat.id, result)
    elif stage[0] == '12':
        result = yandex_translate_text(text_5, lang[0])
        bot.send_message(message.chat.id, result)
        result = yandex_translate_text(text_6, lang[0])
        bot.send_message(message.chat.id, result)
        result = yandex_translate_text(text_7, lang[0])
        bot.send_message(message.chat.id, result)
    else:
        result = yandex_translate_text("Неправильное значение стадии.", lang[0])
        bot.send_message(message.chat.id, result)
        

# Команда /play начинает квест 
@bot.message_handler(commands=['play']) 
def play_quiz(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, st_lang)
    lang = db.check_language(message.from_user.id)
    quiz = text_1
    result = yandex_translate_text(quiz, lang[0])
    bot.send_message(message.chat.id, result)
    quiz = text_2
    result = yandex_translate_text(quiz, lang[0])
    bot.send_message(message.chat.id, result)
    quiz = text_3
    result = yandex_translate_text(quiz, lang[0])
    bot.send_message(message.chat.id, result)
    stage = "1"
    db.set_stage(message.from_user.id, stage)

# Команда /help
@bot.message_handler(commands=['help']) 
def help_quiz(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, st_lang)
    lang = db.check_language(message.from_user.id)
    result = yandex_translate_text("Введите /play для начала игры, /continue для продолжения игры. Введите /languages для смены языка. Для выбора ответа введите цифру, например 1 или 2.", lang[0])
    bot.send_message(message.chat.id, result)

# Обработка ответов пользователя 
@bot.message_handler(func=lambda message: True) 

def handle_answer(message): 
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, st_lang)
    lang = db.check_language(message.from_user.id)
    if message.text == "/languages": 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Русский")
        btn2 = types.KeyboardButton("English")
        btn3 = types.KeyboardButton("Português")
        btn4 = types.KeyboardButton("Español")
        btn5 = types.KeyboardButton("Deutsch")
        btn6 = types.KeyboardButton("Lingua latina")
        btn7 = types.KeyboardButton("Қазақша")
        btn8 = types.KeyboardButton("Esperanto")
        btn9 = types.KeyboardButton("עברית")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        result = yandex_translate_text("Выберите язык.", lang[0])
        bot.send_message(message.from_user.id, result, reply_markup=markup)
    elif message.text == "Русский":
        new_lang = "ru"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "English":
        new_lang = "en"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "Português":
        new_lang = "pt"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "Español":
        new_lang = "es"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "Deutsch":
        new_lang = "de"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "Lingua latina":
        new_lang = "la"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "Қазақша":
        new_lang = "kk"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "Esperanto":
        new_lang = "eo"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "עברית":
        new_lang = "he"
        db.change_lang(message.from_user.id, new_lang)
        delmark = telebot.types.ReplyKeyboardRemove()
        result = yandex_translate_text("Отлично, язык выбран.", new_lang)
        bot.send_message(message.chat.id, result, reply_markup=delmark) 
    elif message.text == "1":
        stage = db.check_stage(message.chat.id)
        if stage[0] == '1':
            result = yandex_translate_text(text_4, lang[0])
            bot.send_message(message.chat.id, result)
            result = yandex_translate_text(text_6, lang[0])
            bot.send_message(message.chat.id, result)
            result = yandex_translate_text(text_7, lang[0])
            bot.send_message(message.chat.id, result)
            stage = "11"
            db.set_stage(message.chat.id, stage)
        elif stage[0] == "11":
            result = yandex_translate_text(text_10, lang[0])
            bot.send_message(message.chat.id, result)
            stage = "0"
            db.set_stage(message.chat.id, stage)
        elif stage[0] == "12":
            result = yandex_translate_text(text_8, lang[0])
            bot.send_message(message.chat.id, result)
            result = yandex_translate_text(text_12, lang[0])
            bot.send_message(message.chat.id, result)
            stage = "0"
            db.set_stage(message.chat.id, stage)
        else:
            result = yandex_translate_text("Я вас не понимаю. Повторите, пожалуйста.", lang[0])
            bot.send_message(message.chat.id, result) 
    elif message.text == "2":
        stage = db.check_stage(message.chat.id)
        if stage[0] == "1":
            result = yandex_translate_text(text_5, lang[0])
            bot.send_message(message.chat.id, result)
            result = yandex_translate_text(text_6, lang[0])
            bot.send_message(message.chat.id, result)
            result = yandex_translate_text(text_7, lang[0])
            bot.send_message(message.chat.id, result)
            stage = "12"
            db.set_stage(message.chat.id, stage)
        elif stage[0] == "11":
            result = yandex_translate_text(text_11, lang[0])
            bot.send_message(message.chat.id, result)
            result = yandex_translate_text(text_12, lang[0])
            bot.send_message(message.chat.id, result)
            stage = "0"
            db.set_stage(message.chat.id, stage)
        elif stage[0] == "12":
            result = yandex_translate_text(text_9, lang[0])
            bot.send_message(message.chat.id, result)
            stage = "0"
            db.set_stage(message.chat.id, stage)
        else:
            result = yandex_translate_text("Я вас не понимаю. Повторите, пожалуйста.", lang[0])
            bot.send_message(message.chat.id, result) 
    else:
        result = yandex_translate_text("Я вас не понимаю. Повторите, пожалуйста.", lang[0])
        bot.send_message(message.chat.id, result) 
bot.polling()