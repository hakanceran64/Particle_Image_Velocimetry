#
# Date: 27.10.2021
# Author: Hakan CERAN
# Content: Girilen dosya yolundaki videyu parçalar ve görüntü olarak kayıt eder.
#

import cv2 as cv

# Input Values
file_path_in = "./test_data_1/video/"
file_name_in = "videoplayback.mp4"
file_path    = file_path_in + file_name_in

# Output Values
path      = "./result/video/"
file_name = "img_"
format    = ".bmp"
total_img = 1199

cap = cv.VideoCapture(file_path)

if not cap.isOpened():
    print("Cannot open video")
    exit()

for i in range(0, total_img, 1):
    ret, frame = cap.read()

    dosya_adi = path + file_name + str(i) + format

    cv.imshow("frame: ", frame)
    cv.imwrite(dosya_adi, frame)
    
    if (cv.waitKey(1) & 0xFF == ord("q")):
        cv.destroyAllWindows()
        print("Program Sonlandirildi.")
        break

cap.release()
cv.destroyAllWindows()
