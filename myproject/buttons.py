from telegram import *
from telegram.ext import * 


# Add information button and handler
def show_product_buttons(product,stock):
    cart_buttons = [InlineKeyboardButton("View Cart", callback_data="view_cart")]
    with_flavours = ["Mode","Protein","Nitric","Base"]
    reply_markup = [
        [InlineKeyboardButton(text="Previous",callback_data="previous_product"),
        # InlineKeyboardButton(text="Information",callback_data="info_product"),
        InlineKeyboardButton(text="Next",callback_data="next_product")]
        ]
    if product in with_flavours:
        reply_markup.append([InlineKeyboardButton(text="Flavours",callback_data="flavours_product")])
    else:
        if isinstance(stock,int):
            cart_buttons = [
                InlineKeyboardButton("View Cart", callback_data="view_cart"),
                InlineKeyboardButton("Add to cart",callback_data="add_to_cart")
                ]
        reply_markup.append(cart_buttons)
    return InlineKeyboardMarkup(reply_markup)

def show_description_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Previous",callback_data="previous_product"),
        InlineKeyboardButton(text="Back",callback_data="info_product"),
        InlineKeyboardButton(text="Next",callback_data="next_product")],
    ])

def get_list_of_buttons(name_list=list()):
    button_list = []
    if len(name_list) > 0:
        for button_name in name_list:
            button_list.append([KeyboardButton(button_name)])   
        return ReplyKeyboardMarkup(button_list,resize_keyboard=True)
    
def get_list_of_inline_buttons(name_list=list()):
    button_list = []
    if len(name_list) > 0:
        for button_name in name_list:
            button_list.append([InlineKeyboardButton(button_name,callback_data=button_name)])   
        return InlineKeyboardMarkup(button_list)

def single_inline_button(name,callback,stock):
    cart_buttons = [InlineKeyboardButton("View Cart", callback_data="view_cart")]
    if isinstance(stock,int):
        cart_buttons = [
                InlineKeyboardButton("View Cart", callback_data="view_cart"),
                InlineKeyboardButton("Add to cart",callback_data="add_to_cart")
                ]
    return InlineKeyboardMarkup([[InlineKeyboardButton(text=name,callback_data=callback)],cart_buttons])

def keypad(number):
    number_pad = [[KeyboardButton(text=f"{n+1}")] for n in range(number)]

    return ReplyKeyboardMarkup(number_pad,one_time_keyboard=True,resize_keyboard=True)

def buttons_incart():
    reply_markup = [
        [InlineKeyboardButton(text="Remove item",callback_data="remove_item")],
        [InlineKeyboardButton(text="Back to products",callback_data="back_one"),
        InlineKeyboardButton(text="Send Order",callback_data="send_order")]
        ]
    return InlineKeyboardMarkup(reply_markup)

def send_order_confirmation():
    reply_markup = [
        [KeyboardButton(text="Confirm"),KeyboardButton(text="Back")]
    ]
    return ReplyKeyboardMarkup(reply_markup)