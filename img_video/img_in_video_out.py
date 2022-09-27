#
# Date: 27.10.2021
# Author: Hakan CERAN
# Content: Girilen dosya yolundaki görüntüleri video formatına dönüştürür.
#

import cv2 as cv

# Input Values
file_path_in   = "./result_data_1/"
file_name_in   = "img_"
file_format_in = ".bmp"
total_img      = 1199

# Output Values
path      = "./result_data_1/video/"
file_name = "output-8-fps"
format    = ".avi"
fps       = 8.0
frame     = (800, 800)
file_path = path + file_name + format

# codec tanımlama ve VideoWriter nesnesi oluşturma bilgi için bkz: https://www.fourcc.org/codecs.php
fourcc = cv.VideoWriter_fourcc(*'XVID')

# Kaydedilecek video dosyasının adı, uzantısı, konumu, saniyedeki çerçeve sayısı ve çözünürlüğü
out = cv.VideoWriter(file_path, fourcc, fps, frame)

file_name_list = []
temp_name      = ""

# Dosya yollarının bir listeye kayıt edilmesi.
for i in range(1, total_img, 1):
        temp_name = (file_path_in + file_name_in + str(i) + file_format_in)
        file_name_list.append(temp_name)

# Görüntülerin video formatında kayıt edilmesi.
for i in range(1, total_img, 1):
    result_img = cv.imread(file_name_list[i])

    cv.imshow("result_img: ", result_img)
    
    # sleep(0.1)

    # cv.flip(src, flipCode, dst) 2 boyutlu diziyi dikey yatay veya her iki eksen etrafında döndürür.
    # 0 => dikey döndürme
    # 1 => yatay döndürme
    # 2 => hem yatay hem dikey döndürme
    # frame = cv.flip(result_img,1,dst=None)
 
    # Gelen görüntüyü video dosyasına yaz.
    out.write(result_img)

    if (cv.waitKey(1) == ord("q")):
        cv.destroyAllWindows()
        print("Program Sonlandirildi.")
        break

out.release()
cv.destroyAllWindows()