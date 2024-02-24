import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *
from .handlers import productConversation, handlers, adminHandler

prd_list = ['mode', 'nitric', 'smooth', 'sigma', 'dream']

# For debugging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



if __name__ == "__main__":
    load_dotenv()


    BOT_TOKEN = "6571919073:AAHFbRXVvq1wJ-pAkOxmoLpq7TUiIC6Uqho"
    BOT_USERNAME = os.getenv("BOT_USERNAME")

    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",handlers.start),1)
    app.add_handler(productConversation.product_handler,2)
    app.add_handler(adminHandler.edit_price_conv,3)
    app.add_handler(adminHandler.edit_stock_conv,3)
    app.add_handler(CommandHandler("help",handlers.help),1)
    app.add_handler(CommandHandler("how_to",handlers.how_to),1)
    

    print("Polling...")
    app.run_polling(poll_interval=3)