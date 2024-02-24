from ..database import query_tables
from requests import *
from telegram import *
from telegram.ext import *
from ..buttons import *
from ..database import populate_tables
from .handlers_utils import *

(   END,
    GET_IMAGE,
) = range(-1,1)



# async def admin_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     return ADMIN_FUNCTIONS


async def add_flavour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter the name of the image in this format : <NameClustered>_<FlavourOptional>")


async def cache_stored_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header = ['file_name','file_id']
    # path = os.getcwd() + "/images/"
    path = "/Users/marcus/Documents/GorillaMind/myproject/database/static/"
    with open(path+"cachedimages.csv","w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for file_name in os.listdir(path+"gorillamindimages"):
            if file_name.startswith("."):
                continue
            infophoto = await context.bot.sendPhoto(chat_id='-4023656196',photo=open(path+"gorillamindimages/"+file_name,'rb'))
            originalphoto = infophoto["photo"][-1]["file_id"]
            writer.writerow([file_name,originalphoto])

async def caches_new_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter the name of the image in this format : <NameClustered>_<FlavourOptional>")
    return GET_IMAGE

async def get_photo_to_cache(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cache_name"] = update.message.text.replace(" ","")
    await update.message.reply_text("Please send the image you want to cache")
    return GET_IMAGE

async def send_cache_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        product, flavour = context.user_data["cache_name"].split("_")
    except ValueError:
        product = context.user_data["cache_name"]
        flavour = "None"
    file_name = format_name_for_image(product,flavour)
    original_photo = update.message["photo"][-1]["file_id"]
    path = "/Users/marcus/Documents/GorillaMind/myproject/database/static/"
    with open(path+"cachedimages.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow([file_name,original_photo]) 
    file.close()
    await update.message.reply_text(f"Your image has been cached with {file_name} file name and {original_photo} this message_id")
    return END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return END

# admin_handler = ConversationHandler(
#     entry_points=[CommandHandler("upload_image",caches_new_photos)],
#     states={
#         # ADMIN_FUNCTIONS : [],
#         GET_IMAGE : [
#             MessageHandler(filters.TEXT,get_photo_to_cache),#Regex(r'(?i)([^\\s]+(\\.(jpe?g|png|gif|bmp))$)')
#             MessageHandler(filters.PHOTO,send_cache_confirmation)
#             ]
        
#     },
#     fallbacks = [CommandHandler("cancel",cancel)],
#     )

# admin_handler = ConversationHandler(
#     entry_points=[CommandHandler("admin_permissions",check_permissions)],
#     states={
#         SELECT_FUNCTION : [],
#         MAIN_PAGE: [
#             MessageHandler(filters.TEXT,get_photo_to_cache),#Regex(r'(?i)([^\\s]+(\\.(jpe?g|png|gif|bmp))$)')
#             MessageHandler(filters.PHOTO,send_cache_confirmation)
#             ],
#         ADD_NEW_PRODUCT
        
#     },
#     fallbacks = [CommandHandler("cancel",cancel)],
#     )


# # (END,
# #  GET_PRODUCT_FLAVOUR,
# #  GET_EACH_IMAGE,
# #  COMPLETE_IMAGE_ADDITION,
# #  PARENT_STATE) = range(-1,4)

# async def get_new_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     update.message.reply_text("Please send the name of the product you want to add (Mode, Nitric, Protein, Etc...)")
#     return GET_PRODUCT_FLAVOUR

# async def get_product_flavour(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["new_product"] = update.message.text
#     update.message.reply_text("Please send the flavours of the products in the order of the images you send : Strawberry, Cotton Candy Lasgna, etc... or None if there is no flavour")
#     return GET_EACH_IMAGE

# async def get_each_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["flavour_names"] = [flavour for flavour in update.message.text.split(", ").lower().title()]
#     update.message.reply_text("Please send the images of the variations of the products you wish to add")
#     try:
#         context.user_data["variant_images"].append(update.message["photo"][-1]["file_id"])
#     except IndexError:
#         context.user_data["variant_images"] = []
#     return GET_EACH_IMAGE

# async def complete_image_addition(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     update.message.reply_text("The new product, it's variations and their images have been cached")
#     return PARENT_STATE

# add_new_product_conv = ConversationHandler(
#     entry_points=[CallbackQueryHandler(get_new_product_name,"new_product")],
#     states={
#         DESCRIPTION: [
#             MessageHandler(filters.TEXT,get_new_product_description)
#             ],
#         PRICE : [MessageHandler(filters.TEXT,get_new_product_price)],
#         FLAVOUR : [MessageHandler(filters.Regex(r"\d"),get_new_product_flavour)],
#         FLAVOUR_DESC : [MessageHandler(filters.TEXT,get_new_product_flavour_desc)],
#         FLAVOUR_IMAGE : [CallbackQueryHandler(get_variation_image)]
#     },
#     fallbacks = [CommandHandler("cancel",cancel)],
#     map_to_parent={END : SELECT_FUNCTION}
#     )


### EDIT STOCK CONV
(VARIATION,GET_STOCK,UPDATE_STOCK) = range(2,5)

async def product_stock_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product_list = query_tables.get_column_from_Products("name")
    markup = get_list_of_buttons(product_list)
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Please select the product to edit",reply_markup=markup)
    return VARIATION

async def product_variation_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    flavour_list = query_tables.get_all_flavours_for_product(context.user_data["product"])
    markup = get_list_of_buttons(flavour_list)
    await update.message.reply_text("Please select the variation to edit the stock of",reply_markup=markup)
    return GET_STOCK

async def get_new_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["flavour"] = update.message.text
    await update.message.reply_text("Please input the new stock",reply_markup=ReplyKeyboardRemove())
    return UPDATE_STOCK

async def change_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        new_stock = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Please input an integer")
        return UPDATE_STOCK
    populate_tables.update_stock(context.user_data["product"],new_stock,context.user_data["flavour"])
    await update.message.reply_text("The stock of the item has been updated.")
    return END
    
edit_stock_conv = ConversationHandler(
    entry_points=[CommandHandler("edit_stock", product_stock_edit)],
    states={
        VARIATION: [
            MessageHandler(filters.TEXT,product_variation_edit)
            ],
        GET_STOCK:[MessageHandler(filters.TEXT,get_new_stock)],
        UPDATE_STOCK : [MessageHandler(filters.TEXT,change_stock)]
    },
    fallbacks = [CommandHandler("cancel",cancel)],
)

### EDIT PRICE CONV
(GET_PRICE,UPDATE_PRICE) = range(5,7)

async def product_price_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product_list = query_tables.get_column_from_Products("name")
    markup = get_list_of_buttons(product_list)
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Please select the product to edit",reply_markup=markup)
    return GET_PRICE

async def get_new_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    await update.message.reply_text("Please input the new price",reply_markup=ReplyKeyboardRemove())
    return UPDATE_PRICE

async def change_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        new_price = float(update.message.text)
    except ValueError:
        await update.message.reply_text("Please input in this format (eg. 20.00 / 20)")
        return UPDATE_STOCK
    populate_tables.update_price(context.user_data["product"],new_price)
    await update.message.reply_text("The price of the item has been updated.")
    return END
    
    

edit_price_conv = ConversationHandler(
    entry_points=[CommandHandler("edit_price", product_price_edit)],
    states={
        GET_PRICE:[MessageHandler(filters.TEXT,get_new_price)],
        UPDATE_PRICE : [MessageHandler(filters.Regex("[\d.]"),change_price)]
    },
    fallbacks = [CommandHandler("cancel",cancel)],
)
