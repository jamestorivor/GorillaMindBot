from ..database.query_tables import *
from requests import *
from telegram import *
from telegram.ext import *
from ..buttons import *
from ..database.populate_tables import *
from .handlers_utils import *


ALLOWED_USER_CHAT_ID = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Hello! Im the supplement bot. You can use me to place orders for your clients.\n
Im currently in my beta phase and would appreciate if you give me some time to handle your requests.\n
Please find out more about how to use me by using /how_to """)


async def how_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""I am an interactive bot:)
Use /products to view the catalouge and place orders

Payment method:
Paynow

If you have any other questions, please feel free to reach out to my creator via email or whatsapp!
Otherwise, all available commands can be found using /help.
""")

async def disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Commission will not be awarded for orders placed with the wrong Trainer's number\nThis is to ensure that there are no disputes between orders with a wrong Trainer's number
                                    
Commission will be paid out on the last day of the month (eg. 31 Jan) to the phone number provided.
""")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Available Commands :- 
/how_to - Learn how to use me better
/products - See all the products and place your order
/cancel - Leave the interaction with me 
/disclaimer - Read about the disclaimers
    """)


