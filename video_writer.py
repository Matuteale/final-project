# coding: latin-1

import cv2, sys, select, time, datetime

def start_video_recording(start_time, collector_max_seconds, video_location, is_video_ready):
    cap = cv2.VideoCapture(0)
    cam_fps = cap.get(cv2.CAP_PROP_FPS)
    print('Cam FPS: ' + str(cam_fps))

    cap.set(3,640)
    cap.set(4,480)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    frames_to_write = cam_fps * collector_max_seconds

    out_video_file = cv2.VideoWriter(video_location + '.avi', fourcc, 30, (int(w),int(h)))

    is_video_ready.acquire()
    time.sleep(1)
    is_video_ready.notify()
    is_video_ready.release()

    finish_time_in_millis = collector_max_seconds * 1000 + int(time.time() * 1000)
      
    while int(time.time() * 1000) < finish_time_in_millis:
        ret, frame = cap.read()
        if ret == True:
            out_video_file.write(frame)
        else:
            break

    cap.release()
    out_video_file.release()
    cv2.destroyAllWindows()
    time.sleep(2)
