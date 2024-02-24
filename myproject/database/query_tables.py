from .createDatabase import mydb
from .database_utils import get_single_sql_value,get_list_of_sql_values

def get_column_from_Products(column_name):
    command = f"SELECT {column_name} FROM Products"
    res = mydb.execute_queries(command)
    return get_list_of_sql_values(res)

def get_from_Products(col_name,name):
    command = f"SELECT {col_name} FROM Products WHERE name LIKE %s "
    command_args = ("%" + name + "%",)
    res = mydb.execute_queries(command,command_args) # result is returned as a tuple in a list eg. [(1,)]
    return get_single_sql_value(res)

def get_column_from_Product_flavours(column_name):
    command = f"SELECT {column_name} FROM Product_flavours"
    res = mydb.execute_queries(command)
    return get_list_of_sql_values(res)

def get_from_Product_flavours(column_name,flavour):
    command = f"SELECT {column_name} FROM Product_flavours WHERE flavour = %s"
    command_args = (flavour,)
    res = mydb.execute_queries(command,command_args) # result is returned as a tuple in a list eg. [(1,)]
    return get_single_sql_value(res)

def get_from_Product_variations(col_name,product_name,flavour):
    product_id = get_from_Products("id",product_name)
    flavour_id = get_from_Product_flavours("flavour_id",flavour)
    command = f"SELECT {col_name} FROM Product_variations WHERE product_id = %s AND flavour_id = %s"
    command_args = (product_id,flavour_id)
    res = mydb.execute_queries(command,command_args) # result is returned as a tuple in a list eg. [(1,)]
    return get_single_sql_value(res)

def get_flavours_for_product(product_name):
    product_id = get_from_Products("id",product_name)
    command = f"SELECT flavour FROM Product_flavours WHERE flavour_id IN (SELECT flavour_id FROM Product_variations WHERE product_id = %s AND in_stock != 0) group by flavour;"
    command_args = (product_id,)
    res = mydb.execute_queries(command,command_args)
    return get_list_of_sql_values(res)

def get_all_flavours_for_product(product_name):
    product_id = get_from_Products("id",product_name)
    command = f"SELECT flavour FROM Product_flavours WHERE flavour_id IN (SELECT flavour_id FROM Product_variations WHERE product_id = %s) group by flavour;"
    command_args = (product_id,)
    res = mydb.execute_queries(command,command_args)
    return get_list_of_sql_values(res)

def product_exists(name):
    command = "SELECT COUNT(1) FROM Products WHERE name = %s"
    command_args = (name,)        
    res = mydb.execute_queries(command,command_args)
    if get_single_sql_value(res) >= 1:
        return True
    return False

def flavour_exists(flavour):
    command = "SELECT COUNT(1) FROM Product_flavours WHERE flavour = %s"
    command_args = (flavour,)        
    res = mydb.execute_queries(command,command_args)
    if get_single_sql_value(res) >= 1:
        return True
    return False

def variant_exists(prd_id,flav_id):
    command = "SELECT COUNT(1) FROM Product_variations WHERE (product_id,flavour_id) = (%s,%s)"
    command_args = (prd_id,flav_id)        
    res = mydb.execute_queries(command,command_args)
    if get_single_sql_value(res) >= 1:
        return True
    return False
