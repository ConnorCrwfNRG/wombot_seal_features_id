import cv2
import os

#Load the video

video_path = os.path.join( os.getcwd(),'videos\Test_Video_WHoles.mov' )
cap=cv2.VideoCapture(video_path,0)

#Inital Setings 
objectName1 = 'hole'
objectName2 = 'bolt' 
frameWidth= 640
frameHeight = 480
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
Neigbors1=1
Min_Area1=150
Brightness1=0

#THRESHOLD FOR SCREWS
Scale2=201
Neigbors2=8
Min_Area2=8400
Brightness2=0

# LOAD THE TRAINED CLASSIFIERS 
hole_cascade_path = os.path.join( os.getcwd(),'images\holes\classifier\cascade.xml')
hole_cascade=cv2.CascadeClassifier(hole_cascade_path)
screw_cascade_path = os.path.join( os.getcwd(),'images\\bolts\classifier\cascade.xml')
## Python error with '\b' -> solved with '\\b'
screw_cascade=cv2.CascadeClassifier(screw_cascade_path)


while (cap.isOpened()):
    
    ret, image =cap.read()
    
        
    #SCREWS 
    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness2 = Brightness2
    # GET VIDEO IMAGE
    success, img = cap.read()
     
    if success == True:
         
        # DETECT THE OBJECT USING THE CASCADE
        scaleVal2=(Scale2 /100)
        screw = screw_cascade.detectMultiScale(img,scaleVal2,Neigbors2)
         
        #HOLES
        # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
        cameraBrightness1 = Brightness1
        # GET VIDEO  IMAGE 
        success, img = cap.read()
        # DETECT THE OBJECT USING THE CASCADE
        scaleVal1=(Scale1 /100)
        hole = hole_cascade.detectMultiScale(img,scaleVal1,Neigbors1)
         
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
             
        #SHOWS THE RESULTANT BOXES
        cv2.imshow("Result", img)
         
        # ALLOWS FOR CANCELATION USING ESCAPE
        k=cv2.waitKey(30) & 0xff
        if k==27:
            break

    else:
        break
    
cap.release()
cv2.destroyAllWindows()
