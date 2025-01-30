import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from data.constants.CONSTANTS import BOT_TOKEN
from data.constants.commands import start_command
from data.db_models import db_session
from handlers.generalis.registration import registration_handler, start

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)


def main():
    db_session.global_init()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler(start_command, start))
    application.add_handler(MessageHandler(filters.CONTACT, registration_handler))
    application.run_polling()


if __name__ == '__main__':
    main()
