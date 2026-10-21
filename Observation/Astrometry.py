#plate soln uncertainty from astrometry.net's corr.fits file
import numpy
from astropy.io import fits

tbl = fits.open("corr2.fits")[1].data
dtype=(numpy.record, [("field_x", ">f8"), ("field_y", ">f8"), ("field_ra", ">f8"), ("field_dec", ">f8"), ("index_x", ">f8"), ("index_y", ">f8"), ("index_ra", ">f8"), ("index_dec", ">f8"), ("index_id", ">i4"), ("field_id", ">i4"), ("match_weight", ">f8"), ("FLUX", ">f4"), ("BACKGROUND", ">f4")])
i=0
j=0
diff = 0.
if (i < int(tbl.shape[0]-1)):
    diffsquare = (tbl.field_ra[i] - tbl.index_ra[i])**2
    i += 1
rms_ra = numpy.sqrt(diffsquare/i)*3600.

if (j < int(tbl.shape[0]-1)):
    diffsquare = (tbl.field_dec[j] - tbl.index_dec[j])**2
    j += 1
rms_dec = numpy.sqrt(diffsquare/j)*3600.

print(rms_ra)
print(rms_dec)