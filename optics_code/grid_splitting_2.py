import datetime
import numpy as np
import dv_processing as dv
import cv2 as cv
#from math import atan2, cos, sin, sqrt, pi
#import matplotlib.pyplot as plt
#import requests


class coordArray:
    def __init__(self,x,y):
        self.x = x
        self.y = y

cArray = np.zeros((640,480),dtype=str)


for i in range(640):
    for j in range(480):
        cVar = coordArray(i,j)
        cArray[i][j] = cVar
    
array_3d_alt = cArray.reshape(3072, 10, 10)
print(array_3d_alt)



