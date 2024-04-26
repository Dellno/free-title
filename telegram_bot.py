# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import Application, CommandHandler, filters, MessageHandler
import requests
import json

BOT_TOKEN = "7199575511:AAEdx0B8Bsw_r3XmfRjEnunuALwB7nbLClk"
API_HOST = "http://127.0.0.1:5000/api/"

async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот сайта free-title. пропиши команду /update <токен> чтобы узнать о своих любимых проектах",
    )


async def help_command(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот сайта free-title. пропиши команду /update <токен> чтобы узнать о своих любимых проектах",
    )


async def echo(update, context):
    print(update.message.text.split(" "))
    if len(update.message.text.split(" ")) == 3 and update.message.text.split(" ")[0] == "/update":
        response = requests.get(API_HOST + update.message.text.split(" ")[2])
        a = json.loads(response.json())
        for i in a:
            await update.message.reply_text(f"игра: {i['name']} \n афтор: {i['author']} \n описаниее : \n {i['content']}")


def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    print("start")
    run_bot()
    print("end")
