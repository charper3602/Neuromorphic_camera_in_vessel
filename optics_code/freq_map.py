import dv_processing as dv
import cv2 as cv
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt


resolution = (640,480)  #resolution of dvxplorer micro

capture = dv.io.CameraCapture()
capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.VeryLow)

# Make sure the opened object supports event stream output, otherwise throw runtime error
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")

#initialize all numpy arrays for calculating frequency
image = np.zeros((480,640), dtype=np.uint8)     #image array used to draw the raw event output thru opencv
pCount = np.zeros((480,640), dtype=np.uint8)    #total num of pos polarities detected across all cycles
nCount = np.zeros((480,640), dtype=np.uint8)    #total num of neg polarities detected across all cycles
currPol = np.zeros((480,640), dtype=np.uint8)   #current polarity of a pixel while looping thru event store
polShifts = np.zeros((480,640), dtype=np.uint8) #num of polarity shifts per pixel
fMap = np.zeros((480,640), dtype='f')           #frequency values for each pixel

sTime = 50000   #50ms
sTime_window = 7500 #7.5ms
refTime = dv.now()  #value of first event timestamp of every sTime interval
brTime = 0  #used to check when to break out of event loop
evOne = 0   #set once first event of every sTime interval has been passed
frameCount = 0  #counts number of cycles(sTime intervals)

#Initialize chain of event filters
#fFilter = dv.EventFilterChain()

# Initialize a background activity noise filter with 10-millisecond half life decay, resolution subdivision
# factor of 4 and noise threshold of 1. Half life decay and noise threshold values controls the quality of
# filtering, while subdivision factor is used for resolution downsizing for internal event representation.
#THIS FILTER IS NOT USED!
'''
fFilter.addFilter(dv.noise.FastDecayNoiseFilter(resolution,
                                       halfLife=timedelta(milliseconds=0.5),
                                       subdivisionFactor=4,
                                       noiseThreshold=0.5))
'''
#main capture loop
while capture.isRunning():
    
    events = capture.getNextEventBatch()
    
    if events is not None:  #check that the event store isn't empty
        #event loop
        for i in events:
            if(evOne == 0):
                refTime = i.timestamp() #if this is the first event in a 50ms(sTime value) batch, choose the
                                        #reference time to be the value of the first timestamp
                evOne = 1

            #print(i.timestamp())
            diff = i.timestamp()-refTime    #calculate the difference between the timestamp window and the reference time
            if ((diff >= sTime) and (diff <= (sTime + sTime_window))):
                
                if((brTime != 0) and (brTime < diff)):  #if diff reaches the value of sTime, break out of the for loop
                    break
                
                #pass x and y coords to variables
                evX = i.x()  
                evY = i.y()
                print(f"{evX} {evY} {i.polarity()}")

                #polarity of an event can only be positive or negative
                if(i.polarity() == True):
                    #checks for neg->pos polarity shifts at this specific pixel 
                    if (currPol[evY][evX] == -1):
                        polShifts[evY][evX] += 1    #counts a polarity shift at this pixel

                    currPol[evY][evX] = 1   #set current polarity for this pixel to pos
                    image[evY][evX] = 255   
                    pCount[evY][evX] += 1
                else:
                    #checks for pos->neg polarity shifts at this specific pixel 
                    if (currPol[evY][evX] == 1):
                        polShifts[evY][evX] += 1    #counts a polarity shift at this pixel

                    currPol[evY][evX] = -1  #set current polarity for this pixel to neg
                    image[evY][evX] = 50
                    nCount[evY][evX] += 1
                
                brTime = diff
                
                #if(frameCount >= 1):        

        #This if statement runs after breaking out of the event loop(after every sTime interval)
        if((diff >= sTime) and (diff <= (sTime + sTime_window))):
            
            cv.imshow("preview",image)
            cv.waitKey(2)
            if (frameCount >= 19):  #Checks if 20 cycles of sTime have been reached
                break   #if so, break out of the capture loop
            
            brTime = 0
            evOne = 0
            frameCount += 1
            image = np.zeros((480,640), dtype=np.uint8)
            

frameCount += 1 #Add 1 to get the total number of cycles run by the capture loop
print(frameCount)   #debug to check if 20

#loop thru 640x480 numpy arrays to calculate frequency using num of polarity shifts for each pixel
for i in range(resolution[0]):
    for j in range(resolution[1]): 
        if ((polShifts[j][i] != 0)): #and (pCount[j][i] == nCount[j][i])
            #fMap[j][i] = 1/(pCount[j][i] * 0.05)
            fMap[j][i] = 1/(((frameCount * 50)/(polShifts[j][i]+1))*0.001)

#plot the frequency map using a simple function
plt.imshow(fMap,cmap='hot',interpolation='nearest')
plt.show()

cv.destroyAllWindows()

    
    
    
    
    