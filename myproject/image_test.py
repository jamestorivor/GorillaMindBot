import os
from os import listdir
import base64
import requests
import json 

product_images = {}

def get_product_image():
    folder_dir = "/Users/marcus/Documents/GorillaMindSupplements/database/gorillamindimages"
    images = os.listdir(folder_dir)
    i = 0
    for image in images:
        with open(folder_dir + "/"+ image,"rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key" : "",
                "image" : base64.b64encode(file.read()),
            }
            response = requests.post(url,payload)
            if response.status_code == 200:
                product_images[image] = {"photo_url":response.json()["data"]["url"], "thumb_url":response.json()["data"]["thumb"]["url"]}
        break
    print(product_images)


get_product_image()
