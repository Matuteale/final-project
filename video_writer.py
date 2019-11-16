#coding: latin-1

# Use me to record a video

import cv2
import sys, select
import time, datetime

def startVideoRecording(start_time, file_name, video_ready, collector_max_seconds):
    cap = cv2.VideoCapture(0)
    cam_fps = cap.get(cv2.CAP_PROP_FPS)
    print('Cam FPS: ' + str(cam_fps))

    cap.set(3,640)
    cap.set(4,480)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(file_name + '_' + start_time + '.avi',fourcc, cam_fps, (int(w),int(h)))

    video_ready.acquire()
    time.sleep(1)
    video_ready.notify()
    video_ready.release()
    
    frames_to_write = cam_fps*collector_max_seconds

    while (frames_to_write > 0):
        input = select.select([sys.stdin], [], [], 0)[0]
        if input:
            print('Exiting video writer...')
            break
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
            print('Frame to Write: ' + str(frames_to_write))
            frames_to_write -= 1
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
