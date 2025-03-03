#to-do notes: 
# - loop over image to find individual clusters(delta x and delta y 
# must not be too big from first event)
# - after finding individual clusters and event coordinates, find center 


import datetime
import numpy as np
import dv_processing as dv
import cv2 as cv
from math import atan2, cos, sin, sqrt, pi
#import matplotlib.pyplot as plt
import requests


url = 'http://127.0.0.1:5500/api/coords/'


init_remove = requests.delete(url)
if init_remove.status_code == 204:
    print(init_remove.status_code)
else:
    #print the response code if there was an error with deleting
    print(f'Error: {init_remove.status_code}, {init_remove.text}')

capture = dv.io.CameraCapture()
capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.VeryLow)

# Make sure the opened object supports event stream output, otherwise throw runtime error
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")

#PCA axis function, from opencv example
def drawAxis(img, p_, q_, colour, scale):
    p = list(p_)
    q = list(q_)
    
    angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 
    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
 
    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
 
    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)

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
    drawAxis(img, cntr, p1, (0, 255, 0), 1)
    drawAxis(img, cntr, p2, (255, 255, 0), 5)
 
    angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    
 
    return angle,cntr

#mean shift code, from dv website example
def run_mean_shift(events):
    #remove previous coord list
    remove = requests.delete(url)
    if remove.status_code == 204:
        print(remove.status_code)
    else:
        #print the response code if there was an error with posting
        print(f'Error: {remove.status_code}, {remove.text}')

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
        response = requests.post(url, json = {"coords":f"{cn[0]} {cn[1]}*"}, stream=True)
        if response.status_code == 201:
            print(response.status_code)
        else:
            #print the response code if there was an error with posting
            print(f'Error: {response.status_code}, {response.text}')
    
    
    
    '''
    for ev in events:
        for j in range(center[0]-10,center[0]+10):
            for k in range(center[1]-10,center[1]+10):
                if((ev.x() == j) and ev.y() == k):
                    if(ev.polarity==True):
                        ax.scatter(j,k,ev.timestamp(),marker='o')
                    else:
                        ax.scatter(j,k,ev.timestamp(),marker='^')
    '''


    # Show the preview image with detected tracks
    #cv.imshow("Preview", image)
    #cv.waitKey(10)


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

# Initialize a list of clusters for synthetic data generation
#clusters = [(550, 400), (70, 300), (305, 100)]

# Generate some random events for a background
#main capture loop

evCount = 0

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

while capture.isRunning():
    
    events = capture.getNextEventBatch()

    #timestamps = [0, 40000, 80000, 120000, 160000, 200000, 240000, 280000, 320000, 360000]
    '''
    num_iter = 0
    for time in timestamps:
        #event_cluster = generate_event_clusters_at_time(time, clusters, num_iter)
        events.add(event_cluster)
        events.add(dv.data.generate.uniformlyDistributedEvents(time, resolution, 10000, num_iter))
        num_iter += 1
    '''
    
    if events is not None:
        '''
        if(evCount >= 4):
            break
        '''
        fFilter.accept(events)
        filtered = fFilter.generateEvents()
        # parameter defining the spatial window [pixels] in which the new track position will be searched
        bandwidth = 10

        # window of time used to compute the time surface used for the tracking update
        time_window = datetime.timedelta(milliseconds=10)

        # Initialize a mean shift tracker
        mean_shift = dv.features.MeanShiftTracker(resolution, bandwidth, time_window)

        visualizer = dv.visualization.EventVisualizer(resolution)

        slicer.doEveryTimeInterval(datetime.timedelta(milliseconds=33), run_mean_shift)
        #evCount += 1
        slicer.accept(filtered)

'''
ax.set_xlabel('X coordinate')
ax.set_ylabel('Y coordinate')
ax.set_zlabel('Timestamp')

plt.show()
'''