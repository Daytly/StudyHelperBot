from telegram import ReplyKeyboardMarkup, KeyboardButton


award_buttons = [[KeyboardButton(f"{j}р") for j in range(i, i + 300 + 1, 100)] for i in range(300, 1200 + 1, 300)]
input_award_keyboard = ReplyKeyboardMarkup(award_buttons, resize_keyboard=True, one_time_keyboard=True)