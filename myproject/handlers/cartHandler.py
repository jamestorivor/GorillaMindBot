from .handlers_utils import *
from ..database import populate_tables, query_tables
from telegram import *
from telegram.ext import *
from ..buttons import *
from prettytable import PrettyTable
from .flavourHandler import back_to_products, catch_flavours_text


(   END,
    SHOW_PRODUCTS,
    LIST_PRODUCTS,
    SHOW_DESCRIPTION,
    SHOW_FLAVOURS,
    CART,
    PAYMENT,
    PAYMENT_CONFIRMATION
) = range(-1,7)



async def go_to_cart(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
    except error.BadRequest:
        pass
    except KeyError:
        pass

    table = PrettyTable()
    table.field_names = ["No.","Product","Price"]
    
    total_amount = 0
    number_of_products = 0
    table_number = 1
    for product in context.user_data["in_cart"]:
        for flavour in context.user_data["in_cart"][product]:
            quantity = context.user_data["in_cart"][product][flavour]
            price = get_from_Products("price",product)
            if quantity > 0 :
                number_of_products += quantity
                total_amount += quantity * price
                if flavour == "None":
                    table.add_row([table_number,f"{quantity}x "+product,quantity*price])
                else:
                    table.add_row([table_number,(f"{quantity}x "+product+"\n"+flavour),f"\n{quantity*price}"])
                table_number += 1
    table.add_row(["","",""])
    if total_amount > 0:
        if number_of_products > 1:
            delivery_fee = "Free"
        else:
            delivery_fee = 2
            total_amount += 2
        table.add_row(["","Delivery",delivery_fee])
    table.add_row(["","Subtotal",total_amount])
    context.user_data["cart_total"] = total_amount
    file_id = get_image_file_id("CartimageDefault.png")
    await context.bot.editMessageMedia(media=InputMediaPhoto(file_id,caption=f"```{table}```",parse_mode="MarkdownV2"),reply_markup=buttons_incart(),chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])

    return CART
    
async def ask_for_item_to_remove(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart_size = 0
    for item in context.user_data["in_cart"]:
        for flavour in context.user_data["in_cart"][item]:
            if context.user_data["in_cart"][item][flavour] > 0:
                cart_size += 1
    if cart_size > 0:
        markup = get_list_of_buttons([x+1 for x in range(cart_size)])
        delete_later = await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Please select the item number that you would like to remove",reply_markup=markup)
        context.user_data["delete_later"] = delete_later.message_id
    else:
        await send_and_delete(text="There is nothing in your cart!",sleep=3,update=update,context=context)
    return CART

async def remove_item(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["delete_later"])
    item_number = int(update.message.text)
    await delete_user_sent_message(update,context)
    table = PrettyTable()
    table.field_names = ["No.","Product","Price"]
    
    prd_no = 1
    table_number = 1
    total_amount = 0
    number_of_products = 0
    for product in context.user_data["in_cart"]:
        for flavour in context.user_data["in_cart"][product]:
            quantity = context.user_data["in_cart"][product][flavour]
            price = get_from_Products("price",product)
            if context.user_data["in_cart"][product][flavour] == 0:
                pass
            elif prd_no == item_number:
                context.user_data["in_cart"][product][flavour] = 0
                prd_no += 1
            else:
                number_of_products += quantity
                total_amount += quantity * price
                if flavour == "None":
                    table.add_row([table_number,f"{quantity}x "+(product),quantity*price])
                else:
                    table.add_row([table_number,(f"{quantity}x "+product+"\n"+flavour),f"\n{quantity*price}"])
                prd_no += 1
                table_number += 1
    table.add_row(["","",""])
    if total_amount > 0:
        if number_of_products > 1:
            delivery_fee = "Free"
        else:
            delivery_fee = 2.0
            total_amount += 2
        table.add_row(["","Delivery",delivery_fee])
    table.add_row(["","Subtotal",total_amount])
    context.user_data["cart_total"] = total_amount
    file_id = get_image_file_id("CartimageDefault.png")
    await context.bot.editMessageMedia(media=InputMediaPhoto(file_id,caption=f"```{table}```",parse_mode="MarkdownV2"),reply_markup=buttons_incart(),chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])

    await send_and_delete(text="Item has been removed from cart",reply_markup=ReplyKeyboardRemove(),sleep=2.5,update=update,context=context)
    return CART

async def back_one(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if context.user_data["products"][context.user_data["product_list_position"]] in ["Mode","Protein","Nitric","Base"]:
        await catch_flavours_text(update,context)
        return SHOW_FLAVOURS
    else:
        await back_to_products(update,context)
        return LIST_PRODUCTS

async def send_order(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        if context.user_data["cart_total"] == 0:
            await send_and_delete("You cant send an empty order!",update,context)
            return CART
        else:
            pass
    except IndexError:
            await send_and_delete("You cant send an empty order!",update,context)
            return CART     
    
    markup = send_order_confirmation()
    context.user_data["send_order_message"] = await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Are you sure you want to send this order?",reply_markup=markup)
    return PAYMENT

async def get_trainer_number(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() in ["confirm","yes"]:
        # PLEASE TYPE YOUR PHONE NUMBER
        await update.message.reply_text("Please type and send your phone number. This will be used to calculate your comission.\nShould the wrong phone number be provided, no comission will be awarded for the order.",reply_markup=ReplyKeyboardRemove())
    else:
        await delete_user_sent_message(update,context)
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data["send_order_message"])
        return CART
    return PAYMENT

async def order_payment(update: Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["phone_number"] = update.message.text
    # PLEASE SEND A SCREENSHOT OF YOUR PAYMNT
    await update.message.reply_text(text="Please PayNow to 91818777 and send a screenshot of the payment here (as an image, no pdf etc...).")
    return PAYMENT_CONFIRMATION

async def get_delivery_address(update: Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["payment_image"] = update.message["photo"][-1]["file_id"]
    await update.message.reply_text("Please send\nBuyer's address(inclusive of postal code), \nName and \nContact number")
    return PAYMENT_CONFIRMATION

# MOVE FROM ORDER_CONFIRMATION TO GET_DELIVERY ADDRESS, UPDATE MESSAGE SENT TO MYSELF.
async def order_confirmation(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.sendPhoto(chat_id="-4151242671",photo=context.user_data["payment_image"],caption=f"Trainer Number: {context.user_data["phone_number"]}\n\nRecipient Details:{update.message.text}")
    await context.bot.forward_message(chat_id="-4151242671",from_chat_id=update.effective_chat.id,message_id=context.user_data["main_message_id"])
    await update.message.reply_text("Your order and proof of payment has been recieved! We will contact you again if there are any issues. Thank you and goodbye.")
    for product in context.user_data["in_cart"]:
        for flavour in context.user_data["in_cart"][product]:
            quantity = context.user_data["in_cart"][product][flavour]
            current_stock = query_tables.get_from_Product_variations("in_stock",product,flavour)
            new_stock = current_stock - quantity
            populate_tables.update_stock(product,new_stock,flavour)
                
    return END