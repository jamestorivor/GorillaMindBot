import os
import base64
from requests import *
from io import BytesIO

def load_sql_file(path):
    with open(path,'r') as file:
        # Splits all the the sql create table commands
        sql = file.read().replace("\n","").split(";")
        # Removes last empty string due to the split(delimiter)
        sql.pop()
        return sql

def get_single_sql_value(result):
    try:
        value = result[0][0]
        return value
    except:
        raise Exception("Null Query, no values extracted")
    
def get_list_of_sql_values(result) -> list:
    values = []
    try:
        for item in result:
            values.append(item[0])
        return values
    except:
        raise Exception("Null Query, no values extracted")


def upload_images():
    product_images = {}
    folder_dir = "/Users/marcus/Documents/GorillaMindSupplements/database/gorillamindimages"
    images = os.listdir(folder_dir)
    for image in images:
        with open(folder_dir + "/"+ image,"rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key" : "8adab157863ffd0f4479762da90dafb7",
                "image" : base64.b64encode(file.read()),
            }
            response = post(url,payload)
            if response.status_code == 200:
                product_images[image] = {"photo_url":response.json()["data"]["url"], "thumb_url":response.json()["data"]["thumb"]["url"]}
    return product_images


# def get_product_image(product_name):
#     image_link = image_links[f'{product_name}.png']
#     photo_url=image_link["photo_url"]
#     image_binary = get(photo_url,headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).content
#     image = BytesIO(image_binary)
#     return image

