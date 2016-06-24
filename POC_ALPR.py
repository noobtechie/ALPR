import cv2
import numpy as np
import subprocess

def display(image):
    while True:
        cv2.imshow('Output', image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

tesseract_cmd = 'tesseract'

image  = cv2.imread('images.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
#display(thresh)
cnt, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnt, key=cv2.contourArea, reverse=True)[0]

# compute the rotated bounding box of the largest contour
(x,y,w,h) = cv2.boundingRect(c)
rect = cv2.minAreaRect(c)
box = np.int0(cv2.cv.BoxPoints(rect))

# draw a bounding box arounded the detected barcode and display the
# image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
#plate = gray[box[0][0]:box[2][0],box[0][1]:box[2][1]]
x1 = min(box[:,1])
x2 = max(box[:,1])
y1 = min(box[:,0])
y2 = max(box[:,0])
#print box
plate = gray[x1:x2, y1:y2]
#print plate
'''
print np.shape(gray)
print box
print box[2][1]
print box[0][1]
print box[2][0]
print box[0][0]
print plate
'''
plate_blur = cv2.GaussianBlur(plate, (3, 3), 0)
_,plate_thresh = cv2.threshold(plate_blur, 100, 255, cv2.THRESH_BINARY)
display(plate_thresh)

cv2.imwrite('output.bmp', plate_thresh)

output_file_name = 'out'
command = [tesseract_cmd, 'output.bmp', output_file_name]
proc = subprocess.Popen(command,
                        stderr=subprocess.PIPE)


exit()
