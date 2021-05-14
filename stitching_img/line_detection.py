#%%
# import the necessary packages
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
imagePath = "/Users/user/Desktop/python_ws/new_t1.jpg"

img = cv2.imread(imagePath, 0)
(H, W) = img.shape[:2]

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
img2  = clahe.apply(img)

blur  = cv2.GaussianBlur(img2, (5, 5), 0)
ret, otsu  = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

inter_list = list()
for x in range(W) :
    _tmp   = np.argwhere(otsu[:, x]==0)
    _inter = (x, _tmp[0][0], _tmp[-1][0])
    inter_list.append(_inter)

mk = np.zeros((H, W))
for _inter in inter_list :
    mk[_inter[1]:_inter[2]+1, _inter[0]] = 255
mk = np.uint8(mk)

roi_img = cv2.bitwise_and(img2, mk)
roi_img2 = clahe.apply(roi_img)
roi_img3 = clahe.apply(roi_img2)
roi_img4 = clahe.apply(roi_img3)

a = random.uniform(-1, 1)
b = random.uniform(inter_list[0][1], inter_list[0][2]+1)
Int_Up = int()
Int_Do = int()
for _inter in inter_list :
    y = a * _inter[0] + b
    # print(y)
    if y < _inter[1] :
        y = _inter[1] - 1
    elif y > _inter[2] :
        y = _inter[2] + 1
    for j in range(_inter[1], _inter[2]+1) :
        if j <= y :
            Int_Up += roi_img[j, _inter[0]]
        else :
            Int_Do += roi_img[j, _inter[0]]


print(Int_Up, Int_Do)

#%%

p1 = (0, int(b))
p2 = (W-1, int(a*(W-1) + b))
roi_img = cv2.line(roi_img, p1, p2, (0, 255, 0), 5)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
cv2.namedWindow('otsu', cv2.WINDOW_NORMAL)
cv2.imshow('img', img)
cv2.imshow('img2', roi_img)
cv2.imshow('otsu', otsu)
cv2.waitKey()
cv2.destroyAllWindows()


# convert the image to grayscale, blur it, and perform Canny
# edge detection

#%%

ret,th1_i = cv2.threshold(img2,25,255,cv2.THRESH_BINARY)
th2_i = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3_i = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
img3 = cv2.Canny(th3, 60, 150)

cv2.namedWindow('img3', cv2.WINDOW_NORMAL)
cv2.imshow('img3', img3)
cv2.waitKey()
cv2.destroyAllWindows()

#%%

