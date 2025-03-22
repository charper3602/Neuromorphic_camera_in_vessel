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
class tracker(): #object to do the calculations
  def __init__(self, vel,ind,success1,success2,failure1,failure2,text_code,count_array,max_freq,coordpresent,coordpast,coordx_array,coordy_array):
    self.vel = vel if vel is not None else (0.0,0.0)
    self.ind = ind if ind is not None else False
    self.max_freq = max_freq if max_freq is not None else 0.0
    self.success1 = success1 if success1 is not None else 0.0
    self.success2 = success2 if success2 is not None else 0.0 #Tell the initalizer to assign a default value to both mutable and imutable variables 
    self.failure1 = failure1 if failure1 is not None else 0.0
    self.failure2 = failure2 if failure2 is not None else 0.0
    self.text_code = text_code if text_code is not None else ""
    self.count_array = count_array if count_array is not None else []
    self.coordpresent= coordpresent if coordpresent is not None else (0.0,0.0)
    self.coordpast= coordpast if coordpast is not None else (0.0,0.0)

    #arrays used for 3d plotting x and y coordinates
    self.coordx_array = coordx_array if coordx_array is not None else []
    self.coordy_array = coordy_array if coordy_array is not None else []

  def plot(self,n,s): #plot a given sample frame number n, using the points in the array count_array_1, use s to vary the sampling frequency
        count_array1=self.count_array
        coordx_array1=self.coordx_array
        coordy_array1=self.coordy_array
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
            plt.subplot(1, 3, 1)
            plt.scatter(x, np.array(count_array1))
            plt.xlabel("Time(s)")
            plt.ylabel("Events Detected")
            plt.title("Event Normalized Count")

            # Plot the frequency spectrum
            plt.subplot(1, 3, 2)
            plt.xlim(0, 5) 
            plt.ylim(0, 10) 
            plt.plot(freq[:y_sorted.size//2], np.abs(yf)[:y_sorted.size//2]) # Consider only positive frequencies
            plt.xlabel("Frequency")
            plt.ylabel("Magnitude")
            plt.title("Fourier Transform")
            index_of_max_frequency = np.argmax(np.abs(yf[1:])) + 1 
            self.max_freq = freq[index_of_max_frequency]
            plt.tight_layout()

            # Plot a 3d scatter graph of coordinates of events against time
            plt.subplot(1, 3, 3)
            plt.axes(projection ='3d')
            plt.scatter(np.array(coordx_array1), np.array(coordy_array1), x)
            plt.xlabel("X Coordinate")
            plt.ylabel("Y Coordinate")
            plt.zlabel("Time(s)")
            plt.title("Event coordinates over time")

          
            plt.show()
            return self #return the max freqency and plot it at the sampling freqency
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
                self.max_freq = freq[index_of_max_frequency]
                return self#return the max freqency for calculations without plotting
        if(len(count_array1)<n):
              self.freq=0
              return self #output nothing if the sample time has not ended

  def add3dPlot(self,x,y): #append data to coordinate and timestamp arrays for 3d plotting
      (self.coordx_array).append(x)
      (self.coordy_array).append(y)
      return self 
  
  def frq(self,n,s): #show but not plot a given sample frame number n, using the points in the array count_array_1, use s to vary the sampling frequency
        count_array1=self.count_array
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
            self.max_freq = abs(freq[index_of_max_frequency])
            return self#return the max freqency for calculations
        if(len(count_array1)<n):
              self.max_freq=0
              return self #return 0 if the sample period has not ended
  def pixel_counter(self,src,count_f=0): #lots of inputs but you need your src array, the past coordinates, count array for plotting/calcuations, and the count_f which here can be ajusted to account for DC offsets
            count_array1=self.count_array
            textpast=self.coordpast
            for j in range(textpast[1]-20,textpast[1]+20):
                for k in range(textpast[0]-20,textpast[0]+20):
                    if(j<480)and(k<640):
                     if((src[j][k][1]!=255)):
                        count_f=count_f+1
                        # print(f"{len(approx)}")
                    if((j==textpast[1]+19)and(k==textpast[0]+19)and(count_f>650)):
                        (self.count_array).append(count_f/1600)
            return self #outputs your count array to be used in the next frame
  def text(self,src): #lots of inputs but you need the max freqency, binary code, success for the first freqency, success for second freqency, failure for the failure freqency, failure for second freqency, the current coords, the past coordinates, the indicator for the first frame, src array, and the coord_detect/vel_detect
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(src,f"Calculated Freqency: {round((np.abs(self.max_freq)),3)}",(300,450), font, .5,(0,0,0),1,cv.LINE_AA)
            if((np.abs(self.max_freq)>=.80)and(np.abs(self.max_freq)<=1.20)):
                self.text_code=self.text_code+"1"
                self.success1=self.success1+1
            else:
                self.failure1=self.failure1+1
                print(f"{self.success1}")    
            if(len(self.text_code)>10):
                self.text_code=self.text_code[8]
            
            if((np.abs(self.max_freq)>=1.85)and(np.abs(self.max_freq)<=2.20)):
                self.text_code=self.text_code+"0"
                self.success2=self.success2+1
            else:
                self.failure2=self.failure2+1   
            if(len(self.text_code)>10):
                self.text_code=self.text_code[8]
            cv.putText(src,f"Calculated Code:"+self.text_code,(300,350), font, .5,(0,0,0),1,cv.LINE_AA)
            if(self.failure1>0):
                cv.putText(src,f"Calculated Running Success Rate: "+f"{round((self.success1/(self.failure1+self.success1)),3)}",(300,375), font, .5,(0,0,0),1,cv.LINE_AA)
            cv.putText(src,f"Coordinate Plot",(250,30), font, .5,(0,0,0),1,cv.LINE_AA)
            #cv.putText(src,f"Count: {count_f}",(250,100), font, .5,(0,0,0),1,cv.LINE_AA)
            if((self.success1/(self.failure1+self.success1)>.68)and((self.success2/(self.failure2+self.success2)<.10))):
                    self.vel=((self.coordpast[1]-self.coordpresent[1])*(55/50),(self.coordpast[0]-self.coordpresent[0])*(55/50))  
                    cv.putText(src,f"ID 1: X:{self.coordpresent[1]}, Y:{self.coordpresent[0]}",(self.coordpresent[0]+10,self.coordpresent[1]), font, .25,(0,0,0),1,cv.LINE_AA)
                    cv.putText(src,f"Velocity: X:{self.vel[0]}, Y:{self.vel[1]}",(self.coordpresent[0]+10,self.coordpresent[1]+50), font, .25,(0,0,0),1,cv.LINE_AA)
            return self #outputs both your coord_detect and vel_detect to be used in the next frame
LED1= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED2= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED3= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED4= tracker(None,None,None,None,None,None,None,None,None,None,None) #initalize all 10 LEDs
LED5= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED6= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED7= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED8= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED9= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED10= tracker(None,None,None,None,None,None,None,None,None,None,None)
LED_array=[LED1,LED2,LED3,LED4,LED5,LED6,LED7,LED8,LED9,LED10] #initalize array of 10 LEDs
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
    # Check if image is loaded successfully
    if src is None:
        print('Could not open or find the image: ', args.input)
        exit(0)
    # Convert image to grayscale
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # Convert image to binary
    _, bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    #cv.imshow('src', bw)
    contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    coord_detect=(0,0) # declare 0,0 as intial coordinates
    textpresent=''# declare empty text as your bit string
    counter=0 #counts ammount of valid contours then used to loop through contours
    for i, c in enumerate(contours):
      #  approx = cv.approxPolyDP(c, 0.01 * cv.arcLength(c, True), True)
        # Calculate the area of each contour
        global indicator
        area = cv.contourArea(c) 
        # Ignore contours that are too small or too large
        if (area < 1e2 or .5e4 < area): #Filters by pixel area
            continue
        # Draw each contour only for visualisation purposes
        coord_detect=getOrientation(c, src)[1] #coordinates for that frame
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.drawContours(src, contours, i, (0, 0, 255), 1)
        if(LED_array[counter].ind==False):
          LED_array[counter].coordpresent=coord_detect #outputs "first" coordinates x,y for the first frame
        if(LED_array[counter].ind==True):
          for g in range(10): #check if any of the 10 LEDs are in the movement region
             if((coord_detect[1]>=LED_array[g].coordpresent[1]*.9)and(coord_detect[0]>=LED_array[g].coordpresent[0]*.9)and(coord_detect[1]<=LED_array[g].coordpresent[1]*1.1)and(coord_detect[0]<=LED_array[g].coordpresent[0]*1.1)): #check if its inside the movement region
              LED_array[g].coordpresent=coord_detect #populate the current coords
              if(input=="Y"or input=="y"): #choose plotting
                LED_array[g].text(src) #output the text
                LED_array[g].pixel_counter(src) #output the pixel count

                LED_array[g].add3dPlot(coord_detect[0],coord_detect[1]) #add x and y coordinates to the 3D plot

                LED_array[g].plot(100,12) #plot and display the pixel count and preform transform to get frq
              if(input=="N"or input=="n"): #choose no plotting
                (LED_array[g]).text(src)#output the text
                (LED_array[g]).pixel_counter(src)#output the pixel count

                (LED_array[g]).add3dPlot(coord_detect[0],coord_detect[1]) #add x and y coordinates to the 3D plot

                (LED_array[g]).frq(100,12) #display the pixel count and preform transform to get frq
          textpresent+=f"X:{LED_array[counter].coordpresent[1]}, Y:{LED_array[counter].coordpresent[0]}" #determine all coordinates inside the count
          cv.putText(src,f"Coord List:{textpresent}",(30,450), font, .5,(0,0,0),1,cv.LINE_AA)#display current coordinates inside the count
        LED_array[counter].ind=True #if this is the first frame its over
        LED_array[counter].coordpast=LED_array[counter].coordpresent #let the new coords be the old coords
    cv.imshow('output', src)
    #cv.waitKey()
   # cv.imshow("Preview", frame)

    # Short sleep, if user clicks escape key (code 27), exit the application
    if cv.waitKey(1) == 27:
       exit(0)

time_ms = 18
# Perform visualization every 18 milliseconds, which should match the server publishing frequency
slicer.doEveryTimeInterval(timedelta(milliseconds=time_ms), show_preview)

# While client is connected
while True:
    # Read the event data
    events = client.getNextEventBatch()

    # Validate the data and feed into the slicer
    if events is not None:
        slicer.accept(events)