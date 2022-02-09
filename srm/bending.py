import cv2
import numpy as np

img_dir = '/Users/shetshield/Desktop/workspace/img/'
img = 'BendingImg.png'
img = cv2.imread(img_dir + img)

l_g = np.array([30, 100, 0])
u_g = np.array([90, 255, 255])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
msk = cv2.inRange(hsv, l_g, u_g)

detected = cv2.bitwise_and(img, img, mask=msk)
gray = cv2.cvtColor(detected, cv2.COLOR_BGR2GRAY)
gray = cv2.multiply(gray, 10)
ret, bi = cv2.threshold(gray, 127, 255, 0)

contours, _ = cv2.findContours(bi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
if len(contours) :
    for cnt in contours :
        M = cv2.moments(cnt)
        A = cv2.contourArea(cnt)
        if A > 300 :
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.drawContours(img, [cnt], 0, (255, 0, 0), 2)
            cv2.circle(img, (cx, cy), 4, (0, 0, 255), -1)

cv2.namedWindow('res', cv2.WINDOW_NORMAL)

cv2.imshow('res', img)

cv2.waitKey()
cv2.imwrite(img_dir+'res.png', img)
cv2.destroyAllWindows()