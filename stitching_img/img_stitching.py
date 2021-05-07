#%%
import cv2
from copy import deepcopy
import numpy as np

img_path = '/Users/shetshield/Desktop/python_ws/processed/'
f_name   = 'i'
f_ext    = '.png'

_f1 = img_path + f_name + '1' + f_ext
_f2 = img_path + f_name + '2' + f_ext
_f3 = img_path + f_name + '3' + f_ext
img1 = cv2.imread(_f1, cv2.IMREAD_COLOR)
img2 = cv2.imread(_f2, cv2.IMREAD_COLOR)
img3 = cv2.imread(_f3, cv2.IMREAD_COLOR)

width  = img1.shape[1]
height = img1.shape[0]

# Determine Shift in X & Y Direction
# xs_1, ys_1, xs_2, ys_2 = 3, 0, 6, 0
xs_1, ys_1, xs_2, ys_2 = 0, 0, 0, 0

# d = 5 mm
# Determine Pixel Shift (predetermined by experiment)
px_shft = 500

# roi1  = img2[height-px_shft:, :, :]
roi1    = img1[:, :px_shft, :]
M1    = np.float32([[1, 0, xs_1], [0, 1, ys_1]])
# roi1  = cv2.warpAffine(roi1, M1, (width, px_shft))
roi1    = cv2.warpAffine(roi1, M1, (px_shft, height))
M2 = np.float32([[1, 0, xs_2], [0, 1, ys_2]])
roi2    = img2[:, : px_shft, :]
roi2    = cv2.warpAffine(roi2, M2, (px_shft, height))

dst    = np.hstack((roi1, roi2))
dst    = np.hstack((dst, img3))

def main() :
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow('img1', img1)
    cv2.imshow('roi1', roi1)
    cv2.imshow('roi2', roi2)
    cv2.imshow('img', dst)
    
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__=="__main__" :
    main()