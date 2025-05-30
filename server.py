import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from data.constants.CONSTANTS import BOT_TOKEN
from data.constants.callback_patterns import customer_menu_pattern, edit_task_menu_pattern, admin_group_menu_pattern, \
    executor_menu_pattern
from data.constants.commands import start_command, open_executor_menu_command, update_tasks_menu_command
from data.db_models import db_session
from handlers.customer.edit_task import edit_task_conv_handler
from handlers.customer.main_menu import main_menu_callback_handler
from handlers.customer.task_maker import task_maker_conv_handler
from handlers.executor.edit_task import open_executor_menu, executor_menu_callback_handler
from handlers.executor.notice import executor_group_callback_handler, update_tasks_handler
from handlers.generalis.registration import registration_handler, start

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)


def main():
    db_session.global_init()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler(start_command, start))
    application.add_handler(CommandHandler(update_tasks_menu_command, update_tasks_handler))
    application.add_handler(MessageHandler(filters.CONTACT, registration_handler))
    application.add_handler(CallbackQueryHandler(main_menu_callback_handler,
                                                 pattern=customer_menu_pattern))
    application.add_handler(CallbackQueryHandler(executor_menu_callback_handler, pattern=executor_menu_pattern))
    application.add_handler(CallbackQueryHandler(executor_group_callback_handler, pattern=admin_group_menu_pattern))
    application.add_handler(task_maker_conv_handler)
    application.add_handler(edit_task_conv_handler)
    application.add_handler(CommandHandler(open_executor_menu_command, open_executor_menu))
    application.run_polling()


if __name__ == '__main__':
    main()
