#coding: latin-1

# Use me to record a video

import argparse

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

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  cv2.imshow('frame',gray)
  cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()