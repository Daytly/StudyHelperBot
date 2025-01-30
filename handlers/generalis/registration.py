from telegram import Update
from telegram.ext import CallbackContext

from data.db_functions.generalis.checks import check_is_register
from data.db_functions.generalis.registration import registration_user
from data.keyboards.generalis.keyboard import registration_keyboard
from data.messages.generalis import send_contact_emission, final_message_registration, registration_emission_message, \
    start_message, start_no_register_message


async def start(update: Update, context: CallbackContext):
    tg_user = update.effective_user
    if check_is_register(tg_user.id):
        sent_message = start_message.format(tg_user.mention_html())
        await update.message.reply_html(sent_message)
        return
    sent_message = start_no_register_message.format(tg_user.mention_html())
    await update.message.reply_html(sent_message, reply_markup=registration_keyboard)


async def registration_handler(update: Update, context: CallbackContext):
    if update.message.contact is None:
        await update.message.reply_html(send_contact_emission, reply_markup=registration_keyboard)
        return
    contact = update.message.contact
    tg_user = update.effective_user
    if registration_user(tg_user.id, contact.first_name, contact.last_name, tg_user.username,
                         contact.phone_number) is None:
        await update.message.reply_html(registration_emission_message)
    else:
        await update.message.reply_html(final_message_registration)
