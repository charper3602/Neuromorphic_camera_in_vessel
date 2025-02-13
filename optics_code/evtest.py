import dv_processing as dv
import cv2 as cv
import numpy as np
from datetime import timedelta
import requests

url = 'http://127.0.0.1:5500/api/coords/'

capture = dv.io.CameraCapture()
capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.VeryLow)

#establish reference time for timestamps
refTime = dv.now()
resolution = (640,480)

#
init_remove = requests.delete(url)
if init_remove.status_code == 204:
    print(init_remove.status_code)
else:
    #print the response code if there was an error with deleting
    print(f'Error: {init_remove.status_code}, {init_remove.text}')

#Initialize chain of event filters
fFilter = dv.EventFilterChain()

# Filter positive polarity events only
fFilter.addFilter(dv.EventPolarityFilter(True))

# Initialize a background activity noise filter with 10-millisecond half life decay, resolution subdivision
# factor of 4 and noise threshold of 1. Half life decay and noise threshold values controls the quality of
# filtering, while subdivision factor is used for resolution downsizing for internal event representation.
fFilter.addFilter(dv.noise.FastDecayNoiseFilter(resolution,
                                       halfLife=timedelta(milliseconds=0.5),
                                       subdivisionFactor=4,
                                       noiseThreshold=0.5))

# Make sure the opened object supports event stream output, otherwise throw runtime error
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")

#holds location of previously identified coordinate string
prevStr = ["-1 -1*","-1 -1*","-1 -1*","-1 -1*","-1 -1*"]
tStamp = ["0","0","0","0","0"]

while capture.isRunning():
    #remove previous coord list
    remove = requests.delete(url)
    if remove.status_code == 204:
        print(remove.status_code)
    else:
        #print the response code if there was an error with posting
        print(f'Error: {remove.status_code}, {remove.text}')
    # Receive events
    events = capture.getNextEventBatch()
    if events is not None:
        fFilter.accept(events)
        filtered = fFilter.generateEvents()

        image = np.zeros((480,640), dtype=np.uint8)
        cImage = np.zeros((480,640), dtype=np.uint8)
        evCoord = filtered.coordinates()
        


        for i in range(len(evCoord)):
            image[evCoord[i][1]][evCoord[i][0]] = 150


        contours,hierarchy=cv.findContours(image,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

        #initialize counter of contours and string variable to hold coordinates
        cCount = 0
        coordStr = ["-1 -1*","-1 -1*","-1 -1*","-1 -1*","-1 -1*"]
        coordSend = ""

        #loop to iterate over each contour
        for i in contours:
            cLen = len(contours)
            #conditional statements that determine if max contour length has been exceeded
            if (((cCount > 4) or (cCount == (cLen - 1))) and (coordStr[0] != "-1 -1*")):
                for j in coordStr:
                    coordSend += j
                response = requests.post(url, json = {"coords":coordSend}, stream=True)
                if response.status_code == 201:
                    print(response.status_code)
                else:
                    #print the response code if there was an error with posting
                    print(f'Error: {response.status_code}, {response.text}')
                break
            elif ((cCount > 4) or (cCount == (cLen - 1))):
                break

            M = cv.moments(i)
            if M['m00'] != 0:

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv.drawContours(image, [i], -1, (100, 100, 100), 2)
                #cv.circle(thresh, (cx, cy), 7, (0, 0, 255), -1)
                
                for ev in filtered:
                    if ((cx==ev.x()) and (cy==ev.y())):
                        tStamp[cCount] = ev.timestamp()
                        break

                coordStr[cCount] = (f"{cx} {cy}*")

                #if prevStr[cCount] != "-1 -1*":
                    #tracking functions go here


                #prevStr[cCount] = (f"{cx} {cy}*")

            cCount += 1

        
        cv.imshow("preview",image)
        cv.waitKey(2)
        
    
    





    

