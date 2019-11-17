#coding: latin-1

# Use me to record a video

import argparse
import cv2

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required .csv file location argument
parser.add_argument('--raw_data_path', help='A required file path to raw data')

# Required .avi file location argument
parser.add_argument('--video_path', help='A required file path to video')

# Parse srguments
args = parser.parse_args()

cap = cv2.VideoCapture(args.video_path)

while cap.isOpened():
  ret, frame = cap.read()
  if ret == True:
    cv2.imshow('Frame',frame)
  else:
    break
  cv2.waitKey(41)

cap.release()
cv2.destroyAllWindows()