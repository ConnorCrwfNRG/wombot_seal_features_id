import cv2
import os
import imutils

#Load the video

video_path = os.path.join( os.getcwd(),'videos\Test_Video_WHoles.mov' )
cap=cv2.VideoCapture(video_path,0)

#Inital Setings 
objectName1 = 'hole'
objectName2 = 'bolt' 
frameWidth= 1280
frameHeight = 720
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
    
        
    #SCREWS 
    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness2 = Brightness2
    # GET VIDEO IMAGE
    success, img = cap.read()
    
    print(success)
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
        
        
        # Display the resulting frame
        # convert the frame to grayscale, blur it, and detect edges
        width = frameWidth
        height = frameHeight
        upper_bound = height-100
        lower_bound = height
        left_bound = 0 
        right_bound = width 
        img = cv2.resize(img, (width,height))
        RIO = img[upper_bound:height,left_bound:right_bound]
        cv2.rectangle(img, (0, upper_bound), (right_bound, height), (0, 255, 0), 2)
        
        
        
        ## Gray for RIO
        gray = cv2.cvtColor(RIO, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        #edged = cv2.Canny(blurred, 50, 150)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        ret,thresh1 = cv2.threshold(blurred,140,255,cv2.THRESH_BINARY_INV)
        edged = cv2.Canny(thresh1, 50, 150)
        cv2.imshow('Threshold', thresh1)

        cv2.imshow('Edged', edged)
        cv2.imshow('Blurred', blurred)
        
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = imutils.grab_contours(cnts)
        left_point = []
        right_point = []
        
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            #print(peri)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)
            #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w/h;
            
            if w > 200 and h < 50 and aspect_ratio > 10:
                
                # Drawing over the countour
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                
                #fitting a bouding rectangle
                #rect = cv2.minAreaRect(c)
                #box = cv2.boxPoints(rect)
                #box = np.int0(box)
                #im = cv2.drawContours(frame,[box],0,(0,0,255),2)

                
                rows,cols = img.shape[:2]
                [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
                lefty = int((-x*vy/vx) + y)
                lefty = lefty + upper_bound
                left_point.append((left_bound,lefty))
                righty = int(((cols-x)*vy/vx)+y)
                righty = righty + upper_bound
                right_point.append((right_bound,righty))
                
                line = cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
                
        ### Code to connect points goes here
        if len(left_point) ==2 and len(right_point)==2:
            left = cv2.line(img, left_point[0], left_point[1], (0,0,255), 2)
            left_dist = float(abs(left_point[0][1] - left_point[1][1])) / 10
            
            right = cv2.line(img, right_point[0], right_point[1], (0,0,255), 2)
            right_dist = float(abs(right_point[0][1] - right_point[1][1])) / 10
            print(left_point, right_point)
            cv2.putText(img, 'The left distance is ' + str(left_dist) + ' cm', (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0,255,0), 2)
            cv2.putText(img, 'The right distance is ' + str(right_dist) + ' cm', (50,100), cv2.FONT_HERSHEY_SIMPLEX , 1, (0,255,0), 2)
        
         

             
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
