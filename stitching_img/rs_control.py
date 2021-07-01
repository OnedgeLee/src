#%%
import pyrealsense2 as rs
import time, cv2
import numpy as np

def main() :
    rs_ctx = rs.context()
    for i in range(len(rs_ctx.devices)) :
        dev = rs_ctx.devices[i].get_info(rs.camera_info.serial_number)
        if dev == "f0190539" :
            RS = dev
    
    devices = rs_ctx.query_devices()
    print(len(devices))
    sensor = devices[0].query_sensors()[1] # 0 is current cam # 1 is color_sensors
    exp      = sensor.get_option(rs.option.exposure) # Get exposure
    exp_rng  = sensor.get_option_range(rs.option.exposure)
    gn       = sensor.get_option(rs.option.gain) # Get gain
    contrast = sensor.get_option(rs.option.contrast)
    cont_rng = sensor.get_option_range(rs.option.contrast)
    auto_exp = sensor.get_option(rs.option.enable_auto_exposure)
    auto_exp_range = sensor.get_option_range(rs.option.enable_auto_exposure)
    # auto_exp = sensor.get_option(rs.option.auto_exposure_mode)
    # emit = sensor.get_option(rs.option.emitter_enabled) # Get emitter status
    print(exp, gn, exp_rng, contrast, cont_rng, auto_exp, auto_exp_range)
    
    sensor.set_option(rs.option.enable_auto_exposure, 0)
    # sensor.set_option(rs.option.exposure, 124.0)
    time.sleep(1)
    
    exp      = sensor.get_option(rs.option.exposure) # Get exposure
    auto_exp = sensor.get_option(rs.option.enable_auto_exposure)
    print(exp, auto_exp)
    
    if RS :
        pipe = rs.pipeline()
        cfg  = rs.config()
        cfg.enable_device(RS)
        cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 60)
        pipe.start(cfg)
        time.sleep(0.5)
        
        counter = 0
        cv2.namedWindow("dst", cv2.WINDOW_NORMAL)

        while True :
            st = time.time()
            
            frame = pipe.wait_for_frames()
            c_frm = frame.get_color_frame()
            c_img = np.asanyarray(c_frm.get_data())
            cv2.imshow("dst", c_img)
            k = cv2.waitKey(1) & 0xFF
            if counter == 0 :
                sensor.set_option(rs.option.exposure, 200)
                time.sleep(0.01)
                counter = 1
            else :
                sensor.set_option(rs.option.exposure, 50)
                time.sleep(0.01)
                counter = 0

            print("elapsed", round(time.time() - st, 3))
            if k == 27 :
                cv2.destroyAllWindows()
                break
        """
        except :
            pipe.stop()
            cv2.destroyAllWindows()
        """

if __name__=="__main__" :
    main()