from PIL import Image, ImageStat
import numpy, sys 

num_input = (str)(input("Enter image number: "))
k_input = int(input("Enter K value: "))

img = "img/test" + num_input.zfill(2) + ".jpg"
im = Image.open(img)

px = im.load()

r,g,b = px[100,100]

print(r," ",g," ",b)
