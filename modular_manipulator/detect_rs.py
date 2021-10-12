#%%
# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""
WEB = True

import sys, time, torch, cv2
from pathlib import Path

import numpy as np
import torch.backends.cudnn as cudnn

import pyrealsense2 as rs
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = ROOT.relative_to(Path.cwd())  # relativevv+

from models.experimental import attempt_load
from utils.datasets import LoadImages, LoadStreams
from utils.general import apply_classifier, check_img_size, check_imshow, check_requirements, check_suffix, colorstr, \
    increment_path, non_max_suppression, print_args, save_one_box, scale_coords, set_logging, \
    strip_optimizer, xyxy2xywh
from utils.plots import Annotator, colors
from utils.torch_utils import load_classifier, select_device, time_sync
from utils.augmentations import letterbox


def cal_dist(_c_int, _d_f, _p) :
	_px = _p[0]
	_py = _p[1]
	_pz = _d_f.get_distance(_px, _py)
	_pt = rs.rs2_deproject_pixel_to_point(_c_int, [_px, _py], _pz)
	return _pt

def main() :
    weights = ROOT / 'runs/train/exp5/weights/best.pt'
    if not WEB :
        source = ROOT / 'clip'
    else :
        source = 0
    fps = 30
    
    """ Detect Green for the test """
    lower_g = np.array([60, 100, 0])
    upper_g = np.array([90, 255, 255])
    
    imgsz   = [1280]
    conf_thres = 0.1
    iou_thres  = 0.45
    max_det    = 1000
    device  = ''
    view_img = True
    save_txt = False
    save_conf = False
    save_crop = False
    
    nosave = True
    
    classes = None
    agnostic_nms = False
    augment = False
    visualize = False
    update = False
    project = ROOT / 'runs/detect'
    name = 'exp'
    exist_ok = False
    line_thickness = 2
    hide_labels = False
    hide_conf = False
    half = False
    
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))
    # webcam = True
    
    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir
    
    # Initialize
    set_logging()
    device = select_device(device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    w = weights[0] if isinstance(weights, list) else weights
    classify, suffix, suffixes = False, Path(w).suffix.lower(), ['.pt', '.onnx', '.tflite', '.pb', '']
    print(classify)
    check_suffix(w, suffixes)  # check weights have acceptable suffix
    pt, onnx, tflite, pb, saved_model = (suffix == x for x in suffixes)  # backend booleans
    stride, names = 64, [f'class{i}' for i in range(1000)]  # assign defaults
    if pt:
        model = attempt_load(weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        names = model.module.names if hasattr(model, 'module') else model.names  # get class names
        if half:
            model.half()  # to FP16
        if classify:  # second-stage classifier
            modelc = load_classifier(name='resnet50', n=2)  # initialize
            modelc.load_state_dict(torch.load('resnet50.pt', map_location=device)['model']).to(device).eval()
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    imgsz = [1280, 1280]
    
    # Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        # dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        # bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
    # vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    if pt and device.type != 'cpu':
        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))  # run once
    dt, seen = [0.0, 0.0, 0.0], 0
    rs_context = rs.context()
    for i in range(len(rs_context.devices)) :
        detected = rs_context.devices[i].get_info(rs.camera_info.serial_number)
        RS = detected

        if RS :
            view_img = check_imshow()
            cudnn.benchmark = True

            pipe   = rs.pipeline()
            rs_cfg = rs.config()
            rs_cfg.enable_device(RS)
            rs_cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, fps)
            rs_cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, fps)
            pipe.start(rs_cfg)
            time.sleep(1)

            """ cv2 putText Option """
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            t_color   = (0, 255, 0)
            thickness = 2
            align_to = rs.stream.color
            # align_to = rs.stream.depth
            align    = rs.align(align_to)

            cv2.namedWindow("yolo_res", cv2.WINDOW_NORMAL)
            cv2.namedWindow("hand_pos", cv2.WINDOW_NORMAL)
            cv2.namedWindow("color_catch", cv2.WINDOW_NORMAL)
            # try :
            with mp_hands.Hands(
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands :
                while True :
                    t1 = time_sync()
                    frames = pipe.wait_for_frames()
                    a_fs   = align.process(frames)
                    d_f    = a_fs.get_depth_frame()
                    c_f    = a_fs.get_color_frame()
                    c_img  = np.asanyarray(c_f.get_data())
                    c_int  = d_f.profile.as_video_stream_profile().intrinsics
                    img = [letterbox(c_img, imgsz, 32, 1)[0]]
                    # Stack
                    img = np.stack(img, 0)

                    # Convert
                    img = img[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
                    img = np.ascontiguousarray(img)
                    img = torch.from_numpy(img).to(device)
                    img = img.half() if half else img.float()  # uint8 to fp16/32
                    img = img / 255.0  # 0 - 255 to 0.0 - 1.0
                    if len(img.shape) == 3:
                        img = img[None]  # expand for batch dim

                    t2 = time_sync()
                    dt[0] += t2 - t1

                    # Inference
                    if pt:
                        # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                        visualize = False
                        pred = model(img, augment=augment, visualize=visualize)[0]
                    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

                    # Process predictions
                    for i, det in enumerate(pred):  # per image
                        seen += 1
                        if webcam:  # batch_size >= 1
                            # p, s, im0, frame = path[i], f'{i}: ', im0s[i].copy(), dataset.count
                            s, im0 = f'{i}: ', c_img.copy()
                        # p = Path(p)  # to Path
                        # save_path = str(save_dir / p.name)  # img.jpg
                        # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
                        s += '%gx%g ' % img.shape[2:]  # print string
                        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                        imc = im0.copy() if save_crop else im0  # for save_crop
                        annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                        if len(det):
                            # Rescale boxes from img_size to im0 size
                            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                            # Print results
                            for c in det[:, -1].unique():
                                n = (det[:, -1] == c).sum()  # detections per class
                                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                            # Write results
                            for *xyxy, conf, cls in reversed(det):
                                if save_txt:  # Write to file
                                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                                    line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                                    # with open(txt_path + '.txt', 'a') as f:
                                    #     f.write(('%g ' * len(line)).rstrip() % line + '\n')

                                if save_img or save_crop or view_img:  # Add bbox to image
                                    c = int(cls)  # integer class
                                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                                    annotator.box_label(xyxy, label, color=colors(c, True))
                                    # if save_crop:
                                    #     save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                        # Print time (inference-only)
                        # print(f'{s}Done. ({t3 - t2:.3f}s)')
                
                        # Stream results
                        im0 = annotator.result()
                        # if view_img:
                        #     cv2.imshow(c_img, im0)
                        #     cv2.waitKey(1)  # 1 millisecond
                    d_img  = np.asanyarray(d_f.get_data())
                    # c_img  = cv2.resize(c_img, dsize=(640, 360), interpolation=cv2.INTER_AREA)
                    # d_img  = cv2.resize(d_img, dsize=(640, 360), interpolation=cv2.INTER_AREA)
                    hsv  = cv2.cvtColor(c_img, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, lower_g, upper_g)
                    color_detect = cv2.bitwise_and(c_img, c_img, mask=mask)
                    
                    c_img.flags.writeable = False
                    c_img = cv2.cvtColor(c_img, cv2.COLOR_BGR2RGB)
                    res   = hands.process(c_img)
                    c_img.flags.writeable = True
                    c_img = cv2.cvtColor(c_img, cv2.COLOR_RGB2BGR)
                    if res.multi_hand_landmarks :
                        for hand_landmarks in res.multi_hand_landmarks :
                            try :
                                index_finger_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * c_img.shape[1])
                                index_finger_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * c_img.shape[0])
                                pt = cal_dist(c_int, d_f, [index_finger_x, index_finger_y])
                                pt = [round(pt[0], 4), round(pt[1], 4), round(pt[2], 4)]
                                msg = "i.f. coordinates : %.5s %.5s %.5s" %(pt[0], pt[1], pt[2]) + 'm'
                                cv2.putText(c_img, msg, (20, 90), font, fontScale, t_color, thickness, cv2.LINE_AA)
                                # print(pt)
                            except :
                                pass
                            
                            mp_drawing.draw_landmarks(
                                c_img,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style())
                    # print(c_img.shape, d_img.shape)
                    # d_cmap = cv2.applyColorMap(cv2.convertScaleAbs(d_img, alpha=0.03), cv2.COLORMAP_JET)
                    cv2.imshow("yolo_res", im0)
                    # cv2.imshow("c_img", c_img)
                    cv2.imshow("hand_pos", c_img)
                    cv2.imshow("color_catch", color_detect)
                    k = cv2.waitKey(1) & 0xFF
                    if k == 27 :
                        break
                    # Print results
                    t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
                    print(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
                    if save_txt or save_img:
                        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
                        print(f"Results saved to {colorstr('bold', save_dir)}{s}")
                    if update:
                        strip_optimizer(weights)  # update model (to fix SourceChangeWarning)

                pipe.stop()
                cv2.destroyAllWindows()    
    
if __name__=="__main__" :
    main()