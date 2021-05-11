# import the necessary packages
import argparse
import cv2
import os
import pyrealsense2 as rs
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

rs_context = rs.context()
for i in range(len(rs_context.devices)) :
    detected = rs_context.devices[i].get_info(rs.camera_info.serial_number)
    print(detected)

cv2.dnn_registerLayer("Crop", CropLayer)

pipe = rs.pipeline()
cfg  = rs.config()
cfg.enable_device(detected)
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipe.start(cfg)
align_to = rs.stream.color
align    = rs.align(align_to)
frames = pipe.wait_for_frames()
a_fs  = align.process(frames)
d_f   = a_fs.get_depth_frame()
c_f   = a_fs.get_color_frame()
(H, W) = (720, 1280)
try :
    while True :
        st = time.time()
        frames = pipe.wait_for_frames()
        a_fs  = align.process(frames)
        d_f   = a_fs.get_depth_frame()
        c_f   = a_fs.get_color_frame()
        c_img = np.asanyarray(c_f.get_data())
        
        print("[INFO] performing Canny edge detection...")
        gray = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, 30, 150)

        blob = cv2.dnn.blobFromImage(c_img, scalefactor=1.0, size=(W, H),
                            mean=(104.00698794, 116.66876762, 122.67891434),
                            swapRB=False, crop=False)
        print("[INFO] performing holistically-nested edge detection...")
        net.setInput(blob)
        hed = net.forward()
        hed = cv2.resize(hed[0, 0], (W, H))
        hed = (255 * hed).astype("uint8")
        
        cv2.imshow("Input", c_img)
        cv2.imshow("Canny", canny)
        cv2.imshow("HED", hed)
        print("elapsed time", round(time.time()-st, 2))
        k = cv2.waitKey(1) & 0xFF
        if k == 27 :
            cv2.destroyAllWindows()
            break
    pipe.stop()
except :
    cv2.destroyAllWindows()
    pipe.stop()
