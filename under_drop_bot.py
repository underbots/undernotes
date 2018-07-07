#!usr/bin/env python

"""
Bot descarga archivos
Authors: Ric y Blanca

COSICAS QUE FALTAN POR HACER:
- Import con el drop
- pedir nombre del archivo (gestionar más adelante el diseño)
- ¿tener también la librería sys pa borrar las fotos?

wed de interés:
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#download-a-file
"""

from telegram.ext import Updater, CommandHandler , MessageHandler, Filters
from _token_bot import TOKEN_BOT



def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def myHelp( bot , update ):
    update.message.reply_text(
        '- Send a photo or a file')
    
def myDownload(bot, update):
    """ download if new mesage is a document or a photo
"""
    #SUPONGO QUE ES UNA FOTO
    if update.message.photo:
        print ('Download in process')
        update.message.reply_text('Descarga en proceso...')
    
        _dir = 'Downloads/' # my dir were bot is executing to save de photos

        photo = update.message.photo[-1]
        path = _dir + 'cambiar_nombre.png' # MODICIAR NOMBRE DE LA FOTO
    
        file_id = photo.file_id
        file_down = bot.get_file(file_id)
        file_down.download(path) # FALLA ESTA FUNCIÓN
    
        update.message.reply_text('Descarga finalizada, muchas gracias por colaborar en nuestro repositorillo,besito psicológico pa\' ti :kissing_heart: ')
        print('Photo has been downloaded')

        # AÑADIR FUNCIÓN PARA SUBIR ALMACENAMIENTO

         # Document download
    elif update.message.document is not None:
        
        doc = update.message.document
        path = pre_path + doc.file_name
        
        file_id = doc.file_id()
        file_down = bot.get_file(file_id)
        file_down.download(path)

        print( f'File {doc.file_name} download :) ')
        #AÑADIR MÓDULO PARA SUBIR AL ALMACENAMIENTO
        


updater = Updater(TOKEN_BOT)

# select in which message call download function
apuntes = MessageHandler(Filters.photo | Filters.document , myDownload)
updater.dispatcher.add_handler(apuntes)

# call help
updater.dispatcher.add_handler(CommandHandler('help', myHelp))

updater.dispatcher.add_handler(CommandHandler('hello', hello))


updater.start_polling()
updater.idle()
