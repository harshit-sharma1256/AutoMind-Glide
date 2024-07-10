import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread

# Initialize the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Image Processing Variables
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

# Points for perspective transform
Source = np.float32([[40, 135], [360, 135], [0, 185], [400, 185]])
Destination = np.float32([[100, 0], [280, 0], [100, 240], [280, 240]])

# Load Cascade Classifiers
Stop_Cascade = cv2.CascadeClassifier('/home/pi/Desktop/MACHINE LEARNING/Stop_cascade.xml')
Object_Cascade = cv2.CascadeClassifier('/home/pi/Desktop/MACHINE LEARNING/Object_cascade.xml')
Traffic_Cascade = cv2.CascadeClassifier('/home/pi/Desktop/MACHINE LEARNING/Trafficc_cascade.xml')

# Camera Setup
camera = PiCamera()
camera.resolution = (400, 240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(400, 240))

time.sleep(0.1)

def capture():
    global frame
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        break
    rawCapture.truncate(0)

def perspective():
    global frame, Matrix, framePers
    cv2.line(frame, (Source[0][0], Source[0][1]), (Source[1][0], Source[1][1]), (0, 0, 255), 2)
    cv2.line(frame, (Source[1][0], Source[1][1]), (Source[3][0], Source[3][1]), (0, 0, 255), 2)
    cv2.line(frame, (Source[3][0], Source[3][1]), (Source[2][0], Source[2][1]), (0, 0, 255), 2)
    cv2.line(frame, (Source[2][0], Source[2][1]), (Source[0][0], Source[0][1]), (0, 0, 255), 2)
    
    Matrix = cv2.getPerspectiveTransform(Source, Destination)
    framePers = cv2.warpPerspective(frame, Matrix, (400, 240))

def threshold():
    global framePers, frameGray, frameThresh, frameEdge, frameFinal, frameFinalDuplicate, frameFinalDuplicate1
    frameGray = cv2.cvtColor(framePers, cv2.COLOR_RGB2GRAY)
    frameThresh = cv2.inRange(frameGray, 230, 255)
    frameEdge = cv2.Canny(frameGray, 900, 900)
    frameFinal = cv2.add(frameThresh, frameEdge)
    frameFinal = cv2.cvtColor(frameFinal, cv2.COLOR_GRAY2RGB)
    frameFinalDuplicate = cv2.cvtColor(frameFinal, cv2.COLOR_RGB2BGR)
    frameFinalDuplicate1 = cv2.cvtColor(frameFinal, cv2.COLOR_RGB2BGR)

def histrogram():
    global histrogramLane, histrogramLaneEnd, frameFinalDuplicate, frameFinalDuplicate1, laneEnd
    histrogramLane.clear()
    
    for i in range(400):
        ROILane = frameFinalDuplicate[140:240, i:i+1]
        ROILane = cv2.divide(255, ROILane)
        histrogramLane.append(int(cv2.sumElems(ROILane)[0]))
    
    histrogramLaneEnd.clear()
    for i in range(400):
        ROILaneEnd = frameFinalDuplicate1[:, i:i+1]
        ROILaneEnd = cv2.divide(255, ROILaneEnd)
        histrogramLaneEnd.append(int(cv2.sumElems(ROILaneEnd)[0]))
    
    laneEnd = sum(histrogramLaneEnd)
    print("Lane END =", laneEnd)

def lane_finder():
    global LeftLanePos, RightLanePos, frameFinal, histrogramLane
    LeftLanePos = np.argmax(histrogramLane[:150])
    RightLanePos = np.argmax(histrogramLane[250:]) + 250
    
    cv2.line(frameFinal, (LeftLanePos, 0), (LeftLanePos, 240), (0, 255, 0), 2)
    cv2.line(frameFinal, (RightLanePos, 0), (RightLanePos, 240), (0, 255, 0), 2)

def lane_center():
    global laneCenter, frameCenter, Result, frameFinal
    laneCenter = (RightLanePos - LeftLanePos) // 2 + LeftLanePos
    frameCenter = 188
    
    cv2.line(frameFinal, (laneCenter, 0), (laneCenter, 240), (0, 255, 0), 3)
    cv2.line(frameFinal, (frameCenter, 0), (frameCenter, 240), (255, 0, 0), 3)
    
    Result = laneCenter - frameCenter

