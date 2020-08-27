import telebot
import wikipedia
from telebot import types
from configparser import ConfigParser
from config import TOKEN, LANGUAGE

wikipedia.set_lang(LANGUAGE)

config = ConfigParser()
config.read("locale.ini")
language = config.get("LOCALE", "language") # устанавливаем локаль
section = language.upper()
config.read(f"locales/{language}/{language}.ini") # читаем файл строковых данных

GREETINGS = config.get(section, "GREETINGS")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=GREETINGS,)


@bot.message_handler(content_types=['text',])
def get_word(message):
    if(message.text.startswith('Что такое',0,9)):
        try:
            search = wikipedia.page(message.text.replace('Что такое ',''))
            answer = search.content[:300]
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(
                text='Ссылка на статью',
                url=search.url
            )
            keyboard.add(button)
            bot.send_message(
            chat_id=message.chat.id,
            text=answer,
            reply_markup=keyboard
        )
        except wikipedia.exceptions.DisambiguationError as error:
            bot.send_message(
                chat_id=message.chat.id,
                text=error
            )

bot.polling()