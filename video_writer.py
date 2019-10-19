#coding: latin-1

# Use me to record a video with an timestamped overlay.
# You can later check the video and see what happened with they guy under study.

import cv2
import sys, select
import time, datetime

def startVideoRecording(fileName, videoReady):
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(fileName + '.avi',fourcc, 24.0, (int(w),int(h)))


    videoReady.acquire()
    time.sleep(1)
    videoReady.notify()
    videoReady.release()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S-%f')
    print(st)
    while (True):
        input = select.select([sys.stdin], [], [], 0)[0]
        if input:
            print('Exiting...!')
            break
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('Video Stream', frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
