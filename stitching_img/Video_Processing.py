#%%
"""
    Video Processing
"""
# import the necessary packages
import cv2, time, os
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from sklearn import linear_model

st = time.time()
videoPath = "/Users/shetshield/Desktop/python_ws/hj_2nd/seam.avi"

if os.path.isfile(videoPath) :
    cap = cv2.VideoCapture(videoPath)

# Adjust Frame Width & Height
f_W    = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
f_H    = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
f_W    = f_W//2
f_H    = f_H//2
f_Size = (f_W, f_H)

excl_mask = np.zeros((f_H, f_W), dtype=np.uint8)
_m_x = 100
for _i in range(_m_x, f_W-_m_x) :
    excl_mask[:, _i] = 255

# Define Parameter
CLIP_LIMIT         = 2.0   # Contrast Limit
t_Grid_x, t_Grid_y = 8, 8  # TileGrid Size x & y
k_u, k_l = 5, 5            # Image Crop
k = 2                      # # of Cluster
area_thr           = 10000 # Small Contour Area Rejection

# Define Linear Regression Model
reg = linear_model.LinearRegression()

# Define Adjustable Window
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
# cv2.namedWindow('otsu', cv2.WINDOW_NORMAL)
# cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
# cv2.namedWindow('roi', cv2.WINDOW_NORMAL)
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
cv2.namedWindow('stack', cv2.WINDOW_NORMAL)
time.sleep(3)
_crp = 3
idx  = 0
while True :
    ret, frame = cap.read()
    if not ret :
        break
    if 62 < idx and idx < 532 :
        # Start Time
        # Convert Gray Scale
        frame = cv2.resize(frame, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Apply CLAHE
        clahe      = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=(t_Grid_x, t_Grid_y))
        gray_clahe = clahe.apply(gray)
    
        # Apply otsu thresholding
        ret, otsu = cv2.threshold(gray_clahe, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
        # Find Mask
        inter_list = list()
        for x in range(f_W) :
            try :
                _tmp   = np.argwhere(otsu[:, x]==0)
                _inter = (x, _tmp[0][0]+k_u, _tmp[-1][0]-k_l)
                inter_list.append(_inter)
            except :
                pass
    
        img_mask = np.zeros((f_H, f_W))
        for _inter in inter_list :
            img_mask[_inter[1]:_inter[2]+1, _inter[0]] = 255
        img_mask = np.uint8(img_mask)
    
        # Find ROI
        roi_img = cv2.bitwise_and(gray_clahe, img_mask)
    
        # k-means clustering
        img = np.float32(roi_img)
        img = img.reshape((-1, 1))
    
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
        ret, label, center = cv2.kmeans(img, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
        center = np.uint8(center)
        res    = center[label.flatten()]
        res    = res.reshape((roi_img.shape))
    
        # Find Decision Boundary
        contours, hierarchy = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c_max = list()
        for i in range(len(contours)) :
            cnt  = contours[i]
            area = cv2.contourArea(cnt)
    
            if area < area_thr :
                c_min = list()
                c_min.append(cnt)
    
                cv2.drawContours(res, c_min, -1, (0, 0, 0), thickness=-1)
    
            c_max.append(cnt)
        cv2.drawContours(res, c_max, -1, (255, 255, 255), thickness=-1)
        
        edge = cv2.Canny(res, 0 , 0)
        edge = cv2.bitwise_and(edge, excl_mask)
        """
        if idx == 63 :
            prev_edge = edge
        else :
            crop  = edge[:, edge.shape[1]-_crp:edge.shape[1]]
            stack = np.hstack((prev_edge, crop))
            prev_edge = stack
            cv2.imshow('stack', stack)
        """
        x_, y_ = list(), list()
        for x in range(f_W) :
            try :
                _tmp = np.nonzero(edge[:, x])
                _tmp = np.where(_tmp[0]>175, _tmp[0], 0)
                _tmp = np.min(_tmp)
                # print(_tmp)
                x_.append(x)
                y_.append(_tmp)
                # X.append([x_, y_])
            except :
                pass
        x_, y_ = np.array(x_), np.array(y_)
        x_ = x_.reshape(-1, 1)
        y_ = y_.reshape(-1, 1)
    
        reg.fit(x_, y_)
        p1 = (0, int(reg.coef_[0][0]*0 + reg.intercept_[0]))
        p2 = (f_W, int(reg.coef_[0][0]*f_W + reg.intercept_[0]))
        # roi_  = deepcopy(roi_img)
        line_img = np.zeros((f_H, f_W, 3))
        line_img = cv2.line(frame, p1, p2, (0, 0, 255), 1)
        if idx == 63 :
            prev_img = line_img
        else :
            crop  = line_img[:, line_img.shape[1]-_crp:line_img.shape[1]]
            stack = np.hstack((prev_img, crop))
            prev_img = stack
            cv2.imshow('stack', stack)
        cv2.imshow('result', line_img)
        # cv2.imshow('otsu', otsu)
        # cv2.imshow('mask', img_mask)
        # cv2.imshow('roi', roi_img)
        cv2.imshow('edge', res)
        # print("processing time", round(time.time() - st, 3))
        # print("coeff", round(reg.coef_[0][0], 4), round(reg.intercept_[0], 3))
        roi_  = deepcopy(roi_img)
        lin_approx  = cv2.line(roi_, p1, p2, (255, 255, 255), 2)
        roi__ = deepcopy(roi_img)
        key = cv2.waitKey(2)
        if key == 27 :
            # ESC
            cv2.destroyAllWindows()
            break
    idx += 1

cv2.waitKey()
cv2.destroyAllWindows()
cap.release()

#%%
import cv2, os, time
import numpy as np
# cv2.namedWindow("img", cv2.WINDOW_NORMAL)
from sklearn import linear_model
reg = linear_model.LinearRegression()
from copy import deepcopy


# Define Parameter
CLIP_LIMIT         = 2.0   # Contrast Limit
t_Grid_x, t_Grid_y = 8, 8  # TileGrid Size x & y
k_u, k_l = 5, 5            # Image Crop
k = 2                      # # of Cluster
area_thr = 10000           # Small Contour Area Rejection
avg = 10

videoPath = "/Users/shetshield/Desktop/python_ws/hj_2nd/seam.avi"

if os.path.isfile(videoPath) :
    cap = cv2.VideoCapture(videoPath)

idx = 0

cv2.namedWindow("stack", cv2.WINDOW_NORMAL)

time.sleep(6)
_crp = 3
while True :
    ret, frame = cap.read()
    if not ret :
        break
    frame = cv2.resize(frame, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)    
    if 62 < idx and idx < 532 :
        if idx == 63 :
            prev_frame = frame
        else :
            crop = frame[:, frame.shape[1]-_crp:frame.shape[1]]
            new = np.hstack((prev_frame, crop))
            prev_frame = new
            cv2.imshow("stack", new)
            # print(prev_frame.shape, frame.shape)
            k = cv2.waitKey(2) & 0xFF
            if k == 27 :
                cv2.destroyAllWindows()
    else :
        prev_frame = frame
    idx += 1

gray  = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)

h, w  = gray.shape

# Apply CLAHE
clahe      = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=(t_Grid_x, t_Grid_y))
gray_clahe = clahe.apply(gray)

