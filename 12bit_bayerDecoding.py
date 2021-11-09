# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:27:10 2021

@author: kwanmo2
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
