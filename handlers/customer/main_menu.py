from telegram import Update
from telegram.ext import CallbackContext

from data.constants.callbacks import expand_tasks_list_callback
from data.decorators import register_command
from data.keyboards.client.customer.maker import create_main_menu_keyboard
from data.messages.client.customer import main_menu_message
from data.messages.generalis import no_registration_emission_message


@register_command
async def open_main_menu(update: Update, context: CallbackContext):
    keyboard = create_main_menu_keyboard(update.effective_user.id)
    if keyboard is None:
        await update.message.reply_html(no_registration_emission_message)
        return await open_main_menu(update, context)
    return await update.message.reply_text(main_menu_message, reply_markup=keyboard)


@register_command
async def main_menu_callback_handler(update: Update, context: CallbackContext) -> None:
    callback = update.callback_query.data
    await update.callback_query.answer()
    if callback == expand_tasks_list_callback:
        pass
        # return await expand_tasks_list(update, context)


