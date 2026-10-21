#from scratch SAP code
#using Python3 - AWR
#last updated: 03 Jul 2024

import astropy
import string
import sys
import os
import math

from astropy.io import fits
from math import log10, sqrt

#inputString = input("Enter name of input fits file: ")
try:
    fitsfile = fits.open("Science2_062325-0001_out.fits")
except FileNotFoundError:
    print('input file %s not found. Exiting. \n' % "Science2_062325-0001_out.fits")
    sys.exit()

subset = 0
centroid = 0
fitsimage = fitsfile[0].data
fitsfile.close()

x = int(input('Approx. x value of object: '))-1
y = int(input('Approx. y value of object: '))-1
ap = int(input('Aperture radius in pixels: '))
ani = int(input('Annulus inner radius in pixels: '))
ano = int(input('Annulus outer radius in pixels: '))

xmin = x-ano
xmax = x+ano+1
ymin = y-ano
ymax = y+ano+1
    
roi = fitsimage[ymin:ymax,xmin:xmax]
xcent = (xmax-xmin-1)/2
ycent = (ymax-ymin-1)/2

annu = 0.0
nap = 0
nann = 0
#sky background - don't worry about fractional pixels
for i in range(0,((2*(ano+1)))):
    for j in range(0,((2*(ano+1)))):
        dist = ((float(xcent)-float(j))**2.0+(float(ycent)-float(i))**2.0)**0.5
        if ((dist>float(ani))&(dist<float(ano))):
            annu += roi[i,j]
            nann +=1
avgSky = float(annu)/float(nann)

#determine xcofm,ycofm using pixel center for inclusion
xcofm = 0.
ycofm = 0.
denom = 0.
for j in range(0,((2*(ano+1)))):
    for i in range(0,((2*(ano+1)))):
        dist = ((float(xcent)-float(j))**2.0+(float(ycent)-float(i))**2.0)**0.5
        if (dist<float(ap)):
            xcofm += (roi[i,j]-avgSky)*j
            ycofm += (roi[i,j]-avgSky)*i
            denom += roi[i,j]-avgSky
xcofm = xcofm/denom
ycofm = ycofm/denom

#determine uncert for xcofm,ycofm
xuncert = 0.
yuncert = 0.
denom = 0.
for j in range(0,((2*(ano+1)))):
    for i in range(0,((2*(ano+1)))):
        dist = ((float(xcent)-float(j))**2.0+(float(ycent)-float(i))**2.0)**0.5
        if (dist<float(ap)):
            xuncert += (roi[i,j]-avgSky)*((j-xcofm)**2.0)
            yuncert += (roi[i,j]-avgSky)*((i-ycofm)**2.0)
            denom += roi[i,j]-avgSky
xuncert = (xuncert / (denom*(denom - 1)))**0.5
yuncert = (yuncert / (denom*(denom - 1)))**0.5

#determine Signal in aperture centered at xcofm,ycofm using pixel center for inclusion
Signal = 0.
nap = 0
for j in range(0,((2*(ano+1)))):
    for i in range(0,((2*(ano+1)))):
        dist = ((float(xcofm)-float(j))**2.0+(float(ycofm)-float(i))**2.0)**0.5
        if (dist<float(ap)):
            Signal += roi[i,j]-avgSky
            nap += 1

#determine SNR
dark = 10.
gain = 0.75
read = 6.48
rhosq = (read*read) + (gain*gain/12.)
SNR = ((gain*Signal)/(1.0+(float(nap)*(1.0+(float(nap)/float(nann)))*(((gain*avgSky)+dark+rhosq)/(gain*Signal)))))**0.5

#determine inst mag and uncert
instmag = -2.5*log10(Signal)
sigmag = 1.0875/SNR

#convert centroid values back to fits pixel space
xcofm = xcofm - ano + x + 1
ycofm = ycofm - ano + y + 1

#print statements
print('xbar =',xcofm,'+\-',xuncert)
print('ybar =',ycofm,'+\-',yuncert)
print('avgSky =',avgSky,'; annulus contains',nann,'pixels')
print('Signal =',Signal,'; aperture contains',nap,'pixels')
print('inst mag = ',instmag,'+\-',sigmag)
print('SNR = ',SNR)
