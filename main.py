import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler, \
    messagequeue as mq

from game import tic, tac, start_game
from settings import TOKEN_FOR_BOT


def start(bot, update):
    text = 'Для того чтобы начать играть введите: /start_game.' \
           ' Если во время игры ввести "stop", то игра прервется'
    update.message.reply_text(text)


def interceptor(bot, update):
    global board
    if update.message.text == "stop":
        return ConversationHandler.END
    else:
        update.message.reply_text("Некорректный ввод. Вы уверены, что ввели число от 1 до 9?")


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='bot.log'
                        )
    updater = Updater(TOKEN_FOR_BOT)

    updater.bot._msg_queue = mq.MessageQueue()
    updater.bot._is_messages_queued_default = True

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start_game", start_game)],

        states={
            "CHOOSING_X": [RegexHandler('^(1|2|3|4|5|6|7|8|9)$', tic)],
            "CHOOSING_O": [RegexHandler('^(1|2|3|4|5|6|7|8|9)$', tac)],
        },

        fallbacks=[MessageHandler(Filters.text, interceptor)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
