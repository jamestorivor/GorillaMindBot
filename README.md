# GorillaMindBot
Telegram Bot created for Gorilla Mind drop shipping business

1. Start the bot and get information about the bot using '/start' and '/how_to'
![](https://github.com/jamestorivor/GorillaMindBot/blob/main/ReadMeGifs/start-ezgif.com-video-to-gif-converter.gif)

2. Use '/products' to see the products available and toggle through the interactive message
![](https://github.com/jamestorivor/GorillaMindBot/blob/main/ReadMeGifs/products-ezgif.com-video-to-gif-converter.gif)

3. Use the 'Flavours' button to change the interactive message to the desired flavour
![](https://github.com/jamestorivor/GorillaMindBot/blob/main/ReadMeGifs/flavour-ezgif.com-video-to-gif-converter.gif)

4. Use the 'Add to cart' button to add the item you want to cart
![](https://github.com/jamestorivor/GorillaMindBot/blob/main/ReadMeGifs/Add_to_cart-ezgif.com-optimize.gif)

5. Use the 'View Cart' button to view the items you have added to cart (Not a very pretty cart)
 - Use the 'Remove Item' button in the cart page to remove the items that you no longer want
   
![](https://github.com/jamestorivor/GorillaMindBot/blob/main/ReadMeGifs/viewcart-ezgif.com-video-to-gif-converter.gif)



## Advice for people using python-telegram-bot
1. The library's documentation is rather confusing with many overlapping methods. These methods do rather similar things with different use cases.
   For example :
   ```
   update.message.reply_text and context.bot.send_message / context.bot.SendMessage
   ```
   all do relatively similar things.

   From my understanding,
   the methods used in the `update` class (update.METHOD) must be used in response to an update ( a message that the bot can recieve as an update )
   the methods in the `context` class can be used at all times and are more versitile. ( The methods usually have a chat_id and message_id input, suggesting that you are not limited to the current chat)

2. Use `context.bot.user_data` when using a `ConverstaionHandler`. `context.bot.user_data` is a dictionary that stores values until it is cleared or the converstaion is ended.
  This allows you to bring over data from one function to another and keep the message_id of an important message cached

3. If using the bot to send images, use Telegram's caching rather than uploading to a server and using an API to get the images. It is signficantly faster to get the images which are cached on Telegram.





