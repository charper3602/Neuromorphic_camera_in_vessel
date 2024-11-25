import cv2 as cv
import dv_processing as dv
from datetime import timedelta
import numpy as np

cap = cv.VideoCapture(0)
fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter('output.mp4',fourcc,20.0,(640,480))
f = open('contourfile.txt','w')
g = open('coordfile.txt','w')
frameC = 0

while(True):
    ret,frame = cap.read()


    

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret,thresh = cv.threshold(gray,250,255,cv.THRESH_BINARY)

    contours = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[-2]
    ''' simple version
    for c in contours:
        cv.drawContours(thresh,[c],-1,(100,100,100),2)
    '''
    

    
    for i in contours:
        
        M = cv.moments(i)
        if M['m00'] != 0:
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv.drawContours(thresh, [i], -1, (100, 100, 100), 2)
            #cv.circle(thresh, (cx, cy), 7, (0, 0, 255), -1)
            #cv.putText(thresh, "center", (cx - 20, cy - 20),
            #           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            g.write(str(frameC)+f" x:{cx} y:{cy}\n")
            
                
                
        

    

    
    threshcolor = cv.cvtColor(thresh,cv.COLOR_GRAY2BGR)
    
       
    

    cv.imshow('frame',thresh)
    out.write(threshcolor)
    
    f.write(str(len(contours)))
    # Press 'q' to exit the loop
    if cv.waitKey(1) == ord('q'):
        break
    
    frameC+=1




cap.release()
cv.destroyAllWindows()
out.release()
f.close()
g.close()


