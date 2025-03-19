from __future__ import print_function
from __future__ import division
import dv_processing as dv
import cv2 as cv
from datetime import timedelta
import cv2 as cv
import numpy as np
import argparse
from math import atan2, cos, sin, sqrt, pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import random
from matplotlib.animation import FuncAnimation
from threading import Thread
# Initiate the client connection to the same port and localhost loopback address
client = dv.io.NetworkReader("127.0.0.1", 5500)
count_array1=[]
max_frequency=0
text_code=''
success=0
success2=0
failure2=0
failure=0
coord_detect=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
vel_detect=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
indicator=0
# Validate that this client is connected to an event data stream
if not client.isEventStreamAvailable():
    raise RuntimeError("Server does not provide event data!")
# Initialize the event visualizer with server reported sensor resolution
visualizer = dv.visualization.EventVisualizer(client.getEventResolution())
visualizer.setBackgroundColor(dv.visualization.colors.white())
visualizer.setPositiveColor(dv.visualization.colors.iniBlue())
visualizer.setNegativeColor(dv.visualization.colors.darkGrey())
# Create a preview window to show the visualized events
#cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Declare an event stream slicer to synchronized event data packets
slicer = dv.EventStreamSlicer()
x = [1]
y = [random.randint(1,10)]
fig, ax = plt.subplots()
graph = ax.plot(x,y,color = 'g')[0]
plt.ylim(0,10)
def update(j):
    global graph

    # updating the data
    x.append(x[-1] + 1)
    y.append(j)

    # creating a new graph or updating the graph
    graph.set_xdata(x)
    graph.set_ydata(y)
    plt.xlim(x[0], x[-1])
def animate(ax1,i):
    graph_data = i
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)
# Callback method to show the generated event visualization
def show_preview(events: dv.EventStore):
    # Display preview image
    frame = visualizer.generateImage(events)
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
        #print(f'X: Coord {cntr[0]}, {cntr[1]}')
    
        
        cv.circle(img, cntr, 1, (255, 0, 255), 2)
        p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
        p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
        #drawAxis(img, cntr, p1, (0, 255, 0), 1)
        #drawAxis(img, cntr, p2, (255, 255, 0), 5)
    
        angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
        
    
        return (angle,cntr)
    
    parser = argparse.ArgumentParser(description='Code for Introduction to Principal Component Analysis (PCA) tutorial.\
                                                This program demonstrates how to use OpenCV PCA to extract the orientation of an object.')
    parser.add_argument('--input', help='Path to input image.', default='pca_test1.jpg')
    args = parser.parse_args()
    
    count_array2=[]
    data_points = []
    timestamps = []
    src = frame
    src2=src
    # Check if image is loaded successfully
    if src is None:
        print('Could not open or find the image: ', args.input)
        exit(0)
    

    counter=0
    # Convert image to grayscale
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    
    # Convert image to binary
    _, bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    #cv.imshow('src', bw)
    
    
    contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    textpast=(0,0)
    textpresent=''
 
    if(len(contours)>0):
        counter=counter+1
    count_f=0
    for i, c in enumerate(contours):
      #  approx = cv.approxPolyDP(c, 0.01 * cv.arcLength(c, True), True)
        # Calculate the area of each contour
        global indicator
        area = cv.contourArea(c)
        # Ignore contours that are too small or too large
        if (area < 1e2 or 5e2 < area):
            continue
        
        # Draw each contour only for visualisation purposes
        cv.drawContours(src, contours, i, (0, 0, 255), 1)
        font = cv.FONT_HERSHEY_SIMPLEX
        textpast=getOrientation(c, src)[1]
        if(indicator==0):
            for j in range(10):
               coord_detect[j][0]=getOrientation(c, src)[1][1]
               coord_detect[j][1]=getOrientation(c, src)[1][0]
               indicator=1
        #print(f"{src2[textpast[0]-1][textpast[1]-1]}")
        for j in range(textpast[1]-10,textpast[1]+10):
            for k in range(textpast[0]-10,textpast[0]+10):
                 if(j<480)and(k<640):
                   if((src[j][k][1]!=255)):
                      count_f=count_f+1
                     # print(f"{len(approx)}")
                 if((j==textpast[1]+9)and(k==textpast[0]+9)):
                     count_array1.append(count_f/400)
                 #  print(f"X:{j}, Y:{k}")
                # anim = FuncAnimation(fig, update(count_f))
                 #plt.show()
                #  
                  
                  
        
        
        textpresent+=f"X:{textpast[1]}, Y:{textpast[0]}"
        global max_frequency
        global text_code
        cv.putText(src,f"Calculated Freqency: {round((np.abs(max_frequency)),3)}",(300,450), font, .5,(0,0,0),1,cv.LINE_AA)
        if((np.abs(max_frequency)>=.85)and(np.abs(max_frequency)<=1.20)):
           text_code=text_code+"1"
           global success
           success=success+1
           if(len(text_code)>10):
               text_code=text_code[8]
        else:
           global failure
           failure=failure+1
        if((np.abs(max_frequency)>=1.85)and(np.abs(max_frequency)<=2.20)):
           text_code=text_code+"0"
           global success2
           success2=success2+1
           if(len(text_code)>10):
               text_code=text_code[8]
        else:
           global failure2
           failure2=failure2+1   
        cv.putText(src,f"Calculated Code:"+text_code,(300,350), font, .5,(0,0,0),1,cv.LINE_AA)
        if(failure>0):
            cv.putText(src,f"Calculated Running Success Rate: "+f"{round((success/(failure+success)),3)}",(300,375), font, .5,(0,0,0),1,cv.LINE_AA)
        cv.putText(src,f"Coord List: {textpresent}",(30,450), font, .5,(0,0,0),1,cv.LINE_AA)
        cv.putText(src,f"Coordinate Plot",(250,30), font, .5,(0,0,0),1,cv.LINE_AA)
        cv.putText(src,f"Count: {count_f}",(250,100), font, .5,(0,0,0),1,cv.LINE_AA)
        for j in range(10):
         if((success/(failure+success)>.68)and((success2/(failure2+success2)<.10))and(indicator==1)and(coord_detect[j][0]>=textpast[1]*.9)and(coord_detect[j][1]>=textpast[0]*.9)and(coord_detect[j][0]<=textpast[1]*1.1)and(coord_detect[j][1]<=textpast[0]*1.1)):
           vel_detect[j]=((textpast[1]-coord_detect[j][0])*(55/50),(textpast[0]-coord_detect[j][1])*(55/50))  
           coord_detect[j]=(textpast[1],textpast[0],0,0)
           cv.putText(src,f"ID 1: X:{coord_detect[j][0]}, Y:{coord_detect[j][1]}",(coord_detect[j][1]+10,coord_detect[j][0]), font, .25,(0,0,0),1,cv.LINE_AA)
           cv.putText(src,f"Velocity: X:{vel_detect[j][0]}, Y:{vel_detect[j][1]}",(coord_detect[j][1]+10,coord_detect[j][0]+50), font, .25,(0,0,0),1,cv.LINE_AA)
          
        count_f=0
        # Find the orientation of each shape
        
    def create_array(n):
      """Creates a list of numbers from 1 to n (inclusive)."""
      return list(range(1, n + 1))
    
   # plt.scatter(create_array(len(count_array1)),count_array1)

