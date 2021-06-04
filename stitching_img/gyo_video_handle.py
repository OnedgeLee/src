#%%
import cv2
import numpy as np
from copy import deepcopy

img = cv2.imread("/Users/shetshield/Desktop/python_ws/super_resol/org.png")
img2 = deepcopy(img)
org  = deepcopy(img)
mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
cv2.line(mask, (0, 628), (720, 618), (255, 0, 0), 1)
cv2.line(mask, (0, 495), (720, 485), (255, 0, 0), 1)
cv2.line(mask, (0, 415), (720, 405), (255, 0, 0), 1)
cv2.line(mask, (0, 350), (720, 340), (255, 0, 0), 1)
cv2.line(img, (0, 628), (720, 618), (255, 0, 0), 1)
cv2.line(img, (0, 495), (720, 485), (255, 0, 0), 1)
cv2.line(img, (0, 415), (720, 405), (255, 0, 0), 1)
cv2.line(img, (0, 350), (720, 340), (255, 0, 0), 1)

points1 = np.array([[0, 628], [720, 618], [720, 485], [0, 495]], np.int32)
points2 = np.array([[0, 350], [720, 340], [720, 405], [0, 415]], np.int32)
mask = cv2.fillConvexPoly(mask, points1, (255, 255, 255))
mask = cv2.fillConvexPoly(mask, points2, (255, 255, 255))

roi  = np.zeros((img.shape[0], img.shape[1]), np.uint8)
roi  = cv2.rectangle(roi, (140, 290), (660, 515), (255, 255, 255), -1)

# points3 = np.array([[150, 515], [660, 505], [660, 280], [150, 290]], np.int32)
# roi  = cv2.fillConvexPoly(roi, points3, (255, 255, 255))

# t_img = cv2.bitwise_and(img2, img2, mask=points3)

rroi = cv2.bitwise_and(org, org, mask=roi)

rroi_gray = cv2.cvtColor(rroi, cv2.COLOR_BGR2GRAY)

# clahe      = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
# gray_clahe = clahe.apply(rroi_gray)
rroi_gray = cv2.medianBlur(rroi_gray, 3)
edge = cv2.Canny(rroi_gray, 40, 30)

contours, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c_max = list()
area_thr = 1
for i in range(len(contours)) :
    cnt = contours[i]
    area = cv2.contourArea(cnt)
    print(area)
    if area < area_thr :
        c_min = list()
        c_min.append(cnt)
        
        cv2.drawContours(edge, c_min, -1, 0, thickness=-1)
    c_max.append(cnt)
cv2.drawContours(edge, c_max, -1, 255, thickness=-1)

# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# mask = cv2.drawContours(mask, contours, -1, [255, 255, 255], thickness=-1)
"""
cv2.imshow("mask", mask)
cv2.imshow("img", img)
cv2.imshow("img2", rroi)
cv2.imshow("org", edge)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
capture = cv2.VideoCapture(cv2.samples.findFileOrKeep("/Users/shetshield/Desktop/python_ws/test1.mp4"))
bg = cv2.imread("/Users/shetshield/Desktop/python_ws/super_resol/bg.png")
if not capture.isOpened():
    print('Unable to open: ' + "test1.mp4")
    exit(0)
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    frm = cv2.bitwise_and(frame, frame, mask=roi)
    
    cv2.imshow('Frame', frame)
    # cv2.imshow('FG Mask', fgMask)
    cv2.imshow('diff', frm)
    
    keyboard = cv2.waitKey(5) & 0xFF
    if keyboard == 'q' or keyboard == 27:
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()
capture.release()
