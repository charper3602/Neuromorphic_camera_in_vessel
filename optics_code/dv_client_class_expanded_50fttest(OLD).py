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
import threading
from multiprocessing import Pool
import multiprocessing
#pool = Pool(10) # on 8 processors
# Initiate the client connection to the same port and localhost loopback address
input=input("Data Mode Y or N: ")
sample = 5
radius = 20

counter=0 #counts number of show_preview executions
maxCounter = 99 #max 'initialization' frames before discarding new LEDs

client = dv.io.NetworkReader("127.0.0.1", 5500)
class tracker(): #object to do the calculations
  def __init__(self,vel,ind,success1,success2,failure1,failure2,text_code,count_array,max_freq,coordpresent,coordpast,ind2,coordx_array,coordy_array,calculated_text,successrate1_text,successrate2_text,running1_text,running2_text,freq_text,textpresent,successCount):
    self.vel = vel if vel is not None else (0.0,0.0)
    self.ind = ind if ind is not None else False
    self.ind2 = ind2 if ind2 is not None else False
    self.max_freq = max_freq if max_freq is not None else 0.0
    self.success1 = success1 if success1 is not None else 0.0
    self.success2 = success2 if success2 is not None else 0.0 #Tell the initalizer to assign a default value to both mutable and imutable variables 
    self.failure1 = failure1 if failure1 is not None else 0.0
    self.failure2 = failure2 if failure2 is not None else 0.0
    self.text_code = text_code if text_code is not None else ""
    self.count_array = count_array if count_array is not None else [(0.0,0.0)]
    self.coordpresent= coordpresent if coordpresent is not None else (0,0)
    self.coordpast= coordpast if coordpast is not None else (0,0)
    self.coordx_array = coordx_array if coordx_array is not None else [0]
    self.coordy_array = coordy_array if coordy_array is not None else [0]
    self.calcuated_text=calculated_text if calculated_text is not None else ""
    self.successrate1_text=successrate1_text if successrate1_text is not None else ""
    self.successrate2_text=successrate2_text if successrate2_text is not None else ""
    self.running1_text=running1_text if running1_text is not None else ""
    self.running2_text=running2_text if running2_text is not None else ""
    self.freq_text=freq_text if freq_text is not None else ""
    self.textpresent=textpresent if textpresent is not None else ""
    self.successCount = successCount if successCount is not None else 0.0
  def plot(self,n,s): #plot a given sample frame number n, using the points in the array count_array_1, use s to vary the sampling frequency
        count_array1=self.count_array
        coordx_array1=self.coordx_array
        coordy_array1=self.coordy_array
        if(len(count_array1)==n):
            #plt.show()
            y_postive, y_negative = [], []
            for x1, y1 in count_array1:
                  y_postive.append(x1)
                  y_negative.append(y1)
            y_postive, y_negative=np.array(y_postive),np.array(y_negative)
            x=np.multiply(np.array(create_array(len(count_array1))),1/s)
            x2=np.multiply(np.array(create_array(len(coordy_array1))),1/s)
            y=remove_dc_offset(np.array(np.add(y_postive,y_negative)))
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
            #plt.scatter(x, np.array(count_array1))
            plt.scatter(x, np.array(y_postive),color = 'green')
            plt.scatter(x, np.array(y_negative),color = 'red')
            #plt.scatter(x, np.array(y),color = 'blue')
            plt.xlabel("Time(s)")
            plt.ylabel("Events Detected")
            plt.title("Event Normalized Count")

            # Plot the frequency spectrum
            plt.subplot(1, 2, 2)
            plt.xlim(0, 10) 
            plt.ylim(0, 10) 
            plt.plot(freq[:y_sorted.size//2], np.abs(yf)[:y_sorted.size//2]) # Consider only positive frequencies
            plt.xlabel("Frequency")
            plt.ylabel("Magnitude")
            plt.title("Fourier Transform")
            index_of_max_frequency = np.argmax(np.abs(yf[1:])) + 1 
            self.max_freq = freq[index_of_max_frequency]
            plt.tight_layout()
            plt.figure(figsize=(12, 12))
            ax = plt.axes(projection="3d")
            ax.scatter(np.array(coordx_array1), np.array(coordy_array1), x2)
            ax.set_xlim(0,640)
            ax.set_ylim(0,480)
            ax.set_xlabel("X Coordinate")
            ax.set_ylabel("Y Coordinate")
            plt.title("Event coordinates over time")
          
            plt.show()
            return self #return the max freqency and plot it at the sampling freqency
        if(len(count_array1)>n):
                plt.close()
              #plt.show()
                y_postive=np.array([x[0] for x in count_array1])
                y_negative=np.array([x[1] for x in count_array1])
                x=np.multiply(np.array(create_array(len(count_array1))),1/s)
                y=remove_dc_offset(np.array(np.add(y_postive,y_negative)))
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
  def frq(self,n,s): #show but not plota given sample frame number n, using the points in the array count_array_1, use s to vary the sampling frequency
        count_array1=self.count_array
        if(len(count_array1)>=n):
            #plt.show()
            y_postive, y_negative = [], []
            for x1, y1 in count_array1:
                  y_postive.append(x1)
                  y_negative.append(y1)
            y_postive, y_negative=np.array(y_postive),np.array(y_negative)
            x=np.multiply(np.array(create_array(len(count_array1))),1/s)
            y=remove_dc_offset(np.array(np.add(y_postive,y_negative)))
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
  def pixel_counter(self,frame,count_positive=0,count_negative=0): #lots of inputs but you need your src array, the past coordinates, count array for plotting/calcuations, and the count_f which here can be ajusted to account for DC offsets
            textpast=self.coordpresent
            for j in range(textpast[0]-20,textpast[0]+20):
                for k in range(textpast[1]-20,textpast[1]+20):
                    if(j<640)and(k<480):
                     #print(f"{frame[k][j][0]},{frame[k][j][1]},{frame[k][j][2]}")
                     if((frame[k][j][0]==43)and(frame[k][j][1]==43)and(frame[k][j][2]==43)): #check for negative events and count
                         count_negative=count_negative+1
                        # print(f"{len(approx)}")
                     if(((frame[k][j][0]==183)and(frame[k][j][1]==93)and(frame[k][j][2]==0))): #check for postive events and count
                         count_positive=count_positive+1
                    if((j==textpast[0]+19)and(k==textpast[1]+19)):
                        inter=(count_positive/1600,count_negative/1600) #add the count to a tuple and update self
                       # print(f"{count_negative}")
                        (self.count_array).append(inter)
            return self #outputs your count array to be used in the next frame
  def rate(self): #handle changes to error rate and calcuate the codes give the freqencies
            if((np.abs(self.max_freq)>=.80)and(np.abs(self.max_freq)<=1.20)): #find if the LED is outputing a 1
                self.text_code=self.text_code+"1"
                self.success1=self.success1+1
            else:
                self.failure1=self.failure1+1
                #print(f"{self.success1}")    
            if(len(self.text_code)>10):
                self.text_code=self.text_code[8]
            
            if((np.abs(self.max_freq)>=1.85)and(np.abs(self.max_freq)<=2.20)):#find if the LED is outputing a 0
                self.text_code=self.text_code+"0"
                self.success2=self.success2+1
            else:
                self.failure2=self.failure2+1   
            if(len(self.text_code)>10):
                self.text_code=self.text_code[8]
            return self #outputs the updated identifers for showing on screen
  def add3dPlot(self,x,y): #append data to coordinate and timestamp arrays for 3d plotting
      (self.coordx_array).append(x)
      (self.coordy_array).append(y)
      return self
def find_first_boolean_occurrence(arr, target_value): #finds the first occurance of a unfilled LED 
    for index, value in enumerate(arr):
        if value == target_value:
            return index #returns the index of the first emty slot if none exist then -1
    return -1
def rangefinder(coordxmin,coordxmax,coordymin,coordymax,LED_array=tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)): # Find if the potenial LED is inside the range of another LED and prevent duplications
     x_array=[LED_array[0].coordpresent[0],LED_array[1].coordpresent[0],LED_array[2].coordpresent[0],LED_array[3].coordpresent[0],LED_array[4].coordpresent[0],LED_array[5].coordpresent[0],LED_array[6].coordpresent[0],LED_array[7].coordpresent[0],LED_array[8].coordpresent[0],LED_array[9].coordpresent[0]]
     y_array=[LED_array[0].coordpresent[1],LED_array[1].coordpresent[1],LED_array[2].coordpresent[1],LED_array[3].coordpresent[1],LED_array[4].coordpresent[1],LED_array[5].coordpresent[1],LED_array[6].coordpresent[1],LED_array[7].coordpresent[1],LED_array[8].coordpresent[1],LED_array[9].coordpresent[1]]  
     for i in range(10):
         if(((x_array[i]<=coordxmax)and(x_array[i]>=coordxmin))and((y_array[i]<=coordymax)and(y_array[i]>=coordymin))):
             return True # The potenial LED is not valid
     return False # The potenial LED is valid
def task(h,coord_detect,frame,input,LED_array=tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)): # Main task function for running plotting,displaying, and inputs
         global sample, radius, counter, maxCounter
         font = cv.FONT_HERSHEY_SIMPLEX #print statement debugger below
        # print(f"{h}: X:{coord_detect[0]} vs {LED_array[h].coordpresent[0]}Y:{coord_detect[1]} vs {LED_array[h].coordpresent[1]}")
         #print(f"{h} vs {LED_array[h].ind}") 
         #print(f"{h} vs {LED_array[h].ind}")

         if((LED_array[h].ind==False) and (counter<=maxCounter)): #case for if the LED has not been filled with a coordinate yet 
              # print(f"{h}vs {coord_detect[1]} vs {LED_array[h].coordpresent[1]*1.1}")
              # print(f"{h}vs {LED_array[h].ind}")
               in_range=rangefinder(coord_detect[0]-radius,coord_detect[0]+radius,coord_detect[1]-radius,coord_detect[1]+radius,LED_array) #check the range to see if its a valid new coordinate
               if((in_range==False)):
                 ind_array=[LED_array[0].ind,LED_array[1].ind,LED_array[2].ind,LED_array[3].ind,LED_array[4].ind,LED_array[5].ind,LED_array[6].ind,LED_array[7].ind,LED_array[8].ind,LED_array[9].ind]
                 index= find_first_boolean_occurrence(ind_array,False)
                 #print(f"{index} number")
                 if(index>=0): #find the index of where to put that coord in the current LED array
                    LED_array[index].ind=True
                    LED_array[index].successCount += 1
                    LED_array[index].coordpresent=coord_detect
                    LED_array[index].coordpast=LED_array[index].coordpresent

         if((LED_array[h].ind==True)and(coord_detect[1]>=LED_array[h].coordpresent[1]-15)and(coord_detect[0]>=LED_array[h].coordpresent[0]-15)and(coord_detect[1]<=LED_array[h].coordpresent[1]+15)and(coord_detect[0]<=LED_array[h].coordpresent[0]+15)):#check if the potenial LED is in the movement region of a currently existing LED
               #print("working")
               LED_array[h].successCount += 1
               LED_array[h].coordpresent=coord_detect #populate the current coords
               LED_array[h].coordpast=LED_array[h].coordpresent
         '''
         else:
              LED_array[h].successCount -= 1
              LED_array[h].ind=False
         '''
         
         if((LED_array[h].successCount >= 5) or (LED_array[h].ind2==True)):
            if(input=="Y"or input=="y"): #choose plotting
              LED_array[h].pixel_counter(frame) #output the pixel count
              LED_array[h].rate() #output the text
              LED_array[h].plot(30,sample) #plot and display the pixel count and preform transform to get frq
              (LED_array[h]).add3dPlot(coord_detect[0],coord_detect[1]) #add x and y coordinates to the 3D plot
            if(input=="N"or input=="n"): #choose no plotting
              (LED_array[h]).pixel_counter(frame)#output the pixel count
              (LED_array[h]).rate()#output the text
              (LED_array[h]).frq(30,sample) #display the pixel count and preform transform to get frq
            LED_array[h].calcuated_text= LED_array[h].calcuated_text+LED_array[h].text_code
            if((LED_array[h].success1/(LED_array[h].failure1+LED_array[h].success1)>.5)and((LED_array[h].success2/(LED_array[h].failure2+LED_array[h].success2)<.10))):#check if its a valid code
                  LED_array[h].vel=((LED_array[h].coordpast[1]-LED_array[h].coordpresent[1])*(55/50),(LED_array[h].coordpast[0]-LED_array[h].coordpresent[0])*(55/50))  
                  cv.putText(frame,f"ID:{h+1} X:{LED_array[h].coordpresent[1]}, Y:{LED_array[h].coordpresent[0]}",(LED_array[h].coordpresent[0]+20,LED_array[h].coordpresent[1]), font, .25,(0,0,0),1,cv.LINE_AA)
                  cv.putText(frame,f"Velocity:{h+1} X:{LED_array[h].vel[0]}, Y:{LED_array[h].vel[1]}",(LED_array[h].coordpresent[0]+10,LED_array[h].coordpresent[1]+50), font, .25,(0,0,0),1,cv.LINE_AA)
            LED_array[h].ind2 = True
         print(LED_array[h].successCount)
         
         return LED_array,frame #return the array for the next frame
            
