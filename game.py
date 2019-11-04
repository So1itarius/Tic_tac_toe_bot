from telegram.ext import ConversationHandler

from utils import keyboard

board = list(range(1, 10))


def draw_board(bot, update):
    global board
    for i in range(3):
        update.message.reply_text(f"| {board[0 + i * 3]} | {board[1 + i * 3]} | {board[2 + i * 3]} |",
                                  reply_markup=keyboard())


def start_game(bot, update):
    global board
    text = 'Отсюда начнется игра:'
    update.message.reply_text(text)
    board = list(range(1, 10))
    draw_board(bot, update)
    update.message.reply_text(f"Куда поставим X?")
    return "CHOOSING_X"


def check_win():
    global board
    # проверяем на победу
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    # проверяем на ничью
    counter = 0
    for i in board:
        if type(i) == int:
            continue
        else:
            counter += 1
    if counter == 9:
        return counter
    else:
        return False


def tic(bot, update):
    global board
    player_answer = int(update.message.text)
    if str(board[player_answer - 1]) not in "XO":
        board[player_answer - 1] = "X"
        draw_board(bot, update)
    else:
        update.message.reply_text("Эта клеточка уже занята,выберите другую")
        return f"CHOOSING_X"
    tmp = check_win()
    if type(tmp) == str:
        update.message.reply_text(f"{tmp} выиграл!")
        return ConversationHandler.END
    elif type(tmp) == int:
        update.message.reply_text("Ничья!")
        return ConversationHandler.END
    else:
        update.message.reply_text(f"Куда поставим O?")
    return "CHOOSING_O"


def tac(bot, update):
    global board
    player_answer = int(update.message.text)
    if str(board[player_answer - 1]) not in "XO":
        board[player_answer - 1] = "O"
        draw_board(bot, update)
    else:
        update.message.reply_text("Эта клеточка уже занята,выберите другую")
        return f"CHOOSING_O"
    tmp = check_win()
    if type(tmp) == str:
        update.message.reply_text(f"{tmp} выиграл!")
        return ConversationHandler.END
    else:
        update.message.reply_text(f"Куда поставим X?")
    return "CHOOSING_X"
