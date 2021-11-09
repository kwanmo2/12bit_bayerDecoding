# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:27:10 2021

@author: 연관모(앤비젼)
"""

import numpy as np
import cv2
from PIL import Image
import tifffile

Width = 4096
Height = 3000
ow, oh = Width//2, Height//2

with open('12bit FFC off.bin') as f:
    rectype = np.dtype(np.uint8)
    bdata = np.fromfile(f, dtype=rectype)

ushort_data = np.zeros((Width*Height), dtype=np.uint16)
"""
##ImageFormat::BayerRG12 ->ushort data
for i in range(0,np.size(bdata)):
    if(i%2 == 1):
        ushort_data[int((i-1)/2)] = bdata[i]<<8 | bdata[i-1]
"""
##ImageFormat::BayerRG12Packed ->ushort data
count = 0
for i in range(0,np.size(bdata)):
    if(i%3 == 0):
        ushort_data[count] = (bdata[i+2]<<4) | (bdata[i+1]>>4)
        count += 1
        ushort_data[count] = (bdata[i]<<4) | (bdata[i+1]&15)
        count += 1
ushort_data = np.reshape(ushort_data,(Height,Width))
tifffile.imsave('ushort_data.tif',ushort_data)

debayer = cv2.cvtColor(ushort_data, cv2.COLOR_BayerRG2BGR)
tifffile.imsave('debayer.tif',debayer)





# Pick up raw uint8 samples
G1  = ushort_data[1::2, 0::2]     # rows 1,3,5,7 columns 0,2,4,6
G0  = ushort_data[0::2, 1::2]     # rows 0,2,4,6 columns 1,3,5,7
R = ushort_data[0::2, 0::2]     # rows 0,2,4,6 columns 0,2,4,6
B = ushort_data[1::2, 1::2]     # rows 1,3,5,7 columns 1,3,5,7

# Chop any left-over edges and average the 2 Green values
R = R[:oh,:ow]
B = B[:oh,:ow]
G = G0[:oh,:ow]//2 + G1[:oh,:ow]//2