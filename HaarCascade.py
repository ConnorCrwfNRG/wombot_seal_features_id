#Load the video
cap=cv2.VideoCapture('/home/adrianabeyta/anaconda3/share/OpenCV/FInal Project/TestVideo.mp4',0)
#cap=cv2.VideoCapture(0)

#Inital Setings 
objectName = 'bolt'       # OBJECT NAME TO DISPLAY
frameWidth= 640                     # DISPLAY WIDTH
frameHeight = 480                  # DISPLAY HEIGHT
color= (255,225,0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass
# CREATE TRACKBAR
cv2.namedWindow("Result")
cv2.resizeWindow("Result",frameWidth,frameHeight+100)
cv2.createTrackbar("Scale","Result",201,1000,empty)
cv2.createTrackbar("Neig","Result",10,50,empty)
cv2.createTrackbar("Min Area","Result",10000,50000,empty)
cv2.createTrackbar("Brightness","Result",100,200,empty)

# LOAD THE CLASSIFIERS DOWNLOADED
screw_cascade= cv2.CascadeClassifier('/home/adrianabeyta/anaconda3/share/OpenCV/haarcascades/haarcascade_bolt.xml')

while True:
    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, cameraBrightness)
    # GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
    success, img = cap.read()
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    # DETECT THE OBJECT USING THE CASCADE
    scaleVal =(cv2.getTrackbarPos("Scale", "Result") /100)
    neig=cv2.getTrackbarPos("Neig", "Result")
    objects = screw_cascade.detectMultiScale(img,scaleVal,neig)
   
    
    # DISPLAY THE DETECTED OBJECTS
    for (x,y,w,h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area >minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color,3)
            cv2.putText(img,objectName,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            roi_color = img[y:y+h, x:x+w]

    cv2.imshow("Result", img)

  
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break
    
cap.release()
cv2.destroyAllWindows()
