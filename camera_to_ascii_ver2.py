from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np

# ascii grayscale
ascii_greyscale = " .:-=+*#%@"
# ascii_greyscale = r'''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''[::-1]
# font type and size
font_size = 16
font_path = "C:\\Windows\\Fonts\\Consolas\\consola.ttf"
font = ImageFont.truetype(font_path, font_size)

# capture video from camera and get size of image
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(w, h)

# render all possible ascii in green on black background
list_of_image_of_rendered_chars = []
for char in ascii_greyscale:
    white_background_one_char_size = np.ones((font_size, font_size // 2, 3), dtype=np.uint8) * 0
    image = Image.fromarray(white_background_one_char_size)
    draw = ImageDraw.Draw(image)
    draw.text(xy=(0, 0), text=char, font=font, fill=(0, 255, 0))
    list_of_image_of_rendered_chars.append(np.array(image))

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
    ascii_rows = []
    for rows in img_resized:
        ascii_row = []
        for pixel in rows:
            color = int(np.floor(pixel / 256 * len(ascii_greyscale)))
            ascii_row.append(list_of_image_of_rendered_chars[color])
        ascii_rows.append(np.hstack(ascii_row))

    ascii_img = np.vstack(ascii_rows)

    # display original and ascii video
    cv2.imshow('ascii', ascii_img)
    # cv2.imshow('camera', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



