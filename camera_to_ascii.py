from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np

# ascii grayscale
ascii_greyscale = " .:-=+*#%@"[::-1]
# font type and size
font_size = 16
font_path = "C:\\Windows\\Fonts\\Consolas\\consola.ttf"
font = ImageFont.truetype(font_path, font_size)

# capture video from camera and get size of image
cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# blank white background
blank_ascii_img = np.ones((h, w, 3), dtype=np.uint8) * 255

while True:
    # get frame from camera
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resize image to map each pixel to corresponding ascii character in further step
    # the vertical size of font is usually 2 times bigger then horizontal
    img_resized = cv2.resize(gray, None, fx=2 / font_size, fy=1 / font_size, interpolation=cv2.INTER_AREA)
    # stretch histogram
    img_resized = cv2.equalizeHist(img_resized)
    # convert pixel to ascii representation
    ascii_repr = []
    for rows in img_resized:
        ascii_row = ''.join([ascii_greyscale[int(np.floor(pixel / 256 * len(ascii_greyscale)))] for pixel in rows])
        ascii_repr.append(ascii_row)
    img_pil = Image.fromarray(blank_ascii_img)

    # create image with ascii text
    draw = ImageDraw.Draw(img_pil)
    for row, ascii_row in enumerate(ascii_repr):
        draw.text((0, font_size * row), ascii_row, font=font, fill=(0, 0, 0))
    ascii_img = np.array(img_pil)

    # display original and ascii video
    cv2.imshow('ascii', ascii_img)
    cv2.imshow('camera', img)

    # wait 30 ms
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