# Apply otsu thresholding
ret, otsu = cv2.threshold(gray_clahe, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Find Mask
inter_list = list()
for x in range(w) :
    try :
        _tmp   = np.argwhere(otsu[:, x]==0)
        _inter = (x, _tmp[0][0]+k_u, _tmp[-1][0]-k_l)
        inter_list.append(_inter)
    except :
        pass

img_mask = np.zeros((gray.shape))
for _inter in inter_list :
    img_mask[_inter[1]:_inter[2]+1, _inter[0]] = 255
img_mask = np.uint8(img_mask)

# Find ROI
roi_img = cv2.bitwise_and(gray_clahe, img_mask)

# k-means clustering
img = np.float32(roi_img)
img = img.reshape((-1, 1))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
ret, label, center = cv2.kmeans(img, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res    = center[label.flatten()]
res    = res.reshape((roi_img.shape))

# Find Decision Boundary
contours, hierarchy = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c_max = list()
for i in range(len(contours)) :
    cnt  = contours[i]
    area = cv2.contourArea(cnt)

    if area < area_thr :
        c_min = list()
        c_min.append(cnt)

        cv2.drawContours(res, c_min, -1, (0, 0, 0), thickness=-1)

    c_max.append(cnt)
cv2.drawContours(res, c_max, -1, (255, 255, 255), thickness=-1)
edge = cv2.Canny(res, 0 , 0)

x_, y_, X = list(), list(), list()
for x in range(w) :
    try :
        _tmp = np.nonzero(edge[:, x])
        _tmp = np.max(_tmp)
        x_.append(x)
        y_.append(_tmp)
        X.append([x_, y_])
    except :
        pass
x_, y_ = np.array(x_), np.array(y_)
x_ = x_.reshape(-1, 1)
y_ = y_.reshape(-1, 1)

reg.fit(x_, y_)
p1 = (0, int(reg.coef_[0][0]*0 + reg.intercept_[0]))
p2 = (w, int(reg.coef_[0][0]*w + reg.intercept_[0]))
# roi_  = deepcopy(roi_img)
lin_approx = cv2.line(new, p1, p2, (0, 0, 255), 2)
cv2.imshow('result', new)
# cv2.imshow('otsu', otsu)
# cv2.imshow('mask', img_mask)
# cv2.imshow('roi', roi_img)
cv2.imshow('edge', res)
# print("processing time", round(time.time() - st, 3))
# print("coeff", round(reg.coef_[0][0], 4), round(reg.intercept_[0], 3))
from sklearn import linear_model

ransac = linear_model.RANSACRegressor()
ransac.fit(x_, y_)
inlier_mask  = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)
line = ransac.predict(x_)
roi_  = deepcopy(roi_img)
lin_approx  = cv2.line(roi_, p1, p2, (255, 255, 255), 2)
roi__ = deepcopy(roi_img)
"""
for x in range(f_W) :
    pt = (x, line[x])
    pix = cv2.remap(roi__, np.array(pt[0], np.float32), np.array(pt[1], np.float32), cv2.INTER_LINEAR)
    print(pix)
    cv2.circle(roi__, pix, 1, (255, 255, 255), -1)
"""
"""
X = np.array(X)
from sklearn.preprocessing import PolynomialFeatures
poly_features = PolynomialFeatures(degree=1)
x_poly   = poly_features.fit_transform(x_)
"""

# lin_reg = linear_model.LinearRegression()
# lin_reg.fit(x_poly, y_)
print("line", 0, line[0])
print("coeff", round(reg.coef_[0][0], 4), round(reg.intercept_[0], 3))
print("")

cv2.waitKey()
cv2.destroyAllWindows()