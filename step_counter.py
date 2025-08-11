#Created by Ege Ata Ceylan

import numpy as np
from csv import reader
import math
from scipy.signal import butter, lfilter

#convolve funtion
def convolve(signal, signalFilter):
    signalFilter = signalFilter[::-1]
    return [
        np.dot(
            signal[max(0,i):min(i+len(signalFilter),len(signal))],
            signalFilter[max(-i,0):len(signal)-i*(len(signal)-len(signalFilter)<i)],
        )
        for i in range(1-len(signalFilter),len(signal))
    ]



#input an acceleration data csv file that you get from an accelerometer app for your phone
print("Welcome to step counting program")
fileName = input("Please enter the file name to count steps from: ")

#getting the respective x y z accelerations
time = list()
accelerationX = list()
accelerationY = list()
accelerationZ = list()

#opening the file and getting the information
with open(fileName, 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        info = row[0].split(";")
        time.append(info[1])
        
        accelerationX.append(info[3])
        accelerationY.append(info[4])
        accelerationZ.append(info[5])

#cleaning the empty info
time.pop(0)
accelerationX.pop(0)
accelerationY.pop(0)
accelerationZ.pop(0)

newTime = np.asarray(time, dtype=float)

newAccX = np.asarray(accelerationX, dtype=float)
newAccY = np.asarray(accelerationY, dtype=float)
newAccZ = np.asarray(accelerationZ, dtype=float)


index = 0
magnitudes = list()
for value in acclerationX:
    magnitude = math.sqrt((newAccX[index]*newAccX[index])
                                         +(newAccY[index]*newAccY[index])
                                         +(newAccZ[index]*newAccZ[index]))
    index += 1
    magnitudes.append(magnitude)


'''
LOW PASS FILTER WITH LIBRARY FUNCTIONS
order = 2
fs = 20      
cutoff = 2



def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

#magnitudes = butter_lowpass_filter(magnitudes, cutoff, fs, order)
'''


#custom low pass filter with sin function
fc = 0.1  
N = 19

n = np.arange(N)

h = np.sinc(2 * fc * (n - (N - 1) / 2))
 

w = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + \
    0.08 * np.cos(4 * np.pi * n / (N - 1))
 

h = h * w
 

h = h / np.sum(h)

magnitudes = convolve(magnitudes, h)

stepCount = 0
dataSetSize = len(magnitudes)
index = 0

for data in magnitudes:
    mightPeak = True
    if (index >=4) & (index != (dataSetSize -4)):
        for value in magnitudes[index-4:index]:
            if(value > data):
                mightPeak = False
                break
            else:
                if(abs(magnitudes[index]- value) < 0.0009):
                    mightPeak = False
                    break
        
        if(mightPeak):
            for value in magnitudes[index+1:index+5]:
                if(value > data):
                    mightPeak = False
                    break
            else:
                if(abs(magnitudes[index]- value) < 0.0009):
                    mightPeak = False
                    break
                
            if(mightPeak):
                stepCount+= 1
                index += 1
            else:
                index += 1
        else:
             index += 1
        
    else:
        index+= 1
    
print("Step count: ",stepCount)
