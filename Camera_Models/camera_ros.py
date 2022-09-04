#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import time
import os
from threading import Thread
from tensorflow.lite.python.interpreter import Interpreter
from std_msgs.msg import String


pub = rospy.Publisher('Object_Detection', String, queue_size=10) # Create node to publish to Object_Detection topic
rospy.init_node('camera', anonymous=True) # Name ROS node "camera"
rate = rospy.Rate(10) # updates 10 times a second


#### Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

#### End Define VideoStream class

# Get current path and tflite path
CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH,'/MobileNet/Sample_TFLite_model/detect.tflite')
PATH_TO_LABELS = os.path.join(CWD_PATH,'/MobileNet/Sample_TFLite_model/labelmap.txt')

# Read label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

 del(labels[0])  # Delete first ???? label

# Load Tflite model
 interpreter = Interpreter(model_path=PATH_TO_CKPT)
 interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
input_mean = 127.5
input_std = 127.5

# index for a tensflow 2.0.0+ model
boxes_idx, classes_idx, scores_idx = 1, 3, 0


# Initialize video stream
videostream = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)

# Key indexes of objects we care about
person_index = 2
stop_sign_index = 14
ball_index = 38

key_objects = [person_index,stop_sign_index,ball_index]


# Start the Object detection modeling
while True:
    # Grab frame from video stream
    frame1 = videostream.read()

    # Acquire frame and resize to expected shape [1xHxWx3]
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Get the classes from the object detection model
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects

    if any(x in classes for x in key_objects): # Check to see if any of the detected objects match the 3 objects we care about
        rospy.loginfo('obstacle') # Print the obstacle to the window and log it
        pub.publish('obstacle') # Publish the message to the Object_Detection topic

    rate.sleep()