titles = ['Original Image', 'Global Thresholding (v = 100)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

images = [img2, th1_i, th2_i, th3_i]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

# plt.subplot(1, 1, 1), plt.imshow(images[2], 'gray')
plt.show()
# construct a blob out of the input image for the Holistically-Nested
# Edge Detector
# set the blob as the input to the network and perform a forward pass
# to compute the edges
print("[INFO] performing holistically-nested edge detection...")

#%%
import cv2
import numpy as np
from copy import deepcopy
from math import pi

img_path = "/Users/user/Desktop/python_ws/new_t1.jpg"
f_name   = 'seam'
f_ext    = '.jpg'


imagePath = "/Users/user/Desktop/python_ws/new_t1.jpg"
# img = cv2.imread(imagePath, 0)
img = th2_i
(H, W) = img.shape[:2]

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
blur  = cv2.GaussianBlur(clahe, (5, 5), 0)
otsu  = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
src = clahe.apply(img)
src_org = src

# _f  = img_path # + f_name + f_ext
# src_org = cv2.imread(_f)
# src = cv2.cvtColor(src_org, cv2.COLOR_BGR2GRAY)
dst = src.copy()

width  = src.shape[1]
height = src.shape[0]
roi    = 80
th1, th2, th3 = 25, 300, 600

a_thr_min = 10000
a_thr_max = 300000
cv2.namedWindow('src', cv2.WINDOW_NORMAL)
cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
"""
src_ = deepcopy(src)
_src = deepcopy(src_org)
src_ = deepcopy(src)
# dst = cv2.Canny(src_, th1, th2)
src_  = np.where(src_ < th1, src_*0, 255)
dst1  = cv2.Canny(src_, 300, 600)
ret, img_binary = cv2.threshold(src_, 127, 255, 0)

cv2.imshow('Canny', src_)
cv2.imshow('src', _src)
cv2.imshow('edge', dst1)
k = cv2.waitKey()
if k == 27 :
    cv2.destroyAllWindows()
elif k == ord('s') :
    cv2.imwrite('/Users/shetshield/Desktop/python_ws/processed.png', src_)
    cv2.destroyAllWindows()
"""
def onChange_th1(k) :
    global th1
    if k > 0 :
        th1 = k
        _src = deepcopy(src_org)
        src_ = deepcopy(src)
        # dst = cv2.Canny(src_, th1, th2)
        src_  = np.where(src_ < th1, src_*0, 255)
        dst1  = cv2.Canny(src_, th2, th3)
        """
        ret, img_binary = cv2.threshold(src_, 127, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if a_thr_min < area < a_thr_max :
                cv2.drawContours(src_, [cnt], 0, (255, 0, 0), 3)
                cv2.drawContours(_src, [cnt], 0, (255, 0, 0), 3)
        """
        cv2.imshow('Canny', src_)
        cv2.imshow('src', _src)
        cv2.imshow('edge', dst1)
        c = cv2.waitKey(1)
        if c == ord('s') :
            cv2.imwrite('/Users/shetshield/Desktop/python_ws/processed.png', src_)
            cv2.destroyAllWindows()
def onChange_th2(k) :
    global th2
    if k > 0 :
        th2 = k
        _src = deepcopy(src_org)
        src_ = deepcopy(src)
        # dst = cv2.Canny(src_, th1, th2)
        src_  = np.where(src_ < th1, src_*0, 255)
        dst1   = cv2.Canny(src_, th2, th3)
        """
        ret, img_binary = cv2.threshold(src_, 127, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if a_thr_min < area < a_thr_max :
                cv2.drawContours(src_, [cnt], 0, (255, 0, 0), 3)
                cv2.drawContours(_src, [cnt], 0, (255, 0, 0), 3)
        """
        cv2.imshow('Canny', src_)
        cv2.imshow('src', _src)
        cv2.imshow('edge', dst1)
        
def onChange_th3(k) :
    global th3
    if k > 0 :
        th3 = k
        print(th1, th2, th3)
        _src = deepcopy(src_org)
        src_ = deepcopy(src)
        # dst = cv2.Canny(src_, th1, th2)
        src_  = np.where(src_ < th1, src_*0, 255)
        dst1  = cv2.Canny(src_, th2, th3)
        """
        ret, img_binary = cv2.threshold(src_, 127, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if a_thr_min < area < a_thr_max :
                cv2.drawContours(src_, [cnt], 0, (255, 0, 0), 3)
                cv2.drawContours(_src, [cnt], 0, (255, 0, 0), 3)
        """
        cv2.imshow('Canny', src_)
        cv2.imshow('src', _src)
        cv2.imshow('edge', dst1)
def main() :
    cv2.namedWindow('src', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
    cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
    cv2.imshow('src', src_org)
    cv2.imshow('Canny', dst)
    cv2.imshow('edge', dst)
    
    cv2.createTrackbar('th1', 'Canny', 0, 255, onChange_th1)
    cv2.createTrackbar('th2', 'Canny', 0, 2000, onChange_th2)
    cv2.createTrackbar('th3', 'Canny', 0, 2000, onChange_th3)
    
    k = cv2.waitKey(0)
    if k == 27 :
        cv2.destroyAllWindows()
if __name__=="__main__" :
    main()
