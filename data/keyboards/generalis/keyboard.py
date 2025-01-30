from telegram import ReplyKeyboardMarkup, KeyboardButton


registration_button = KeyboardButton("Отправьте свой контакт", request_contact=True)
registration_keyboard = ReplyKeyboardMarkup([[registration_button]],
                                            resize_keyboard=True,
                                            one_time_keyboard=True)