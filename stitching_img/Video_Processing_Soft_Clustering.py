#%%
"""
    Video Processing
"""
# import the necessary packages
import cv2, time, os
import numpy as np
from sklearn import linear_model
from sklearn.cluster import KMeans
from math import sqrt

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

goal_d   = 3 # in mm
pre_pix  = 33
pre_dis  = 10
goal_pix = pre_pix/pre_dis * goal_d
spacing  = 8

# Define Linear Regression Model
reg = linear_model.LinearRegression()

# Define Adjustable Window
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)

roi_mask   = np.zeros((f_H, f_W), dtype=np.uint8)
roi_mask[UP-mask_margin:LO+mask_margin, :] = 255

cluster_thr = 8
pix_thr     = 1.8
idx = 0 
while True :
    ret, frame = cap.read()
    if not ret :
        break
    # Start Time
    st    = time.time()
    frame = cv2.resize(frame, dsize=(0, 0), fx=1/wRatio, fy=1/hRatio, interpolation=cv2.INTER_LINEAR)

    # Convert to Gray & Apply otsu thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_and(gray, roi_mask)

    # Apply CLAHE
    clahe      = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=(t_Grid_x, t_Grid_y))
    gray_clahe = clahe.apply(gray)

    ret, otsu = cv2.threshold(gray_clahe, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

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

    kmns = KMeans(n_clusters=2, init=centroid, random_state=0).fit(y_)

    # print(kmns.cluster_centers_)

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

    # Soft Clustering
    if cluster_index != 2 :
        clu     = kmns.transform(yy)
        cur_clu = clu[:, cluster_index]
        yy      = yy[cur_clu<pix_thr]
        xx      = xx[cur_clu<pix_thr]
    reg.fit(xx, yy)
    
    slope = reg.coef_[0][0]
    p1 = (np.float32(0), np.float32(slope*0 + reg.intercept_[0]))
    p2 = (np.float32(f_W), np.float32((slope*f_W + reg.intercept_[0])))

    p3 = (np.float32(0), np.float32(slope*0 + reg.intercept_[0]-goal_pix))
    p4 = (np.float32(f_W), np.float32(slope*f_W + reg.intercept_[0]-goal_pix))

    x0, x1 = np.float32(0), np.float32(0)
    y0 = np.float32(reg.intercept_[0] - goal_pix)
    points = list()
    points.append((x0, y0))
    while x1 < f_W :
        dx = spacing/sqrt(1+slope**2)
        x1 = np.float32(x0 + dx)
        dy = dx * slope
        y1 = np.float32(y0 + dy)
        points.append((x1, y1))
        x0, y0 = x1, y1

    
    # p1 = (0, int(reg.coef_[0][0]*0 + reg.intercept_[0]))
    # p2 = (f_W, int(reg.coef_[0][0]*f_W + reg.intercept_[0]))
    lin_approx = cv2.line(frame, p1, p2, (0, 0, 255), 1)
    lin_approx = cv2.line(frame, p3, p4, (255, 0, 0), 1)
    for pt in points :
        cv2.circle(lin_approx, pt, 1, (0, 255, 0), 1)

    elapsed = round(time.time() - st, 3)
    txt    = "elapsed %.3f" %(elapsed) + " sec"
    cv2.putText(lin_approx, txt, (5, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    cv2.imshow('result', lin_approx)
    cv2.imshow('edge', res)

    idx += 1
    key = cv2.waitKey(1)
    if key == 27 :
        # ESC
        cv2.destroyAllWindows()
        break
cap.release()

#%%
res = kmns.transform(yy)
# print(res)
cur_cluster = res[:, cluster_index]
print(len(cur_cluster))
filtered = yy[cur_cluster<pix_thr]
print(len(filtered))
# print(filtered)
# print(res[:, cluster_index])


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
