from telegram import Update, ChatMember
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ChatMemberHandler
)
from collections import defaultdict
import time
import re

TOKEN = "8079599334:AAE2-azAjR-_tSV9HirqMb2_tjhEpI9HSOU"
LOG_CHAT_ID = -1002812429283  # Cambia esto por tu ID real

user_warnings = {}
bad_words = {"spam", "estafa", "porno"}
user_message_times = defaultdict(list)

MAX_WARNINGS = 3
SPAM_THRESHOLD = 5
SPAM_INTERVAL = 10

RULES_TEXT = """
*Reglas del Grupo*:
1. No spam.
2. No contenido ofensivo.
3. Respeta a los demás.
4. Nada de enlaces promocionales.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activado y funcionando.")

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Responde a un mensaje para advertir.")
        return

    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.effective_chat.id
    key = f"{chat_id}:{user_id}"
    user_warnings[key] = user_warnings.get(key, 0) + 1
    warnings = user_warnings[key]

    await update.message.reply_text(f"⚠️ Advertencia {warnings}/{MAX_WARNINGS}")
    await context.bot.send_message(
        LOG_CHAT_ID,
        f"Usuario {user_id} advertido ({warnings}/{MAX_WARNINGS}) en {chat_id}"
    )

    if warnings >= MAX_WARNINGS:
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            await update.message.reply_text("Usuario expulsado por acumular advertencias.")
            await context.bot.send_message(LOG_CHAT_ID, f"Usuario {user_id} baneado por advertencias.")
            user_warnings[key] = 0
        except Exception as e:
            await update.message.reply_text(f"No se pudo expulsar al usuario: {e}")

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"¡Bienvenido/a {member.mention_html()}!",
            parse_mode='HTML'
        )
    await update.message.reply_text(RULES_TEXT, parse_mode='Markdown')

async def filter_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in bad_words):
        await update.message.delete()
        await context.bot.send_message(
            LOG_CHAT_ID,
            f"Mensaje eliminado por palabra prohibida: {update.message.text}"
        )

async def anti_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()
    user_message_times[user_id] = [
        t for t in user_message_times[user_id] if now - t < SPAM_INTERVAL
    ]
    user_message_times[user_id].append(now)

    if len(user_message_times[user_id]) > SPAM_THRESHOLD:
        await update.message.delete()
        await context.bot.send_message(
            update.effective_chat.id,
            f"{update.effective_user.mention_html()} fue detectado por spam.",
            parse_mode='HTML'
        )
        await context.bot.send_message(LOG_CHAT_ID, f"Spam detectado de {user_id}")
        user_message_times[user_id].clear()

async def anti_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if re.search(r"(https?://|t\.me/|telegram\.me/|@)", text):
        await update.message.delete()
        await context.bot.send_message(
            LOG_CHAT_ID,
            f"Mensaje promocional eliminado de {update.effective_user.mention_html()}",
            parse_mode='HTML'
        )

async def track_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = update.my_chat_member.new_chat_member.status
    if status == ChatMember.MEMBER:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Gracias por agregarme!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet))
    app.add_handler(ChatMemberHandler(track_bot, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler
