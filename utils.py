from telegram import ReplyKeyboardMarkup


def keyboard():
    my_keyboard = ReplyKeyboardMarkup([["1", "2", "3"],
                                       ["4", "5", "6"],
                                       ["7", "8", "9"]
                                       ], resize_keyboard=True)
    return my_keyboard
