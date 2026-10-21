import astropy
from astropy.io import fits
fitsfile = fits.open("2.fit") #open the FITS file
fitsimage = fitsfile[0].data #load all the ADU data
fitsfile.close() #close the FITS file

roi = fitsimage[379:386,507:514]
print(roi)