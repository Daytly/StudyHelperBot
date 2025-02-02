from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from data.db_functions.generalis.checks import check_is_admin, check_is_register, check_is_executor
from data.messages.generalis import message_about_restricted_access


def admin_command(function_to_decorate):
    async def check_admin(update: Update, context: CallbackContext, *args, **kwargs):
        if check_is_admin(update.effective_user.id):
            return await function_to_decorate(update, context, *args, **kwargs)
        else:
            sent_message = message_about_restricted_access
            await update.get_bot().send_message(update.message.chat_id, sent_message)
            return ConversationHandler.END

    return check_admin

def register_command(function_to_decorate):
    async def check_register(update: Update, context: CallbackContext, *args, **kwargs):
        if check_is_register(update.effective_user.id):
            return await function_to_decorate(update, context, *args, **kwargs)
        else:
            sent_message = message_about_restricted_access
            await update.get_bot().send_message(update.message.chat_id, sent_message)
            return ConversationHandler.END
    return check_register


def executor_command(function_to_decorate):
    async def check_executor(update: Update, context: CallbackContext, *args, **kwargs):
        if check_is_executor(update.effective_user.id):
            return await function_to_decorate(update, context, *args, **kwargs)
        else:
            sent_message = message_about_restricted_access
            await update.get_bot().send_message(update.message.chat_id, sent_message)
            return ConversationHandler.END
    return check_executor

