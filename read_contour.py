import dicom
import numpy as np
import math as math
import matplotlib.pyplot as plt
import pylab
import random


import os
current_working_directory = 'your_working_directory'
os.chdir(current_working_directory)

# mm:pixel ration = 1:0.78125
# the xrange (-200,200) and yrange (-124,-524)
# y-pixel is from bottom (0) to top (512)
# y-mm is from bottom (-124) to top (-524)
# y-pixel to y-mm by : y-mm = y-pixel*0.78125 + (-524)
# y-mm to y-pixel : y-pixel = (524 + (y-mm))*1.28
# x-pixel is from left (0) to right (512)
# x-mm is from left (-200) to right (200)
# x-pixel to x-mm : x-mm = x-pixel*0.78125 + (200)
# x-mm to x-pixel : x-pixel = (x-mm + 200)*1.28
# z-axis from 113 (319) to 0 (879)
# z-mm from -315.8125 to -651.5
# given my_pt as (254,222) in pixels then in mm will be (-1.6,-293)
# z-coordinate, slice 31 = -559, spacing is +3mm   !it seems like the 

#Define parameters:
Lung_L1_serial_number = 3
Lung_R1_serial_number = 4
Target_serial_number = 5
dataID_ini = 879  #data arrangement is in reversing order
dataID_fin = 319
dataID_step = 5
num_dataID = int(abs(dataID_fin-dataID_ini)/dataID_step) +1 

filename = 'RS.2.16.840.1.113669.2.931128.644656085.20161014231755.125473.dcm'  ##structure filename
structure_file = dicom.read_file(filename) 


#################################### Fake Dose HERE!!!   #######################################################
blank = np.zeros((512,512,113))
my_pt = (254,222,31)
r = my_pt[0]
c = my_pt[1]
z = my_pt[2]
print(r)
print(c)
print(z)

my_top_ht = blank
for i in range (-10,10):
    print(r+i)
    for j in range (-10,10):
        for k in range(-3, 3):
            my_top_ht[r+i, c+j, z+k] = 1.0
            

import scipy.ndimage.filters as filters
smth = 200*filters.gaussian_filter(my_top_ht,[50,50,10], [0,0,0] )


#################################### Function to convert pixel to mm  #######################################################
def xpixel_conv(x): 
    y = x*0.78125 + (200)
    return y
 
def get_xpixel(x):
    y = (x + 200)*1.28
    y = int(y)
    return y
    
def ypixel_conv(x): 
    y = x*0.78125 + (-524)
    return y
    
def get_ypixel(x):
    y = ((x)+524)*1.28
    y = int(y)
    return y

def zslice_conv(x):
    y = int((879 - x)/5)
    return y
    
def get_zmm(x):
    y = -651.5 + x*3.0
    return y

#################################### For first organ (in this case, Lung_L1)     ##########################################################
maxcontseq = len(structure_file.ROIContourSequence[Lung_L1_serial_number].ContourSequence)

for k in range (0,maxcontseq,1):
	data_write = structure_file.ROIContourSequence[Lung_L1_serial_number].ContourSequence[k].ContourData
	dataID_len= len(structure_file.ROIContourSequence[Lung_L1_serial_number].ContourSequence[k].ContourImageSequence[0].RefdSOPInstanceUID)
	dataID = int(structure_file.ROIContourSequence[Lung_L1_serial_number].ContourSequence[k].ContourImageSequence[0].RefdSOPInstanceUID[dataID_len-3:dataID_len])

	
	maxlength = len(data_write)
	x = np.zeros(maxlength/3)
	y = np.zeros(maxlength/3)
	z = np.zeros(maxlength/3)
	dose = np.zeros(maxlength/3)

	
	j = 0
	for i in range (0,maxlength,3):
	  x[j] = data_write[i]
	  y[j] = data_write[i+1]
	  z[j] = data_write[i+2]
	  j+=1
	  
	######## inserting data from smth to dose
	zslice = zslice_conv(dataID)
	zmm = get_zmm(zslice)
	
	for i in range (0,j):
	     dose[i] = smth[get_xpixel(x[i]), get_ypixel(y[i]),zslice]	                  
	  
	f = file('ContourData_Lung_L1Real.txt','a') #append the file. Please remove this file before you run the script
  
	np.savetxt(f,np.c_[x,y,z,dose],fmt='%f,%f,%f,%f')
	

