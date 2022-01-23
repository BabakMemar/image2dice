
from PIL import Image, ImageOps, ImageDraw
from math import ceil

def get_image(path):
    #load the image and convert it to black and white
    img = Image.open(path)
    img = ImageOps.grayscale(img)
    img = ImageOps.equalize(img)

    return img

def image_preprocess(img, width, height):
    new_image = img.resize((width, height))
    
    return new_image

def dice_process(img, diceSize):
    dice_width = ceil(float(img.width) / dice_size) #round to up
    dice_height  = ceil(float(img.height) / dice_size)
    diceNumber = dice_width * dice_height #total number of dices that is needed

    new_img = Image.new(mode="L", size=(img.width, img.height), color="white") #creat a raw image with the same size of original image
    new_img_d = ImageDraw.Draw(new_img) #creat an object to draw on image

    for h in range(0, img.height - dice_size, dice_size):
        for w in range(0, img.width - dice_size, dice_size):
            sectorColor = 0
            for diceh in range(0, dice_size):
                for dicew in range(0, dice_size):
                    pixelColor = img.getpixel((w + dicew, h + diceh))
                    sectorColor += pixelColor
            sectorColor /= (dice_size ** 2) #calculate the average of the amount of pixels in each dice, between 0-255
            new_img_d.rectangle([(w, h), (w + dice_size, h + dice_size)], int(sectorColor))

            diceDigit = str(int((255 - sectorColor) * 6 / 255 + 1)) #change the scale from 0-255 to 1-6
            with open("image.txt", "a") as f:
                f.write(diceDigit)
            f.close()
        with open("image.txt", "a") as f:
            f.write("\n")
        f.close()
            # print(diceDigit, end=" ")
        # print()
    print("The total number of dices you need: ", diceNumber)
    # new_img.show()

# path = input("Please enter the path of your image: ")
path = "C:/Users/Win 1809 UEFI/Pictures/Wallpapers/Wallpaper (126).jpg"
print("Please enter the size of your picture frame")
sizeWidth = int(input("Frame width: "))
sizeHeight = int(input("Frame height:" ))
dice_size = int(input("Please enter the size of the dice in centimeters: "))
image = get_image(path)
image = image_preprocess(image, sizeWidth, sizeHeight)
dice_process(image, dice_size)