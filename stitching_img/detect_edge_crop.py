#%%
# import the necessary packages
import argparse
import cv2
import os
import numpy as np
import time

"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--edge-detector", type=str, required=True,
                help="path to OpenCV's deep learning edge detector")
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input image")
args = vars(ap.parse_args())
"""

class CropLayer(object):
    def __init__(self, params, blobs):
        # initialize our starting and ending (x, y)-coordinates of the crop
        self.startX = 0
        self.startY = 0
        self.endX = 0
        self.endY = 0

    def getMemoryShapes(self, inputs):
        # the crop layer will receive two inputs -- we need to crop
        # the first input blob to match the shape of the second one,
        # keeping the batch size and number of channels
        (inputShape, targetShape) = (inputs[0], inputs[1])
        (batchSize, numChannels) = (inputShape[0], inputShape[1])
        (H, W) = (targetShape[2], targetShape[3])

        # compute the starting and ending crop coordinates
        self.startX = int((inputShape[3] - targetShape[3]) / 2)
        self.startY = int((inputShape[2] - targetShape[2]) / 2)
        self.endX = self.startX + W
        self.endY = self.startY + H

        # return the shape of the volume (we'll perform the actual
        # crop during the forward pass)
        return [[batchSize, numChannels, H, W]]

    def forward(self, inputs):
        # use the derviced (x, y)-coordinates to perform the crop
        return [inputs[0][:, :, self.startY:self.endY,
                                self.startX:self.endX]]


# load our serialized edge detector from disk
protoPath = "/Users/shetshield/Desktop/python_ws/hed-opencv-dl-master/hed_model/deploy.prototxt"
modelPath = "/Users/shetshield/Desktop/python_ws/hed-opencv-dl-master/hed_model/hed_pretrained_bsds.caffemodel"
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

cv2.dnn_registerLayer("Crop", CropLayer)

(H, W) = (540, 960)
roi = 50

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

try :
    while True :
        st = time.time()
        ret, frame = cap.read()
        frame_crop = frame[H//2-roi:H//2+roi, :]
        
        print("[INFO] performing Canny edge detection...")
        gray = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, 30, 150)

        blob = cv2.dnn.blobFromImage(frame_crop, scalefactor=1.0, size=(W, 2*roi),
                            mean=(104.00698794, 116.66876762, 122.67891434),
                            swapRB=False, crop=False)
        print("[INFO] performing holistically-nested edge detection...")
        net.setInput(blob)
        hed = net.forward()
        hed = cv2.resize(hed[0, 0], (W, 2*roi))
        hed = (255 * hed).astype("uint8")
        
        cv2.imshow("Input", frame_crop)
        cv2.imshow("Canny", canny)
        cv2.imshow("HED", hed)
        print("elapsed time", round(time.time()-st, 2))
        k = cv2.waitKey(1) & 0xFF
        if k == 27 :
            cap.release()
            cv2.destroyAllWindows()
            break
except :
    cap.release()
    cv2.destroyAllWindows()
