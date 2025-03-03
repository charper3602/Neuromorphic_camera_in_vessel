import datetime
import numpy as np
import dv_processing as dv
import cv2 as cv
from math import atan2, cos, sin, sqrt, pi
import matplotlib.pyplot as plt



capture = dv.io.CameraCapture()
capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.VeryLow)


posEvX = []
posEvY = []
posEvTime = []
negEvX = []
negEvY = []
negEvTime = []

evCount = 0
startTime = 0
endLoop = 0

# Make sure the opened object supports event stream output, otherwise throw runtime error
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")


#PCA angle function, from opencv example
def getOrientation(pts, img):
    
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i,0] = pts[i,0,0]
        data_pts[i,1] = pts[i,0,1]
 
    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
 
    # Store the center of the object
    cntr = (int(mean[0,0]), int(mean[0,1]))
    
 
    
    cv.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
    p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])

    angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    
 
    return angle,cntr


#mean shift code, from dv website example, modified
def run_mean_shift(events):
    
    global posEvX,posEvY,posEvTime,negEvX,negEvY,negEvTime,evCount,startTime,endLoop

    image = np.zeros((480,640,3), dtype=np.uint8)     #image array used to draw the mean shift markers
    mean_shift.accept(events)
    mean_shift_tracks = mean_shift.runTracking()

    #preview = visualizer.generateImage(events)

    # Draw markers on each of the track coordinates
    if len(mean_shift_tracks.keypoints) > 0:
        for index in range(5): #only draw 5 points at one time
            if ((index+1)>=len(mean_shift_tracks.keypoints)):
                break
            track = mean_shift_tracks.keypoints[index]
            image = cv.circle(image, (int(track.pt[0]), int(track.pt[1])), radius=1, color=(255,255,255),
                              thickness=-1)
            #cv.drawMarker(image, (int(track.pt[0]), int(track.pt[1])), dv.visualization.colors.red(), cv.MARKER_CROSS,
                          #20, 2)
            #print(f"{track.pt[0]} {track.pt[1]}")

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    contours,hierarchy=cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    c = np.zeros((len(contours), 1, 2), dtype=np.int32)

    #for i,c in enumerate(contours):
    for i in range(len(contours)):
        tempCont = contours[i]
        c[i][0] = tempCont[0][0]
        # Calculate the area of each contour
        #area = cv.contourArea(c)
        # Ignore contours that are too small or too large
        #if area < 1e2 or 1e5 < area:
        #    continue
        # Draw each contour only for visualisation purposes
        #cv.drawContours(image, contours, i, (0, 0, 255), 2)
        # Find the orientation of each shape
    if (len(contours) > 1):
        an,cn=getOrientation(c, image)
    
    for ev in events:
        evTime = ev.timestamp()
        if evCount == 0:
            evCount = 1
            startTime = ev.timestamp()
        if((ev.x()>=cn[0]-10) and (ev.x()<=cn[0]+10) and (ev.y()>=cn[1]-10) and (ev.y()<=cn[1]+10)):
            if (ev.polarity() == True):
                posEvX.append(ev.x())
                posEvY.append(ev.y())
                posEvTime.append(ev.timestamp())
            else:
                negEvX.append(ev.x())
                negEvY.append(ev.y())
                negEvTime.append(ev.timestamp())
        if((evTime-startTime) >= 100000):
            endLoop = 1
            return




# Use VGA resolution
resolution = (640, 480)


# Initialize a slicer
slicer = dv.EventStreamSlicer()



#Initialize chain of event filters
fFilter = dv.EventFilterChain()

# Allow positive polarity events only
fFilter.addFilter(dv.EventPolarityFilter(True))

# Initialize a background activity noise filter with 10-millisecond half life decay, resolution subdivision
# factor of 4 and noise threshold of 1. Half life decay and noise threshold values controls the quality of
# filtering, while subdivision factor is used for resolution downsizing for internal event representation.
fFilter.addFilter(dv.noise.FastDecayNoiseFilter(resolution,
                                       halfLife=datetime.timedelta(milliseconds=0.5),
                                       subdivisionFactor=4,
                                       noiseThreshold=0.5))

# Initialize a preview window
#cv.namedWindow("Preview", cv.WINDOW_NORMAL)


#main capture loop
while capture.isRunning():
    
    events = capture.getNextEventBatch()
    
    if events is not None:
        
        fFilter.accept(events)
        filtered = fFilter.generateEvents()
        # parameter defining the spatial window [pixels] in which the new track position will be searched
        bandwidth = 10

        # window of time used to compute the time surface used for the tracking update
        time_window = datetime.timedelta(milliseconds=10)

        # Initialize a mean shift tracker
        mean_shift = dv.features.MeanShiftTracker(resolution, bandwidth, time_window)

        visualizer = dv.visualization.EventVisualizer(resolution)

        slicer.doEveryTimeInterval(datetime.timedelta(milliseconds=40), run_mean_shift)
        if (endLoop == 1):
            break
        slicer.accept(filtered)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(posEvX,posEvY,posEvTime,marker='o')
ax.scatter(negEvX,negEvY,negEvTime,marker='^')

ax.set_xlabel('X coord')
ax.set_ylabel('Y coord')
ax.set_zlabel('Timestamp')

plt.show()