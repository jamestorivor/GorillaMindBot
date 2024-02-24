from .handlers_utils import *
from ..database import query_tables
from telegram import *
from telegram.ext import *
from ..buttons import *
import re

(   END,
    SHOW_PRODUCTS,
    LIST_PRODUCTS,
    SHOW_DESCRIPTION,
    SHOW_FLAVOURS,
    CART,
    PAYMENT
) = range(-1,6)

async def catch_text(update: Update, context:ContextTypes.DEFAULT_TYPE):
    product = update.message.text.lower().title()
    if product not in context.user_data["products"]:
        try:
            await context.bot.deleteMessage(chat_id=update.message.chat_id,message_id=context.user_data["main_message_id"])
        except KeyError:
            pass
        await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Sorry, that is not a valid catagory. Goodbye.",reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    await delete_user_sent_message(update,context)
    formatted_name = format_name_for_image(product)
    file_id = get_image_file_id(formatted_name)
    context.user_data["product_list_position"] = context.user_data["products"].index(product)
    price = re.escape(str(get_from_Products("price",product)))
    if product in ["Mode","Nitric","Protein"]:
        instock = "Please check individual flavours for their stock"
    else:
        context.user_data["instock"] = instock = check_stock(get_from_Product_variations("in_stock",product,"None"))
    product_info = re.escape(get_from_Products("description",product))
    markup = show_product_buttons(product,instock)
    await context.bot.editMessageMedia(media=InputMediaPhoto(file_id,caption=f"__{product}__\n*Price:*{price}\n\n*Product Info:*\n{product_info}\n*Stock:*{instock}",parse_mode="MarkdownV2"),reply_markup=markup,chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])

    return LIST_PRODUCTS

async def get_products(update: Update, context:ContextTypes.DEFAULT_TYPE):
    # context.user_data["products"] = query_tables.get_column_from_Products("name")
    context.user_data["products"] = ["Mode","Protein","Nitric"]
    context.user_data["flavours"] = query_tables.get_column_from_Product_flavours("flavour")[:-1]
    context.user_data["product_list_position"] = 0
    context.user_data["in_cart"] = {}
    markup = get_list_of_buttons(context.user_data["products"])
    await update.message.reply_text(text="Select the product you would like to see",reply_markup=markup)
    return SHOW_PRODUCTS


async def show_products(update: Update, context:ContextTypes.DEFAULT_TYPE):
    product = update.message.text.lower().title()
    if product not in context.user_data["products"]:
        try:
            await context.bot.deleteMessage(chat_id=update.message.chat_id,message_id=context.user_data["main_message_id"])
        except KeyError:
            pass
        await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Sorry, that is not a valid catagory. Goodbye.",reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    await delete_user_sent_message(update,context)
    context.user_data["product_list_position"] = context.user_data["products"].index(product)
    formatted_name = format_name_for_image(product)
    image = get_image_file_id(formatted_name)
    price = re.escape(str(get_from_Products("price",product)))
    if product in ["Mode","Nitric","Protein"]:
        instock = "Please check individual flavours for their stock"
    else:
        context.user_data["instock"] = instock = check_stock(get_from_Product_variations("in_stock",product,"None"))
    markup = show_product_buttons(product,instock)
    product_info = re.escape(get_from_Products("description",product))
    sent_image = await update.message.reply_photo(photo=image,caption=f"__{product}__\n*Price\:*{price}\n\n*Product Info:*\n{product_info}\n*Stock:*{instock}",reply_markup=markup,parse_mode="MarkdownV2")
    context.user_data["main_message_id"] = sent_image.message_id
    return LIST_PRODUCTS


async def change_product(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "previous_product":
        context.user_data["product_list_position"] = reposition(context.user_data["product_list_position"]-1,len(context.user_data["products"]))
    else:
        context.user_data["product_list_position"] = reposition(context.user_data["product_list_position"]+1,len(context.user_data["products"]))
    product = context.user_data["products"][context.user_data["product_list_position"]]
    formatted_name = format_name_for_image(product)
    file_id = get_image_file_id(formatted_name)
    price = re.escape(str(get_from_Products("price",product)))
    if product in ["Mode","Nitric","Protein"]:
        instock = "Please check individual flavours for their stock"
    else:
        context.user_data["instock"] = instock = check_stock(get_from_Product_variations("in_stock",product,"None"))
    markup = show_product_buttons(product,instock)
    product_info = re.escape(get_from_Products("description",product))
    await query.message.edit_media(media=InputMediaPhoto(file_id,caption=f"__{product}__\n*Price\:*{price}\n\n*Product Info:*\n{product_info}\n*Stock:*{instock}",parse_mode="MarkdownV2"),reply_markup=markup)
    return LIST_PRODUCTS


async def get_quantity_in_product(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    flavour = "None"
    product = context.user_data["products"][context.user_data["product_list_position"]]
    markup = keypad(get_from_Product_variations("in_stock",product,flavour))
    delete_this = await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Please input the number of tubs you want",reply_markup=markup)
    context.user_data["delete_later"] = delete_this.message_id
    return LIST_PRODUCTS


async def add_variation_to_cart_in_product(update: Update, context:ContextTypes.DEFAULT_TYPE):
    quantity_requested = int(update.message.text)
    if quantity_requested > context.user_data["instock"] or quantity_requested <= 0:
        await send_and_delete("That is not a valid number in stock! Please select again.",sleep=2.3,update=update,context=context)
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=update.message.message_id)
        return LIST_PRODUCTS
    product = context.user_data["products"][context.user_data["product_list_position"]]
    flavour = "None"
    if product in context.user_data["in_cart"]:
        if context.user_data["in_cart"][product][flavour] + quantity_requested > query_tables.get_from_Product_variations("in_stock",product,flavour):
            await send_and_delete("The number you are trying to add and what you have in cart exceeds the total stock. Please try adding less than the total stock to your cart.",sleep=3.5,update=update,context=context)
            await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
            await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=update.message.message_id)
            return LIST_PRODUCTS
        context.user_data["in_cart"][product][flavour] += quantity_requested
    else:
        context.user_data["in_cart"][product] = {flavour : quantity_requested}
    await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=update.message.message_id)
    try:
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
    except error.BadRequest:
        pass
    await send_and_delete(text="Item(s) have been added to cart",reply_markup=ReplyKeyboardRemove(),sleep=3,update=update,context=context)
    return LIST_PRODUCTS


async def cancel(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Goodbye!")
    await context.bot.deleteMessage(chat_id=update.message.chat_id,message_id=context.user_data["main_message_id"])
    context.user_data.clear()
    return ConversationHandler.END
