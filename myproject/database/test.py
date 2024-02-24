# from io import BytesIO
# from requests import *
# from image_location import image_links
# from PIL import Image

# image_link = image_links['DreamIngredients.png']

# photo_url=image_link["photo_url"]
# image_binary = get(photo_url).content
# img_strem = BytesIO(image_binary)
# image = Image.open(img_strem)
# image.show()

him = {"this":"that",
 "not_this": "Not_that"}

for row in him:
    print(row)