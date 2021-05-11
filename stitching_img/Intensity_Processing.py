#%%
import cv2
import numpy as np
from copy import deepcopy
from math import pi

img_path = '/Users/shetshield/Desktop/python_ws/processed/'
f_name   = '10mm_y10mm_darkroom'
f_ext    = '.jpg'

_f  = img_path + f_name + f_ext
src_org = cv2.imread(_f)
src = cv2.cvtColor(src_org, cv2.COLOR_BGR2GRAY)
dst = src.copy()

width  = src.shape[1]
height = src.shape[0]
roi    = 80
th1, th2, th3 = 32, 300, 600

a_thr_min = 10000
a_thr_max = 300000


src_ = deepcopy(src)
_src = deepcopy(src_org)
src_ = deepcopy(src)
# dst = cv2.Canny(src_, th1, th2)
src_  = np.where(src_ < th1, src_*0, 255)
dst1  = cv2.Canny(src_, 0, 0)

cv2.imshow('Canny', src_)
cv2.imshow('src', _src)
cv2.imshow('edge', dst1)
k = cv2.waitKey()
if k == 27 :
    cv2.destroyAllWindows()
elif k == ord('s') :
    cv2.imwrite('/Users/shetshield/Desktop/python_ws/processed2.png', src_)
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
        dst1  = cv2.Canny(src_, 300, 600)
        ret, img_binary = cv2.threshold(src_, 127, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if a_thr_min < area < a_thr_max :
                cv2.drawContours(src_, [cnt], 0, (255, 0, 0), 3)
                cv2.drawContours(_src, [cnt], 0, (255, 0, 0), 3)
        cv2.imshow('processing', src_)
        cv2.imshow('10mm_y10mm_darkroom', _src)
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
        ret, img_binary = cv2.threshold(src_, 127, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if a_thr_min < area < a_thr_max :
                cv2.drawContours(src_, [cnt], 0, (255, 0, 0), 3)
                cv2.drawContours(_src, [cnt], 0, (255, 0, 0), 3)
        cv2.imshow('processing', src_)
        cv2.imshow('10mm_y10mm_darkroom', _src)
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
  
        ret, img_binary = cv2.threshold(src_, 127, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if a_thr_min < area < a_thr_max :
                cv2.drawContours(src_, [cnt], 0, (255, 0, 0), 3)
                cv2.drawContours(_src, [cnt], 0, (255, 0, 0), 3)
  
        cv2.imshow('processing', src_)
        cv2.imshow('10mm_y10mm_darkroom', _src)
        cv2.imshow('edge', dst1)

def main() :
    cv2.namedWindow('processing', cv2.WINDOW_NORMAL)
    cv2.namedWindow('10mm_y10mm_darkroom', cv2.WINDOW_NORMAL)
    cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
    cv2.imshow('10mm_y10mm_darkroom', src_org)
    cv2.imshow('processing', dst)
    cv2.imshow('edge', dst)
    
    cv2.createTrackbar('th1', 'processing', 0, 255, onChange_th1)
    cv2.createTrackbar('th2', 'processing', 0, 255, onChange_th2)
    cv2.createTrackbar('th3', 'processing', 0, 255, onChange_th3)
    
    k = cv2.waitKey(0)
    if k == 27 :
        cv2.destroyAllWindows()


if __name__=="__main__" :
    main()
"""