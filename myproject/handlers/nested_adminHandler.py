async def select_function(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [
        [InlineKeyboardButton("Edit Stock", callback_data=str(EDIT_STOCK))]
    ]
    markup = InlineKeyboardMarkup(buttons)
    sent_message = await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Please select what you would like to do today",reply_markup=markup)
    context.user_data["main_message"] = sent_message.id

admin_conv = ConversationHandler(
    entry_points=[CommandHandler("admin_functions",select_function)],
    states={
        MAIN_MENU : [CallbackQueryHandler(select_function,pattern="MAIN_MENU")],
        EDIT_STOCK : [edit_stock_conv],
        # EDIT_PRICE : [edit_price_conv],
        # EDIT_DESCRIPTION : [edit_description_conv],
        # REMOVE_VARIATION : [remove_variation_conv],
        # ADD_NEW_PRODUCT : [new_product_conv],
        # ADD_NEW_VARIATION : [new_varation_conv]
    },
    fallbacks = [CommandHandler("cancel",cancel)],
    )