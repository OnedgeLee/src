#%%
import cv2, os

# Interpolation : Magification - INTER_LINEAR / Reducing - INTER_AREA

def main() :
    fname    = "5"
    file_ext = '.MOV'
    save_ext = '.jpg'
    cur_dir  = os.getcwd()

    video = fname + file_ext
    if os.path.isfile(video) :
        cap = cv2.VideoCapture(video)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if w > h :
        re_w = 1280
        re_h = 720
    else :
        re_w = 720
        re_h = 1280
    
    cv2.namedWindow('org', cv2.WINDOW_NORMAL)
    cv2.namedWindow('flip', cv2.WINDOW_NORMAL)
    cnt = 0
    while True :
        ret, frame = cap.read()
        if not ret :
            break
        
        frame = cv2.resize(frame, dsize=(re_w, re_h), interpolation=cv2.INTER_AREA)
        flip = cv2.flip(frame, 1) # 1 for LR / 0 for UD
        
        f1  = cur_dir + '/' + fname + '/' + fname + "_" + str(cnt) + save_ext
        f2  = cur_dir + '/' + fname + '/' + fname + "_" + str(cnt+1) + save_ext
        cnt = cnt + 2
        cv2.imwrite(f1, frame)
        cv2.imwrite(f2, flip)
        
        cv2.imshow('org', frame)
        cv2.imshow('flip', flip)
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27 :
            cv2.destroyAllWindows()
            break

if __name__ == "__main__" :
    main()