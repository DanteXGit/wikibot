import telebot
import wikipedia
from telebot import types
from config import TOKEN

wikipedia.set_lang('ru')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет!\nЯ-бот,который поможет тебе найти информацию из Википедии. Чтобы спросить у меня напиши:\n"Что такое <слово>"',)


@bot.message_handler(content_types=['text',])
def get_word(message):
    message.text = message.text.lower()
    if(message.text.startswith('что такое',0,9) or message.text.startswith('кто такой',0,9)):
        try:
            message.text = message.text.replace('кто такой ','')
            message.text = message.text.replace('что такое ','')
            search = wikipedia.page(message.text)
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