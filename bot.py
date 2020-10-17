"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import os
from datetime import datetime
from weatherFunctsOld import findLatLon, checkNewData, getMinutely, evalMinutely, plotMinutelyPrec, doRainMins
from convHandlerBike import getConvHandlerBike
from convHandlerWeather import getConvHandlerWeather

PORT = int(os.environ.get('PORT', 5000))

WECHSLER, EINGABE, AUSWAHL, AUSWAHLWECHSLER, STANDORT = range(5)
ENTERLOC, FIXEDLOC, USERLOC = range(3)
FIRST, SECOND, THIRD = range(3)
coordBuffer = {}
fixedAdr = [["Kriegerstrasse 22",", 30161 Hannover"],
            ["Stadtfelddamm 34", ", 30625 Hannover"],
            ["Wiedenthaler Sand 9", ", 21147 Hamburg"],
            ["An der Hasenkuhle 7", ", 21224 Rosengarten"]]


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ["TELTOKEN"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    
def chatID(update, context):
    update.message.reply_text(update.message.chat.id)
    
def messageTest(update, context):
    bot = context.bot
    bot.sendMessage(532298931,"Test")

def photo(update, context):
    bot = context.bot
    bot.send_photo(update.message.chat.id,open("img.jpg",'rb'))
    #bot.send_photo(update.message.chat.id,"https://homepages.cae.wisc.edu/~ece533/images/airplane.png")



def rainForecast(update, context): #, location, fileName
    bot = context.bot
    fileName = "minutelyRain"
    address = "Kriegerstrasse 22, 30161 Hannover"
    coord = findLatLon(address)
    [data,returnVal] = checkNewData(coord)
    if returnVal == 0:
        update.message.reply_text("New data, nothing here")
    elif returnVal == 1:
        update.message.reply_text("Old data")
    elif returnVal == 2:
        update.message.reply_text("New data, too old")
    elif returnVal == 3:
        update.message.reply_text("New data, wrong coordinates")

    minutely = getMinutely(data["minutely"])
    returnStr = evalMinutely(minutely)
    plotMinutelyPrec(minutely,fileName)
    
    bot.send_photo(update.message.chat.id,open(fileName + ".jpg",'rb'))
    update.message.reply_text(returnStr)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def time(update, context):
    """Returns the time"""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    update.message.reply_text(current_time)

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))
    bot = context.bot
    bot.sendMessage(532298931,"button")
    
def switchAnswer(update, context):
    answerText = update.message.text
    update.message.reply_text(answerText)
    if answerText == 'Adresse eingeben':
        return EINGABE
    elif answerText == 'Auswahl':
        return AUSWAHL
    elif answerText == 'Eigener Standort':
        return STANDORT
    else:
        return -1
    


def sendPickle(update, context):
    
    if os.path.isfile("weatherData"):
        bot = context.bot
        bot.send_document(update.message.chat.id,open("weatherData",'rb'))
        update.message.reply_text("There you go")
    else:
        update.message.reply_text("No file saved")
        

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
 
    return ConversationHandler.END




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("photo", photo))
    dp.add_handler(CommandHandler("chatID", chatID))
    dp.add_handler(CommandHandler("regen", rainForecast))
    #dp.add_handler(CommandHandler("regenTest", rainForecastVar))
    dp.add_handler(CommandHandler("messageTest", messageTest))
    dp.add_handler(CommandHandler("sendPickle", sendPickle))
    
    # New weather conversation handler

    
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
    if False:
        # Weather conversation handler 1
        convHandlerWeather = ConversationHandler(
            entry_points=[CommandHandler("wetter",rainForecastVar)],
            states={
                WECHSLER: [MessageHandler(Filters.all,switchAnswer),
                          CommandHandler('cancel',cancel)],
                EINGABE: [MessageHandler(Filters.text,enterLoc),
                          CommandHandler('cancel',cancel)],
                AUSWAHL: [MessageHandler(Filters.text,fixedLoc),
                          CommandHandler('cancel',cancel)],
                AUSWAHLWECHSLER: [MessageHandler(Filters.location,switchAnswer),
                          CommandHandler('cancel',cancel)],
                STANDORT: [MessageHandler(Filters.location,userLoc),
                          CommandHandler('cancel',cancel)]
                },
            
            fallbacks=[CommandHandler('cancel', cancel)]
            )

    dp.add_handler(getConvHandlerWeather())

    # TODO: get the conversationhandler here
    dp.add_handler(getConvHandlerBike())

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://gbweatherbot.herokuapp.com/' + TOKEN)
    
    updater.bot.sendMessage(532298931,"Bot running")
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()