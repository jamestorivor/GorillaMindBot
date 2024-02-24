from ..buttons import *
from telegram import *
from telegram.ext import *
from ..database.query_tables import *
import os
import csv
import time


def get_image_list():
    path = "/Users/marcus/Documents/GorillaMind/myproject/database/static/gorillamindimages/"
    image_list = {}
    for filename in os.listdir(path):
        image = open(path + filename,"rb")
        image_list[filename] = image
    return image_list

def get_image_file_id(name):
    path = "/Users/marcus/Documents/GorillaMind/myproject/database/static/cachedimages.csv"
    with open(path,"r") as file:
        reader_obj = csv.reader(file)
        csv_headings = next(reader_obj)
        name_index = csv_headings.index("file_name")
        id_index = csv_headings.index("file_id")
        for line in reader_obj:
            if line[name_index] == name:
                return line[id_index]


def reposition(current_position,list_length):
    if 0 <= current_position < list_length:
        return current_position
    elif current_position == list_length:
        return 0
    elif current_position == -1:
        return list_length - 1

def format_name_for_image(product_name,flavour=None):
    if flavour == None or flavour == "None":
        return product_name.title() + "Default.png"
    return product_name.title() + "_" + flavour.replace(" ","") + ".png"

async def send_and_delete(text,update,context,reply_markup=None,sleep=1.8):
    delete_this = await context.bot.sendMessage(chat_id=update.effective_chat.id,text=f"{text}",reply_markup=reply_markup)
    time.sleep(sleep)
    await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=delete_this.message_id)

def check_stock(number):
    if number > 0:
        return number
    else:
        return "Out of stock\!"
    
async def delete_user_sent_message(update,context):
    await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=update.message.id)
