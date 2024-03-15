import cv2
import numpy as np
import time
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO

# Image Processing variables
frame = None
Matrix = None
framePers = None
frameGray = None
frameThresh = None
frameEdge = None
frameFinal = None
frameFinalDuplicate = None
frameFinalDuplicate1 = None
ROILane = None
ROILaneEnd = None
LeftLanePos = 0
RightLanePos = 0
frameCenter = 0
laneCenter = 0
Result = 0
laneEnd = 0
histrogramLane = []
histrogramLaneEnd = []

# Machine Learning variables
Stop_Cascade = cv2.CascadeClassifier()
Object_Cascade = cv2.CascadeClassifier()
Traffic_Cascade = cv2.CascadeClassifier()
frame_Stop = None
RoI_Stop = None
gray_Stop = None
frame_Object = None
RoI_Object = None
gray_Object = None
frame_Traffic = None
RoI_Traffic = None
gray_Traffic = None
dist_Stop = 0
dist_Object = 0
dist_Traffic = 0

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Camera setup
camera = PiCamera()
camera.resolution = (400, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(400, 240))
time.sleep(0.1)

def Perspective(frame):
    global framePers, Matrix
    src = np.float32([(40, 135), (360, 135), (0, 185), (400, 185)])
    dst = np.float32([(100, 0), (280, 0), (100, 240), (280, 240)])
    Matrix = cv2.getPerspectiveTransform(src, dst)
    framePers = cv2.warpPerspective(frame, Matrix, (400, 240))
    
def Threshold(frame):
    global frameThresh, frameEdge, frameFinal
    frameGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frameThresh = cv2.inRange(frameGray, 230, 255)
    frameEdge = cv2.Canny(frameGray, 900, 900)
    frameFinal = cv2.add(frameThresh, frameEdge)

def Histrogram(frame):
    global histrogramLane, histrogramLaneEnd, laneEnd
    histrogramLane = np.sum(frame[140:, :], axis=0)
    histrogramLaneEnd = np.sum(frame[:240, :], axis=0)
    laneEnd = np.sum(histrogramLaneEnd)

def LaneFinder(frame):
    global LeftLanePos, RightLanePos
    midpoint = len(histrogramLane) // 2
    LeftLanePos = np.argmax(histrogramLane[:midpoint])
    RightLanePos = np.argmax(histrogramLane[midpoint:]) + midpoint

def LaneCenter():
    global laneCenter, frameCenter, Result
    laneCenter = (RightLanePos - LeftLanePos) // 2 + LeftLanePos
    frameCenter = 188
    Result = laneCenter - frameCenter

def Stop_detection(frame):
    global dist_Stop
    stops = Stop_Cascade.detectMultiScale(frame_Stop, 1.1, 5)
    for (x, y, w, h) in stops:
        cv2.rectangle(frame_Stop, (x, y), (x+w, y+h), (255, 0, 0), 2)
        dist_Stop = (-1.07)*(x+w-x) + 102.597

def Traffic_detection(frame):
    global dist_Traffic
    traffic = Traffic_Cascade.detectMultiScale(frame_Traffic, 1.1, 5)
    for (x, y, w, h) in traffic:
        cv2.rectangle(frame_Traffic, (x, y), (x+w, y+h), (255, 0, 0), 2)
        dist_Traffic = (-1.07)*(x+w-x) + 102.597

def Object_detection(frame):
    global dist_Object
    objects = Object_Cascade.detectMultiScale(frame_Object, 1.1, 5)
    for (x, y, w, h) in objects:
        cv2.rectangle(frame_Object, (x, y), (x+w, y+h), (255, 0, 0), 2)
        dist_Object = (-0.48)*(x+w-x) + 56.6

def main():
    global frame, frame_Stop, frame_Object, frame_Traffic
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        frame_Stop = frame[0:140, 200:400]
        frame_Object = frame[50:240, 100:300]
        frame_Traffic = frame[0:140, 200:400]

        Perspective(frame)
        Threshold(framePers)
        Histrogram(frameFinal)
        LaneFinder(frameFinal)
        LaneCenter()
        Stop_detection(frame_Stop)
        Traffic_detection(frame_Traffic)
        Object_detection(frame_Object)

        # Perform driving decisions based on detected objects and lane markings

        rawCapture.truncate(0)

if __name__ == "__main__":
    main()