# Customize the plot (optional)
    #plt.title("Array Plot")
    #plt.xlabel("Index")
    #plt.ylabel("Value")

# Show the plot
    def remove_dc_offset(signal):
       return signal - np.mean(signal)
    if(len(count_array1)>20):
        #plt.show()
        x=np.multiply(np.array(create_array(len(count_array1))),1/12)
        y=remove_dc_offset(np.array(count_array1))
      # Sort data based on x-values (required for FFT)
        sort_indices = np.argsort(x)
        x_sorted = x[sort_indices]
        y_sorted = y[sort_indices]
        # Calculate the sampling rate (assuming uniform spacing)
        sampling_rate = 1 / np.mean(np.diff(x_sorted))
        #sampling_rate = 33
        # Apply the Fourier Transform
        yf = np.fft.fft(y_sorted)
        T = 1.0 / sampling_rate
        freq = np.fft.fftfreq(y_sorted.size, d=T)
        # Plot the results
        #plt.figure(figsize=(12, 6))

        # Plot the original scatter plot
        #plt.subplot(1, 2, 1)
        #plt.scatter(x, np.array(count_array1))
        #plt.xlabel("Time(s)")
        #plt.ylabel("Events Detected")
        #plt.title("Event Normalized Count")

        # Plot the frequency spectrum
        #plt.subplot(1, 2, 2)
        #plt.xlim(0, 5) 
        #plt.ylim(0, 10) 
        #plt.plot(freq[:y_sorted.size//2], np.abs(yf)[:y_sorted.size//2]) # Consider only positive frequencies
        #plt.xlabel("Frequency")
        #plt.ylabel("Magnitude")
        #plt.title("Fourier Transform")
        index_of_max_frequency = np.argmax(np.abs(yf[1:])) + 1 
        max_frequency = freq[index_of_max_frequency]
        #font = cv.FONT_HERSHEY_SIMPLEX
        #plt.tight_layout()
        
        #plt.close(1)
        #plt.show()
        
        
   # if(len(count_array1)>18):
     #   plt.close()
    #print(f"{np.abs(max_frequency)}")
    cv.imshow('output', src)
    #cv.waitKey()
   # cv.imshow("Preview", frame)

    # Short sleep, if user clicks escape key (code 27), exit the application
    if cv.waitKey(1) == 27:
       exit(0)

# Perform visualization every 10 milliseconds, which should match the server publishing frequency
slicer.doEveryTimeInterval(timedelta(milliseconds=18), show_preview)

# While client is connected
while True:
    # Read the event data
    events = client.getNextEventBatch()

    # Validate the data and feed into the slicer
    if events is not None:
        slicer.accept(events)