#################################### For second organ (in this case, Lung_R1)     ##########################################################

maxcontseq = len(structure_file.ROIContourSequence[Lung_R1_serial_number].ContourSequence)

for k in range (0,maxcontseq,1):
	data_write = structure_file.ROIContourSequence[Lung_R1_serial_number].ContourSequence[k].ContourData
	dataID_len= len(structure_file.ROIContourSequence[Lung_R1_serial_number].ContourSequence[k].ContourImageSequence[0].RefdSOPInstanceUID)
	dataID = int(structure_file.ROIContourSequence[Lung_R1_serial_number].ContourSequence[k].ContourImageSequence[0].RefdSOPInstanceUID[dataID_len-3:dataID_len])

	maxlength = len(data_write)
	x = np.zeros(maxlength/3)
	y = np.zeros(maxlength/3)
	z = np.zeros(maxlength/3)
	dose = np.zeros(maxlength/3)

	j = 0
	for i in range (0,maxlength,3):
	  x[j] = data_write[i]
	  y[j] = data_write[i+1]
	  z[j] = data_write[i+2]
	  j+=1
	  
	######## inserting data from smth to dose
	zslice = zslice_conv(dataID)
	zmm = get_zmm(zslice)

	for i in range (0,j):
	     dose[i] = smth[get_xpixel(x[i]), get_ypixel(y[i]),zslice]	 	        
	
#	for k in range (0,512):
#	    for l in range (0,512):
#	        for i in range (0,j):
#	           if (x[i] < xpixel_conv(k)+1.0   and  x[i] > xpixel_conv(k)-1.0):
#	               if (y[i] < ypixel_conv[l]+1.0 and y[i] > ypixel_conv[l]-1.0):
#	                  dose[i] = smth(k,l,zslice)
	  
	f = file('ContourData_Lung_R1Real.txt','a')   #append the file. Please remove this file before you run the script
  
	np.savetxt(f,np.c_[x,y,z,dose],fmt='%f,%f,%f,%f')
	

#################################### For third organ (in this case, Target)     ##########################################################

maxcontseq = len(structure_file.ROIContourSequence[Target_serial_number].ContourSequence)

for k in range (0,maxcontseq,1):
	data_write = structure_file.ROIContourSequence[Target_serial_number].ContourSequence[k].ContourData
	dataID_len= len(structure_file.ROIContourSequence[Target_serial_number].ContourSequence[k].ContourImageSequence[0].RefdSOPInstanceUID)
	dataID = int(structure_file.ROIContourSequence[Target_serial_number].ContourSequence[k].ContourImageSequence[0].RefdSOPInstanceUID[dataID_len-3:dataID_len])

	maxlength = len(data_write)
	x = np.zeros(maxlength/3)
	y = np.zeros(maxlength/3)
	z = np.zeros(maxlength/3)
	dose = np.zeros(maxlength/3)

	j = 0
	for i in range (0,maxlength,3):
	  x[j] = data_write[i]
	  y[j] = data_write[i+1]
	  z[j] = data_write[i+2]
	  j+=1
	  
	######## inserting data from smth to dose
	zslice = zslice_conv(dataID)
	zmm = get_zmm(zslice)
	
	for i in range (0,j):
	     dose[i] = smth[get_xpixel(x[i]), get_ypixel(y[i]),zslice]	 	
	                  
	f = file('ContourData_TargetReal.txt','a')   #append the file. Please remove this file before you run the script
  
	np.savetxt(f,np.c_[x,y,z,dose],fmt='%f,%f,%f,%f')