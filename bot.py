
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

logging.basicConfig(level=logging.INFO)

TOKEN = '8079599334:AAE2-azAjR-_tSV9HirqMb2_tjhEpI9HSOU'
URL = 'https://grouphelperbot.onrender.com'
PORT = int(os.environ.get("PORT", 10000))

def start(update, context):
    logging.info('Comando /start recibido')
    logging.info(f'Chat ID: {update.effective_chat.id}')
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text='¡Hola! Soy CrimsonMeguBot')
        logging.info('Mensaje enviado correctamente')
    except Exception as e:
        logging.error(f'Error al enviar mensaje: {e}')

def unknown(update, context):
    logging.info('Mensaje recibido')
    logging.info(f'Texto del mensaje: {update.message.text}')

def main():
    logging.info('Iniciando el bot...')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.all, unknown))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,url_path='webhook',
        webhook_url=URL + '/webhook'
    )
    logging.info('Webhook iniciado correctamente')
    updater.idle()

if _name_ == '_main_':
    main()


