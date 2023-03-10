import cv2 as cv
import numpy as np
import math
from ImageEditor.editBar import EditBar
def nothing(x):
    pass


def histogram(firstFrame,cap, r, h, c, w):
    # roi = firstFrame[r:r+h, c:c+w]
    hsv_roi = cv.cvtColor(firstFrame, cv.COLOR_BGR2HSV)
    hl, hu, sl, su, vl, vu = setMask(cap)
    low = np.array([hl, sl, vl])
    up = np.array([hu, su, vu])
    mask = cv.inRange(hsv_roi, low, up)
    hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
    return [hist]


def setMask(cap):
    cv.namedWindow("Settings")
    cv.resizeWindow("Settings", 640, 250)

    cv.createTrackbar("H Low", "Settings", 0, 180, nothing)
    cv.createTrackbar("H Up", "Settings", 0, 180, nothing)
    cv.createTrackbar("S Low", "Settings", 0, 255, nothing)
    cv.createTrackbar("S Up", "Settings", 0, 255, nothing)
    cv.createTrackbar("V Low", "Settings", 0, 255, nothing)
    cv.createTrackbar("V Up", "Settings", 0, 255, nothing)

    cv.setTrackbarPos("H Low", "Settings", 0)
    cv.setTrackbarPos("H Up", "Settings", 180)
    cv.setTrackbarPos("S Low", "Settings", 0)
    cv.setTrackbarPos("S Up", "Settings", 255)
    cv.setTrackbarPos("V Low", "Settings", 0)
    cv.setTrackbarPos("V Up", "Settings", 255)

    while True:
        _, frame = cap.read()
        frame = cv.flip(frame, 1)
        cv.rectangle(frame, (380, 0), (635, 475), (0, 255, 0), 1)
        roi = frame[0:475, 380:635]
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

        hl = cv.getTrackbarPos("H Low", "Settings")
        hu = cv.getTrackbarPos("H Up", "Settings")
        sl = cv.getTrackbarPos("S Low", "Settings")
        su = cv.getTrackbarPos("S Up", "Settings")
        vl = cv.getTrackbarPos("V Low", "Settings")
        vu = cv.getTrackbarPos("V Up", "Settings")

        low = np.array([hl, sl, vl])
        up = np.array([hu, su, vu])

        mask = cv.inRange(hsv, low, up)
        ker = np.ones((5, 5), np.uint8)

        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, ker)
        mask = cv.dilate(mask, ker, iterations=1)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, ker)
        mask = cv.medianBlur(mask, 15)
        res = cv.bitwise_and(roi, roi, mask=mask)

        cv.imshow("Original", frame)
        cv.imshow("Filter", res)
        print("S1")
        k = cv.waitKey(1)
        if k & 0xFF == ord("s"):
            print("S")
            break

    cv.destroyAllWindows()

    return hl, hu, sl, su, vl, vu


def subtractBg(frame,bgCap):
    fgMask = bgCap.apply(frame, learningRate=0)
    ker = np.ones((3, 3), np.uint8)
    fgMask = cv.erode(fgMask, ker, iterations=1)
    res = cv.bitwise_and(frame, frame, mask=fgMask)

    return res


