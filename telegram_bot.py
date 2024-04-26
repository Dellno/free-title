# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import Application, CommandHandler, filters, MessageHandler

BOT_TOKEN = "7199575511:AAEdx0B8Bsw_r3XmfRjEnunuALwB7nbLClk"


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот сайта free-title. отправуь мне свой токен, и пропиши команду /update чтобы узнать о новых проектах любимых авторов",
    )


async def help_command(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот сайта free-title. отправуь мне свой токен, и пропиши команду /update чтобы узнать о новых проектах любимых авторов",
    )


async def echo(update, context):
    await update.message.reply_text(update.message.text)


def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    run_bot()
    print("end")
