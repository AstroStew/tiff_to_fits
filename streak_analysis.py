# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 12:10:15 2022

@author: mstew
"""
import cv2 as cv
import matplotlib
import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt
matplotlib.use('TKAgg')


from astropy.nddata import CCDData


img_dir="D:\School\RSO_photo_sequence3\RSO_photo_sequence\FITS\DeepStackResults\Dec 3rd Night Rec 1_00030.fits"

fits_image=fits.open(img_dir)


edges=cv.Canny((fits_image[0].data*255).astype(np.uint8),0,0.01,3)

painted_image=(fits_image[0].data*255)


# Probablistic
lines=cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=20,maxLineGap=2)
blank_canvas=np.zeros(np.shape(fits_image[0].data))
for line in lines:

    x1,y1,x2,y2=line[0]
    cv.line(painted_image,(x1,y1),(x2,y2),(255,255,255),1)

cv.imwrite(img_dir.split('.')[0]+'houglines.jpg',painted_image)