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
input=input("Data Mode Y or N: ")
client = dv.io.NetworkReader("127.0.0.1", 5500)
count_array1=[]
max_frequency=0
text_code=''
success=0
success2=0   #global variables list if you need more please let others know to Change
failure2=0
failure=0
has_run=False
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
def create_array(n):
      """Creates a list of numbers from 1 to n (inclusive)."""
      return list(range(1, n + 1))
def remove_dc_offset(signal): #removes DC offset to eliminate a spike on the fourier transform at 0Hz
    return signal - np.mean(signal) #outputs ajusted signal
def frq(n,count_array1,s): #show but not plota given sample frame number n, using the points in the array count_array_1, use s to vary the sampling frequency
        if(len(count_array1)>=n):
            #plt.show()
            x=np.multiply(np.array(create_array(len(count_array1))),1/s)
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
            index_of_max_frequency = np.argmax(np.abs(yf[1:])) + 1 
            max_frequency = freq[index_of_max_frequency]
            return max_frequency#return the max freqency for calculations
        if(len(count_array1)<n):
              return 0 #return 0 if the sample period has not ended
def plot(n,count_array1,s): #plot a given sample frame number n, using the points in the array count_array_1, use s to vary the sampling frequency
        if(len(count_array1)==n):
            #plt.show()
            x=np.multiply(np.array(create_array(len(count_array1))),1/s)
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
            plt.figure(figsize=(12, 6))

            # Plot the original scatter plot
            plt.subplot(1, 2, 1)
            plt.scatter(x, np.array(count_array1))
            plt.xlabel("Time(s)")
            plt.ylabel("Events Detected")
            plt.title("Event Normalized Count")

            # Plot the frequency spectrum
            plt.subplot(1, 2, 2)
            plt.xlim(0, 5) 
            plt.ylim(0, 10) 
            plt.plot(freq[:y_sorted.size//2], np.abs(yf)[:y_sorted.size//2]) # Consider only positive frequencies
            plt.xlabel("Frequency")
            plt.ylabel("Magnitude")
            plt.title("Fourier Transform")
            index_of_max_frequency = np.argmax(np.abs(yf[1:])) + 1 
            max_frequency = freq[index_of_max_frequency]
            plt.tight_layout()
            
          
            plt.show()
            return max_frequency #return the max freqency and plot it at the sampling freqency
        if(len(count_array1)>n):
                plt.close()
              #plt.show()
                x=np.multiply(np.array(create_array(len(count_array1))),1/s)
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
                index_of_max_frequency = np.argmax(np.abs(yf[1:])) + 1 
                max_frequency = freq[index_of_max_frequency]
                return max_frequency#return the max freqency for calculations without plotting
        if(len(count_array1)<n):
              return 0 #output nothing if the sample time has not ended 
def pixel_counter(src,textpast,count_array1,count_f=0): #lots of inputs but you need your src array, the past coordinates, count array for plotting/calcuations, and the count_f which here can be ajusted to account for DC offsets
            for j in range(textpast[1]-20,textpast[1]+20):
                for k in range(textpast[0]-20,textpast[0]+20):
                    if(j<480)and(k<640):
                     if((src[j][k][1]!=255)):
                        count_f=count_f+1
                        # print(f"{len(approx)}")
                    if((j==textpast[1]+19)and(k==textpast[0]+19)and(count_f>650)):
                        count_array1.append(count_f/1600)
            return count_array1 #outputs your count array to be used in the next frame
def text(max_frequency,text_code,success,failure, success2,failure2, textpresent,src,coord_detect,vel_detect,indicator,textpast): #lots of inputs but you need the max freqency, binary code, success for the first freqency, success for second freqency, failure for the failure freqency, failure for second freqency, the current coords, the past coordinates, the indicator for the first frame, src array, and the coord_detect/vel_detect
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(src,f"Calculated Freqency: {round((np.abs(max_frequency)),3)}",(300,450), font, .5,(0,0,0),1,cv.LINE_AA)
            if((np.abs(max_frequency)>=.80)and(np.abs(max_frequency)<=1.20)):
                text_code=text_code+"1"
                success=success+1
            if(len(text_code)>10):
                text_code=text_code[8]
            else:
                failure=failure+1
            if((np.abs(max_frequency)>=1.85)and(np.abs(max_frequency)<=2.20)):
                text_code=text_code+"0"
            success2=success2+1
            if(len(text_code)>10):
                text_code=text_code[8]
            else:
                failure2
                failure2=failure2+1   
            cv.putText(src,f"Calculated Code:"+text_code,(300,350), font, .5,(0,0,0),1,cv.LINE_AA)
            if(failure>0):
                cv.putText(src,f"Calculated Running Success Rate: "+f"{round((success/(failure+success)),3)}",(300,375), font, .5,(0,0,0),1,cv.LINE_AA)
            cv.putText(src,f"Coord List: {textpresent}",(30,450), font, .5,(0,0,0),1,cv.LINE_AA)
            cv.putText(src,f"Coordinate Plot",(250,30), font, .5,(0,0,0),1,cv.LINE_AA)
            #cv.putText(src,f"Count: {count_f}",(250,100), font, .5,(0,0,0),1,cv.LINE_AA)
            for j in range(10):
                if((success/(failure+success)>.68)and((success2/(failure2+success2)<.10))and(indicator==1)and(coord_detect[j][0]>=textpast[1]*.9)and(coord_detect[j][1]>=textpast[0]*.9)and(coord_detect[j][0]<=textpast[1]*1.1)and(coord_detect[j][1]<=textpast[0]*1.1)):
                    vel_detect[j]=((textpast[1]-coord_detect[j][0])*(55/50),(textpast[0]-coord_detect[j][1])*(55/50))  
                    coord_detect[j]=(textpast[1],textpast[0],0,0)
                    cv.putText(src,f"ID 1: X:{coord_detect[j][0]}, Y:{coord_detect[j][1]}",(coord_detect[j][1]+10,coord_detect[j][0]), font, .25,(0,0,0),1,cv.LINE_AA)
                    cv.putText(src,f"Velocity: X:{vel_detect[j][0]}, Y:{vel_detect[j][1]}",(coord_detect[j][1]+10,coord_detect[j][0]+50), font, .25,(0,0,0),1,cv.LINE_AA)
            return coord_detect,vel_detect #outputs both your coord_detect and vel_detect to be used in the next frame
# Callback method to show the generated event visualization
def show_preview(events: dv.EventStore): #PCA function 
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
            
    
    def getOrientation(pts, img): #PCA mean function outputs the mean value for centers of clusters
        
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
        
    
        return (angle,cntr) #center and angle of cluster
    
    parser = argparse.ArgumentParser(description='Code for Introduction to Principal Component Analysis (PCA) tutorial.\
                                                This program demonstrates how to use OpenCV PCA to extract the orientation of an object.')
    parser.add_argument('--input', help='Path to input image.', default='pca_test1.jpg')
    args = parser.parse_args()
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
    textpast=(0,0) # declare 0,0 as intial coordinates
    textpresent=''# declare empty text as your bit string
 
    if(len(contours)>0):
        counter=counter+1
    count_f=0
    for i, c in enumerate(contours):
      #  approx = cv.approxPolyDP(c, 0.01 * cv.arcLength(c, True), True)
        # Calculate the area of each contour
        global indicator
        area = cv.contourArea(c) 
        # Ignore contours that are too small or too large
        if (area < 1e2 or .5e4 < area): #Filters by pixel area
            continue
        global coord_detect
        global vel_detect
        # Draw each contour only for visualisation purposes
        cv.drawContours(src, contours, i, (0, 0, 255), 1)
        textpast=getOrientation(c, src)[1] #outputs "past" coordinates y,x
        textpresent+=f"X:{textpast[1]}, Y:{textpast[0]}"
        if(indicator==0):
            for j in range(10):
               coord_detect[j][0]=getOrientation(c, src)[1][1]       #outputs first frame coord to fill the array
               coord_detect[j][1]=getOrientation(c, src)[1][0]
               indicator=1
        global text_code
        global count_array1
        count_array1=pixel_counter(src,textpast,count_array1)#outputs live pixel count given an array 
        if(input=="Y"or input=="y"):
            max_frequency=plot(100,count_array1,25)#outputs live freqency with plot 
            coord_detect=text(max_frequency,text_code,success,failure, success2,failure2, textpresent,src,coord_detect,vel_detect,indicator,textpast)[0] #outputs live coordinates and displays them ;indicator determines if its the first frame or not
            vel_detect=text(max_frequency,text_code,success,failure, success2,failure2, textpresent,src,coord_detect,vel_detect,indicator,textpast)[1]# outpust live velocity and displays them ;indicator determines if its the first frame or not
        if(input=="N"or input=="n"):
            max_frequency=frq(100,count_array1,25)#outputs live freqency without plot 
            coord_detect=text(max_frequency,text_code,success,failure, success2,failure2, textpresent,src,coord_detect,vel_detect,indicator,textpast)[0] #outputs live coordinates and displays them ;indicator determines if its the first frame or not
            vel_detect=text(max_frequency,text_code,success,failure, success2,failure2, textpresent,src,coord_detect,vel_detect,indicator,textpast)[1]# outpust live velocity and displays them ;indicator determines if its the first frame or not
       # print(f"{np.abs(max_frequency)}")
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