# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import myutils
from myLogger import log

class CV():

    def __init__(self):
        log("initializing Videostream...")
        self.videoStream = VideoStream(src=0).start()
        time.sleep(2.0)
        self.lowerColor = (0, 80, 138)
        self.upperColor = (38, 251, 255)
        self.position = (10,10)
        log("Videostream initialized")

    def __del__(self):
        self.videoStream.stop()
        log("Videostream stopped")

    def getPosition(self):
        center = None
        frame = self.videoStream.read()
        # log("Frame read")
        if frame is None:
            log("no frame available", "WARN")
            return self.position
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # construct a mask for the color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.lowerColor, self.upperColor)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
		# find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # log("found contour!", "OK")
            # find the largest contour in the mask
            c = max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            x = myutils.map(center[0], 0, 600, 0, 100)
            y = myutils.map(center[1], 0, 600, 0, 100)
            self.position = (x, y)
            cv2.drawContours(frame, [c], 0, (0,255,0),3)
        else:
            log("no contour found", "WARN")
        cv2.imshow("Frame", frame)
        log("Position is {}".format(self.position))
        return self.position
