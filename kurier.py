import telebot
from telebot import types
import re
import time

TOKEN = '8132092948:AAH9POu-PTZ8u5fil-yb8MwrJUKI_lmcOys'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🛒 Сборщик", "🚲 Курьер")
    bot.send_message(message.chat.id, "Привет! На какую позицию ты претендуешь?", reply_markup=markup)
    user_data[message.chat.id] = {}

@bot.message_handler(func=lambda message: message.text in ["🛒 Сборщик", "🚲 Курьер"])
def choose_role(message):
    user_data[message.chat.id]['role'] = message.text
    bot.send_message(message.chat.id, "Отлично! Напиши, пожалуйста, сколько тебе лет", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_age)

def process_age(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, введи корректное значение (только цифрами)")
        bot.register_next_step_handler(message, process_age)
        return

    age = int(message.text)
    if age < 18:
        bot.send_message(message.chat.id, "Извини, тебе должно быть больше 18 лет, чтобы сотрудничать с Самокатом 😔")
        return

    user_data[message.chat.id]['age'] = age

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✅ Да", "❌ Нет")
    bot.send_message(message.chat.id, "Сотрудничал ли ты ранее с Самокатом?", reply_markup=markup)
    bot.register_next_step_handler(message, process_experience)

def process_experience(message):
    user_data[message.chat.id]['experience'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇷🇺 РФ", "🌍 Иностранный гражданин")
    bot.send_message(message.chat.id, "Уточни, пожалуйста, своё гражданство", reply_markup=markup)
    bot.register_next_step_handler(message, process_citizenship)

def process_citizenship(message):
    user_data[message.chat.id]['citizenship'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Екатеринбург", "Тюмень", "Челябинск", "Пермь", "Сургут", "Ижевск", "Курган", "Нижний Тагил", "Нефтеюганск", "Магнитогорск", "❌ Нет моего города")
    bot.send_message(message.chat.id, "В каком городе ты хочешь сотрудничать?", reply_markup=markup)
    bot.register_next_step_handler(message, process_city)

def process_city(message):
    if message.text == "❌ Нет моего города":
        bot.send_message(message.chat.id, "Напиши, пожалуйста, название своего города")
        bot.register_next_step_handler(message, process_city_input)
    else:
        user_data[message.chat.id]['city'] = message.text
        bot.send_message(message.chat.id, "Как тебя зовут? Напиши, пожалуйста, свое имя")
        bot.register_next_step_handler(message, process_name)

def process_city_input(message):
    if not message.text.isalpha():
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, введи корректное название города")
        bot.register_next_step_handler(message, process_city_input)
        return

    user_data[message.chat.id]['city'] = message.text
    bot.send_message(message.chat.id, "Как тебя зовут? Напиши, пожалуйста, свое имя")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    if not message.text.replace(" ", "").isalpha():
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, введи корректное имя")
        bot.register_next_step_handler(message, process_name)
        return

    user_data[message.chat.id]['name'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("📞 Номер телефона", "✍️ Ник в Telegram")
    bot.send_message(message.chat.id, "Как с тобой лучше связаться? Выбери удобный вариант:", reply_markup=markup)
    bot.register_next_step_handler(message, process_contact_choice)

def process_contact_choice(message):
    if message.text == "📞 Номер телефона":
        bot.send_message(message.chat.id, "Введите номер телефона (только цифры):", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_phone)
    elif message.text == "✍️ Ник в Telegram":
        # Спрашиваем ник и предоставляем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("✍️ Ввести ник", "🔍 Где найти ник?")
        bot.send_message(message.chat.id, "Теперь выбери «Ввести ник», если ты его знаешь, или выбери, «Где его найти», если нужна помощь:", reply_markup=markup)
        bot.register_next_step_handler(message, process_nick_choice)
    else:
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, выбери способ связи: номер телефона или ник в Telegram")
        bot.register_next_step_handler(message, process_contact_choice)

def process_nick_choice(message):
    if message.text == "🔍 Где найти ник?":
        # Предлагаем кнопки для ввода или установки ника
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("✍️ Ввести ник", "🔧 Установить ник")
        bot.send_message(
            message.chat.id,
            "🔍 Как найти свой ник в Telegram?\n\n"
            "📱 На Android:\n"
            "1. Открой Telegram\n"
            "2. Нажми ☰ (три полоски в левом верхнем углу)\n"
            "3. Перейди в «Настройки»\n"
            "4. Твой ник указан в разделе «Имя пользователя», ты можешь скопировать его прямо оттуда\n\n"
            "📱 На iPhone:\n"
            "1. Открой Telegram\n"
            "2. Перейди в «Настройки» (шестерёнка внизу)\n"
            "3. Нажми «Изм.» в правом верхнем углу\n"
            "4. Твой ник указан в разделе «Имя пользователя», ты можешь скопировать его прямо оттуда\n\n"
            "❗️Если у тебя нет ника, то ты можешь установить его в этом же разделе"
        )
        bot.send_message(message.chat.id, "Выбери, что ты хочешь сделать:", reply_markup=markup)
        bot.register_next_step_handler(message, process_nick_setup_choice)
    elif message.text == "✍️ Ввести ник":
        bot.send_message(message.chat.id, "Напиши свой ник в Telegram, начиная с @", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_telegram_nick)
    else:
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, выбери один из вариантов: «Ввести ник» или «Где найти ник?»")
        bot.register_next_step_handler(message, process_nick_choice)

def process_nick_setup_choice(message):
    if message.text == "🔧 Установить ник":
        bot.send_message(
            message.chat.id,
            "🔧 Как установить ник в Telegram?\n\n"
            "📱 На Android:\n"
            "1. Открой Telegram\n"
            "2. Нажми ☰ (три полоски в левом верхнем углу)\n"
            "3. Перейди в «Настройки»\n"
            "4. Нажми на раздел «Имя пользователя»\n"
            "5. Введи свой новый ник\n"
            "6. Нажми «Готово»\n\n"
            "📱 На iPhone:\n"
            "1. Перейди в «Настройки» (шестерёнка внизу)\n"
            "2. Нажми «Изм.» в правом верхнем углу\n"
            "3. Нажми на раздел «Имя пользователя»\n"
            "4. Введи свой новый ник\n"
            "5. Нажми «Готово»"
        )
        bot.send_message(message.chat.id, "Теперь, пожалуйста, введи свой новый ник, начиная с @")
        bot.register_next_step_handler(message, process_telegram_nick)
    elif message.text == "✍️ Ввести ник":
        bot.send_message(message.chat.id, "Напиши свой ник в Telegram, начиная с @", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_telegram_nick)
    else:
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, выбери один из вариантов: «Ввести ник» или «Установить ник»")
        bot.register_next_step_handler(message, process_nick_setup_choice)

def process_phone(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, введите корректный номер телефона (только цифры)")
        bot.register_next_step_handler(message, process_phone)
        return

    user_data[message.chat.id]['contact'] = message.text
    process_finish(message)

def process_telegram_nick(message):
    username = message.text.strip()
    if not username.startswith("@"):
        username = "@" + username

    if not re.match(r"^@[A-Za-z0-9_]{5,}$", username):
        bot.send_message(message.chat.id, "⭕️ Пожалуйста, введи корректный ник в Telegram")
        bot.register_next_step_handler(message, process_telegram_nick)
        return

    user_data[message.chat.id]['contact'] = username
    process_finish(message)

def process_finish(message):
    bot.send_message(message.chat.id, "✅ Спасибо! Скоро с вами свяжется рекрутер, хорошего дня!")

    user = user_data[message.chat.id]
    bot.send_message('443359121', f"Новая анкета:\nРоль: {user['role']}\nВозраст: {user['age']}\nРанее сотрудничал с Самокатом: {user['experience']}\nГражданство: {user['citizenship']}\nГород: {user['city']}\nИмя: {user['name']}\nКонтакт: {user['contact']}")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🔄 Пройти опрос заново")
    bot.send_message(message.chat.id, "Если хочешь пройти опрос заново, нажми на кнопку ниже", reply_markup=markup)
    user_data.pop(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "🔄 Пройти опрос заново")
def restart_survey(message):
    start(message)

# Запускаем бота только один раз
bot.polling(none_stop=True)
