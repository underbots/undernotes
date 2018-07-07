#!usr/bin/env python

# Authors: Ric y Blanca

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dropbot import myUpload
from _token_bot import TOKEN_BOT


def start(bot, update):
    msg = (f"Hola {update.message.from_user.first_name}, "
           "bienvenido a nuestra secta <3."
           "¿Quieres colaborar en los apuntes?")
    update.message.reply_text(msg)


def help(bot, update):
    update.message.reply_text(" - Envia una foto o un archivo")


def upload(bot, update):
    """Descarga el archivo enviado y lo sube a la plataforma"""

    prefix = 'Downloads/'
    if update.message.photo:

        photo = update.message.photo[-1]
        # Añadir interfaz

        # Preguntar por el nombre de la foto
        update.message.reply_text("¿Cómo dice que se llama esta foto?")
        path = prefix + "cambiar_nombre.png"

        file_id = photo.file_id
        file_down = bot.get_file(file_id)
        file_down.download(path)

        update.message.reply_text("Voy a ver si lo subo al dropbox")
        myUpload(path, "fotillo.png")

        msg = ("Descarga finalizada, muchas gracias por colaborar "
               "en nuestro repositorillo, besito psicológico para *ti* :)")

        update.message.reply_text(msg)
        print("Foto descargada")

        # Upload?

    elif update.message.document:

        doc = update.message.document
        path = prefix + doc.file_name

        file_id = doc.file_id()
        file_down.download(path)

        print(f"Archivo {doc.file_name} descargado :) ")

        # Upload?


updater = Updater(TOKEN_BOT)

# Filtrar mensajes con documentos o fotos
notes = MessageHandler(Filters.photo | Filters.document, upload)
updater.dispatcher.add_handler(notes)


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
updater.idle()
