import os, sys, random, math, re, time
import numpy as np
import tensorflow as tf

# Root directory of the project
ROOT_DIR = os.path.abspath("/Users/shetshield/Downloads/Study/")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
sys.path.append(ROOT_DIR+"/mask_tutorial/Mask_RCNN")
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

MODEL_DIR = os.path.join(ROOT_DIR, "logs")

from mrcnn.config import Config

class CustomConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "bottle"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + toy

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 70% confidence
    DETECTION_MIN_CONFIDENCE = 0.7

config = CustomConfig()
config.display()

DEVICE="/cpu:0"

TEST_MODE="inference"

with tf.device(DEVICE) :
    model = modellib.MaskRCNN(mode=TEST_MODE, model_dir=MODEL_DIR, config=config)

weights_path = model.find_last()
print("Loaded weights ", weights_path)
model.load_weights(weights_path, by_name=True)


import cv2, time, colorsys
from skimage.measure import find_contours

font = cv2.FONT_HERSHEY_SIMPLEX
org  = (20, 50)
fontScale = 1
t_color   = (0, 255, 0) # green
thickness = 1

def apply_mask(image, mask, color, alpha=0.5) :
    for c in range(3) :
        image[:, :, c] = np.where(mask==1,
                                  image[:, :, c] *
                                 (1-alpha) + alpha*color[c]*255,
                                  image[:, :, c])
    return image


def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

v_dir  = "/Users/shetshield/Downloads/Study/mask_tutorial/test/"
v_name = "test_low_fps_2.MP4"
v_file = os.path.join(v_dir, v_name)

ADJUST_WINDOW_SIZE = False

if os.path.isfile(v_file) :
    cap = cv2.VideoCapture(v_file)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('frame_size = ', frame_size)
else :
    print("video does not exist in %s" %(v_file))

colors    = None
captions  = None
show_mask = True
show_bbox = True
figsize = (16, 16)

while True :
    st = time.time()
    ret, frame = cap.read()
    if not ret :
        break

    if ADJUST_WINDOW_SIZE :
        cv2.namedWindow('detected', cv2.WINDOW_NORMAL)
    
    # frame = cv2.resize(frame, (frame_size[0]//2, frame_size[1]//2))
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_np = np.array(frame)
    # input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    results = model.detect([image_np], verbose=1)
    r = results[0]
    boxes  = r['rois']
    masks  = r['masks']
    scores = r['scores']
    class_ids = r['class_ids']

    N = boxes.shape[0]
    if not N :
        print("\n*** No instnaces to display *** \n")
    else :
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]
    colors = colors or random_colors(N)

    h, w = frame.shape[:2]
    masked_image = frame.astype(np.uint32).copy()
    for i in range(N) :
        color = colors[i]

        if not np.any(boxes[i]) :
            continue
        y1, x1, y2, x2 = boxes[i]
        if show_bbox :
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
        
        if not captions :
            class_id = class_ids[i]
            score    = scores[i] if scores is not None else None
            # print(class_id)
            label    = ["module"][class_id-1]
            caption  = "{} {:.3f}".format(label, score) if score else label
        else :
            caption = captions[i]
        cv2.putText(frame, caption, org, font, fontScale, t_color, thickness, cv2.LINE_AA)
        mask = masks[:, :, i]
        if show_mask :
            masked_image = apply_mask(frame, mask, color)
        padded_mask = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        thresh = cv2.threshold(padded_mask, 120, 255, cv2.THRESH_BINARY)[1]
        cnts   = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts :
            cv2.drawContours(frame, [c], -1, color, -1)
        
        # contours = find_contours(padded_mask, 0.5)
        # for verts in contours :
        #    verts = np.fliplr(verts) - 1
        #    p = Polygon(verts, facecolor="none", edgecolor=color)


    # visualize.display_instances(frame, r['rois'], r['masks'], r['class_ids'], ['module'], r['scores'], ax=ax, title="Predictions")
    elapsed = round(time.time() - st,2)
    t_msg = "time: %5s" %(str(elapsed)) + 's'
    cv2.putText(frame, t_msg, (20, 90), font, fontScale, t_color, thickness, cv2.LINE_AA)
    cv2.imshow("inferenced", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 :
        break

if cap.isOpened() :
    cap.release()
cv2.destroyAllWindows()