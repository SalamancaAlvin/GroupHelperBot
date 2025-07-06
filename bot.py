import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = '8079599334:AAE2-azAjR-_tSV9HirqMb2_tjhEpI9HSOU'
bot = Bot(token=TOKEN)

app = Flask(_name_)

logging.basicConfig(level=logging.INFO)

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='¡Hola! Soy CrimsonMeguBot')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Comando no reconocido.')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def home():
    return 'Bot en funcionamiento'

if _name_ == '_main_':
    app.run(port=10000)
