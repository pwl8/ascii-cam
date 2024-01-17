from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np

# ascii grayscale
ascii_greyscale = " .:-=+*#%@"[::-1]
font_size = 8
font = 'Consolas'

PATH_TO_IMAGE = "images/lenna.png"
# display original image in grayscale
img = cv2.imread(PATH_TO_IMAGE, flags=cv2.cv2.IMREAD_GRAYSCALE)
cv2.imshow('original image - grayscale', img)
# original size of image
h, w = img.shape[:2]

# # resize image to map each pixel to corresponding ascii character in further step
img_resized = cv2.resize(img, None, fx=2 / font_size, fy=1 / font_size, interpolation=cv2.INTER_AREA)
# stretch histogram
img_resized = cv2.equalizeHist(img_resized)
cv2.imshow('resized image', img_resized)
# convert pixel to ascii representation
ascii_repr = []
for rows in img_resized:
    ascii_row = ''.join([ascii_greyscale[int(np.floor(pixel / 256 * len(ascii_greyscale)))] for pixel in rows])
    ascii_repr.append(ascii_row)
    print(ascii_row)

# create image with ascii text
ascii_img = np.ones((h, w, 3), dtype=img.dtype) * 255

font = ImageFont.truetype('C:\Windows\Fonts\Consolas\consola.ttf', font_size)
img_pil = Image.fromarray(ascii_img)
draw = ImageDraw.Draw(img_pil)
for row, ascii_row in enumerate(ascii_repr):
    draw.text((0, font_size * row), ascii_row, font=font, fill=(0, 0, 0))
ascii_img = np.array(img_pil)

cv2.imshow('white background', ascii_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
