import cv2
import numpy as np

# img = cv2.imread('background.jpg', 0)
# retval, threshold = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
# cv2.imshow('image', img)
# cv2.imshow('thr', threshold)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


img = cv2.imread('background.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)


_, contours, _= cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    rect = cv2.boundingRect(c)
    if rect[2] < 10 or rect[3] < 10: continue
    print cv2.contourArea(c)
    x,y,w,h = rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(img,'Moth Detected',(x+w+10,y+h),0,0.3,(0,255,0))
cv2.imshow("Show",img)
cv2.waitKey()
cv2.destroyAllWindows()