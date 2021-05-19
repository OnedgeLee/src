#%%
# import the necessary packages
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
imagePath = "/Users/shetshield/Desktop/python_ws/new_t1.jpg"

img = cv2.imread(imagePath, 0)
(H, W) = img.shape[:2]
# default 8, 8
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
img2  = clahe.apply(img)

# blur  = cv2.GaussianBlur(img2, (5, 5), 0)
ret, otsu  = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

k1 = 0 # 10
k2 = 0 # 15
inter_list = list()
for x in range(W) :
    _tmp   = np.argwhere(otsu[:, x]==0)
    _inter = (x, _tmp[0][0]+k1, _tmp[-1][0]-k2)
    inter_list.append(_inter)

mk = np.zeros((H, W))
for _inter in inter_list :
    mk[_inter[1]:_inter[2]+1, _inter[0]] = 255
mk = np.uint8(mk)
roi_img = cv2.bitwise_and(img2, mk)
# roi_img = 255-roi_img

#%%

# k-means clustering
img = np.float32(roi_img)
img = img.reshape((-1, 1)) # Vectorization

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
k = 2

ret, label, center = cv2.kmeans(img, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res  = center[label.flatten()]
res2 = res.reshape((roi_img.shape))

contours, hierarchy = cv2.findContours(res2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

area_thr = 10000
c_max = list()
for i in range(len(contours)) :
    cnt  = contours[i]
    area = cv2.contourArea(cnt)
    
    # Small Contour Area Rejection
    if area < area_thr :
        c_min = list()
        c_min.append(cnt)
        
        cv2.drawContours(res2, c_min, -1, (0, 0, 0), thickness=-1)
        continue
    
    c_max.append(cnt)

cv2.drawContours(res2, c_max, -1, (255, 255, 255), thickness=-1)
edge = cv2.Canny(res2, 0, 0)

cv2.namedWindow('res2', cv2.WINDOW_NORMAL)
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
cv2.imshow('res2', res2)
cv2.imshow('edge', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()

#%%
# Gradient Section

diff_list = list()
for _inter in inter_list :
    x     = _inter[0]
    _diff = np.diff(roi_img[_inter[1]:_inter[2]+1, x])
    print(_diff)


#%%

# Filtering and Smoothing Section

"""
# roi_img = 255 - roi_img
sobely = cv2.Sobel(roi_img, cv2.CV_8U, 0, 1, ksize=5)
denoised_img1 = cv2.fastNlMeansDenoising(roi_img, None, 10, 7, 21) # NLmeans
dst4 = cv2.bilateralFilter(roi_img,9,75,75)
dst5 = cv2.medianBlur(roi_img, 9)
th2_i = cv2.adaptiveThreshold(roi_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,7,3)
"""
img_blur = cv2.GaussianBlur(roi_img, (3, 9), 4.5)
img_canny = cv2.Canny(img_blur, 10, 30)
kernel = np.ones((7, 7))
img_dilate = cv2.dilate(img_canny, kernel, iterations=4)
img_erode = cv2.erode(img_dilate, kernel, iterations=4)

kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(roi_img,cv2.MORPH_OPEN,kernel,iterations=2)
# dst = cv2.Canny(roi_img, 50, 150)
contours, _ = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours :
    img = cv2.drawContours(img_erode, [cnt], 0, (255, 0, 0), 1)
# cnt = contours[0]

# roi_img = cv2.medianBlur(roi_img, 3)
# roi_img = cv2.bilateralFilter(roi_img, 13, 75, 75)

hist = cv2.calcHist([roi_img[:, 10]], [0], None, [256], [0, 256])
# print(np.argmax(hist))
# plt.plot(hist)
plt.show()
# roi_img = 255 - roi_img
"""
roi_img2 = clahe.apply(roi_img)
roi_img3 = clahe.apply(roi_img2)
roi_img4 = clahe.apply(roi_img3)
roi_img5 = clahe.apply(roi_img4)
roi_img6 = clahe.apply(roi_img5)
"""

#%%

# Algorithm 1

from scipy.signal import argrelextrema

# res = list()
res_find = list()
res = list()

for _inter in inter_list :
    x = _inter[0]
    res_ = list()
    for j in range(_inter[1], _inter[2]+1) :
        n1 = 0
        tot_int1 = int()
        n2 = 0
        tot_int2 = int()
        for _j in range(_inter[1], _inter[2]+1) :
            if _j <= j :
                tot_int1 += int(roi_img[_j, x])
                n1 += 1
            else :
                tot_int2 += int(roi_img[_j, x])
                n2 += 1
        try :
            """
            if x == 0 :
                print(n1, tot_int2/n2-tot_int1/n1)
            """
            res_.append([x, j, tot_int1, round(tot_int1/n1, 2), n1, tot_int2, round(tot_int2/n2, 2), n2])
            res.append([x, j, tot_int1, round(tot_int1/n1, 2), n1, tot_int2, round(tot_int2/n2, 2), n2])
        except :
            res_.append([x, j, tot_int1, tot_int1/n1, n1, tot_int2, 0, n2])
            res.append([x, j, tot_int1, tot_int1/n1, n1, tot_int2, 0, n2])
    res_ = np.array(res_)
    _lminima = argrelextrema(res_[:, 3], np.less)
    if x == 0 :
        print(_lminima[0].tolist())
    _tmp = [x, _inter[1], _inter[2]+1]
    _tmp.append(_lminima[0].tolist())
    _tmp.extend(res_[_lminima, 3].tolist())
    res_find.append(_tmp)
# print(res_find)
# print(res)
b  = 0
# print(res[0:inter_list[0][2]+1-inter_list[0][1]])
res = np.array(res)
print(res[:150, 3])
# print(res[0:inter_list[0][2]+1-inter_list[0][1], 2:])
# print(res[0:inter_list[0][2]+1-inter_list[0][1], 4:])
plt.plot(res[0:inter_list[b][2]+1 - inter_list[b][1], 3])
# print(argrelextrema(res[0:inter_list[b][2]+1 - inter_list[b][1], 3], np.less))
# plt.plot(np.flip(res[0:inter_list[b][2]+1 - inter_list[b][1], 6]))
plt.plot(res[0:inter_list[b][2]+1 - inter_list[b][1], 6])
# plt.plot(res[0:inter_list[b][2]+1 - inter_list[b][1], 2])
plt.show()
# roi_img = cv2.line(roi_img, p1, p2, (0, 255, 0), 5)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
cv2.namedWindow('otsu', cv2.WINDOW_NORMAL)
cv2.imshow('img', roi_img)
cv2.imshow('img2', img_erode)
cv2.imshow('otsu', img_blur)
cv2.waitKey()
cv2.destroyAllWindows()

# convert the image to grayscale, blur it, and perform Canny
# edge detection

#%%

ret,th1_i = cv2.threshold(roi_img,25,255,cv2.THRESH_BINARY)
th2_i = cv2.adaptiveThreshold(roi_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,25,2)
th3_i = cv2.adaptiveThreshold(roi_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,25,2)
img3 = cv2.Canny(th3_i, 60, 150)

titles = ['Original Image', 'Global Thresholding (v = 100)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

images = [roi_img, th1_i, th2_i, th3_i]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

# plt.subplot(1, 1, 1), plt.imshow(images[2], 'gray')
plt.show()

"""
cv2.namedWindow('img3', cv2.WINDOW_NORMAL)
cv2.imshow('img3', img3)
cv2.waitKey()
cv2.destroyAllWindows()
"""
#%%

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
img = roi_img
(H, W) = img.shape[:2]
"""
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
blur  = cv2.GaussianBlur(clahe, (5, 5), 0)
otsu  = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
"""
# src = clahe.apply(img)
# src_org = src
src = roi_img*2
src_org = roi_img

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

#%%
src = roi_img*2
src_org = roi_img
dst = cv2.Canny(src, 160, 50)

width  = src.shape[1]
height = src.shape[0]
roi    = 80
th1, th2 = 0, 0

def onChange_th1(k) :
    global th1
    if k > 0 :
        th1 = k
        try :
            _src = deepcopy(src_org)
            lines = cv2.HoughLinesP(dst, 1, pi/180, 40, minLineLength=th1, maxLineGap=th2)
            for i, line in enumerate(lines) :
                if height/2 - roi < line[0][1] < height/2 + roi and height/2 - roi < line[0][3] < height/2 + roi :
                    cv2.line(_src, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 2)
            cv2.imshow('HoughP', _src)
        except :
            cv2.imshow('HoughP', _src)

def onChange_th2(k) :
    global th2
    if k > 0 :
        th2 = k
        try :
            _src = deepcopy(src_org)
            lines = cv2.HoughLinesP(dst, 1, pi/180, 40, minLineLength=th1, maxLineGap=th2)
            for i, line in enumerate(lines) :
                if height/2 - roi < line[0][1] < height/2 + roi and height/2 - roi < line[0][3] < height/2 + roi :
                    cv2.line(_src, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 2)
            cv2.imshow('HoughP', _src)
        except :
            cv2.imshow('HoughP', _src)

def main() :
    cv2.imshow('HoughP', src)
    cv2.imshow('Canny', dst)
    
    cv2.createTrackbar('th1', 'HoughP', 0, 600, onChange_th1)
    cv2.createTrackbar('th2', 'HoughP', 0, 600, onChange_th2)
    
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__=="__main__" :
    main()