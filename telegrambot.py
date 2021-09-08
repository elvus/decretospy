import logging
from pymongo import MongoClient
import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
client=MongoClient("mongodb://localhost:27017/")
db=client["decretospy"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hola! Mi trabajo es filtrar los decretos del Ministerio de Tecnologias de la Información, pidemelos cuando quieras usuando el comando /decretos')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/decretos: Trae los 3 útimos decretos del Mitic.')


def decretos(update, context):
    """Trae los tres ultimos decretos sobre el Mitic."""
    docs = db.decretos.find({'descripcion':{'$regex':'ministerio de tec|mitic', '$options':'i'}}).sort("decreeId",-1).limit(3)
    for i in docs:
       context.bot.send_message(chat_id=update.message.chat_id,
                     text="Decreto Nº %s\n%s %s"%(i['decreeId'],i['descripcion'], i['link'].replace(" ","%20")))

def nuevosDecretos(update, context):
    docs = db.decretos.find({'descripcion':{'$regex':'ministerio de tec|mitic', '$options':'i'}, 'tweet':False}).sort("decreeId",-1)
    for i in docs:
        context.bot.send_message(chat_id=update.message.chat_id, 
                text="Decreto Nº %s\n%s %s"%(i['decreeId'],i['descripcion'], i['link'].replace(" ","%20")))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TOKEN_TE, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(CommandHandler("decretos", decretos))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # set commands
    updater.bot.set_my_commands(
        [
            ('decretos', 'Envia los 3 últimos decretos del Mitic'),
        ]
    )

    updater.idle()
if __name__ == '__main__':
    main()
#db.decretos.find({'descripcion':{'$regex':'ministerio de tec|mitic', '$options':'i'}})