from telegram.ext import Updater, CommandHandler
from _token_bot import TOKEN_BOT


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater(TOKEN_BOT)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
