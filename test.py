import cv2 as cv
import sys
import numpy as np
import matplotlib.pyplot as plt
import imageio
from time import sleep
from openpiv import tools, pyprocess, validation, filters, scaling

cap = cv.VideoCapture("http://192.168.137.61:8080/video")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

image = np.array([np.ones([480, 640, 3]), np.zeros([480, 640, 3])], dtype=np.uint8)
gray  = np.array([np.ones([480, 640]),    np.zeros([480, 640])],    dtype=np.uint8)

dikey_siyah = np.ones([480, 10], dtype=np.uint8)
yatay_siyah = np.ones([10, (10 + 640 + 10 + 640 + 10)], dtype=np.uint8)

konum = 0

def getFigureAsRGBArray(fig):
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    print(img.shape)

    return img

while True:
    ret, frame = cap.read()

    image = frame
    
    # cv.imshow("image", image)

    if (konum == 0):
        gray[0] = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # cv.imshow("gray[0]", gray[0])
        cv.imwrite("./exp1_001_a.bmp", gray[0])
        konum += 1
    elif (konum == 1):
        gray[1] = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # cv.imshow("gray[1]", gray[1])

        # Processing
        winsize    = 32 # pixels, interrogation window size in frame A
        searchsize = 40  # pixels, search area size in frame B
        overlap    = 17 # pixels, 50% overlap
        dt         = 0.066 # sec, time interval between the two frames
        
        u0, v0, sig2noise = pyprocess.extended_search_area_piv(
            gray[0].astype(np.int32),
            gray[1].astype(np.int32),
            window_size = winsize,
            overlap = overlap,
            dt = dt,
            search_area_size = searchsize,
            sig2noise_method = 'peak2peak')
        
        x, y = pyprocess.get_coordinates(
            image_size=gray[0].shape,
            search_area_size=searchsize,
            overlap=overlap)
        
        # Post-processing
        u1, v1, mask = validation.sig2noise_val(u0, v0, sig2noise, threshold = 0.55)
        u2, v2       = filters.replace_outliers(u1, v1, method='localmean', max_iter=3, kernel_size=3)
        x, y, u3, v3 = scaling.uniform(x, y, u2, v2, scaling_factor = 96.52)
        x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)
        
        # result
        tools.save(x, y, u3, v3, mask, 'exp1_001.txt' )

        fig, ax = plt.subplots(figsize=(8, 8))
        
        fig, ax = tools.display_vector_field(
            'exp1_001.txt',
            ax = ax,
            scaling_factor = 96.52,
            scale          = 50,
            width          = 0.0035,
            on_img         = True,
            image_name     = "./exp1_001_a.bmp",
        )

        islenmis = getFigureAsRGBArray(fig)

        cv.imshow("islenmis: ", islenmis)

        # sleep(10)

        # dikey_toplam = np.concatenate((dikey_siyah, gray[0], dikey_siyah, gray[1], dikey_siyah), axis = 1)
        # yatay_toplam = np.concatenate((yatay_siyah, dikey_toplam, yatay_siyah), axis = 0)
        # cv.imshow("frame 1", yatay_toplam)
        konum = 0

    if (cv.waitKey(1) == ord("q")):
        cv.destroyAllWindows()
        print("Program Sonlandirildi.")
        break
