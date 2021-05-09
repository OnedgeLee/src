#%%
import cv2
import numpy as np
from copy import deepcopy
from sklearn import linear_model

def main() :
    img_path = '/Users/shetshield/Desktop/python_ws/'
    f_name   = 'processed'
    f_ext    = '.png'
    
    _f  = img_path + f_name + f_ext
    src = cv2.imread(_f)
    dst = deepcopy(src)
    
    width  = src.shape[1]
    height = src.shape[0]
    th1, th2 = 800, 800
    dst = cv2.Canny(src, th1, th2)
    reg = linear_model.LinearRegression()
    cv2.namedWindow('src', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)

    seamline = list()
    x_ = list()
    y_ = list()
    for x in range(width) :
        arr = dst[height//2:, x]
        xy = [x, height//2 + np.min(np.nonzero(arr))]
        x_.append(x)
        y_.append(height//2 + np.min(np.nonzero(arr)))
        seamline.append(xy)

    # print(seamline)
    # print(x_, y_)
    x_ = np.array(x_)
    y_ = np.array(y_)
    x_ = x_.reshape(-1, 1)
    y_ = y_.reshape(-1, 1)
    reg.fit(x_, y_)
    print(reg.coef_, reg.intercept_)
    p1 = (0, int(reg.coef_[0][0]*0 + reg.intercept_[0]))
    p2 = (width, int(reg.coef_[0][0]*width + reg.intercept_[0]))
    
    src = cv2.line(src, p1, p2, (0, 255, 0), 2)
    cv2.imshow('Canny', dst)
    cv2.imshow('src', src)

    k = cv2.waitKey()
    if k == 27 :
        cv2.destroyAllWindows()
    elif k == ord('s') :
        cv2.imwrite('/Users/shetshield/Desktop/python_ws/src.png', src)
        cv2.imwrite('/Users/shetshield/Desktop/python_ws/edge.png', dst)
        cv2.destroyAllWindows()
    # cv2.waitKey()
    # cv2.destroyAllWindows()

if __name__=="__main__" :
    main()