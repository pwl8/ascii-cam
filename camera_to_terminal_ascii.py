import cv2
import os
import numpy as np
import time



# ascii_greyscale = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
ascii_greyscale = " .:-=+*#%@"
# Console size
LINE, ROW = 60, 200

cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# resize image to higher dimension of console window size
ratio = max(h / (LINE * 2), w / ROW)
# compute final size
h_dst, w_dst = int(h / 2 // ratio), int(w // ratio)

while True:
    ret, img = cap.read()
    #cv2.imshow('frame', img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img, (w_dst, h_dst), interpolation=cv2.INTER_AREA)
    img_resized = cv2.equalizeHist(img_resized)
    ascii_repr = ['\n']
    for rows in img_resized:
        for pixel in rows:
            color = int(np.floor(pixel / 256 * len(ascii_greyscale)))
            ascii_repr.append(ascii_greyscale[::-1][color])
        ascii_repr.append('\n')

    os.system('cls')
    print(''.join(ascii_repr))
    time.sleep(1/60)




