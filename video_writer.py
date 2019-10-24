#coding: latin-1

# Use me to record a video

import cv2
import sys, select
import time, datetime

def startVideoRecording(start_time, fileName, videoReady):
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(fileName + '_' + start_time + '.avi',fourcc, 24.0, (int(w),int(h)))

    videoReady.acquire()
    time.sleep(1)
    videoReady.notify()
    videoReady.release()

    while (True):
        input = select.select([sys.stdin], [], [], 0)[0]
        if input:
            print('Exiting video writer...')
            break
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('Video Stream', frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
