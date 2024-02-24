from .createDatabase import mydb
from .query_tables import *

def add_to_Products(name,description,price):
    command = "INSERT INTO Products (name,description,price) VALUES (%s,%s,%s)"
    command_args = (name,description,price)
    mydb.execute_commands(command,command_args)

def add_to_Product_flavours(flavour,description):
    command = "INSERT INTO Product_flavours (flavour,description) VALUES (%s,%s)"
    command_args = (flavour,description)
    mydb.execute_commands(command,command_args)

def add_to_Product_variations(product_name,flavour,in_stock):
    product_id = get_from_Products("id",product_name)
    flavour_id = get_from_Product_flavours("flavour_id",flavour)
    command = "INSERT INTO Product_variations (product_id,flavour_id,in_stock) VALUES (%s,%s,%s)"
    command_args = (product_id,flavour_id,in_stock)
    mydb.execute_commands(command,command_args)

def update_stock(product_name,new_stock,flavour):
    product_id = get_from_Products("id",product_name)
    flavour_id = get_from_Product_flavours("flavour_id",flavour)
    command = "UPDATE Product_variations SET in_stock = %s WHERE (product_id, flavour_id) = (%s,%s)"
    command_args = (new_stock,product_id,flavour_id)
    mydb.execute_commands(command,command_args)

def update_price(product_name,new_price):
    product_id = get_from_Products("id",product_name)
    command = "UPDATE Products SET price = %s WHERE (product_id) = (%s)"
    command_args = (new_price,product_id)
    mydb.execute_commands(command,command_args)


# for flavour in flavours:
#     add_to_Product_flavours(flavour,flavours[flavour])
# add_to_Product_flavours("Capsules","Well, tastes like capsules")

# for product in products:
#     product_id = get_from_Products("id",product)
#     if product in ["Mode","Nitric"]:
#         for flavour in flavours:
#             flavour_id = get_from_Product_flavours("flavour_id",flavour)
#             add_to_Product_variations(product_id,flavour_id,0)
#     else:
#         flavour_id = get_from_Product_flavours("flavour_id","Capsules")
#         add_to_Product_variations(product_id,flavour_id,0)

if __name__ == '__main__':
    add_to_Product_flavours("Sour Candy Apple"," A carnival classic, bursting with crisp, sweet, and sour deliciousness.")