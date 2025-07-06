import logging
from telegram.ext import Updater, CommandHandler, MessageHandler

logging.basicConfig(level=logging.INFO)

TOKEN = '8079599334:AAE2-azAjR-_tSV9HirqMb2_tjhEpI9HSOU'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='¡Hola! Soy CrimsonMeguBot')

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
