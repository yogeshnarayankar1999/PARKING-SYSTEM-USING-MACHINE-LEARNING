import cv2
import csv

VIDEO_SOURCE = 0  #1 for inbuilt camera and 0 for secondary camera

cap = cv2.VideoCapture(VIDEO_SOURCE) #for capturing video
suc, image = cap.read()
cv2.imwrite("frame0.jpg", image) #frame 0 refrence image machine sathi learn vhayala
cap.release()
cv2.destroyAllWindows()

img = cv2.imread("frame0.jpg")
font = cv2.FONT_HERSHEY_SIMPLEX
img = cv2.putText(img , 'SELECT THE PARKING SPOTS', (5, 25), font, 0.75, (0, 255, 0), 2) #this text will show on the image

img = cv2.putText(img , 'Press ESC after selecting all spots', (375, 460), font, 0.45, (225, 225, 50), 1)#this text will show on the image

r = cv2.selectROIs('SELECTOR', img, showCrosshair = False, fromCenter = False) #console project name 
rlist = r.tolist()

with open('data/rois.csv', 'w', newline='') as outf: #Excel sheet opening for cordinates and writing it into list format
    csvw = csv.writer(outf)
    csvw.writerows(rlist)

def drawRectangle(img, a, b, c, d): #for Showing green and red based upon parking space cordinates in image source.
    sub_img = img[b:b + d, a:a + c]
    edges = cv2.Canny(sub_img, lowThreshold, highThreshold)
    pix = cv2.countNonZero(edges)
    if pix in range(min, max):
        cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 0), 3)
        spots.loc += 1
    else:
        cv2.rectangle(img, (a, b), (a + c, b + d), (0, 0, 255), 3)

def callback(foo):
    pass

cv2.namedWindow('parameters') # Parameters of console of detector and managing the canny values for black and white pixel 
cv2.createTrackbar('Threshold1', 'parameters', 186, 700, callback)  
cv2.createTrackbar('Threshold2', 'parameters', 122, 700, callback)
cv2.createTrackbar('Min pixels', 'parameters', 100, 1500, callback)
cv2.createTrackbar('Max pixels', 'parameters', 323, 1500, callback)

class spots:
    loc = 0 #static variable used for further counting the avaliable spots

with open('data/rois.csv', 'r', newline='') as inf: #Excel sheet opening for cordinates
    csvr = csv.reader(inf)
    rois = list(csvr) #capturing Excel sheet data list used by machine for learning

rois = [[int(float(j)) for j in i] for i in rois]
VIDEO_SOURCE = 0
cap = cv2.VideoCapture(VIDEO_SOURCE) #live video opening

while True:
    spots.loc = 0

    ret, frame = cap.read()
    ret2, frame2 = cap.read()
    min = cv2.getTrackbarPos('Min pixels', 'parameters')
    max = cv2.getTrackbarPos('Max pixels', 'parameters')
    lowThreshold = cv2.getTrackbarPos('Threshold1', 'parameters')
    highThreshold = cv2.getTrackbarPos('Threshold2', 'parameters')

    for i in range(len(rois)):
        drawRectangle(frame, rois[i][0], rois[i][1], rois[i][2], rois[i][3])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'AVAILABLE SPOTS: ' + str(spots.loc), (5, 25), font, 0.75, (225, 225, 225), 2)
    cv2.imshow('Detector', frame)
    
    canny = cv2.Canny(frame2, lowThreshold, highThreshold) #seprating white and black portion for live video used by canny
    cv2.imshow('canny', canny)#displaying canny console

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
