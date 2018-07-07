#!usr/bin/env python

# Authors: Ric y Blanca

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from platform.dropbox import upload_to_dropbox
from platform.drive import upload_to_drive
from _config import TOKEN


def start(bot, update):
    msg = (f"Hola {update.message.from_user.first_name}, "
           "bienvenido a nuestra secta <3.\n"
           "¿Quieres colaborar en los apuntes?")
    update.message.reply_text(msg)


def help(bot, update):
    update.message.reply_text(" - Envia una foto o un archivo")


def upload(bot, update):
    """Descarga el archivo enviado y lo sube a la plataforma"""

    prefix = 'downloads/'

    # Elegir plataforma
    upload_file = upload_to_drive

    update.message.reply_text("Marchando, a ver si lo subo")
    if update.message.photo:

        photo = update.message.photo[-1]
        # Preguntar por el nombre de la foto y modificar
        path = prefix + "photo.png"

        file_id = photo.file_id
        file_down = bot.get_file(file_id)
        file_down.download(path)

    elif update.message.document:

        doc = update.message.document
        path = prefix + doc.file_name

        file_id = doc.file_id
        file_down = bot.get_file(file_id)
        file_down.download(path)

    upload_file(path)
    msg = ("Subida finalizada, muchas gracias por colaborar "
           "en nuestro repositorillo, besito psicológico para *ti* :)")

    update.message.reply_text(msg)


updater = Updater(TOKEN)

# Filtrar mensajes con documentos o fotos
notes = MessageHandler(Filters.photo | Filters.document, upload)
updater.dispatcher.add_handler(notes)


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
updater.idle()