def stop_detection():
    global frame_Stop, RoI_Stop, gray_Stop, dist_Stop
    RoI_Stop = frame_Stop[0:140, 200:400]
    gray_Stop = cv2.cvtColor(RoI_Stop, cv2.COLOR_RGB2GRAY)
    gray_Stop = cv2.equalizeHist(gray_Stop)
    Stop = Stop_Cascade.detectMultiScale(gray_Stop)
    
    for (x, y, w, h) in Stop:
        cv2.rectangle(RoI_Stop, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(RoI_Stop, "Stop Sign", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        dist_Stop = (-1.07) * w + 102.597
        cv2.putText(RoI_Stop, f"D = {dist_Stop:.2f}cm", (1, 130), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

def traffic_detection():
    global frame_Traffic, RoI_Traffic, gray_Traffic, dist_Traffic
    RoI_Traffic = frame_Traffic[0:140, 200:400]
    gray_Traffic = cv2.cvtColor(RoI_Traffic, cv2.COLOR_RGB2GRAY)
    gray_Traffic = cv2.equalizeHist(gray_Traffic)
    Traffic = Traffic_Cascade.detectMultiScale(gray_Traffic)
    
    for (x, y, w, h) in Traffic:
        cv2.rectangle(RoI_Traffic, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(RoI_Traffic, "Traffic Light", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        dist_Traffic = (-1.07) * w + 102.597
        cv2.putText(RoI_Traffic, f"D = {dist_Traffic:.2f}cm", (1, 130), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

def object_detection():
    global frame_Object, RoI_Object, gray_Object, dist_Object
    RoI_Object = frame_Object[50:240, 100:300]
    gray_Object = cv2.cvtColor(RoI_Object, cv2.COLOR_RGB2GRAY)
    gray_Object = cv2.equalizeHist(gray_Object)
    Object = Object_Cascade.detectMultiScale(gray_Object)
    
    for (x, y, w, h) in Object:
        cv2.rectangle(RoI_Object, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(RoI_Object, "Object", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        dist_Object = (-0.48) * w + 56.6
        cv2.putText(RoI_Object, f"D = {dist_Object:.2f}cm", (1, 130), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

def motor_control():
    global Result, laneEnd, dist_Stop, dist_Traffic, dist_Object
    
    if Result == 0:
        GPIO.output(21, False)
        GPIO.output(22, False)
        GPIO.output(23, False)
        GPIO.output(24, False)
    elif 0 < Result < 10:
        GPIO.output(21, True)
        GPIO.output(22, False)
        GPIO.output(23, False)
        GPIO.output(24, False)
    elif 10 <= Result < 20:
        GPIO.output(21, True)
        GPIO.output(22, True)
        GPIO.output(23, False)
        GPIO.output(24, False)
    elif Result >= 20:
        GPIO.output(21, True)
        GPIO.output(22, True)
        GPIO.output(23, True)
        GPIO.output(24, False)
    elif -10 < Result < 0:
        GPIO.output(21, False)
        GPIO.output(22, False)
        GPIO.output(23, False)
        GPIO.output(24, True)
    elif -20 < Result <= -10:
        GPIO.output(21, False)
        GPIO.output(22, False)
        GPIO.output(23, True)
        GPIO.output(24, True)
    elif Result <= -20:
        GPIO.output(21, False)
        GPIO.output(22, True)
        GPIO.output(23, True)
        GPIO.output(24, True)
    
    if 0 < dist_Stop < 55:
        print("Stop Sign Detected")
        GPIO.output(21, False)
        GPIO.output(22, False)
        GPIO.output(23, False)
        GPIO.output(24, False)
    
    if 0 < dist_Traffic < 55:
        print("Traffic Light Detected")
        GPIO.output(21, False)
        GPIO.output(22, False)
        GPIO.output(23, False)
        GPIO.output(24, False)
    
    if 0 < dist_Object < 30:
        print("Object Detected")
        GPIO.output(21, False)
        GPIO.output(22, False)
        GPIO.output(23, False)
        GPIO.output(24, False)

def display():
    global frame
    cv2.imshow('Frame', frame)
    cv2.imshow('Perspective', framePers)
    cv2.imshow('Final', frameFinal)

def main():
    while True:
        capture()
        perspective()
        threshold()
        histrogram()
        lane_finder()
        lane_center()
        stop_detection()
        traffic_detection()
        object_detection()
        motor_control()
        display()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.close()
    cv2.destroyAllWindows()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
