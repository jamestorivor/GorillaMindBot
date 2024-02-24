from .productHandler import *
from .descriptionHandler import *
from .flavourHandler import *
from telegram import *
from telegram.ext import *
from .cartHandler import *


product_handler = ConversationHandler(
    entry_points=[CommandHandler("products",get_products)],
    states={
        SHOW_PRODUCTS: [MessageHandler(filters.TEXT & (~ filters.COMMAND),show_products)],

        LIST_PRODUCTS : [
            MessageHandler(filters.Regex(r'^[a-zA-Z ]*$')& (~ filters.COMMAND),catch_text),
            CallbackQueryHandler(change_product,pattern="previous_product"),
            CallbackQueryHandler(change_product,pattern="next_product"),
            CallbackQueryHandler(catch_flavour,pattern="flavours_product"),
            CallbackQueryHandler(go_to_cart,pattern="view_cart"),
            CallbackQueryHandler(get_quantity_in_product,pattern="add_to_cart"),
            MessageHandler(filters.Regex(r'\d') & (~ filters.COMMAND),add_variation_to_cart_in_product),
        ],  
        # SHOW_DESCRIPTION: [
        #     CallbackQueryHandler(product_description,pattern="info_product"),
        #     CallbackQueryHandler(next_description,pattern="next_info"),
        #     ],
        SHOW_FLAVOURS: [
            MessageHandler(filters.Regex(r"^[a-zA-Z \'’ñ]+$") & (~ filters.COMMAND),catch_flavours_text),
            CallbackQueryHandler(back_to_products,pattern="back_to_products"),
            CallbackQueryHandler(get_quantity_in_flavour,pattern="add_to_cart"),
            MessageHandler(filters.Regex(r'\d') & (~ filters.COMMAND),add_variation_to_cart_in_flavour),
            CallbackQueryHandler(go_to_cart,pattern="view_cart")
            ],
        CART: [
            MessageHandler(filters.Regex(r'\d') & (~ filters.COMMAND),remove_item),
            CallbackQueryHandler(ask_for_item_to_remove,pattern="remove_item"),
            CallbackQueryHandler(back_one,pattern="back_one"),
            CallbackQueryHandler(send_order,"send_order")
               ],
        PAYMENT: [
            MessageHandler(filters.Regex(r"Confirm") & (~ filters.COMMAND),get_trainer_number),
            MessageHandler(filters.Regex(r'[\d ]+') & (~ filters.COMMAND),order_payment)
        ],
        PAYMENT_CONFIRMATION: [MessageHandler(filters.PHOTO & (~ filters.COMMAND),get_delivery_address),
                               MessageHandler(filters.TEXT & (~ filters.COMMAND),order_confirmation),]
    },
    fallbacks = [CommandHandler("cancel",cancel),],
    per_user=True,
    per_chat=True
)