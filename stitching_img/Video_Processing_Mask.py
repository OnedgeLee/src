#%%
"""
    Video Processing
"""
# import the necessary packages
import cv2, time, os
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

wRatio = 4
hRatio = 2
f_W    = f_W//wRatio
f_H    = f_H//hRatio

# Define Parameter
CLIP_LIMIT         = 2.0   # Contrast Limit
t_Grid_x, t_Grid_y = 8, 8  # TileGrid Size x & y
k_u, k_l = 5, 5            # Image Crop
k = 2                      # # of Cluster
area_thr = 1000            # Small Contour Area Rejection
avg = 10

UP     = 176
LO     = 209
shift  = 3
mask_margin = 12

# Define Linear Regression Model
reg = linear_model.LinearRegression()

# Define Adjustable Window
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)

roi_mask   = np.zeros((f_H, f_W), dtype=np.uint8)
roi_mask[UP-mask_margin:LO+mask_margin, :] = 255

cluster_thr = 8
idx = 0 
while True :
    ret, frame = cap.read()
    if not ret :
        break
    # Start Time
    st    = time.time()
    frame = cv2.resize(frame, dsize=(0, 0), fx=1/wRatio, fy=1/hRatio, interpolation=cv2.INTER_LINEAR)
    # cv2.imwrite("/Users/user/Desktop/python_ws/output/new/frame"+str(idx)+".png", frame)

    # Convert to Gray & Apply otsu thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_and(gray, roi_mask)

    # Apply CLAHE
    clahe      = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=(t_Grid_x, t_Grid_y))
    gray_clahe = clahe.apply(gray)

    ret, otsu = cv2.threshold(gray_clahe, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # cv2.imshow("otsu", otsu)

    # Find Mask
    inter_list = list()
    for x in range(f_W) :
        try :
            _tmp   = np.argwhere(otsu[UP-mask_margin:LO+mask_margin, x]==0)
            _inter = (x, _tmp[0][0]+k_u+UP-mask_margin, _tmp[-1][0]-k_l+UP-mask_margin)
            inter_list.append(_inter)
        except :
            pass

    img_mask  = np.zeros((f_H, f_W), dtype=np.uint8)
    for _inter in inter_list :
        img_mask[_inter[1]:_inter[2]+1, _inter[0]] = 255

    # Find ROI
    roi_img = cv2.bitwise_and(gray_clahe, img_mask)
    # cv2.imshow("roi_img", roi_img)

    # k-means clustering
    img = np.float32(roi_img)
    img = img.reshape((-1, 1))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
    ret, label, center = cv2.kmeans(img, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res    = center[label.flatten()]
    res    = res.reshape((roi_img.shape))

    # Find Decision Boundary
    # contours, hierarchy = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

    x_, y_ = list(), list()
    for x in range(f_W) :
        try :
            _tmp = np.nonzero(edge[:, x])
            _tmp = np.min(_tmp)
            x_.append(x)
            y_.append(_tmp)
        except :
            pass
    cent_yl = 0
    cent_yr = 0
    for i in range(avg) :
        cent_yl += y_[i]
    cent_yl  = cent_yl/avg
    for i in range(avg) :
        cent_yr += y_[len(y_)-avg+i]
    cent_yr  = cent_yr/avg
    centroid = np.array([[cent_yl], [cent_yr]])
    x_, y_ = np.array(x_), np.array(y_)
    x_ = x_.reshape(-1, 1)
    y_ = y_.reshape(-1, 1)

    from sklearn.cluster import KMeans
    kmns = KMeans(n_clusters=2, init=centroid, random_state=0).fit(y_)
    # kmns = KMeans(n_clusters=2, random_state=0).fit(y_)
    # print(kmns.labels_)

    print(kmns.cluster_centers_)
    
    cluster_index = 2
    if abs(kmns.cluster_centers_[0][0] - kmns.cluster_centers_[1][0]) > cluster_thr :
        if kmns.cluster_centers_[0][0] > kmns.cluster_centers_[1][0] :
            cluster_index = 0
        else :
            cluster_index = 1
        yy = y_[kmns.labels_==cluster_index]
        xx = x_[kmns.labels_==cluster_index]
    else :
        yy = y_
        xx = x_

    reg.fit(xx, yy)
    p1 = (0, int(reg.coef_[0][0]*0 + reg.intercept_[0]))
    p2 = (f_W, int(reg.coef_[0][0]*f_W + reg.intercept_[0]))
    # roi_  = deepcopy(roi_img)
    lin_approx = cv2.line(frame, p1, p2, (0, 0, 255), 1)
    cv2.imshow('result', lin_approx)
    cv2.imshow('edge', res)
    # edge_out = "/Users/user/Desktop/python_ws/output/new/edge" + str(idx) + ".png"
    # line_out = "/Users/user/Desktop/python_ws/output/new/line" + str(idx) + ".png"
    idx += 1
    # cv2.imwrite(edge_out, edge)
    # cv2.imwrite(line_out, lin_approx)
    key = cv2.waitKey(1)
    print("processing time", round(time.time() - st, 3))
    if key == 27 :
        # ESC
        cv2.destroyAllWindows()
        break
cap.release()


#%%
print(kmns.cluster_centers_[0][0])
cluster_index = 2
if kmns.cluster_centers_[0][0] > kmns.cluster_centers_[1][0] :
    cluster_index = 0
else :
    cluster_index = 1
yy = y_[kmns.labels_==cluster_index]
xx = x_[kmns.labels_==cluster_index]
print(xx, yy)
print(kmns.cluster_centers_[cluster_index])
# print(kmns.labels_==1)
