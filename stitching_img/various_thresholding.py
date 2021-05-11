#%%
# import the necessary packages
import cv2
import matplotlib.pyplot as plt
imagePath = "/Users/shetshield/Desktop/python_ws/processed/10mm_y0mm.jpg"

image = cv2.imread(imagePath, 0)
(H, W) = image.shape[:2]

# convert the image to grayscale, blur it, and perform Canny
# edge detection

ret,th1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [image, th1, th2, th3]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


# construct a blob out of the input image for the Holistically-Nested
# Edge Detector
# set the blob as the input to the network and perform a forward pass
# to compute the edges
print("[INFO] performing holistically-nested edge detection...")
