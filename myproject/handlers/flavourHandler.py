from .handlers_utils import *
from ..database import query_tables
from telegram import *
from telegram.ext import *
from ..buttons import *
import time
import re

(   END,
    SHOW_PRODUCTS,
    LIST_PRODUCTS,
    SHOW_DESCRIPTION,
    SHOW_FLAVOURS,
    CART,
    PAYMENT
) = range(-1,6)

async def catch_flavour(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = context.user_data["products"][context.user_data["product_list_position"]]
    flavour_list = query_tables.get_flavours_for_product(product)
    if len(flavour_list) > 1:
        markup = get_list_of_buttons(flavour_list)
    else:
        markup = ReplyKeyboardRemove()
    flavour_message = await query.message.reply_text(text="Please use command button in your text field / keyboard to select your desired flavour.\n You may use the text field / keyboard at any time to change the flavour as well.",reply_markup=markup)
    context.user_data["flavour_message_id"] = flavour_message.message_id
    return SHOW_FLAVOURS


async def catch_flavours_text(update: Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        flavour = update.message.text
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=update.message.message_id)
        if flavour not in context.user_data["flavours"]:
            await context.bot.sendMessage(chat_id=update.effective_chat.id,text="That is not a flavour of this product, please use your keyboard",reply_markup = get_list_of_buttons(context.user_data["flavours"]))
            await delete_user_sent_message(update,context)
            return SHOW_FLAVOURS
        context.user_data["current_flavour"] = flavour
    except AttributeError:
        flavour = context.user_data["current_flavour"]
    try:
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["flavour_message_id"])
    except error.BadRequest:
        pass
    product = context.user_data["products"][context.user_data["product_list_position"]]
    context.user_data["instock"] = check_stock(get_from_Product_variations("in_stock",product,flavour))
    formatted_name = format_name_for_image(product,flavour)
    file_id = get_image_file_id(formatted_name)
    markup = single_inline_button("Back to products","back_to_products",context.user_data["instock"])
    flavour_description = re.escape(get_from_Product_flavours("description",flavour)).replace("!", r'\!')
    await context.bot.editMessageMedia(media=InputMediaPhoto(file_id,caption=f"*__Flavour Page__*\n\n*Product Name:* {product+' '+flavour}\n\n*Flavour Profile:* {flavour_description}\n\n*In Stock:* {context.user_data["instock"]}",parse_mode="MarkdownV2"),reply_markup=markup,chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])
    return SHOW_FLAVOURS

async def get_quantity_in_flavour(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    flavour = context.user_data["current_flavour"]
    product = context.user_data["products"][context.user_data["product_list_position"]]
    markup = keypad(get_from_Product_variations("in_stock",product,flavour))
    delete_this = await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Please input the number of tubs you want",reply_markup=markup)
    context.user_data["delete_later"] = delete_this.message_id
    return SHOW_FLAVOURS

async def add_variation_to_cart_in_flavour(update: Update, context:ContextTypes.DEFAULT_TYPE):
    quantity_requested = int(update.message.text)
    if quantity_requested > context.user_data["instock"] or quantity_requested <= 0:
        await send_and_delete("That is not a valid number in stock! Please select again.",update=update,context=context)
        await delete_user_sent_message(update,context)
        return SHOW_FLAVOURS
    product = context.user_data["products"][context.user_data["product_list_position"]]
    flavour = context.user_data["current_flavour"]
    if product in context.user_data["in_cart"]:
        try:
            if context.user_data["in_cart"][product][flavour] + quantity_requested > query_tables.get_from_Product_variations("in_stock",product,flavour):
                await send_and_delete("The number you are trying to add and what you have in cart exceeds the total stock. Please try adding less than the total stock to your cart.",sleep=3.5,update=update,context=context)
                await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
                await delete_user_sent_message(update,context)
                return SHOW_FLAVOURS
            context.user_data["in_cart"][product][flavour] += quantity_requested
        except KeyError:
            context.user_data["in_cart"][product][flavour] = quantity_requested
    else:
        context.user_data["in_cart"][product] = {flavour : quantity_requested}

    await delete_user_sent_message(update,context)
    try:
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
    except KeyError:
        pass
    except error.BadRequest:
        pass
    await send_and_delete(text="Item(s) have been added to cart",reply_markup=get_list_of_buttons(query_tables.get_flavours_for_product(product)),sleep=3,update=update,context=context)
    return SHOW_FLAVOURS

async def back_to_products(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = context.user_data["products"][context.user_data["product_list_position"]]
    formatted_name = format_name_for_image(product)
    file_id = get_image_file_id(formatted_name)
    price = re.escape(str(get_from_Products("price",product)))
    if product in ["Mode","Nitric","Protein"]:
        instock = "Please check individual flavours for their stock"
    else:
        instock = check_stock(get_from_Product_variations("in_stock",product,"None"))
    markup = show_product_buttons(product,instock)

    try:
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
    except error.BadRequest:
        pass
    except KeyError:
        pass
    try:
        await context.bot.editMessageMedia(media=InputMediaPhoto(file_id,caption=f"__{product}__\n*Price\:*{price}\n\n*In Stock:*{instock}",parse_mode="MarkdownV2"),reply_markup=markup,chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])
    except error.BadRequest:
        pass

    delete_this = await context.bot.sendMessage(chat_id=update.effective_chat.id,text="You are back at the product page.",reply_markup=get_list_of_buttons(context.user_data["products"]))
    time.sleep(3)
    await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=delete_this.message_id)
    context.user_data["current_flavour"] = None
    return LIST_PRODUCTS