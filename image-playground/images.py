from PIL import Image, ImageFilter

img = Image.open('./astro.jpg')
new_img = img.resize((400, 400))
new_img.save('thumbnail.jpg')

