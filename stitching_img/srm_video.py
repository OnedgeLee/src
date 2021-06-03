#%%
# Video Processing

import cv2, os

def main() :
    # cv2.namedWindow("VideoFrame", cv2.WINDOW_NORMAL)
    f_dir  = "/Users/shetshield/Desktop/python_ws/srm_video/"
    f_name = "5"
    f_ext  = ".MOV"
    if f_name == "3" or f_name == "5" or f_name == "4":
        f_ext = ".mp4"
    f_read = f_dir + f_name + f_ext
    cap    = cv2.VideoCapture(f_read)
    cnt    = 1
    ws_out = f_dir + "output/" + f_name

    try :
        os.mkdir(ws_out)
    except :
        pass

    while True : 
        ret, frame = cap.read()
        # print("here")
        if ret :
            w = frame.shape[1]//2
            h = frame.shape[0]//2
            frame = cv2.resize(frame, (w, h))
            if int(f_name) < 3 :
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow("VideoFrame", frame)
            f_write = ws_out + "/" + f_name + "_" + str(cnt) + ".png"
            cv2.imwrite(f_write, frame)
            cnt += 1
            k = cv2.waitKey(1) & 0xFF
            if k == 27 :
                break
        else :
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__" :
    main()