#%%
# import the necessary packages
import cv2
import matplotlib.pyplot as plt
import numpy as np

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

import time
st = time.time()
x_ = list()
y_ = list()
X  = list()
for x in range(W) :
    try :
        _tmp = np.nonzero(edge[:, x])
        _tmp = np.min(_tmp)
        x_.append(x)
        y_.append(_tmp)
        X.append([x_, y_])
    except :
        pass

x_ = np.array(x_)
y_ = np.array(y_)
x_ = x_.reshape(-1, 1)
y_ = y_.reshape(-1, 1)

from sklearn import linear_model
reg = linear_model.LinearRegression()

reg.fit(x_, y_)
print("Linear Approx Time", round(time.time()-st, 2))
print(reg.coef_, reg.intercept_)
p1 = (0, int(reg.coef_[0][0]*0 + reg.intercept_[0]))
p2 = (W, int(reg.coef_[0][0]*W + reg.intercept_[0]))
lin_approx = cv2.line(roi_img, p1, p2, (255, 255, 255), 2)

X = np.array(X)
from sklearn.preprocessing import PolynomialFeatures
poly_features = PolynomialFeatures(degree=2)
x_poly   = poly_features.fit_transform(x_)

lin_reg = linear_model.LinearRegression()
lin_reg.fit(x_poly, y_)
print(lin_reg.intercept_, lin_reg.coef_)


cv2.namedWindow('linear_approx', cv2.WINDOW_NORMAL)
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
cv2.imshow('linear_approx', lin_approx)
cv2.imshow('edge', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()
