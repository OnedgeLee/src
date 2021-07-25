#%%
import cv2, time
import numpy as np

img_dir = '/Users/shetshield/Desktop/python_ws/hojeon/image/'
img_f   = img_dir + '2.png'

img = cv2.imread(img_f, cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('img1', cv2.WINDOW_NORMAL)

window_y  = 720//9   # 80
window_yy = window_y // 2
window_x = 1280//20 # 64

st = time.time()

idx_max = 0
arr_sum = 0
canvas = np.zeros((img.shape), dtype=np.uint8)

for i in range(img.shape[1]//window_x) :
    idx_max = 0
    arr_sum = 0
    for j in range(img.shape[0]//window_y) :
        _img = img[j*window_y:(j+1)*window_y, i*window_x:(i+1)*window_x]
        _sum = np.sum(_img)
        # print(_sum, i, j)
        if arr_sum < _sum :
            arr_sum = _sum
            idx_max = j
            arr     = _img
    arr_sum = 0
    idx_max_subwin = 0
    for jj in range(arr.shape[0]//window_yy) :
        _img = arr[jj*window_yy:(jj+1)*window_yy, :]
        _sum = np.sum(_img)
        if arr_sum < _sum :
            arr_sum = _sum
            idx_max_subwin = jj
            arr_ = _img
    sob_y = cv2.Sobel(arr_, cv2.CV_64F, 0, 1, ksize=3)
    sob_y = cv2.convertScaleAbs(sob_y)
    edge  = cv2.Canny(sob_y, 50, 150)
    for x in range(edge.shape[1]) :
        col = np.nonzero(edge[:, x])
        if len(col[0]) > 0 :
            idx = np.min(col)
            canvas[idx_max*window_y+idx_max_subwin*window_yy+idx, i*window_x+x] = 255

print("elapsed", round(time.time()-st, 8))

cv2.imshow('img1', canvas)
# cv2.imshow('img2', img_list[6][0])

cv2.waitKey()
cv2.destroyAllWindows()