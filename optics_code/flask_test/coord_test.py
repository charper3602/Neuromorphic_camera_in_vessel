import cv2 as cv
import dv_processing as dv
import requests
from datetime import timedelta


url = 'http://127.0.0.1:5000/api/coords/'

capture = dv.io.CameraCapture()

capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.VeryLow)
#g = open('coordfile.txt','w')

eventBC = 0

# Make sure the opened object supports event stream output, otherwise throw runtime error
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")




# Initialize an accumulator with some resolution
accumulator = dv.Accumulator(capture.getEventResolution())

# Apply configuration, these values can be modified to taste
accumulator.setMinPotential(0.0)
accumulator.setMaxPotential(1.0)
accumulator.setNeutralPotential(0.0)
accumulator.setEventContribution(0.05)
accumulator.setDecayFunction(dv.Accumulator.Decay.EXPONENTIAL)
accumulator.setDecayParam(1e+5)
accumulator.setIgnorePolarity(False)
accumulator.setSynchronousDecay(False)

# Initialize preview window
#cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Initialize a slicer
slicer = dv.EventStreamSlicer()



# Declare the callback method for slicer
def slicing_callback(events: dv.EventStore):
    # Pass events into the accumulator and generate a preview frame
    accumulator.accept(events)
    frame_dv = accumulator.generateFrame()
    # Show the accumulated image
    frame = frame_dv.image

    #edge = cv.Canny(frame, 30,200)
    
    #threshold the created frame
    ret,thresh = cv.threshold(frame,127,255,0)
    #draw contours onto the thresholded image
    contours,hierarchy=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

    #initialize counter of contours and string variable to hold coordinates
    cCount = 0
    coordStr = ""

    #loop to iterate over each contour
    for i in contours:

        #conditional statements that determine if max contour length has been exceeded
        if (((cCount > 9) or (cCount == (len(contours) - 1))) and (coordStr != "")):
            response = requests.post(url, json = {"coords":coordStr}, stream=True)
            if response.status_code == 200:
                print(response.status_code)
                #response1 = requests.get('http://127.0.0.1:5000/api/coords/')
                #dataR = response1.json()
            else:
                #print the response code if there was an error with posting
                print(f'Error: {response.status_code}, {response.text}')
            break
        elif ((cCount > 9) or (cCount == (len(contours) - 1))):
            break

        M = cv.moments(i)
        if M['m00'] != 0:
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv.drawContours(thresh, [i], -1, (100, 100, 100), 2)
            #cv.circle(thresh, (cx, cy), 7, (0, 0, 255), -1)
            #cv.putText(thresh, "center", (cx - 20, cy - 20),
            #           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            #g.write(str(frameC)+f" x:{cx} y:{cy}\n")
            #yield (str(frameC)+f" x:{cx} y:{cy}\n")
            
            coordStr += (f"x:{cx} y:{cy} ")
            
        cCount += 1
                
    
    #cv.imshow("Preview", frame.image)
    #cv.drawContours(thresh,contours,-1,(0,255,255),3)
    
    #cv.imshow("preview",thresh)
    #print(str(len(contours)))
    
    #cv.waitKey(2)

# Register a callback every 33 milliseconds
slicer.doEveryTimeInterval(timedelta(milliseconds=33), slicing_callback)
#slicer.doEveryNumberOfEvents(1000,slicing_callback)
# Run the event processing while the camera is connected
while capture.isRunning():
    # Receive events
    events = capture.getNextEventBatch()

    # Check if anything was received
    if events is not None:
        # If so, pass the events into the slicer to handle them
        slicer.accept(events)
        eventBC += 1

cv.destroyAllWindows()
#g.close()
    