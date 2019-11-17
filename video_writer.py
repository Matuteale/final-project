#coding: latin-1

# Use me to record a video

import cv2
import sys, select
import time, datetime

def startVideoRecording(start_time, file_name, video_ready, collector_max_seconds, notify_finish):
    cap = cv2.VideoCapture(0)
    cam_fps = cap.get(cv2.CAP_PROP_FPS)
    print('Cam FPS: ' + str(cam_fps))

    cap.set(3,640)
    cap.set(4,480)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    frames_to_write = cam_fps*collector_max_seconds

    out = cv2.VideoWriter(file_name + '_' + start_time + '.avi', fourcc, 30, (int(w),int(h)))

    video_ready.acquire()
    time.sleep(1)
    video_ready.notify()
    video_ready.release()

    max_millis = collector_max_seconds * 1000
    start_writing_time = int(time.time() * 1000)
      
    while int(time.time() * 1000) < start_writing_time + max_millis :
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    time.sleep(2)
