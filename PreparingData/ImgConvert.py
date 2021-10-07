#%%
import cv2, os

cur_path = os.getcwd()
img_f    = os.listdir(cur_path)

cnt = 0
for f in img_f :
    img = os.path.join(cur_path, f)
    ext = os.path.splitext(f)[1]
    if ext != '.jpg' :
        pass
    else :
        im = cv2.imread(img, cv2.IMREAD_COLOR)
        h, w = im.shape[0:2]
        if h > w :
            w_t = 960
            h_t = 1280
        else :
            w_t = 1280
            h_t = 960
        im   = cv2.resize(im, dsize=(w_t, h_t), interpolation=cv2.INTER_AREA)
        flip = cv2.flip(im, 1)
        im_90  = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
        im_180 = cv2.rotate(im, cv2.ROTATE_180)
        im_270 = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        fname = '_' + str(cnt) + '.jpg'
        s_im  = os.path.join(cur_path, 'output/1/1' + fname)
        s_90  = os.path.join(cur_path, 'output/2/2' + fname)
        s_180 = os.path.join(cur_path, 'output/3/3' + fname)
        s_270 = os.path.join(cur_path, 'output/4/4' + fname)
        s_f   = os.path.join(cur_path, 'output/5/5' + fname)
        
        cv2.imwrite(s_im, im)
        cv2.imwrite(s_90, im_90)
        cv2.imwrite(s_180, im_180)
        cv2.imwrite(s_270, im_270)
        cv2.imwrite(s_f, flip)
        cnt += 1