import cv2
import numpy as np

#Load the video
#cap=cv2.VideoCapture('/home/adrianabeyta/anaconda3/share/OpenCV/FInal Project/TestVideo.mp4',0)
#cap=cv2.VideoCapture('/home/adrianabeyta/anaconda3/share/OpenCV/FInal Project/Test_Video_WHoles.mov',0)
cap=cv2.VideoCapture('/home/adrianabeyta/anaconda3/share/OpenCV/FInal Project/slowed.mp4',0)
#cap=cv2.VideoCapture(0)

#Inital Setings 
objectName1 = 'hole'  # OBJECT NAME TO DISPLAY
objectName2 = 'bolt' 
frameWidth= 640                     # DISPLAY WIDTH
frameHeight = 480                  # DISPLAY HEIGHT
color1= (255,225,0)
color2= (255,0,0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass
# CREATE thresholds
#cv2.namedWindow("Result")
#cv2.resizeWindow("Result",frameWidth,frameHeight+100)

# #THRESHOLD FOR HOLES
Scale1=200
Neig1=1
Min_Area1=150
Brightness1=0

#THRESHOLD FOR SCREWS
Scale2=201
Neig2=8
Min_Area2=1200
Brightness2=0

# LOAD THE CLASSIFIERS DOWNLOADED
#screw_cascade= cv2.CascadeClassifier('/home/adrianabeyta/anaconda3/share/OpenCV/haarcascades/haarcascade_bolt.xml')
hole_cascade=cv2.CascadeClassifier('/home/adrianabeyta/anaconda3/share/OpenCV/haarcascades/haarcascade_holes.xml')
screw_cascade=cv2.CascadeClassifier('/home/adrianabeyta/anaconda3/share/OpenCV/haarcascades/haarcascade_bolt3.xml')
while (cap.isOpened()):
    
    ret=cap.read()
    
    if not ret:
        break
    
    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness2 = Brightness2
    # GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
    success, img = cap.read()
    # DETECT THE OBJECT USING THE CASCADE
    scaleVal2=(Scale2 /100)
    neig2=Neig2
    screw = screw_cascade.detectMultiScale(img,scaleVal2,neig2)
    

    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness1 = Brightness1
    # GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
    success, img = cap.read()
    # DETECT THE OBJECT USING THE CASCADE
    scaleVal1=(Scale2 /100)
    neig1=Neig1
    hole = hole_cascade.detectMultiScale(img,scaleVal1,neig1)
    
    #DISPLAY THE DETECTED SCREWS
    for (x,y,w,h) in screw:
        area = w*h
        minArea = Min_Area2
        if area >minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color1,3)
            cv2.putText(img,objectName2,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color1,1)
            roi_color = img[y:y+h, x:x+w]
            
    # DISPLAY THE DETECTED HOLES
    for (x,y,w,h) in hole:
        area = w*h
        minArea = Min_Area1
        if area >minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color2,3)
            cv2.putText(img,objectName1,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color2,1)
            roi_color = img[y:y+h, x:x+w]
            
  
    cv2.imshow("Result", img)

  
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break
    
cap.release()
cv2.destroyAllWindows()
