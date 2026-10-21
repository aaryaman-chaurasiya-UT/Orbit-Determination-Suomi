import numpy as np
import astropy
from astropy.io import fits
from photutils.datasets import make_100gaussians_image
from astropy.table import Table
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry, ApertureStats

# fitsfile = fits.open("aptest.fit") #open the FITS file
# fitsimage = fitsfile[0].data #load all the ADU data
# fitsfile.close() #close the FITS file
# #Perhaps need to use ROI from ImageClipping.py? Yes.

data = make_100gaussians_image()
hdu = fits.PrimaryHDU(data)
hdu.writeto('aptest.fits', overwrite=True)

hdul = fits.open('aptest.fits')
image_data = hdul[0].data
hdul.close()

darkCurr = 10
x = 490 - 1
y = 293 - 1
r_ap = 5
r_in = 8
r_out = 13

#roi = fitsimage[y - r_out:y + r_out,x - r_out:x + r_out]

positions = (x, y)  # Example positions
apertures = CircularAperture(positions, r_ap)
ap_stats = ApertureStats(image_data, apertures)
annuli = CircularAnnulus(positions, r_in, r_out)

phot_table = aperture_photometry(image_data, apertures, method = 'exact')
ann_phot_table = aperture_photometry(image_data, annuli, method = 'exact')



print(phot_table)