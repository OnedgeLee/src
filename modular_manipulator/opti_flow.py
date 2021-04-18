import cv2, os
import numpy as np

v_dir  = "/Users/shetshield/Downloads/Study/mask_tutorial/test/"
v_name = "test_low_fps_2.MP4"
v_file = os.path.join(v_dir, v_name)

def main() :
    if os.path.isfile(v_file) :
        cap = cv2.VideoCapture(v_file)
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('frame_size = ', frame_size)
    else :
        print("video does not exist in %s" %(v_file))
    
    ret, frame1 = cap.read()
    if not ret :
        prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        hsv  = np.zeros_like(frame1)
        hsv[..., 1] = 255
    
    while True :
        ret, frame2 = cap.read()
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 2, 5, 1.2 , 0)

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        cv2.imshow('frame2',rgb)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('opticalfb.png',frame2)
            cv2.imwrite('opticalhsv.png',rgb)
        prvs = next

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__" :
    main()
