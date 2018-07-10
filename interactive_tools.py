#!usr/bin/env python

"""
Interface tool to interact in te app
Author: Blanca 
File: interactive_tools.py
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,  ConversationHandler)
import logging

from general_info import help_ms
from _token_bot import TOKEN_BOT
from wearhouse.my_dropbox import upload_to_dropbox


############### GENERAL DEFINITIONS ################

CHOOSING, TYPING_NAME, TYPING_REPLY = range(3)

reply_keyboard = [['Upload', 'Download'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

################## OPTIONS' FUNTIONS ######################
def start(bot , update):
    """ start messge: show help and load reply_markup
    """
    update.message.reply_text(help_ms , reply_markup=markup)
    return CHOOSING

def show_help(bot , update):
    update.message.reply_text(help_ms)
    
def upload(bot, update):
    """
    Sent a massege quering for file's name
"""
    print('have enter to upload')
    option = update.message.text
    update.message.reply_text(f'Let {option}, First tell me what it is')

    return TYPING_NAME  #go to received_information

def name_introduction(bot, update , file_name):
    """get the name and upload to platform
"""
    file_name = update.message.text
    update.message.reply_text( f' El archivo {file_name} ha sido subido con éxito')
    
    return CHOOSING

def done(bot, update):

    update.message.reply_text('I have susccesfully finished my services, have a blessful day')

    file_name.clear()
    return ConversationHandler.END

###########################################################    

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN_BOT)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^Upload$',upload ,pass_user_data=True)],

            TYPING_NAME: [MessageHandler(Filters.text, name_introduction, pass_user_data=True) ],

            #TYPING_REPLY: [MessageHandler(Filters.text,  received_information,  pass_user_data=True),   ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('help',show_help))


    # log all errors
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    
if __name__ == '__main__':
    from _token_bot import TOKEN_BOT
    main()