LED1= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED2= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED3= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED4= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None) #initalize all 10 LEDs
LED5= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED6= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED7= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED8= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED9= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
LED10= tracker(None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
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
    global counter
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
            
    
    def getOrientation(pts): #PCA mean function outputs the mean value for centers of clusters
        
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
    
        
        #cv.circle(img, cntr, 1, (255, 0, 255), 2)
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
    src = frame.copy()
    src2=frame.copy()
    # Check if image is loaded successfully
    if src2 is None:
        print('Could not open or find the image: ', args.input)
        exit(0)
    # Convert image to grayscale
    gray = cv.cvtColor(src2, cv.COLOR_BGR2GRAY)
    # Convert image to binary
    _, bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    #cv.imshow('src', bw)
    contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    coord_detect=(0,0) # declare 0,0 as intial coordinates
    font = cv.FONT_HERSHEY_SIMPLEX
    #start = time.time()
    for i, c in enumerate(contours):
        global LED_array
        # Calculate the area of each contour
        area = cv.contourArea(c) 
        # Ignore contours that are too small or too large
        if (area < 1e2 or .5e4 < area): #Filters by pixel area
            continue
        # Draw each contour only for visualisation purposes
        coord_detect=getOrientation(c)[1] #coordinates for that frame
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame,f"Coordinate Plot",(250,30), font, .5,(0,0,0),1,cv.LINE_AA)
        #if __name__ == '__main__':
           #  with multiprocessing.Pool(processes=3) as pool:

        for h in range(10):
            results = task(h,coord_detect,frame,input,LED_array)
            LED_array=results[0]
            frame=results[1]
    #end = time.time()
    #print("Time Taken:{}".format(end - start))
    if(input=="Y"or input=="y"): #displaying code outside the main function for each frame
            for j in range(10):
                if((LED_array[j].failure1>0)and(LED_array[j].failure2>0)):
                    cv.putText(src2,f"Coordinate Plot Debugger",(250,30), font, .5,(0,0,0),1,cv.LINE_AA)
                    cv.putText(src2,f"Coord List: X:{LED_array[j].coordpresent[1]}, Y:{LED_array[j].coordpresent[0]}",(75,50+(j*15)), font, .5,(0,0,0),1,cv.LINE_AA)#display current coordinates inside the count
                    cv.putText(src2,f"Calculated Running Success Rate 1 for LED {j+1}: "+f"{round((LED_array[j].success1/(LED_array[j].failure1+LED_array[j].success1)),3)}",(75,90+(j*15)), font, .5,(0,0,0),1,cv.LINE_AA)
                    cv.putText(src2,f"Calculated Running Success Rate 2: for LED {j+1}:  "+f"{round((LED_array[j].success2/(LED_array[j].failure2+LED_array[j].success2)),3)} ",(75,130+(j*15)), font, .5,(0,0,0),1,cv.LINE_AA)
                    cv.putText(src2,f"Calculated Code for LED {j+1}: "+LED_array[j].calcuated_text,(75,170+(j*15)), font, .5,(0,0,0),1,cv.LINE_AA)
                    cv.putText(src2,f"Calculated Freqency for LED {j+1}: "+ f"{round((np.abs(LED_array[j].max_freq)),3)}" ,(75,210+(j*15)), font, .5,(0,0,0),1,cv.LINE_AA)
            cv.imshow('Debug', src2)
                                           
    #cv.imshow('output', frame)
    #cv.waitKey()
   # cv.imshow("Preview", frame)
    borderoutput = cv.copyMakeBorder(  #add a border to prevent errors in checking coords +40 and -40 from a mean center as that seems to be the size of the LED spread could be made better using a smaller LED or better lens
    frame, radius, radius, radius, radius, cv.BORDER_CONSTANT, value=[255, 255, 255]) 
    cv.imshow('output', borderoutput)
    # Short sleep, if user clicks escape key (code 27), exit the application
    if cv.waitKey(1) == 27:
       exit(0)
    counter += 1

# Perform visualization every 10 milliseconds, which should match the server publishing frequency
slicer.doEveryTimeInterval(timedelta(milliseconds=33), show_preview) #33 seems to work best for latency

# While client is connected
while True:
    # Read the event data
    events = client.getNextEventBatch()

    # Validate the data and feed into the slicer
    if events is not None:
        slicer.accept(events)
