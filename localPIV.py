from typing import final
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from openpiv import tools, pyprocess, validation, filters, scaling

frame_a = []
gray  = np.array([np.ones([720, 512]),    np.zeros([720, 512])],    dtype=np.uint8)

firstWord = "./test_data_1/test_img_"
finalWord = ".bmp"
file_name = ""

## Figure'un RGB Array'e dönüştürülmesi.
def getFigureAsRGBArray(fig):
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    return img

# Dosya yollarının bir listeye kayıt edilmesi.
for i in range(0, 1199, 1):
    file_name = (firstWord + str(i) + finalWord)
    frame_a.append(file_name)

# Görüntü işleme alanı.
for i in range(0, 1198, 1):
    img_a = cv.imread(frame_a[i])
    img_b = cv.imread(frame_a[i+1])

    gray[0] = cv.cvtColor(img_a, cv.COLOR_BGR2GRAY)
    gray[1] = cv.cvtColor(img_b, cv.COLOR_BGR2GRAY)
    
    # sleep(0.05)

    if (cv.waitKey(1) == ord("q")):
        cv.destroyAllWindows()
        print("Program Sonlandirildi.")
        break

# while False:    
    ## Processing
    winsize    = 25   # pixels, interrogation window size in frame A
    searchsize = 36   # pixels, search area size in frame B
    overlap    = 16   # pixels, 50% overlap
    dt         = 0.02 # sec, time interval between the two frames
    u0, v0, sig2noise = pyprocess.extended_search_area_piv(
        gray[0].astype(np.int32),
        gray[1].astype(np.int32),
        window_size=winsize,
        overlap=overlap,
        dt=dt,
        search_area_size=searchsize,
        sig2noise_method='peak2peak',
    )
    x, y = pyprocess.get_coordinates(image_size=gray[0].shape, search_area_size=searchsize, overlap=overlap)

    ## Post-processing
    u1, v1, mask = validation.sig2noise_val(u0, v0, sig2noise, threshold = 1.05)
    u2, v2 = filters.replace_outliers(u1, v1, method='localmean', max_iter=3, kernel_size=3)
    # convert x, y to mm
    # convert u, v to mm/sec
    x, y, u3, v3 = scaling.uniform(
        x, y, u2, v2,
        scaling_factor = 96.52,  # 96.52 pixels/millimeter
    )
    # 0,0 shall be bottom left, positive rotation rate is counterclockwise
    x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)

    ## result
    tools.save(x, y, u3, v3, mask, 'exp1_001.txt' )
    fig, ax = plt.subplots(figsize=(8, 8))
    fig, ax = tools.display_vector_field(
        'exp1_001.txt',
        ax=ax,
        scaling_factor=100,
        scale=60, # scale defines here the arrow length
        width=0.0025, # width is the thickness of the arrow
        on_img=True, # overlay on the image
        image_name=frame_a[i],
    )

    sonuc = getFigureAsRGBArray(fig)

    cv.imshow("sonuc: ", sonuc)

    dosya_adi = "./result_data_1/img_" + str(i) + ".bmp"
    cv.imwrite(dosya_adi, sonuc)

    if (cv.waitKey(1) == ord("q")):
        cv.destroyAllWindows()
        print("Program Sonlandirildi.")
        break
