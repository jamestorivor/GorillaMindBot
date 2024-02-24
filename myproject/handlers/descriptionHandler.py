from ..database import query_tables
from telegram import *
from telegram.ext import *
from ..buttons import *

async def product_description(update: Update, context:ContextTypes.DEFAULT_TYPE):
    product = context.user_data["products"][context.user_data["product_list_position"]]
    await context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"],reply_markup=None)
    await send_description(update,context,product)

async def next_description(update: Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["product_list_position"] = reposition(context.user_data["product_list_position"]+1,len(context.user_data["products"]))
    product = context.user_data["products"][context.user_data["product_list_position"]]
    await change_description(update,context,product)

async def previous_description(update: Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["product_list_position"] = reposition(context.user_data["product_list_position"]-1,len(context.user_data["products"]))
    product = context.user_data["products"][context.user_data["product_list_position"]]
    await change_description(update,context,product)

async def exit_description(update: Update, context:ContextTypes.DEFAULT_TYPE):
    product = context.user_data["products"][context.user_data["product_list_position"]]
    markup = show_product_buttons()
    await context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"],reply_markup=markup)
    await context.bot.deleteMessage(chat_id=update.message.chat_id,message_id=context.user_data["description_message_id"])

async def product_flavours(update: Update, context:ContextTypes.DEFAULT_TYPE):
    product = context.user_data["products"][context.user_data["product_list_position"]]

async def change_description(update,context,product):
    query = update.callback_query
    await query.answer()
    product_description = query_tables.get_from_Products("description",product)
    formatted_name = query_tables.format_name_for_image(product,)
    image = context.user_data["product_images"][formatted_name]
    await context.bot.editMessageMedia(media=InputMediaPhoto(image,caption="not text"),chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])
    await query.message.edit_text(text=product_description)

async def send_description(context,update,product):
    product_description = query_tables.get_from_Products("description",product)
    markup = show_description_buttons()
    description_message = await update.message.reply_text(text=product_description,reply_markup=markup)
    context.user_data["description_message_id"] = description_message.message_id

async def next_description(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    query.message.edit_text()
    await change_description