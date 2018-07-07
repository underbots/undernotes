#!usr/bin/env python

"""
Interface tool to interact in te app
Author: Blanca 
File: interactive_tools.py
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from general_info import help_ms
from _token_bot import TOKEN_BOT

############### GENERAL DEFINITIONS ################

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['upload', 'download'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

################## OPTIONS' FUNTIONS ######################

def upload(bot, update, user_data):
    """
    Sent a massege quering for file's name
"""
    option = update.message.text
    update.message.reply_text(f'Let {option}, First tell me what it is')

    return TYPING_REPLY  #go to received_information

def received_information(bot,update , user_data):
    """get the name 
"""
###########################################################    

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN_BOT)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^upload$',upload ,pass_user_data=True)
            ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text, 
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
   # dp.add_handler(CommandHandler('help',))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    from _token_bot import TOKEN_BOT
    main()

